# -*- coding: utf-8 -*-
from app.BinanceAPI import BinanceAPI
from app.authorization import api_key,api_secret
from data.runBetData import RunBetData
from app.dingding import Message
from data.calcIndex import CalcIndex
import time

binan = BinanceAPI(api_key,api_secret)
runbet = RunBetData()
msg = Message()

index = CalcIndex()

class Run_Main():

    def __init__(self):
        self.coinList = runbet.get_coinList()
        pass

    def pre_data(self,cointype):
        '''获取交易对的data.json基础信息
            cointype:交易对
        '''
        grid_buy_price = runbet.get_buy_price(cointype)  # 当前网格买入价格
        grid_sell_price = runbet.get_sell_price(cointype)  # 当前网格卖出价格
        quantity = runbet.get_quantity(cointype)  # 买入量
        step = runbet.get_step(cointype)  # 当前步数
        cur_market_price = binan.get_ticker_price(cointype)  # 当前交易对市价
        right_size = len(str(cur_market_price).split(".")[1])
        return [grid_buy_price,grid_sell_price,quantity,step,cur_market_price,right_size]
    def loop_run(self):
        while True:

            for coinType in self.coinList:
                [grid_buy_price,grid_sell_price,quantity,step,cur_market_price,right_size] = self.pre_data(coinType)


                if grid_buy_price >= cur_market_price and index.calcAngle(coinType,"5m",False,right_size):   # 是否满足买入价
                    res = msg.buy_limit_msg(coinType, quantity,cur_market_price)
                    if 'orderId' in res: # 挂单成功
                        success_price = float(res['fills'][0]['price'])
                        runbet.set_ratio(coinType)
                        runbet.set_record_price(coinType,success_price)
                        runbet.modify_price(coinType,success_price, step+1,cur_market_price) #修改data.json中价格、当前步数
                        time.sleep(60*2) # 挂单后，停止运行1分钟
                    else:
                        break

                elif grid_sell_price < cur_market_price and index.calcAngle(coinType,"5m",True,right_size):  # 是否满足卖出价
                    if step==0: # setp=0 防止踏空，跟随价格上涨
                        runbet.modify_price(coinType,grid_sell_price,step,cur_market_price)
                    else:
                        last_price = runbet.get_record_price(coinType)
                        sell_amount = runbet.get_quantity(coinType,False)
                        porfit_usdt = (cur_market_price - last_price) * sell_amount
                        res = msg.sell_limit_msg(coinType, runbet.get_quantity(coinType,False),grid_sell_price,porfit_usdt)
                        if 'orderId' in res: #True 代表下单成功
                            runbet.set_ratio(coinType) #启动动态改变比率
                            runbet.modify_price(coinType,runbet.get_record_price(coinType), step - 1,cur_market_price)
                            runbet.remove_record_price(coinType)
                            time.sleep(60*1)  # 挂单后，停止运行1分钟
                        else:
                            break
                else:
                    print("币种:{coin}当前市价：{market_price}。未能满足交易,继续运行".format(market_price = cur_market_price,coin=coinType))
                    time.sleep(1)

if __name__ == "__main__":
    instance = Run_Main()
    try:
        instance.loop_run()
    except Exception as e:
        error_info = "报警：做多网格,服务停止"
        msg.dingding_warn(error_info)

# 调试看报错运行下面，正式运行用上面       
# if __name__ == "__main__":
#     instance = Run_Main()

# -*- coding: utf-8 -*-
from app.BinanceAPI import BinanceAPI
from app.authorization import api_key,api_secret
import os,json
binan = BinanceAPI(api_key,api_secret)
# linux
data_path = os.getcwd()+"/data/data.json"
# windows
# data_path = os.getcwd() + "\data\data.json"

class RunBetData:

    def _get_json_data(self):
        '''读取json文件'''
        tmp_json = {}
        with open(data_path, 'r') as f:
            tmp_json = json.load(f)
            f.close()
        return tmp_json


    def _modify_json_data(self,data):
        '''修改json文件'''
        with open(data_path, "w") as f:
            f.write(json.dumps(data, indent=4))
        f.close()


    ####------下面为输出函数--------####


    
    def get_buy_price(self):
        data_json = self._get_json_data()
        return data_json["runBet"]["next_buy_price"]


    def get_sell_price(self):
        data_json = self._get_json_data()
        return data_json["runBet"]["grid_sell_price"]

    def get_cointype(self):
        data_json = self._get_json_data()
        return data_json["config"]["cointype"]

    def get_record_price(self):
        '''卖出后，step减一后，再读取上次买入的价格'''
        data_json = self._get_json_data()
        cur_step = self.get_step() - 1
        return data_json['runBet']['recorded_price'][cur_step]

    def get_quantity(self,exchange_method=True):
        '''
        :param exchange: True 代表买入，取买入的仓位 False：代表卖出，取卖出应该的仓位
        :return:
        '''

        data_json = self._get_json_data()
        cur_step = data_json["runBet"]["step"] if exchange_method else data_json["runBet"]["step"] - 1 # 买入与卖出操作对应的仓位不同
        quantity_arr = data_json["config"]["quantity"]

        quantity = None
        if cur_step < len(quantity_arr): # 当前仓位 > 设置的仓位 取最后一位
            quantity = quantity_arr[0] if cur_step == 0 else quantity_arr[cur_step]
        else:
            quantity = quantity_arr[-1]
        return quantity

    def get_step(self):
        data_json = self._get_json_data()
        return data_json["runBet"]["step"]

    def remove_record_price(self):
        '''记录交易价格'''
        data_json = self._get_json_data()
        del data_json['runBet']['recorded_price'][-1]
        self._modify_json_data(data_json)

    def get_ratio_coefficient(self):
        '''获取倍率系数'''
        data_json = self._get_json_data()
        return data_json['config']['RatioCoefficient']

    def get_profit_ratio(self):
        '''获取补仓比率'''
        data_json = self._get_json_data()
        return data_json['config']['profit_ratio']

    def get_double_throw_ratio(self):
        '''获取止盈比率'''
        data_json = self._get_json_data()
        return data_json['config']['double_throw_ratio']

    def set_record_price(self,value):
        '''记录交易价格'''
        data_json = self._get_json_data()
        data_json['runBet']['recorded_price'].append(value)
        self._modify_json_data(data_json)

    def get_atr(self,symbol,interval='4h',kline_num=20):

        data = binan.get_klines(symbol, interval, kline_num)
        percent_total = 0
        for i in range(len(data)):
            percent_total = abs(float(data[i][3]) - float(data[i][2])) / float(data[i][4]) + percent_total

        return round(percent_total/kline_num * 100,1)

    def set_ratio(self,symbol):
        '''修改补仓止盈比率'''
        data_json = self._get_json_data()
        atr_value = self.get_atr(symbol)
        data_json['config']['double_throw_ratio'] = atr_value
        data_json['config']['profit_ratio'] = atr_value
        self._modify_json_data(data_json)


    # 买入后，修改 补仓价格 和 网格平仓价格以及步数
    def modify_price(self, deal_price,step,market_price):
        data_json = self._get_json_data()
        data_json["runBet"]["next_buy_price"] = round(deal_price * (1 - data_json["config"]["double_throw_ratio"] / 100), 6) # 默认保留6位小数
        data_json["runBet"]["grid_sell_price"] = round(deal_price * (1 + data_json["config"]["profit_ratio"] / 100), 6)
        #  如果修改的价格满足立刻卖出则，再次更改
        if data_json["runBet"]["next_buy_price"] > market_price:
            data_json["runBet"]["next_buy_price"] = round( market_price * (1 + data_json["config"]["profit_ratio"] / 100), 6)
        elif data_json["runBet"]["grid_sell_price"] < market_price:
            data_json["runBet"]["grid_sell_price"] = round(market_price * (1 - data_json["config"]["double_throw_ratio"] / 100), 6)

        data_json["runBet"]["step"] = step
        self._modify_json_data(data_json)
        print("修改后的补仓价格为:{double}。修改后的网格价格为:{grid}".format(double=data_json["runBet"]["next_buy_price"],
                                                           grid=data_json["runBet"]["grid_sell_price"]))



if __name__ == "__main__":
    instance = RunBetData()
    # print(instance.modify_price(8.87,instance.get_step()-1))
    print(instance.get_quantity(False))

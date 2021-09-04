import requests,json

# windows
from app.authorization import dingding_token, recv_window,api_secret,api_key
from app.BinanceAPI import BinanceAPI
# linux
# from app.authorization import dingding_token

class Message:

    def buy_market_msg(self, market, quantity):
        try:
            res = BinanceAPI(api_key,api_secret).buy_market(market, quantity)
            if 'orderId' in res:
                buy_info = "报警：币种为：{cointype}。买单量为：{num}.买单价格为：{price}".format(cointype=market,num=quantity,price=float(res['fills'][0]['price']))
                self.dingding_warn(buy_info)
                return res
            else:
                error_info = "报警：币种为：{cointype},买单失败.{info}".format(cointype=market, info=res)
                self.dingding_warn(error_info)
        except BaseException as e:
            error_info = "报警：币种为：{cointype},买单失败.{info}".format(cointype=market,info=str(e))
            self.dingding_warn(error_info)
            return res

    def sell_market_msg(self,market, quantity,profit_usdt=0):
        '''
        :param market:
        :param quantity: 数量
        :param rate: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key,api_secret).sell_market(market, quantity)
            if 'orderId' in res:
                buy_info = "报警：币种为：{cointype}。卖单量为：{num}。预计盈利{profit_num}U".format(cointype=market,num=quantity,profit_num=round(profit_usdt,2))
                self.dingding_warn(buy_info)
                return res
            else:
                error_info = "报警：币种为：{cointype},卖单失败.{info}".format(cointype=market, info=res)
                self.dingding_warn(error_info)

        except BaseException as e:
            print("-------报错信息------")
            print(BaseException) # 报错内容输出到 nohup,out
            error_info = "报警：币种为：{cointype},卖单失败.{info}".format(cointype=market,info=str(e))
            self.dingding_warn(error_info+str(res))
            return res


    def dingding_warn(self,text):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % dingding_token
        json_text = self._msg(text)
        requests.post(api_url, json.dumps(json_text), headers=headers).content

    def _msg(self,text):
        json_text = {
            "msgtype": "text",
            "at": {
                "atMobiles": [
                    "11111"
                ],
                "isAtAll": False
            },
            "text": {
                "content": text
            }
        }
        return json_text

if __name__ == "__main__":
    msg = Message()
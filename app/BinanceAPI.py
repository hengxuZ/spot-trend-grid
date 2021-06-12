# -*- coding: utf-8 -*
import requests, time, hmac, hashlib,json,os
from app.authorization import dingding_token, recv_window,api_secret,api_key
# from app.dingding import Message
# linux
data_path = os.getcwd()+"/data/data.json"
# windows
# data_path = os.getcwd() + "\data\data.json"
try:
    from urllib import urlencode
# python3
except ImportError:
    from urllib.parse import urlencode

class BinanceAPI(object):
    BASE_URL = "https://www.binance.com/api/v1"
    FUTURE_URL = "https://fapi.binance.com"
    BASE_URL_V3 = "https://api.binance.com/api/v3"
    PUBLIC_URL = "https://www.binance.com/exchange/public/product"

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def ping(self):
        path = "%s/ping" % self.BASE_URL_V3
        return requests.get(path, timeout=180, verify=True).json()

    def get_ticker_price(self,market):
        path = "%s/ticker/price" % self.BASE_URL_V3
        params = {"symbol":market}
        res =  self._get_no_sign(path,params)
        time.sleep(2)
        return float(res['price'])

    def get_ticker_24hour(self,market):
        path = "%s/ticker/24hr" % self.BASE_URL_V3
        params = {"symbol":market}
        res =  self._get_no_sign(path,params)
        return res

    def get_klines(self, market, interval, limit,startTime=None, endTime=None):
        path = "%s/klines" % self.BASE_URL
        params = None
        if startTime is None:
            params = {"symbol": market, "interval":interval, "limit":limit}
        else:
            params = {"symbol": market,"limit":limit, "interval":interval, "startTime":startTime, "endTime":endTime}
        return self._get_no_sign(path, params)

    def buy_limit(self, market, quantity, rate):
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "BUY", rate)
        return self._post(path, params)

    def sell_limit(self, market, quantity, rate):
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "SELL", rate)
        return self._post(path, params)

    def buy_market(self, market, quantity):
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "BUY")
        return self._post(path, params)

    def sell_market(self, market, quantity):
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "SELL")
        return self._post(path, params)
    
    def get_ticker_24hour(self,market):
        path = "%s/ticker/24hr" % self.BASE_URL
        params = {"symbol":market}
        res =  self._get_no_sign(path,params)
        return round(float(res['priceChangePercent']),1)
    
    def get_positionInfo(self, symbol):
        '''当前持仓交易对信息'''
        path = "%s/positionRisk" % self.BASE_URL
        params = {"symbol":symbol}
        time.sleep(1)
        return self._get(path, params)

    def get_future_positionInfo(self, symbol):
        '''当前期货持仓交易对信息'''
        path = "%s/fapi/v2/positionRisk" % self.FUTURE_URL
        params = {"symbol":symbol}
        res = self._get(path, params)
        print(res)
        return res

    def dingding_warn(self,text):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % dingding_token
        json_text = json_text = {
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
        requests.post(api_url, json.dumps(json_text), headers=headers).content
    def get_cointype(self):
        '''读取json文件'''
        tmp_json = {}
        with open(data_path, 'r') as f:
            tmp_json = json.load(f)
            f.close()
        return tmp_json["config"]["cointype"]
    ### ----私有函数---- ###
    def _order(self, market, quantity, side, price=None):
        '''
        :param market:币种类型。如：BTCUSDT、ETHUSDT
        :param quantity: 购买量
        :param side: 订单方向，买还是卖
        :param price: 价格
        :return:
        '''
        params = {}

        if price is not None:
            params["type"] = "LIMIT"
            params["price"] = self._format(price)
            params["timeInForce"] = "GTC"
        else:
            params["type"] = "MARKET"

        params["symbol"] = market
        params["side"] = side
        params["quantity"] = '%.8f' % quantity

        return params

    def _get(self, path, params={}):
        params.update({"recvWindow": recv_window})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        res = requests.get(url, headers=header,timeout=30, verify=True).json()
        if isinstance(res,dict):
            if 'code' in res:
                error_info = "报警：币种{coin},请求异常.错误原因{info}".format(coin=self.get_cointype(), info=str(res))
                self.dingding_warn(error_info)
        return res

    def _get_no_sign(self, path, params={}):
        query = urlencode(params)
        url = "%s?%s" % (path, query)
        res = requests.get(url, timeout=180, verify=True).json()
        if isinstance(res,dict):
            if 'code' in res:
                error_info = "报警：币种{coin},请求异常.错误原因{info}".format(coin=self.get_cointype(), info=str(res))
                self.dingding_warn(error_info)

        return res

    def _sign(self, params={}):
        data = params.copy()

        ts = int(1000 * time.time())
        data.update({"timestamp": ts})
        h = urlencode(data)
        b = bytearray()
        b.extend(self.secret.encode())
        signature = hmac.new(b, msg=h.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        data.update({"signature": signature})
        return data

    def _post(self, path, params={}):
        params.update({"recvWindow": recv_window})
        query = self._sign(params)
        url = "%s" % (path)
        header = {"X-MBX-APIKEY": self.key}
        res = requests.post(url, headers=header, data=query, timeout=180, verify=True).json()

        if isinstance(res,dict):
            if 'code' in res:
                error_info = "报警：币种{coin},请求异常.错误原因{info}".format(coin=self.get_cointype(), info=str(res))
                self.dingding_warn(error_info)

        return res

    def _format(self, price):
        return "{:.8f}".format(price)

if __name__ == "__main__":
    instance = BinanceAPI(api_key,api_secret)
    # print(instance.buy_limit("EOSUSDT",5,2))
    # print(instance.get_ticker_price("WINGUSDT"))
    print(instance.get_ticker_24hour("WINGUSDT"))

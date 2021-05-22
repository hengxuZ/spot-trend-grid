# wechat ： findpanpan
from data.runBetData import RunBetData
from app.BinanceAPI import BinanceAPI
from app.authorization import api_key,api_secret
from data.calcIndex import CalcIndex

binan = BinanceAPI(api_key,api_secret)
index = CalcIndex()
runbet = RunBetData()

tmp_data = {
    "runBet": {
        "next_buy_price": 0,
        "grid_sell_price": 0,
        "step": 0
    },
    "config": {
        "profit_ratio": 0,
        "double_throw_ratio": 0,
        "cointype": "",
        "quantity": []
    }
}

class CreateData():
    def __init__(self):
        pass



if __name__ == "__main__":


    print("******欢迎使用-生成data.json脚本*****")
    print("***输入完成后，请按下回车键结束***")
    print("")
    print("请输入：你要交易对的交易对。例如：ETH。")
    symbol = input()
    print("正在加速运算中...")
    cointype = str(symbol).upper() + "USDT"
    cur_market_price = binan.get_ticker_price(cointype) #当前市价
    #[is_open, position] = index.is_open_position(cointype) #最小位数
    buy_size = len(str(cur_market_price).split(".")[1]) if str(cur_market_price).find(".") != -1 else 0
    tmp_data['config']['cointype'] = cointype

    print("请输入：您要间隔的买卖的比率。例如：5。（此处5代表这5%）")
    ratio = input()
    tmp_data["config"]["profit_ratio"] = float(ratio)
    tmp_data["config"]["double_throw_ratio"] = float(ratio)
    # 计算价格
    tmp_data['runBet']['next_buy_price'] = cur_market_price * (100 - float(ratio)) / 100
    tmp_data['runBet']['grid_sell_price'] = cur_market_price * (100 + float(ratio)) / 100

    print("请输入您单次计划花费的USDT量。请输入大于10的数（单次下注最小10U）")
    const_usdt = input()
    quantity = round(float(const_usdt) / cur_market_price, buy_size)
    tmp_data["config"]["quantity"].append(quantity)

    runbet._modify_json_data(tmp_data)

    print("data.json生成成功。请输入下列命令开启网格")
    print('nohup python3 run.py &')






### 🎉第二版本🎉 （现货趋势网格）

v2适合震荡上涨的行情

如果您对后面的行情看跌，建议您使用 v4版 [合约开空趋势网格](https://github.com/hengxuZ/future-short-grid)
---

### 介绍
在第一版本的基础上

**趋势判断，不在固定点位开单，选择更优的开仓点位**


### 优势：🎉
1. 简单易上手
2. 安全(不用将api_secret告诉他人)


### 如何启动

1. 修改app目录下的authorization文件

```
api_key='你的key'
api_secret='你的secret'

dingding_token = '申请钉钉群助手的token'   # 强烈建议您使用 （若不会申请，请加我个人微信）
```

如果你还没有币安账号： [注册页面](https://www.binancezh.top/zh-CN/register?ref=OW7U53AB)  [免翻墙地址](https://www.binancezh.cc/zh-CN/register?ref=OW7U53AB)
交易返佣20%  注册立刻返现5元，充值交易再返现15元（下方加微信返现）。

或者可以注册火币账号：[注册页面](https://www.huobi.ms/zh-cn/topic/double-reward/?invite_code=w2732223)交易返佣15% 注册立刻返现5元，充值并且交易再返现10元

>交易返佣计算公式：交易金额1W元 * 手续费比率0.1% * 0.02 = 2元（交易1w节约2元）

申请api_key地址: [币安API管理页面](https://www.binance.com/cn/usercenter/settings/api-management)
>申请api_key时一定要勾选上 
1.允许现货及杠杆交易 
2.允许合约 
2. 安装依赖包
'''
pip install requests
'''

3. 修改data/data.json配置文件  （参数详细解读->[一定要看](https://github.com/hengxuZ/binance-quantization/blob/master/dev-ReadMe.md)）
```
由于本版本支持多币对，配置文件略有不同
1.coinList中填入你要执行的币对，下方的该币对一一对应配置项
{
    "coinList": [
        "ETHUSDT",
        "BTCUSDT",
        "BNBUSDT"
    ],
    "ETHUSDT": {                           # 每个币对象要一一对应
        "runBet": {
            "next_buy_price": 3800,        # 下次买入价
            "grid_sell_price": 4000,       # 下次卖出价 （没有仓位，自动更新价格，不做卖出操作）
            "step": 0,                    # 已经购入多少手（根据quantity推算）
            "recorded_price": [           # 此项不用管，
            ]
        },
        "config": {
            "profit_ratio": 2.3,           # 此项不用管，根据4小时ART，20根k线计算
            "double_throw_ratio": 2.3,     # 此项不用管，根据4小时ART，20根k线计算
            "quantity": [                  # 每次要买入多少 (单次购买0.003个ETH)
                0.003
            ]
        }
    },
    "BTCUSDT": {
        "runBet": {
            "next_buy_price": 49000.0,
            "grid_sell_price": 50000.0,
            "step": 0,
            "recorded_price": []
        },
        "config": {
            "profit_ratio": 1.7,
            "double_throw_ratio": 1.7,
            "quantity": [
                0.001
            ]
        }
    },
    "BNBUSDT": {
        "runBet": {
            "next_buy_price": 450,
            "grid_sell_price": 500,
            "step": 0,
            "recorded_price": []
        },
        "config": {
            "profit_ratio": 2.0,
            "double_throw_ratio": 2.0,
            "quantity": [
                0.02
            ]
        }
    }
}
```

4. 运行主文件
```
# nohup python3 run.py > run.log &  #后台挂载 程序买卖、异常会通过钉钉通知(推荐使用钉钉模式启动👍)
```


如果您不想那么麻烦，又是python、linux 服务器。可以使用下面链接注册派网。体验网格交易
![派网注册](https://www.pionex.cc/zh-CN/sign/ref/gP7byIO9)（通过该链接注册的用户，加我立马返现5元）

### 注意事项（一定要看）
- 由于交易所的api在大陆无法访问，默认运行环境是国外的服务器,默认环境是python3(linux自带的是python2)

- 如果您使用的交易所为币安，那么请保证账户里有足够的bnb
    - 手续费足够低
    - 确保购买的币种完整(如果没有bnb,比如购买1个eth,其中你只会得到0.999。其中0.001作为手续费支付了)

- 动态百分比可调整(参考atr计算)
    - data/runBetData 里的 get_atr(‘时间维度’,‘参考k线数量’)

- 第一版本现货账户保证有足够的U
   
### 钉钉预警

如果您想使用钉钉通知，那么你需要创建一个钉钉群，然后加入自定义机器人。最后将机器人的token粘贴到authorization文件中的dingding_token
关键词输入：报警

#### 钉钉通知交易截图

![钉钉交易信息](https://s3.ax1x.com/2021/02/01/yZSi1x.jpg)
#### 25日实战收益
![收益图](https://s3.ax1x.com/2021/02/01/yVzytA.jpg)


### 私人微信：欢迎志同道合的朋友一同探讨，一起进步。
![qq交流群](https://img02.sogoucdn.com/app/a/100520146/D179E91E279E65E3DD642C24D482D23D)
#### qq群号：1143200770

![币圈快讯爬取群](https://s3.ax1x.com/2021/02/01/yZSU4s.jpg)
![钉钉群二维码](https://i0.hdslb.com/bfs/album/4f50bfd7f1fddaa7c340bc06d7ce078404670fb2.jpg)
### 钉钉设置教程
![钉钉设置教程](https://s3.ax1x.com/2021/01/08/suMVIK.png)


### 免责申明
本项目不构成投资建议，投资者应独立决策并自行承担风险
币圈有风险，入圈须谨慎。

> 🚫风险提示：防范以“虚拟货币”“区块链”名义进行非法集资的风险。

---
- 市价单改为限价单
- 调整set_ratio可配置
- 行情数据使用websocket
- 引入talib指标

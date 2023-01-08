import configparser
import json
import re
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)
from tradingview_ta import TA_Handler, Interval, Exchange
from py3cw.request import Py3CW
import time
import sys
import logging


logger=logging.getLogger()

formate = json.dumps({
"@timestamp": "%(asctime)s",
"level": "%(levelname)s",
"message": "%(message)s",
})

logging.basicConfig(level=logging.INFO,
      format=formate)


def main(arg1, arg2, arg3, arg4, arg5, arg6):
    api_id = arg1
    api_hash = arg2
    tele_channel = arg3
    commas_account_id = arg4
    commas_account_key = arg5
    commas_account_secret = arg6
    # print(api_id, api_hash, tele_channel, commas_account_id)
    sum_cost = 100  #  spent for each trade
    tp = 1.1  #  target_profit 
    sl = 0.9  # stop_loss
    limit = 0.99 #for limit price 

    client = TelegramClient('session', api_id, api_hash)

    p3cw = Py3CW(
            key=commas_account_key, 
            secret=commas_account_secret,
            request_options={
                'request_timeout': 10,
                'nr_of_retries': 1,
                'retry_status_codes': [502]
            }
    )
    # Trade 

    def commas_new_trade(pair,units,limit_price,sl_price,tp_price):
        logger.info("start new trade")
        error, data  = p3cw.request(
            entity='smart_trades_v2', 
            action='new', 
            payload={
                "account_id": commas_account_id,
                "pair": pair,
                "position": {
                    "type": "buy",
                    "units": {
                        "value": "{:.2f}".format(units)
                    },
                    "price": {
                    "value": "{:.2f}".format(limit_price)
                    },
                    "order_type": "limit"
                },
                "take_profit": {
                    "enabled": "true",
                    "steps": [
                    {
                        "order_type": "limit",
                        "price": {
                        "value": "{:.2f}".format(tp_price),
                        "type": "bid"
                        },
                        "volume": 100
                    }
                    ]
                },
                "stop_loss": {
                    "enabled": "true",
                    "order_type": "market",
                    "conditional": {
                    "price": {
                        "value": "{:.2f}".format(sl_price),
                        "type": "bid"
                        }
                    }
                }
            }
        )
        logger.info(f"{data}")
        msg = f"{pair} has placed new order"
        logger.info(f"{msg}")

    @client.on(events.NewMessage(chats=tele_channel))
    async def my_event_handler(event):
        sub_str = re.sub(u"([^\u0030-\u0039\u0041-\u005a\u0061-\u007a])"," ",event.text)
        out  = sub_str.split()
        if 'New' in out and 'signal' in out:
          if out[0] == "Futures" or out[0] == "Spot":
            if 'USDT' in out[1]:
                symbol = out[1]
            else: 
                symbol = out[1]+'USDT'  
            logger.info(f"{symbol} is in BUY ZONE")

            ta = TA_Handler(
                symbol=symbol,
                screener="crypto",
                exchange="BINANCE",
                interval=Interval.INTERVAL_1_MINUTE
            )
            current_price = float(ta.get_analysis().indicators["open"])
            limit_price = current_price * limit
            sl_price = limit_price * sl
            tp_price = limit_price * tp

            amount = float(sum_cost / limit_price)
            logger.info(f"Amount is {amount}")
            pair = 'USDT_' + symbol[:-4]
            #start new trade
            commas_new_trade(pair,amount,limit_price,sl_price,tp_price)


    client.start()
    client.run_until_disconnected()


if __name__=='__main__':
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]))

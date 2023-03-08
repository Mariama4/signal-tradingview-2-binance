import logging
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from binance.error import ClientError
from datetime import datetime, timedelta

config_logging(logging, logging.DEBUG)


class Account:
    key = ""
    secret = ""
    symbol = "BTCBUSD"
    quantity = "0.03"
    timeOfLastAlert = datetime.now() - timedelta(hours=0, minutes=2)


um_futures_client = UMFutures(key=Account.key, secret=Account.secret)


def toFixed(numObj, digits=0):
    return float(f"{numObj:.{digits}f}")


def getOrderParams(price):
    # 1 - покупка
    # 2 - лимитный тейк-профит
    # 3 - стоп-лосс
    return [
        {
            "symbol": Account.symbol,
            "side": "BUY",
            "type": "MARKET",
            "quantity": Account.quantity,
        },
        {
            "symbol": Account.symbol,
            "side": "SELL",
            "type": "STOP_MARKET",
            "stopPrice": f"{toFixed(price * 0.9964, 1)}",
            "quantity": Account.quantity,
        },
        {
            "symbol": Account.symbol,
            "side": "SELL",
            "type": "LIMIT",
            "price": f"{toFixed(price * 1.0016, 1)}",
            "quantity": Account.quantity,
            "timeInForce": "GTC",
        }
    ]


async def sendNewOrder():
    timeOfNewAlert = datetime.now()
    logging.info('new alert from tradeview')
    if Account.timeOfLastAlert > timeOfNewAlert:
        return
    Account.timeOfLastAlert = timeOfNewAlert + timedelta(hours=0, minutes=2)
    try:
        orderParams = getOrderParams(float(um_futures_client.book_ticker("BTCBUSD")['bidPrice']))
        response = um_futures_client.new_batch_order(orderParams)
        logging.info(response)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )
    except Exception as error:
        logging.error(
            "Found error. error message: {}".format(
                error
            )
        )

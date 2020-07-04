
from app.config.app_context import ApplicationContext
from app.services.setups import setup_factory


def find_setup(ticker, today):
    app = ApplicationContext.instance()

    list_stock = app.stock_repository.find_all_stocks_by_ticker(ticker)
    stocks = generate_setup_values(list_stock, today)

    return setup_factory.find_setup(stocks)


def generate_setup_values(list_stock, today):
    stock_update = False

    stocks = dict()
    for key, value in enumerate(list_stock):
        if value.des_date == str(today):
            stock_update = True

        stocks[f'stock_{key}_price_close'] = float(value.price_close)
        stocks[f'stock_{key}_price_open'] = float(value.price_open)
        stocks[f'stock_{key}_price_low'] = float(value.price_low)
        stocks[f'stock_{key}_price_high'] = float(value.price_high)
        stocks[f'stock_{key}_date'] = value.des_date
        stocks[f'stock_{key}_ema_9'] = float(value.ema_9())
        stocks[f'stock_{key}_ema_21'] = float(value.ema_21())

    if not list_stock or len(list_stock) == 0 or not stock_update:
        return None

    return stocks

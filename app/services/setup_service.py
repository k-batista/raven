
from app.config.app_context import ApplicationContext
from app.services.setups import setup_factory


def find_setup(ticker, time_frame, today):
    app = ApplicationContext.instance()

    list_stock = app.stock_repository.find_all_stocks_by_ticker(
        ticker, time_frame)
    stocks = generate_setup_values(list_stock, today)

    return setup_factory.find_setup(stocks)


def generate_setup_values(list_stock, today):
    stock_update = False

    stocks = dict()
    for key, stock in enumerate(list_stock):
        if stock.quote_date == str(today):
            stock_update = True

        if not stock.ema_9() or not stock.ema_21():
            stock_update = True
            break

        stocks[f'stock_{key}_price_close'] = float(stock.price_close())
        stocks[f'stock_{key}_price_open'] = float(stock.price_open())
        stocks[f'stock_{key}_price_low'] = float(stock.price_low())
        stocks[f'stock_{key}_price_high'] = float(stock.price_high())
        stocks[f'stock_{key}_date'] = stock.quote_date
        stocks[f'stock_{key}_ema_9'] = float(stock.ema_9())
        stocks[f'stock_{key}_ema_21'] = float(stock.ema_21())

    if not list_stock or len(list_stock) == 0 or not stock_update:
        return None

    return stocks

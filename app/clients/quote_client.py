from app.clients import alphavantage_client
from app.clients import yahoo_client


clients = {
    'yahoo': yahoo_client,
    'alpha': alphavantage_client
}


def get_client(client_name):
    client = clients[client_name]

    if not client:
        raise NotImplementedError

    return client.get_prices

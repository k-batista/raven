import requests
# LinearRegression is a machine learning library for linear regression
from sklearn.linear_model import LinearRegression

# pandas and numpy are used for data manipulation
import pandas as pd
import numpy as np

# matplotlib and seaborn are used for plotting graphs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use('seaborn-darkgrid')

# yahoo finance is used to fetch data
import yfinance as yf


def prediction(ticker):
    # Read data
    data = yf.download(ticker+'.SA', '2010-01-01', '2020-07-18', auto_adjust=True, interval='1d')

    # Define explanatory variables
    data['S_3'] = data['Close'].rolling(window=3).mean()
    data['S_9'] = data['Close'].rolling(window=9).mean()
    data['S_21'] = data['Close'].rolling(window=21).mean()
    data_training = data.copy()
    data_training['next_day_price'] = data_training['Close'].shift(-1)

    # Drop rows with missing values
    data = data.dropna()
    data_training = data_training.dropna()

    # Define independent variable
    X = data_training[['S_3', 'S_9']]

    # Define dependent variable
    y = data_training['next_day_price']

    # Split the data into train and test dataset
    t = .8
    t = int(t*len(data_training))

    # Train dataset
    X_train = X[:t]
    y_train = y[:t]

    # Test dataset
    X_test = X[t:]
    y_test = y[t:]

    # Create a linear regression model
    linear = LinearRegression().fit(X_train, y_train)

    # Preditct
    data['predicted_price_next_day'] = linear.predict(data[['S_3', 'S_9']])

    # # R square
    r2_score = linear.score(X[t:], y[t:])*100
    print(float("{0:.2f}".format(r2_score)))

    #Set signal
    # data['returns'] = data['Close'].pct_change().shift(-1)
    # data['signal'] = np.where(data.predicted_price_next_day.shift(1) < data.predicted_price_next_day,1,0)

    # data['strategy_returns'] = data.signal * data['returns']
    # ((data['strategy_returns']+1).cumprod()).plot(figsize=(10,7),color='g')
    # plt.ylabel('Cumulative Returns')
    # plt.show()

    line = data.tail(3)
    print(ticker)
    print(line)
    predicted_price = round(line['predicted_price_next_day']['2020-07-17'], 2)
    close = round(line['Close']['2020-07-17'], 2)
    close_last = round(line['Close']['2020-07-17'], 2)
    
    return (f'{predicted_price}  '
            f'[{round(((predicted_price*100)/close)-100, 2)} % ] ')


def send_message(message_html):
    url = "https://api.telegram.org/bot1119179717:AAHbh_7Y6vaCo2SjAcu7ITYEVaiTthiticY/sendMessage"
    
    querystring = {"chat_id":"@ravenspalerts","text":message_html,"parse_mode":"html"}

    response = requests.request("POST", url, params=querystring)

    return True


tickers = [
 'ABEV3',
'AMAR3',
'AZUL4',
'B3SA3',
'BBAS3',
'BBDC4',
'BEEF3',
'BIDI4',
'BMGB4',
'BPAC11',
'CAML3',
'CCRO3',
'CIEL3',
'CMIG4',
'COGN3',
'CVCB3',
'EGIE3',
'EMBR3',
'GGBR4',
'IRBR3',
'ITSA4',
'ITUB4',
'JBSS3',
'JHSF3',
'KLBN11',
'LAME4',
'MGLU3',
'OIBR3',
'PETR4',
'RLOG3',
'SANB11',
'TAEE11',
'USIM5',
'VALE3',
"VVAR3",
'WEGE3'
        ]

message_html = '<b>Previsões para Fechamento do Pregão - 17/07/2020</b> \n'
for t in tickers:
    message_html = f'{message_html} \n <b>{t} :</b> {prediction(t)}'

print(message_html)



    
import requests
# LinearRegression is a machine learning library for linear regression
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

# pandas and numpy are used for data manipulation
import pandas as pd
import numpy as np

# matplotlib and seaborn are used for plotting graphs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use('seaborn-darkgrid')

# yahoo finance is used to fetch data
import yfinance as yf

date = '2020-07-23'

def prediction(ticker):
    # Read data
    data = yf.download(ticker+'.SA', '2016-01-01', '2020-07-25', auto_adjust=True, interval='1d')

    # Define explanatory variables
    data = data[['Close']]
    data['S_3'] = data['Close'].rolling(window=3).mean()
    data['S_9'] = data['Close'].rolling(window=9).mean()
    data['S_21'] = data['Close'].rolling(window=21).mean()
    data = data.dropna()
    data['next_day_price'] = data['Close'].shift(-1)

    # Create a linear regression model
    linear = train(data, ['S_3', 'S_9', 'Close'])
    # decision = DecisionTreeRegressor().fit(xx_train, yy_train)

    # Preditct
    data['predicted_price'] = linear.predict(data[['S_3', 'S_9', 'Close']])
    # data['decision_predicted'] = decision.predict(data[['Close']])
    data['var'] = diff(data['predicted_price'], data['next_day_price']).replace(np.nan, 0)
    data['var'] = data['var'].shift(1)
    data['var'] = data['var'].replace(np.nan, 0)

    # print(data.tail(10))
    linear1 = train(data, ['S_3', 'var', 'Close'])
    data['new'] = linear1.predict(data[['S_3','var', 'Close']])

    #Set signal
    # data['returns'] = data['Close'].pct_change().shift(-1)
    # data['signal'] = np.where(data.predicted_price_next_day.shift(1) < data.predicted_price_next_day,1,0)

    # plt.ylabel('Cumulative Returns')
    # plt.show()
    # Predicting the Gold ETF prices
    # graph = data.copy()
    # teste = graph[-50:]
    # teste.plot(y=['predicted_price_next_day','decision_predicted', 'next_day_price'])
    # plt.legend(['linear_model','decision_model', 'price'])
    # plt.ylabel("Gold ETF Price")
    # plt.show()

    line = data.tail(5)
    print(ticker)
    print(line)
    predicted_price = round(line['predicted_price'][date], 2)
    new_price = round(line['new'][date], 2)
    close = round(line['Close'][date], 2)
    close_last = round(line['next_day_price'][date], 2)

    return (f'{predicted_price}  '
            f'[{diff(predicted_price, close)} % ] \n'
            # f'{predicted_price}  - {new_price}  - {close_aa}\n'
            f' - Fch: {close_last} Previsão: {predicted_price} Diff: {diff(predicted_price, close_last)}% \n'
            f' - Fch: {close_last} Previsão: {new_price} Diff: {diff(new_price, close_last)} %')

    return ''

def train(data, test):
    data_training = data.copy()

    # Drop rows with missing values
    # data = data.dropna()
    data_training = data_training.dropna()

    # Define independent variable
    X = data_training[test]

    # Define dependent variable
    y = data_training['next_day_price']

    # Split the data into train and test dataset
    t = .8
    t = int(t*len(data_training))

    # Train dataset
    x_train = X[:t]
    y_train = y[:t]

    # Test dataset
    x_test = X[t:]
    y_test = y[t:]

    linear =  LinearRegression().fit(x_train, y_train)

    # R square
    r2_score = linear.score(X[t:], y[t:])*100
    print(float("{0:.2f}".format(r2_score)))

    return linear

def diff(current, old):
    return round(((current*100)/old)-100, 2)


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
    'BPAC11',
    'CAML3',
    'CCRO3',
    'CIEL3',
    'COGN3',
    'CVCB3',
    'CSNA3',
    'EGIE3',
    'EMBR3',
    'GGBR4',
    'GOLL4',
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
    'TASA4',
    'USIM5',
    'VALE3',
    "VVAR3",
    'WEGE3'
    ]

tickers.append('BBDC4')

message_html = '<b>Previsões para Fechamento do Pregão - 22/07/2020</b> \n'
for t in tickers:
    message_html = f'{message_html} \n <b>{t} :</b> {prediction(t)}'

# send_message(message_html)
print(message_html)



    
# lower = [70, 79, 88, 97, 106]
# upper = [78, 87, 105, 114, 123]
# num = [5, 3, 4, 2, 6, 4]

# # for l, u, n in zip(lower, upper, num):
# # words = "line".split()
# line_new = '{:>15}{:>10}  {:>12}'.format(' words[0]', 'words[1]', 'words[2]')

# print(line_new)


# ​	  
# EMA=Price(t)×k+EMA(y)×(1−k)
# where:
# t=today
# y=yesterday
# N=number of days in EMA
# k=2÷(N+1)
# ​	

# EMA = price x 0,2 + EMA(y)


# EMA
# "2000-07-04": "2.5688"
# "2000-07-03":"2.5368"
# "2000-06-30":"2.5127"
# "2000-06-29":"2.4988"


# # Price

# "2000-07-04": "2.6834",
# "2000-07-03": "2.6329",
# "2000-06-30": "2.5686",
# "2000-06-29": "2.5133",
# "2000-06-28": "2.5243",
# "2000-06-27": "2.4823",
# "2000-06-26": "2.5133",
# "2000-06-23": "2.5243",
# "2000-06-22": "2.5022",
# "2000-06-21": "2.5133",
# "2000-06-20": "2.4845",
# "2000-06-19": "2.4313",



# def ema(period, prices):

#     count = 1
#     multiplier = 2 / (period+1)
#     average = 0
    
#     for value in prices:
#         if count < period:
#             average += value
#             count += 1
#             continue
#         elif count == period:
#             average = average / (period - 1)
#             count += 1
        
#         ema = (((value - average) * multiplier) + average)
#         average = ema
#         print(ema)
        
        
# ema(9, [2.4313, 2.4845, 2.5133, 2.5022, 2.5243,2.5133, 2.4823,2.5243, 2.5133, 2.5686, 2.6329])      
#   

# print('/stocks  bbdc4'.replace('/stocks ', '').replace(" ", "").upper())

import requests
import time

tickers = ["ABEV3", "AMAR3", "AZUL4", "B3SA3", "BBAS3",
               "BBDC4", "BBSE3", "BIDI4", "BOVA11", "BEEF3",
               "BRFS3", "BRKM5", "BRML3", "CAML3", "CCRO3",
               "CIEL3", "CMIG4", "CNTO3", "COGN3", "CSAN3",
               "CSNA3", "CYRE3", "CVCB3", "ECOR3", "EGIE3",
               "ELET3", "EMBR3", "EQTL3", "EZTC3", "FLRY3",
               "GFSA3", "GNDI3", "GOLL4", "GUAR3", "GGBR4",
               "GOAU4", "HBOR3", "HYPE3", "IRBR3", "ITSA4",
               "ITUB4", "JBSS3", "JHSF3", "KLBN11", "LAME4",
               "LINX3", "LREN3", "MGLU3", "MEAL3", "MRFG3",
               "ODPV3", "PETR4", "QUAL3", "RADL3", "RAIL3",
               "RENT3", "RAPT4", "SANB11", "SAPR4", "SMLS3",
               "SBSP3", "SUZB3", "TAEE11", "TASA4", "TCSA3",
               "UGPA3", "USIM5", "VALE3", "VIVT4", "VVAR3",
               "WEGE3", "WIZS3", "YDUQ3"]

for t in tickers:
    response = requests.get(f'https://ravensp.herokuapp.com/stocks/{t}')
    print(response)
    time.sleep(0.2)

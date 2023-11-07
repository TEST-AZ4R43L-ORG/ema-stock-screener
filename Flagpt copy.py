from yahoo_fin.stock_info import *
from datetime import date,datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np



today=datetime.now()
print(today)
ed_date= (today + timedelta(days=1)).strftime("%m/%d/%Y")
print(ed_date)
# 3 months data
st_date= (today - timedelta(days=90)).strftime("%m/%d/%Y")
print(st_date)
ticker_list=['TATACHEM.NS','BAJAJ-AUTO.NS', 'BAJAJFINSV.NS']#, 'BAJFINANCE.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'GRASIM.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'ITC.NS', 'KOTAKBANK.NS', 'LT.NS']#, 'MARUTI.NS', 'M&M.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'RELIANCE.NS', 'SHREECEM.NS', 'TATACONSUM.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'WIPRO.NS']
#ticker_list=['IRCTC.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'GRASIM.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'ITC.NS', 'KOTAKBANK.NS', 'LT.NS', 'MARUTI.NS', 'M&M.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'RELIANCE.NS', 'SHREECEM.NS', 'TATACONSUM.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'WIPRO.NS', 'PIIND.NS']

now=datetime.now()
historical_datas = {}
ema26={}
ema13={}
ema5={}

for ticker in ticker_list:
    historical_datas[ticker] = get_data(ticker, start_date = st_date, end_date = ed_date, index_as_date = True, interval='1d')
    ema26[ticker] = historical_datas[ticker]['close'].ewm(span=26).mean()
    ema13[ticker] = historical_datas[ticker]['close'].ewm(span=13).mean()
    ema5[ticker] = historical_datas[ticker]['close'].ewm(span=5).mean()
hist_dates=historical_datas['BAJAJ-AUTO.NS'].index

dates=[]

t=None
for d in hist_dates:
    tm=d.month
    td=d.day
    dates.append(str(td)+'/'+str(tm))

print('\ndates formatting complete\n')

# print(dates)
results={}
#intialise results dict with index list
for ticker in ticker_list:
    results[ticker]=[]

for ticker in ticker_list:
    print(ticker)
    # print(type(ema5[ticker]))
    # print(ema13[ticker])
    # print(ema26[ticker])
    for date in ema5[ticker].index:
        print(date)
        # print(ema5[ticker][date])
        # print(ema13[ticker][date])
        # print(ema26[ticker][date])

        if ema5[ticker][date] > ema13[ticker][date] and ema13[ticker][date] > ema26[ticker][date]:
            print("Upwards flag")
            results[ticker].append(1)
        elif ema5[ticker][date] < ema13[ticker][date] and ema13[ticker][date] < ema26[ticker][date]:
            print("Downwards flag")
            results[ticker].append(-1)
        else:
            print("No flag")
            results[ticker].append(0)
        
        
print(results)


# plots=[]
# for i in range(0,4):
#     for j in range(0,4):
#         plots.append(plt.subplot2grid((4, 4), (i, j)))   #Change HERE


# for ticker in ticker_list:
#     cur_plot=plots.pop()
#     cur_plot.plot(dates, ema5[ticker], color='r', label='ema5')
#     cur_plot.plot(dates, ema13[ticker], color='b', label='ema13')
#     cur_plot.plot(dates, ema26[ticker], color='g', label='ema26')
#     cur_plot.set_title(ticker)

# plt.tight_layout()
# plt.show()


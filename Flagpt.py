import tkinter as tk
from yahoo_fin.stock_info import *
from datetime import date,datetime
# import matplotlib.pyplot as plt
"""ticker_list=tickers_nifty50()
print(ticker_list)
print(type(ticker))
print(len(ticker))"""

today=date.today()
ed_date=today.strftime("%m/%d/%Y")
st_date=ed_date[:-1]+'0'
#ticker_list=['TATACHEM.NS','BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'GRASIM.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'ITC.NS', 'KOTAKBANK.NS', 'LT.NS', 'MARUTI.NS', 'M&M.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'RELIANCE.NS', 'SHREECEM.NS', 'TATACONSUM.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'WIPRO.NS', 'PIID.NS']
ticker_list=['IRCTC.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'GRASIM.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'ITC.NS', 'KOTAKBANK.NS', 'LT.NS', 'MARUTI.NS', 'M&M.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'RELIANCE.NS', 'SHREECEM.NS', 'TATACONSUM.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'WIPRO.NS']

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



def last_intersec(ticker):
    for i in range(len(ema26[ticker])-1,26):
        if ((ema5[ticker][i]>ema13[ticker][i] and ema13[ticker][i]>ema26[ticker][i]) and not(ema5[ticker][i-1]>ema13[ticker][i-1] and ema13[ticker][i-1]>ema26[ticker][i-1])):
            return ema26[ticker].index[i]
    return 'None'



def main():
    window=tk.Tk()
    window.title("Flags Overview")
    window.geometry('700x600')
    window.resizable(0,0)

    date_frame=tk.Frame(window)
    date_label=tk.Label(date_frame, text='Last Updated: -> '+now.strftime("%d/%m/%Y %H:%M:%S"))
    date_label.pack()
    date_frame.pack()

    data_frame=tk.Frame(window)

    class Table:
        def __init__(self,root):
            for i in range(total_rows):
                for j in range(total_columns):
                    wd=17
                    if j==0:
                        wd=20
                    elif j>0 and j<4:
                        wd=10
                    self.e = tk.Entry(root, width=wd,
                                font=('Arial',8,'bold'))
                    
                    self.e.grid(row=i, column=j)
                    self.e.insert(tk.END, lst[i][j])
                    ##########
                    self.e.configure({"background": "green"})
                    self.e.configure(state='readonly')


    total_rows=len(ticker_list)+1
    total_columns=7
    lst=[('Name', 'ema5', 'ema13', 'ema26', 'Current Flag', 'Last Up Intersection', 'Pending status')]

    for ticker in ticker_list:
        lst_name=ticker
        lst_ema5=float("{:.2f}".format(ema5[ticker][-1]))
        lst_ema13=float("{:.2f}".format(ema13[ticker][-1]))
        lst_ema26=float("{:.2f}".format(ema26[ticker][-1]))

        lst_cur='None'
        if lst_ema5>lst_ema13 and lst_ema13>lst_ema26:
            lst_cur='Upward Flag'
        elif lst_ema5<lst_ema13 and lst_ema13<lst_ema26:
            lst_cur='Downward Flag'

        lst_intersec=str(last_intersec(ticker))
        lst_status='None'

        if lst_cur=='None':
            if abs(lst_ema5-lst_ema26)<0.08*lst_ema26:
                lst_status='Flags close'

        lst.append((lst_name,lst_ema5,lst_ema13,lst_ema26,lst_cur, lst_intersec, lst_status))


    t=Table(data_frame)
    data_frame.pack()
    


    window.mainloop()

if __name__=='__main__':
    main()
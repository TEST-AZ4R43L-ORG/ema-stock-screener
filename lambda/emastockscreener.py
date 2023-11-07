from yahoo_fin.stock_info import *
import datetime
from datetime import date, datetime, timedelta
# import matplotlib.pyplot as plt
import boto3
import os
import random
import string
import logging
import base64
import json
logging.getLogger("pandas").setLevel(logging.DEBUG)

def publish_to_sns(table):
    HTML_EMAIL_CONTENT = """Today's Stock Eval: "{}""".format(table)


    topic_arn = "arn:aws:sns:us-east-1:123456789123:StockNotifier"
    sns = boto3.client("sns", region_name="us-east-1")
    response = sns.publish(TargetArn=topic_arn,Message=HTML_EMAIL_CONTENT,Subject="Recent Stock Flags - "+datetime.now().strftime('%d-%m-%Y'))

def send_html_email(table):
    ses_client = boto3.client("ses")
    CHARSET = "UTF-8"
    HTML_EMAIL_CONTENT = """
        <html>
            <head></head>
            <br>
            Today's Stock Eval: <a target=\"_blank\" href=\"{}\"> Flags Table</a><br>
            </body>
        </html>
    """.format(table)
    #print(HTML_EMAIL_CONTENT)
    response = ses_client.send_email(
        Destination={
            "ToAddresses": os.environ['EMAILS'].split(","),
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": HTML_EMAIL_CONTENT,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Top Stock Flags - "+datetime.now().strftime('%d-%m-%Y'),
            },
        },
        Source="kale.shantanu101@gmail.com"
    )
    
    return HTML_EMAIL_CONTENT


def dict2htmltable(tickers,dates,data):
    html = '<thead><tr style="text-align: center;"><th style="min-width: 90px;"></th>'
    html += ''.join('<th style="min-width: 130px;">' + x + '</th>' for x in tickers)
    index=29
    html += '</tr></thead><tbody>'
    for date in dates:  
        html+='<tr><td>'+str(date).split(" ")[0]+'</td>'

        for ticker in tickers:
            # html+='<td>'+str(data[ticker][index])+'</td>'
            if int(data[ticker][index]) == 1:
                html+="<td style='background-color: green;text-align: center;'>Flag Up</td>"
            
            elif int(data[ticker][index]) == -1:
                html+="<td style='background-color: red;text-align: center;'>Flag Down</td>"
            
            elif int(data[ticker][index]) == 0:
                html+="<td style='background-color: yellow;text-align: center;'>No Flag</td>"
        index-=1            
        html+='</tr>'
            # html += '<tr>' + ''.join('<td>' + x + '</td>' for x in d.values()) + '</tr>'
    html += '</tbody>'
    return '<table border=1 class="stocktable" id="table1">' + html + '</table>'

def lambda_handler(event, context):
    today = datetime.now()
    # print(today)
    ed_date = (today + timedelta(days=1)).strftime("%m/%d/%Y")
    # print(ed_date)
    # 3 months data
    st_date = (today - timedelta(days=355)).strftime("%m/%d/%Y")
    # print(st_date)
    # ticker_list = [
    #     "TATACHEM.NS",
    #     "BAJAJ-AUTO.NS",
    #     "BAJAJFINSV.NS",
    #     "LT.NS",
    # ]  
    # , 'BAJFINANCE.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'GRASIM.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'ITC.NS', 'KOTAKBANK.NS', 'LT.NS']#, 'MARUTI.NS', 'M&M.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'RELIANCE.NS', 'SHREECEM.NS', 'TATACONSUM.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'WIPRO.NS']
    ticker_list=["BAJAJ-AUTO.NS","BAJAJFINSV.NS","TATACHEM.NS",'IRCTC.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'GRASIM.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'ITC.NS', 'KOTAKBANK.NS', 'LT.NS', 'MARUTI.NS', 'M&M.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'RELIANCE.NS', 'SHREECEM.NS', 'TATACONSUM.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'WIPRO.NS', 'PIIND.NS']
    
    now = datetime.now()
    historical_datas = {}
    ema26 = {}
    ema13 = {}
    ema5 = {}
    
    for ticker in ticker_list:
        historical_datas[ticker] = get_data(
            ticker, start_date=st_date, end_date=ed_date, index_as_date=True, interval="1d"
        )
        print("Data acquired for " + ticker)
        ema26[ticker] = historical_datas[ticker]["close"].ewm(span=26, adjust=True).mean()
        ema13[ticker] = historical_datas[ticker]["close"].ewm(span=13, adjust=True).mean()
        ema5[ticker] = historical_datas[ticker]["close"].ewm(span=5, adjust=True).mean()
        # print(historical_datas[ticker]['close'].ewm(span=5))
    hist_dates = historical_datas["BAJAJ-AUTO.NS"].index
    # exit()
    
    dates = []
    print("Data acquired")
    t = None
    for d in hist_dates:
        tm = d.month
        td = d.day
        dates.append(str(td) + "/" + str(tm))
    
    print("\ndates formatting complete\n")
    
    # print(dates)
    results = {}
    # intialise results dict with index list
    for ticker in ticker_list:
        results[ticker] = []
    
    for ticker in ticker_list:
        # print(ticker)
        # print(type(ema5[ticker]))
        # print(ema13[ticker])
        # print(ema26[ticker])
        for date in hist_dates:
            # print(date)
            # print(ema5[ticker][date])
            # print(ema13[ticker][date])
            # print(ema26[ticker][date])
    
            if (
                ema5[ticker][date] > ema13[ticker][date]
                and ema13[ticker][date] > ema26[ticker][date]
            ):
                # print("Upwards flag")
                results[ticker].append(1)
            elif (
                ema5[ticker][date] < ema13[ticker][date]
                and ema13[ticker][date] < ema26[ticker][date]
            ):
                # print("Downwards flag")
                results[ticker].append(-1)
            else:
                # print("No flag")
                results[ticker].append(0)
    
    
    # print(results)
    new_results={}
    for ticker, values in results.items():
        new_results[ticker]=values[-30:]
        # print(len(new_results[ticker]))
    # print(new_results)
    print("Formatting hist dates")
    dates=hist_dates[-30:][::-1]
    # print(dates)
    html=dict2htmltable(ticker_list,dates,new_results)
    # print(html)
    print("Generated HTMl")
    # with open("/tmp/StockHistory3.html","w") as f:
    #     f.write(html)
    #     f.close()
    print("written file")
    """
    # convert results dict to dataframe
    df = pandas.DataFrame(new_results)
    # change column rows to dates
    df.index = hist_dates[-30:]
    # Get last 30 days of data and reverse it
    df = df.iloc[-30:][::-1]
    df.style.background_gradient(subset=["C"], cmap="RdYlGn", vmin=-1, vmax=1)
    df.style.set_table_styles([dict(selector='th', props='min-width: 600px;'),])
    # print(df)
    # pandas.set_option('display.max_colwidth', 400)
    df.to_html("/tmp/StockHTML.html",col_space='130px', justify='center')
    new_html_file=""
    new_f=open("/tmp/StockHTML.html","r")
    for line in new_f.readlines():
        if ">1<" in line:
            new_html_file+="<td style='background-color: green;text-align: center;'>Flag Up</td>"
        
        elif  ">-1<" in line:
            new_html_file+="<td style='background-color: red;text-align: center;'>Flag Down</td>"
        
        elif ">0<" in line:
            new_html_file+="<td style='background-color: yellow;text-align: center;'>No Flag</td>"
        else:
            new_html_file+=line+"\n"
    
    with open("/tmp/StockHistory3.html","w") as f:
        f.write(new_html_file)
        f.close()
    """
    # random_string=(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))).lower()
    random_string=datetime.now().strftime('%f')
    print("Random generated")
    lambda_=boto3.client("lambda")
    print("got lambbda")
    print(type(html))
    lambda_payload = {"html":str(base64.b64encode(html.encode("ascii"))).encode("utf-8")}
    # print(base64.b64encode(html.encode("ascii")))
    print(type(base64.b64encode(html.encode("ascii"))))
    payload3 = {"html":html}
    pyld=json.dumps(payload3)
    resp=lambda_.invoke(FunctionName='s3uploader',
                     InvocationType='RequestResponse',
                     Payload=pyld)
    print(resp)
    print("invoked htnl")
    """
    s3_ = boto3.client('s3', region_name="ap-south-1")
    print("got s3 resource")
    file_path="https://sins3bucektvalue.s3.ap-south-1.amazonaws.com/"
    file_name=datetime.now().strftime('%Y-%m-%d')+'-'+random_string+'z'
    file_path+=file_name+'.html'
    
    print("creating s3 object")
    object = s3_.Object('sins3bucektvalue', file_name+'.html')
    print("going to put object")
    result = object.put(Body=open('/tmp/StockHistory3.html', 'rb'),ContentType='xml')
    print(file_path)
    publish_to_sns(file_path)
    """
    return "OK"
"""
dict_data={}
date_headers=""
for ticker in ticker_list:
    dict_data[ticker]=""
    # print(len(results[ticker]))
    for day in range(len(results[ticker])-1,len(results[ticker])-30,-1):
        # print(day)
        prev = results[ticker][day - 1]
        curr = results[ticker][day]
        # create a html table with the results with the header columns as dates, row header as ticker name, and horizontal values the results
        date_headers+=dates[day]+","


        if prev != curr:
            if curr == 1:
                # print("Buy " + ticker + " on " + dates[day])
                # dict_data[ticker]+="<td style='background-color: green;'>"+str(dates[day])+"</td>"
                dict_data[ticker]+="green,"
                print("Upwards flag on "+ticker+" on "+dates[day])
                # broker.buy(
                #     ticker,
                #     1,
                #     round(historical_datas[ticker]["close"][hist_dates[day]],2),
                #     dates[day],
                # )
            elif curr == -1:
                dict_data[ticker]+="red,"
                # dict_data[ticker]+="<td style='background-color: red;'>"+str(dates[day])+"</td>"
                pass
                # broker.sell(
                #     ticker,
                #     1,
                #     round(historical_datas[ticker]["close"][hist_dates[day]],2),
                #     dates[day],
                # )
                
            elif curr == 0 and prev == 1:
                dict_data[ticker]+="yellow,"

                # dict_data[ticker]+="<td style='background-color: yello;'>"+str(dates[day])+"</td>"
                pass
                # try:
                #     broker.sell(
                #         ticker,
                #         1,
                #         round(historical_datas[ticker]["close"][hist_dates[day]],2),
                #         dates[day],
                #     )
                # except:
                #     print(ticker)
                #     print(day)
                #     print(hist_dates[day-1])
                #     print(hist_dates)

                #     print(hist_dates[day])
            elif curr == 0 and prev == -1:
                dict_data[ticker]+="yellow,"
                # dict_data[ticker]+="<td style='background-color: yello;'>"+str(dates[day])+"</td>"
                pass
        else:
            dict_data[ticker]+="white,"
            # dict_data[ticker]+="<td>"+str(dates[day])+"</td>"
print(date_headers)
print(dict_data)

csv_string="Ticker,"+date_headers+"\n"
for ticker in ticker_list:
    csv_string+=ticker+","+dict_data[ticker]+"\n"
print(csv_string)

with open("output.csv","w") as f:
    f.write(csv_string)
    f.close()
import pandas 
file = pandas.read_csv("output.csv")
file.to_html("StockHistory.html")
"""
# lambda_handler(None,None)
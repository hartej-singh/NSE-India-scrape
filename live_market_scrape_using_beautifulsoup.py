# HARTEJ SINGH (+917405559669, hartejsingh2001@gmail.com)

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from requests.api import head

d1a = {}
d1b_corporate_announcements = {}
d1b_board_meetings = {}
d1b_financial_results = {}
d1b_corporate_actions = {}
d1c = {}

stock = str(input("Enter stock code: ")) # example = ['INFY', 'SBIN']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}


# Objective 1a - Details of a Stock
url1 = requests.get(f'https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={stock}', headers=headers).text
soup = BeautifulSoup(url1, 'lxml')
stock_data = json.loads(soup.find('div', id='responseDiv').text.strip())["data"][0]
d1a['StockName'] = stock_data['companyName']
d1a['StockCode'] = stock_data['symbol']
d1a['open'] = stock_data['open']
d1a['HighDay'] = stock_data['dayHigh']
d1a['LowDay'] = stock_data['dayLow']
d1a['Date'] = stock_data['recordDate']
d1a['Symbol'] = stock_data['symbol']
d1a['ISINcode'] = stock_data['isinCode']
d1a['closePrice'] = stock_data['closePrice']
d1a['totalTradedVolume'] = stock_data['totalTradedVolume']
d1a['deliveryToTradedQuantity'] = stock_data['deliveryToTradedQuantity']
d1a['VWAP'] = stock_data['averagePrice']
d1a['FaceValue'] = stock_data['faceValue']
d1a['TradedVolume'] = stock_data['totalTradedVolume']
d1a['TradedValue'] = stock_data['totalTradedValue']
d1a['FreeFloatMarketCap'] = stock_data['cm_ffm']
d1a['52weekHigh'] = stock_data['high52']
d1a['52weekLow'] = stock_data['low52']
d1a['LowerPriceBand'] = stock_data['pricebandlower']
d1a['UpperPriceBand'] = stock_data['pricebandupper']
t1 = ['buyQuantity', 'buyPrice', 'sellPrice', 'sellQuantity']
for i in range(5):
    for j in range(4):
        q = t1[j] + str(i+1)
        d1a[q] = stock_data[q]
print("d1a\n", json.dumps(d1a, indent=2))


# Objective 1b - Details of a Stock - Comapany Information 
# Corporate Announcements
url2 = requests.get(f"https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/companySnapshot/getAnnouncements{stock}.json", headers=headers).text
corporate_announcements = url2.split(":")
j = 1
for i in range(len(corporate_announcements)):
    if corporate_announcements[i].endswith('desc"'):
        x = 'Description' + str(j)
        d1b_corporate_announcements[x] = corporate_announcements[i+1].split(",")[0].strip('"')
        y = 'Date' + str(j)
        d1b_corporate_announcements[y] = corporate_announcements[i+2].split("}")[0].strip('"')
        j = j+1
print("\n\nd1b_corporate_announcements\n", json.dumps(d1b_corporate_announcements, indent=2))

# Board Meetings
url3 = requests.get(f"https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/companySnapshot/getBoardMeetings{stock}.json", headers=headers).text
board_meetings = url3.split(":")
j = 1
for i in range(len(board_meetings)):
    if board_meetings[i].endswith('Purpose"'):
        x = 'Purpose' + str(j)
        d1b_board_meetings[x] = board_meetings[i+1].split(",")[0].strip('"')
        y = 'BoardMeetingDate' + str(j)
        d1b_board_meetings[y] = board_meetings[i+2].split('"')[1].strip('"')
        j = j+1
print("\n\nd1b_board_meetings\n", json.dumps(d1b_board_meetings, indent=2))

# Financial Result
url4 = requests.get(f"https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/companySnapshot/getFinancialResults{stock}.json", headers=headers).text
financial_results = url4.split(":")
for i in range(len(financial_results)):
    if financial_results[i].endswith('toDate"'):
        j = financial_results[i+1].split(",")[0].strip('"')
        x = 'TotalIncome_' + str(j)
        d1b_financial_results[x] = financial_results[i].split('",')[0].strip('"')
    if financial_results[i].endswith('reProLossBefTax"'):
        y = 'PBT_' + j
        d1b_financial_results[y] = financial_results[i+1].split('",')[0].strip('"')
    if financial_results[i].endswith('proLossAftTax"'):
        z = 'NetProfit/Loss_' + j
        d1b_financial_results[z] = financial_results[i+1].split('}')[0].strip('"')
print("\n\nd1b_financial_results\n", json.dumps(d1b_financial_results, indent=2))

# Corporate Actions
url5 = requests.get(f"https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/companySnapshot/getCorporateActions{stock}.json", headers=headers).text
corporate_actions = url5.split(":")
j = 1
for i in range(len(corporate_actions)):
    if corporate_actions[i].endswith('sub"'):
        x = 'Purpose' + str(j)
        d1b_corporate_actions[x] = corporate_actions[i+1].split(",")[0].strip('"')
        y = 'Ex-Date' + str(j)
        d1b_corporate_actions[y] = corporate_actions[i+2].split('"')[1].strip('"')
        j = j+1
print("\n\nd1b_corporate_actions\n", json.dumps(d1b_corporate_actions, indent=2))


# Objective 1c - Details of a Stock - Peer Comparison 
c1 = json.loads(soup.find('div', id='responseDiv').text.strip())["data"][0]
d1c['FaceValue'] = stock_data['faceValue']
d1c['LTP'] = stock_data['lastPrice']
d1c['%change'] = stock_data['pChange']
d1c['TradedValue'] = stock_data['totalTradedValue']
d1c['TradedVolume'] = stock_data['totalTradedVolume']
d1c['VWAP'] = stock_data['averagePrice']
d1c['ExDate'] = stock_data['exDate']
d1c['CorporateAction'] = stock_data['purpose']
d1c['QtyTraded'] = stock_data['totalTradedVolume']
d1c['DeliverableQty'] = stock_data['deliveryQuantity']
d1c['%DeliveryQtytoTradedQty'] = stock_data['deliveryToTradedQuantity']
d1c['Security VaR'] = stock_data['securityVar']
d1c['VaRMargin'] = stock_data['varMargin']
d1c['ApplicableMarginRate'] = stock_data['applicableMargin']
d1c['ExtremeLossRate'] = stock_data['extremeLossMargin']
print("\n\nd1c\n", json.dumps(d1c, indent=2))


# Objective 1d - Details of a Stock - Historical data
history_available = ['1day', '7days', '2weeks', '1month', '3months']
print("\n\n", history_available)
for_past = str(input("View historical price data for past (select from above list): "))
for_past = for_past.replace(" ", "").lower()
url6 = requests.get(f"https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol={stock}&series=EQ&fromDate=undefined&toDate=undefined&datePeriod={for_past}", headers=headers).text
soup2 = BeautifulSoup(url6, 'lxml')
historical_data0 = str(soup2.find('div', id='csvContentDiv')).strip('<div id="csvContentDiv" style="display:none;"').strip('</div>')
historical_data1 = historical_data0.split(":")
d1d_historical_data = {"Date":[], "Symbol":[], "Series":[], "Open Price":[], "High Price":[],"Low Price":[], "Last Traded Price ":[] ,"Close Price":[], "Total Traded Quantity":[], "Turnover (in Lakhs)":[]}
for i in range(1,(len(historical_data1)-1)):
    x = historical_data1[i].split('","')
    d1d_historical_data["Date"].append(x[0].strip('"'))
    d1d_historical_data["Symbol"].append(x[1])
    d1d_historical_data["Series"].append(x[2])
    d1d_historical_data["Open Price"].append(x[3])
    d1d_historical_data["High Price"].append(x[4])
    d1d_historical_data["Low Price"].append(x[5])
    d1d_historical_data["Last Traded Price "].append(x[6].strip("       "))
    d1d_historical_data["Close Price"].append(x[7])
    d1d_historical_data["Total Traded Quantity"].append(x[8])
    d1d_historical_data["Turnover (in Lakhs)"].append(x[9].strip('"'))
print("\n\nd1d_historical_data\n", json.dumps(d1d_historical_data, indent=2))


# exporting to csv
path = r'C:\Users\admin\Desktop\'
c1a = pd.DataFrame(d1a, index=[0])
c1a.to_csv(f'{path}\Objective-1a.csv')

c1b_board_meetings = pd.DataFrame(d1b_board_meetings, index=[0])
c1b_board_meetings.to_csv(f'{path}\Objective-1b_BoardMeetings.csv')

c1b_corporate_actions = pd.DataFrame(d1b_corporate_actions, index=[0])
c1b_corporate_actions.to_csv(f'{path}\Objective-1b_CorporateActions.csv')

c1b_corporate_announcements = pd.DataFrame(d1b_corporate_announcements, index=[0])
c1b_corporate_announcements.to_csv(f'{path}\Objective-1b_CorporateAnnouncements.csv')

c1b_financial_results = pd.DataFrame(d1b_financial_results, index=[0])
c1b_financial_results.to_csv(f'{path}\Objective-1b_FinancialResults.csv')

c1c = pd.DataFrame(d1c, index=[0])
c1c.to_csv(f'{path}\Objective-1c.csv')

c1d_historical_data = pd.DataFrame.from_dict(d1d_historical_data)
c1d_historical_data.to_csv(f'{path}\Objective-1d_HistoricalData.csv')

print("\n\n")
print(f"Objective 1: Exported succefully to {path} files.")
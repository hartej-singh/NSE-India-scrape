# HARTEJ SINGH (+917405559669, hartejsingh2001@gmail.com)

from selenium import webdriver
from webdrivermanager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd

stock = str(input("Enter stock code: ")) # example = ['INFY', 'SBIN']
driver = webdriver.Chrome(executable_path=r'C:\Users\admin\Downloads\chromedriver_win32\chromedriver')
driver.minimize_window()
driver.get(f"https://www1.nseindia.com/companytracker/cmtracker.jsp?symbol={stock}")
driver.implicitly_wait(10)
sleep(1)

# Objective 2a - Company Information , Corporate Actions and Annoncements
# Company Information
t = driver.find_element_by_id('compInfo')
x = t.text.split("\n")
d2a_compInfo = {}
for i in range(len(x)):
    if i==0:
        d2a_compInfo['StockName'] = x[i]
    elif i==10:
        d2a_compInfo['Other'] = x[i]
    else:
        l = x[i].split(":")
        d2a_compInfo[l[0]] = l[1]
print("d2a_compInfo\n", d2a_compInfo)

# Corporate Actions
t = driver.find_element_by_id('corpAction')
x = t.text.split("\n")
d2a_corpAction = {'Ex-Date':[] , 'Purpose':[]}
for i in range(1,len(x)):
    l = x[i].split(":")
    d2a_corpAction['Ex-Date'].append(l[0])
    d2a_corpAction['Purpose'].append(l[1])
print("\n\nd2a_corpAction\n", d2a_corpAction)

# Announcements
t = driver.find_element_by_id('annoucement')
x = t.text.split("\n")
d2a_announcments = {'Content':[] , 'Date':[], 'Time':[]}
for i in range(len(x)):
    l = x[i].strip("  - ")
    d2a_announcments['Time'].append(l[-5:])
    d2a_announcments['Date'].append(l[-19:-7])
    d2a_announcments['Content'].append(l[:-20])
print("\n\nd2a_announcments\n", d2a_announcments)


# Objective 2b - Price Watch
t = driver.find_element_by_id('centertab')
x = t.text.split("\n")
d2b = {'Security':[], 'LTP':[], 'Buy Qty':[], 'Buy Price':[], 'Sell Price':[], 'Sell Qty':[], 'Turnover':[], 'Premium Turnover':[]}
for i in range(len(x)):
    if x[i] == 'Equity Shares':
        d2b['Security'].append(x[i])
        d2b['LTP'].append(x[i+1])
        d2b['Buy Qty'].append(x[i+2])
        d2b['Buy Price'].append(x[i+3])
        d2b['Sell Price'].append(x[i+4])
        d2b['Sell Qty'].append(x[i+5])
        d2b['Turnover'].append(x[i+6])
        d2b['Premium Turnover'].append(x[i+7])
    elif x[i] == 'Most Active Futures' or x[i] == 'Most Active Call' or x[i] == 'Most Active Put' or x[i] == 'Most Active Nifty 50 Futures':
        d2b['Security'].append(x[i] + " " + x[i+1])
        d2b['LTP'].append(x[i+2])
        d2b['Buy Qty'].append(x[i+3])
        d2b['Buy Price'].append(x[i+4])
        d2b['Sell Price'].append(x[i+5])
        d2b['Sell Qty'].append(x[i+6])
        d2b['Turnover'].append(x[i+7])
        d2b['Premium Turnover'].append(x[i+8])
    elif x[i] == 'Most Active Nifty Midcap 50 Futures':
        d2b['Security'].append(x[i])
        d2b['LTP'].append(" ")
        d2b['Buy Qty'].append(" ")
        d2b['Buy Price'].append(" ")
        d2b['Sell Price'].append(" ")
        d2b['Sell Qty'].append(" ")
        d2b['Turnover'].append(" ")
        d2b['Premium Turnover'].append(x[i+1])
print("\n\nd2b\n", d2b)


# Objective 2c - Financial Results
driver = webdriver.Chrome(executable_path=r'C:\Users\admin\Downloads\chromedriver_win32\chromedriver')
driver.minimize_window()
driver.get(f"https://www1.nseindia.com//marketinfo/companyTracker/resultsCompare.jsp?symbol={stock}")
driver.implicitly_wait(10)
sleep(1)
d2c = {}
keys = []
t1 = []
t2 = []
t3 = []
t4 = []
t5 = []
t6 = []
for i in range(1,7):
    t = driver.find_element_by_xpath(f"/html/body/table/tbody/tr/td/table[3]/tbody/tr[1]/td[{i}]").text
    keys.append(t)

for j in range(2,42):
    if j == 7:
        pass
    else:
        for i in range(1,7):
            t = driver.find_element_by_xpath(f"/html/body/table/tbody/tr/td/table[3]/tbody/tr[{j}]/td[{i}]").text
            if i==1:
                t1.append(t)
            elif i==2:
                t2.append(t)
            elif i==3:
                t3.append(t)
            elif i==4:
                t4.append(t)
            elif i==5:
                t5.append(t)
            elif i==6:
                t6.append(t) 
for i in range(0,6):
    if i==0:
        d2c[keys[(i)]] =  t1
    elif i==1:
        d2c[keys[(i)]] =  t2
    elif i==2:
        d2c[keys[(i)]] =  t3
    elif i==3:
        d2c[keys[(i)]] =  t4
    elif i==4:
        d2c[keys[(i)]] =  t5
    elif i==5:
        d2c[keys[(i)]] =  t6
print("\n\nd2c\n", d2c)


# Objective 2d - Board Meetings
driver.get(f"https://www1.nseindia.com//marketinfo/companyTracker/boardMeeting.jsp?symbol={stock}")
driver.implicitly_wait(10)
sleep(1)
d2d_boardMeetings = {'Meeting Date':[], 'Meeting Purpose':[]}
rows = 1 + len(driver.find_elements_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr"))
for i in range (1, rows):
    t1 = driver.find_element_by_xpath(f"/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[{i}]/td[1]").text
    d2d_boardMeetings['Meeting Date'].append(t1) 
    t2 = driver.find_element_by_xpath(f"/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[{i}]/td[2]").text
    d2d_boardMeetings['Meeting Purpose'].append(t2)
print("\n\nd2d_boardMeetings\n", d2d_boardMeetings)


# Objective 2e - Trade History
driver.get(f"https://www1.nseindia.com//marketinfo/companyTracker/tradeHistory.jsp?symbol={stock}")
driver.implicitly_wait(10)
sleep(1)
rows = 1+ len(driver.find_elements_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr"))
d2e = {'Date':[], 'High Price':[], 'Low Price':[], 'Close Price':[], 'Total Traded Quantity':[], 'Turnover':[], 'No Of Contracts':[]}
for i in range(2, rows):
    d2e['Date'].append(driver.find_element_by_xpath(f"/html/body/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[{i}]/td[1]").text)
    d2e['High Price'].append(driver.find_element_by_xpath(f"/html/body/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[{i}]/td[2]").text)
    d2e['Low Price'].append(driver.find_element_by_xpath(f"/html/body/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[{i}]/td[3]").text)
    d2e['Close Price'].append(driver.find_element_by_xpath(f"/html/body/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[{i}]/td[4]").text)
    d2e['Total Traded Quantity'].append(driver.find_element_by_xpath(f"/html/body/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[{i}]/td[5]").text)
    d2e['Turnover'].append(driver.find_element_by_xpath(f"/html/body/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[{i}]/td[6]").text)
    d2e['No Of Contracts'].append(driver.find_element_by_xpath(f"/html/body/table/tbody/tr/td/table/tbody/tr[2]/td[2]/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[{i}]/td[7]").text)
print("\n\nd2e\n", d2e)

driver.close()
driver.quit()

# exporting to csv
path = r'C:\Users\admin\Desktop\'
c2a_compInfo = pd.DataFrame(d2a_compInfo, index=[0])
c2a_compInfo.to_csv(f'{path}\Objective-2a_compInfo.csv')

c2a_corpActions = pd.DataFrame.from_dict(d2a_corpAction)
c2a_corpActions.to_csv(f'{path}\Objective-2a_corpAction.csv')

c2a_announcements = pd.DataFrame.from_dict(d2a_announcments)
c2a_announcements.to_csv(f'{path}\Objective-2a_announcements.csv')

c2b = pd.DataFrame.from_dict(d2b)
c2b.to_csv(f'{path}\Objective-2b.csv')

c2c = pd.DataFrame.from_dict(d2c)
c2c.to_csv(f'{path}\Objective-2c.csv')

c2d_boardMeetings = pd.DataFrame.from_dict(d2d_boardMeetings)
c2d_boardMeetings.to_csv(f'{path}\Objective-2d_boardMeetings.csv')

c2e = pd.DataFrame.from_dict(d2e)
c2e.to_csv(f'{path}\Objective-2e.csv')

print("\n\n")
print(f"Objective 2: Exported succefully to {path} files.")
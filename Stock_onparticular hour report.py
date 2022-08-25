
# Raw Package
from xmlrpc.client import _datetime
import numpy as np
import pandas as pd
import Date_time_module as DT  # Importing Date_time_module.py 
import csv  

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go
import pandas_datareader.data as web

d2 = DT.today.strftime("%b_%d_%Y")
print("d2 =", d2)
#Createing a file with Stcok name,date and Time 
Stock_name = input("Stock Name with.NS Eg RBLBANK \n")+".NS"
current_datetime = str(d2)
file_name = Stock_name +"_" +current_datetime+".csv"   

header = ['NSE Company_Name', d2] # Writing data to the countries.csv file   
with open(file_name, 'w', encoding='UTF8',newline='') as f:  # opening the file and countries.csv file in write mode and encoding the data in ITF and asking file python to write in next line with newline = ''
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)

# In data we are defining Stock name and star, end date and timeings and with time interval 5mins 
#data = yf.download(input('Stock Name with.NS Eg RBLBANK.NS \n'),start,end,interval='5m')
data = yf.download(Stock_name,DT.start,DT.end,interval='5m')

header = ['NSE Company_Name', d2, data]   
with open(file_name, 'w', encoding='UTF8',newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)

print (data)


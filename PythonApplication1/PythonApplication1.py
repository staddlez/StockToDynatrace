import stockquotes
from bs4 import BeautifulSoup as bs
import datetime
import math
import requests
import time
from alpha_vantage.timeseries import TimeSeries
from pprint import pprint


# Using Alpha Vantage API to get current price stock:
ts = TimeSeries(key=' WDT25OH0Y4H4S4Y9', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')

# Get the most recent price:
dynatraceCurrentStockPrice = data['4. close'][0]

#Get stock price every minute:
while(1):

    # For the sake of speed and simplicity, just pull from stockquotes:
    dynatrace = stockquotes.Stock('DY')
    dynaPrice = str(dynatrace.current_price)
    timeNow = str(math.floor(datetime.datetime.utcnow().timestamp() * 1000) - 14300000)

    print("Current Price: $" + dynaPrice);
    print("Time in milliseconds: " + timeNow);


    #CURL and POST metrics to the custom device "DynatraceStock"
    headers = {
        'Authorization': 'Api-Token --',
        'Content-Type': 'application/json',
    }

    data = '{ "tags": [ "tag2" ], "type": "Stock-Price", "properties" : { "Dynatrace Stock Price": "USD" }, "series" : [ { "timeseriesId" : "custom:dynatrace.stock.price","dimensions" : { "nic" : "finance"},"dataPoints" : [ [ ' + timeNow + ',' + dynaPrice + ' ] ] } ] }'
    response = requests.post(' https://mcq82513.sprint.dynatracelabs.com/api/v1/entity/infrastructure/custom/DynatraceStock', headers=headers, data=data)
    
    # Check for a 200:
    print(response.text)
    print(response.status_code)

    time.sleep(60)



# Ref:https://pypi.org/project/stockquotes/ 
# https://www.youtube.com/watch?v=1yNeUcHM7Rs
# https://curl.trillworks.com/#python
# https://stackoverflow.com/questions/25491090/how-to-use-python-to-execute-a-curl-command/48005899
# https://curl.trillworks.com/#python
# https://www.dynatrace.com/support/help/dynatrace-api/environment-api/topology-and-smartscape/custom-device-api/report-custom-device-metric-via-rest-api/
# https://github.com/RomelTorres/alpha_vantage
# https://medium.com/alpha-vantage/get-started-with-alpha-vantage-data-619a70c7f33a
# https://www.youtube.com/watch?v=1yNeUcHM7Rs

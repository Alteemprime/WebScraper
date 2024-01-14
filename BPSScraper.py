#library to handle http request
import requests
#library to handle html file manipulation
from bs4 import BeautifulSoup
#library to store scrape result to a dataframe
import pandas as pd

url = 'https://www.bps.go.id/id/statistics-table/1/MTU1OSMx/indikator-kesehatan-1995-2023.html'
#get method to get the page
html_text = requests.get(url).text

#cast instance of soup of html text parsed by lxml module
soup = BeautifulSoup(html_text, 'lxml')
#get table tags with no search filter (since there is only one table at the page)
table = soup.find('table')
#get every page line in table object
pagelines = table.find_all('tr')
#select pageline of table Title
title = pagelines[0].find('td').text
#select pageline of table column heading
column_headings = pagelines[2].find_all('td')
#define list to contain table heading
columns = []
i = 0
for column_heading in column_headings :
    i += 1
    #only do 4 number formatting after column number 3 and save the heading to a column list
    if i > 2 :
        columns.append(column_heading.text[:4])
    else :
        columns.append(column_heading.text)
#select pageline of table column data, slicing operation make column datum a list, no longer beautifulsoup class
column_datum = pagelines[3:16]
#define list to contain data for one row
row_data = []
#define list to contain table data (whole rows)
data = []

#list all text data in td tags
for table_rows in column_datum :   
    table_datas = table_rows.find_all('td')
    for table_data in table_datas :
        # remove unwanted data values while taking account '&nbsp' character returned as '\xa0' char after soup.text method
        text_content = table_data.text
        if text_content not in ['*)','**)','5)','\xa0'] :
            row_data.append(text_content)
    data.append(row_data)
    row_data=[]

#check if all data has equal length to column heading, if not display column
#list containing row data not equal to column length
not_equal_list =[]
for each_row_data in data :
    if len(each_row_data) == len(columns) :
        print(f'suitable, {len(columns)} data')
    else :
        #print(each_row_data)
        not_equal_list.append(each_row_data)

#somehow the table in url purposely, give blank spaces in data that is not available. shortening list length in assosiated table row data.
#so, for this list null values must be added manually
for each_list in not_equal_list :
    each_list.insert(13,'-')
    each_list.insert(13,'-')
    
print (columns)
print(data)
#merge column heading and column data to a single dataframe
df = pd.DataFrame(data,columns=columns)

print(df)

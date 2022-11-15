from bs4 import BeautifulSoup
import requests
import pandas as pd
# start data extraction 

current_url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie&release_date=1999-01-01,2020-12-31&user_rating=1.0,10.0&groups=oscar_nominee&colors=color&languages=en&count=250'

# get request 

response = requests.get(current_url)

# status code 

response.status_code

# Soup object 
Soup = BeautifulSoup(response.content, 'html.parser')

# result item (starting point )
list_item = Soup.find_all('div', {'class':'lister-item'})

# Data we need to extract : --> Start scraping 

# movie title :

list_item[0].find('h3').find('a').get_text()

# year :

list_item[0].find('h3').find('span', {'class':'lister-item-year'}).get_text().replace('(','').replace(')', '')

# duration 

list_item[0].find('p').find('span', {'class':'runtime'}).get_text()

# genre 

list_item[0].find('p').find('span', {'class':'genre'}).get_text().strip()

# Rating

list_item[0].find('div', {'class':'ratings-imdb-rating'}).get_text().strip()

# list comprehansion to store data :

movie_title = [result.find('h3').find('a').get_text() for result in list_item]
year  = [result.find('h3').find('span', {'class':'lister-item-year'}).get_text().replace('(','').replace(')', '') for result in list_item]
duration = [result.find('p').find('span', {'class':'runtime'}).get_text() for result in list_item]
genre = [result.find('p').find('span', {'class':'genre'}).get_text().strip() for result in list_item]
Rating = [result.find('div', {'class':'ratings-imdb-rating'}).get_text().strip() for result in list_item]

# put data into dataframe using pandas:

imbd_pd = pd.DataFrame({'Movie title': movie_title, 'Year':year, 'duration':duration, 'genre':genre, 'rating':Rating}, index=False)
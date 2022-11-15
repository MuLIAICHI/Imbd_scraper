# import moduls 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4 import BeautifulSoup
import requests
# start browse automation 
driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get('https://imdb.com')


# maximise window :
driver.maximize_window()

# change the language if it's not in english :
print("change the langauge to En")
input("hit enter to start :")
# find the drop down 
driver.implicitly_wait(100)
dropdown = driver.find_element(By.CLASS_NAME, 'ipc-icon--arrow-drop-down')
dropdown.click()

# go the advanced search and navigate to it from the dropdown menu.

advnaced_search = driver.find_element(By.LINK_TEXT,'Advanced Search')
driver.implicitly_wait(10)
advnaced_search.click()


# click on Advanced Title Search :

advs = driver.find_element(By.LINK_TEXT, 'Advanced Title Search')
driver.implicitly_wait(10)
advs.click()

# select future film :

future_film = driver.find_element(By.ID, 'title_type-1')
driver.implicitly_wait(10)
future_film.click()

# select TV movie :

tv_movie = driver.find_element(By.ID, 'title_type-2')
driver.implicitly_wait(10)
tv_movie.click()

# min date :

min_date = driver.find_element(By.NAME, 'release_date-min')
driver.implicitly_wait(10)
min_date.click()
min_date.send_keys('1999')

# max date :
max_date = driver.find_element(By.NAME, 'release_date-max')
driver.implicitly_wait(10)
max_date.click()
max_date.send_keys('2020')


# rating min : 
rating_min = driver.find_element(By.NAME, 'user_rating-min')
driver.implicitly_wait(10)
rating_min.click()
dropdown_2 = Select(rating_min)
dropdown_2.select_by_visible_text('1.0')

# rating max:
rating_max = driver.find_element(By.NAME, 'user_rating-max')
driver.implicitly_wait(10)
rating_max.click()
dropdown_3 = Select(rating_max)
dropdown_3.select_by_visible_text('10')

# get the oscar nominated  :
oscar_nom = driver.find_element(By.ID,'groups-7')
oscar_nom.click()

# chek the color box :

color = driver.find_element(By.ID, 'colors-1')
color.click()

# Select the  language :

lang = driver.find_element(By.NAME, 'languages')
driver.implicitly_wait(10)
dropdown_4 = Select(lang)
dropdown_4.select_by_visible_text('English')

# get 250 result per page :
result_count = driver.find_element(By.ID, 'search-count')
dropdown_5 = Select(result_count)
dropdown_5.select_by_index(2)

# click on the search button :

button  = driver.find_element(By.XPATH, '(//button[@type="submit"])[2]')
button.click()


# current url --> start the intersection between selenium and beautifulSoup

current_url = driver.current_url

############################################ start data extraction ###############################


# get request 

response = requests.get(current_url)

# status code 

response.status_code

# Soup object 
Soup = BeautifulSoup(response.content, 'html.parser')

# result item (starting point )
list_item = Soup.find_all('div', {'class':'lister-item'})

# list comprehansion to store data :

movie_title = [result.find('h3').find('a').get_text() for result in list_item]
year  = [result.find('h3').find('span', {'class':'lister-item-year'}).get_text().replace('(','').replace(')', '') for result in list_item]
duration = [result.find('p').find('span', {'class':'runtime'}).get_text() for result in list_item]
genre = [result.find('p').find('span', {'class':'genre'}).get_text().strip() for result in list_item]
Rating = [result.find('div', {'class':'ratings-imdb-rating'}).get_text().strip() for result in list_item]

# put data into dataframe using pandas:

imbd_pd = pd.DataFrame({'Movie title': movie_title, 'Year':year, 'duration':duration, 'genre':genre, 'rating':Rating})

# output in Excel 

imbd_pd.to_csv('imbd_movies.xlsx', index=False)
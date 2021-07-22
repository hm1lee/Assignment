from selenium import webdriver
from bs4 import BeautifulSoup
import time, os
from datetime import datetime
import pandas as pd

# review link link
link = 'https://play.google.com/store/apps/details?id=com.banhala.android&hl=ko&gl=US&showAllReviews=true'

# how many scrolls we need
scroll_cnt = 10

# download chrome driver https://sites.google.com/a/chromium.org/chromedriver/home
driver = webdriver.Chrome('../chromedriver')
driver.get(link)

os.makedirs('result', exist_ok=True)

for i in range(10):
    # scroll to bottom
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(3)

    # click 'Load more' button, if exists
    try:
        load_more = driver.find_element_by_xpath('//*[contains(@class,"U26fgb O0WRkf oG5Srb C0oVfc n9lfJ")]').click()
    except:
        print('Cannot find load more button...')

# get review containers
reviews = driver.find_elements_by_xpath('//*[@jsname="fk8dgd"]//div[@class="d15Mdf bAhLNe"]')

print('There are %d reviews avaliable!' % len(reviews))
print('Writing the data...')

# create empty dataframe to store data
df = pd.DataFrame(columns=['name', 'ratings', 'date', 'comment'])

# get review data
for review in reviews:
    # parse string to html using bs4
    soup = BeautifulSoup(review.get_attribute('innerHTML'), 'html.parser')

    # reviewer
    name = soup.find(class_='X43Kjb').text

    # rating
    ratings = int(
        soup.find('div', role='img').get('aria-label').replace('별표 5개 만점에', '').replace('개를 받았습니다.', '').strip())

    # review date
    date = soup.find(class_='p2TkOb').text
    date = datetime.strptime(date, '%Y년 %m월 %d일')
    date = date.strftime('%Y-%m-%d')


    # review text
    comment = soup.find('span', jsname='fbQN7e').text
    if not comment:
        comment = soup.find('span', jsname='bN97Pc').text


    # append to dataframe
    df = df.append({
        'name': name,
        'ratings': ratings,
        'date': date,
        'comment': comment,
    }, ignore_index=True)

# finally save the dataframe into csv file
filename = datetime.now().strftime('result/%Y-%m-%d_%H-%M-%S.csv')
df.to_csv(filename, encoding='utf-8-sig', index=False)
driver.stop_client()
driver.close()

print('Done!')
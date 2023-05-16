import httpx
from bs4 import BeautifulSoup
import psycopg2
import os

main = psycopg2.connect(
    user='postgres',
    database='postgres',
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

cur = main.cursor()


def create_table():
    query = '''
    CREATE TABLE IF NOT EXISTS users(
        user_id varchar(100) not null
    )
    '''
    cur.execute(query)
    main.commit()


def register(user_id: str):
    query = 'INSERT INTO users (user_id) values (%s)'  # noqa
    cur.execute(query, (user_id,))
    main.commit()


def get_user():
    query = 'SELECT * FROM users'  # noqa
    cur.execute(query)
    users = cur.fetchall()
    return users


def check_user(user_id: str):
    query = 'SELECT * FROM users WHERE user_id = %s'  # noqa
    cur.execute(query, (user_id,))
    user = cur.fetchone()
    return user


def main_data():
    response = httpx.get(url='https://xitmuzon.net/')
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('div', {'class': 'track-item fx-row fx-middle js-item js-share-item'})
    desk = []
    for i in data:
        desk.append({"artist": i['data-artist'], "title": i['data-title'], "track": i['data-track']})
    return desk


def new_trek():
    desk = []
    response = httpx.get(url='https://uzhits.net/')
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('div', {'class': 'sect-col'})
    top_data = data[0].find_all('div', {'class': 'track-item fx-row fx-middle js-item'})
    sana = 1
    for i in top_data:
        desk.append({"id": str(sana), "artist": i['data-artist'], "title": i['data-title'], "track": i['data-track']})
        sana += 1
    return desk


def top_music():
    desk = []
    response = httpx.get(url='https://uzhits.net/')
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('div', {'class': 'sect-col'})
    top_data = data[1].find_all('div', {'class': 'track-item fx-row fx-middle js-item'})
    sana = 11
    for i in top_data:
        desk.append({"id": str(sana), "artist": i['data-artist'], "title": i['data-title'], "track": i['data-track']})
        sana += 1
    return desk


def world_music():
    desk = []
    response = httpx.get(url='https://xitmuzon.net/musics/tiktok')
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('div', {'class': 'track-item fx-row fx-middle js-item js-share-item'})
    sana = 21
    for i in data:
        desk.append({"id": str(sana), "track": i['data-track'], "artist": i['data-artist'], "title": i['data-title']})
        sana += 1
    return desk

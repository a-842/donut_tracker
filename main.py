import sqlite3
import requests


def create_table(connection):

    cursor = connection.cursor()
    print("database connected")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transactions (
            unixMillisDateSold INTEGER PRIMARY KEY
            item TEXT
            count INTEGER
            price INTEGER
        )
    """)
    connection.commit()


def fetch_data(API_KEY):
    headers = {
        "accept": "application / json",
        f"Authorization": API_KEY
    }

    url = "https://api.donutsmp.net/v1/auction/transactions/1"
    response = requests.get(url, headers=headers)
    print(response)


def main():
    with sqlite3.connect('transactions.db') as connection:
        create_table(connection)

    fetch_data()

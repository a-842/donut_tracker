import sqlite3
import requests
from secrets import API_KEY
import json
import time


def create_table(connection):

    cursor = connection.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transactions (
            time INTEGER PRIMARY KEY,
            name TEXT,
            item TEXT,
            count INTEGER,
            price INTEGER,
            lore TEXT
        )
    """)
    connection.commit()


def fetch_data(api_key):
    headers = {
        "accept": "application / json",
        f"Authorization": api_key
    }

    url = "https://api.donutsmp.net/v1/auction/transactions/1"
    response = requests.get(url, headers=headers).content

    data = json.loads(response)

    return data["result"]

def add_to_db(connection, transaction):

    time = transaction["unixMillisDateSold"]
    name = transaction["seller"]["name"]
    item = transaction["item"]["id"][10:]
    count = transaction["item"]["count"]
    price = transaction["price"]
    lore = transaction["item"]["lore"]

    cursor = connection.cursor()

    cursor.execute(f"""
        INSERT INTO Transactions (time, name, item, count, price, lore)
        SELECT ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM Transactions WHERE time = ?
        );
    """,
    (time, name, item, count, price, str(lore), time)
    )

def main():
    running = True

    while running:
        with sqlite3.connect('transactions.db') as connection:
            create_table(connection)

        

            for trans in fetch_data(API_KEY):
                add_to_db(connection, trans)
            time.sleep(1)



if __name__ == "__main__":
    main()
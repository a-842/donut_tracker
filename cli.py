import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy


item = input("What item do you want to analyse")

with sqlite3.connect('transactions.db') as connection:
    cursor = connection.cursor()

    cursor.execute("""
    SELECT time, count, price 
    FROM transactions
    WHERE item = ?
    AND count = 64
    """, (item,))

output = cursor.fetchall()
# Create DataFrame
df = pd.DataFrame(output, columns=['time', 'amount', 'total_price'])

# Calculate price per unit
df['price_per_unit'] = df['total_price'] / df['amount']

# Convert time to datetime
df['time'] = pd.to_datetime(df['time'], unit='ms')

# Plot
plt.figure(figsize=(12, 6))
for amount, group in df.groupby('amount'):
    plt.plot(group['time'], group['price_per_unit'], marker='o', linestyle='-', label=f'Amount {amount}')

plt.xlabel('Time')
plt.ylabel('Price per Unit')
plt.title('Price per Unit over Time by Amount')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
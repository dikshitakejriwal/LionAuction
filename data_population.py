import pandas as pd
import sqlite3
'''
#clean reserve file

# Read the CSV file into a DataFrame
data = pd.read_csv('LionAuctionDataset-v5/Auction_Listings.csv')

# Remove the $ sign and comma convert the reserve price column to a numeric type
data['Reserve_Price'] = data['Reserve_Price'].str.replace('[$,]', '').str.strip().astype(float)

# Save the cleaned data to a new CSV file or directly insert it into the database
data.to_csv('LionAuctionDataset-v5/Auction_Listings.csv', index=False)

'''



#Auction Listing Database Extention
'''
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('ALTER TABLE auction_listings ADD COLUMN Remaining_Bids INT')
cursor.execute('ALTER TABLE auction_listings ADD COLUMN Off_Reason TEXT')

cursor.execute('UPDATE auction_listings SET Remaining_Bids = Max_bids')

conn.commit()
conn.close()
'''

#update remaining_bids from the bids already there in the bids table
def get_all_listing_ids():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT Listing_ID FROM Bids')
    listing_ids = cursor.fetchall()

    connection.close()

    # Extract the listing IDs from the query result tuples
    listing_ids = [item[0] for item in listing_ids]

    return listing_ids

def update_remaining_bids(listing_ids):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    for listing_id in listing_ids:
        cursor.execute('UPDATE Auction_Listings SET Remaining_Bids = Remaining_Bids - 1 WHERE Listing_ID = ?', (listing_id,))

    connection.commit()
    connection.close()

listing_ids = get_all_listing_ids()
update_remaining_bids(listing_ids)
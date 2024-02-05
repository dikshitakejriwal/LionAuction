from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_session import Session
import sqlite3 as sql
import uuid 
import hashlib
from datetime import datetime

#set up our application
app = Flask(__name__)
host = 'http://127.0.0.1:5000/'
app.secret_key = "super secret key"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'myapp_session_'
Session(app)

@app.route('/', methods=['POST', 'GET'])
def login():
    error = None
    # hash_password()
    if request.method == 'POST':
        email = request.form['email']
        session['email'] = email
        password = request.form['password']
        session['password'] = password
        role = request.form['role']
        print(role)
        # pw_hash = make_pw_hash(password)
        # print(pw_hash)
        # result = valid_email_password(email, pw_hash)
        result = valid_email_password(email, password)
        is_valid_role = valid_role(email, role)
        if result and is_valid_role:
            session['user'] = is_valid_role
            session['user_role'] = role 
            if role == 'Bidder':
                return render_template('bidder_welcome.html', error=error, result=result, user=session.get('user'))
            elif role == 'Seller':
                session['seller_user'] = result
                return render_template('seller_welcome.html', error=error, result=result, seller_user=session.get('seller_user'))
            elif role == 'Helpdesk':
                return render_template('helpdesk_welcome.html', error=error, result=result, user=session.get('user'))

        elif not is_valid_role:
            flash(f'You are not registered as a {role}! Please change your role!')
        else:
            flash('invalid email or password')
            error = 'invalid email or password'

    return render_template('login.html', error = error)

@app.route('/change_role', methods=['POST'])
def change_role():
    role = request.form['role']
    email = session.get('user')[0]
    is_valid_role = valid_role(email, role)

    if is_valid_role:
        session['user_role'] = role
        if role == 'Bidder':
            return redirect(url_for('bidder_welcome'))
        elif role == 'Seller':
            session['seller_user'] = session['user']
            return redirect(url_for('seller_welcome'))
        elif role == 'Helpdesk':
            return redirect(url_for('helpdesk_welcome'))
    else:
        flash(f'You are not registered as a {role}! Please change your role!', category = 'error')
        return redirect(url_for('login'))


@app.route('/bidder_welcome', methods=['POST', 'GET'])
def bidder_welcome():
    #notification welcome 
    user=session.get('user')
    # if 'notifications' in session and user[0] in session['notifications']:
    #     del session['notifications'][user[0]]
    return render_template('bidder_welcome.html', user=session.get('user'))

@app.route('/bidder_personal_info', methods=['POST', 'GET'])
def bidder_personal_info():
    user = session.get('user')
    email = user[0]
    address_id = user[5] 
    address = get_address_by_id(address_id)
    card_nums = get_cardinfo_by_email(email)
    return render_template('bidder_personal_info.html', user=user, address=address, card_nums=card_nums)
    
@app.route('/seller_welcome', methods=['POST', 'GET'])
def seller_welcome():
    return render_template('seller_welcome.html', seller_user=session.get('seller_user'))

@app.route('/helpdesk_welcome')
def helpdesk_welcome():
    helpdesk_email = session['user'][0]
    position = get_helpdesk_position(helpdesk_email)
    return render_template('helpdesk_welcome.html', user=session['user'], position=position)


@app.route('/categories', methods=['GET'])
def categories():
    user_role = session.get('user_role')
    root_categories = get_root_categories()
    return render_template('categories.html', categories=root_categories, user_role = user_role)

@app.route('/sub_categories/<string:category_name>', methods=['GET'])
def sub_categories(category_name):
    subcategories, parent_category = get_subcategories(category_name)
    items = get_items(category_name)
    # print(f"Items for category {category_name}: {items}")
    return render_template('sub_categories.html', subcategories=subcategories, items=items, parent_category=parent_category, category_name=category_name)

@app.route('/sub_categories/<string:category_name>/<int:listing_id>/<string:product_name>/<string:sellers_email>', methods=['GET'])
def auction_details(listing_id, category_name, product_name, sellers_email):
    auction_data = get_auction_data(listing_id, sellers_email)
    session['auction_data'] = auction_data
    listing_bids_data = get_listing_bids_data(listing_id, sellers_email)
    session['listing_bids_data'] = listing_bids_data
    if auction_data:
        return render_template('auction_details.html', auction=auction_data, listing_bids_data=listing_bids_data)
    else:
        return "Opps! Auction not found", 404


#auction listing
@app.route('/publish_auctions', methods=['GET', 'POST'])
def publish_auctions():
    if request.method == 'POST':
        auction_title = request.form['auction_title']
        product_name = request.form['product_name']
        product_description = request.form['product_description']
        quantity = request.form['quantity']
        reserve_price = request.form['reserve_price']
        max_bids = request.form['max_bids']
        categories = request.form.getlist('categories')
        categories = [str(category).strip() for category in categories]
        print(f"Categories: {categories}")
        
        seller_user = session.get('seller_user')
        seller_email = seller_user[0]
        listing_id = get_next_listing_id()

        connection = sql.connect('database.db')
        cursor = connection.cursor()

        for category in categories:
            cursor.execute('''
                INSERT INTO auction_listings (Seller_Email, Listing_ID, Category, Auction_Title, Product_Name,
                                                Product_Description, Quantity, Reserve_Price, Max_bids, Status, Remaining_Bids)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (seller_email, listing_id, category, auction_title, product_name, product_description, quantity, reserve_price, max_bids, 1, max_bids))
            connection.commit()

        connection.close()
        flash('Your auction has been published!',  category='success')
    

        
    all_categories_name = get_categories_name()
    session['all_categories_name'] = all_categories_name
    return render_template('publish_auctions.html', all_categories_name=session.get('all_categories_name'))


@app.route('/manage_auctions', methods=['GET', 'POST'])
def manage_auctions():
    seller_email = session.get('seller_user')[0]
    active_auctions = get_auctions_by_status(seller_email, 1)
    inactive_auctions = get_auctions_by_status(seller_email, 0)
    sold_auctions = get_auctions_by_status(seller_email, 2)
    return render_template('manage_auctions.html', active_auctions=active_auctions, inactive_auctions=inactive_auctions, sold_auctions=sold_auctions, all_categories_name=session.get('all_categories_name'))

@app.route('/edit_auction/<int:auction_listing_id>', methods=['GET', 'POST'])
def edit_auction(auction_listing_id):
    if request.method == 'POST':
        auction_title = request.form['auction_title']
        product_name = request.form['product_name']
        product_description = request.form['product_description']
        quantity = request.form['quantity']
        reserve_price = request.form['reserve_price']
        max_bids = request.form['max_bids']
        categories = request.form.getlist('categories')

        seller_email = session.get('seller_user')[0]

        update_auction(auction_listing_id, auction_title, product_name, product_description, quantity, reserve_price, max_bids, categories, seller_email)
        flash('Auction has been updated.', category='success')
      
    seller_email = session.get('seller_user')[0]
    auction = get_auction_data(auction_listing_id, seller_email)
    return render_template('edit_auction.html', auction=auction, all_categories_name = session.get('all_categories_name'))


@app.route('/take_off_market/<int:auction_listing_id>', methods=['GET', 'POST'])
def take_off_market(auction_listing_id):
    if request.method == 'POST':
        reason = request.form['reason']
        seller_email = session.get('seller_user')[0]
        update_auction_status(seller_email, auction_listing_id, 0, reason)
        flash('Auction Listing has been taken off the market!', category='success')
        # return redirect(url_for('manage_auctions'))

    return render_template('take_off_market.html', auction_listing_id=auction_listing_id)

@app.route('/place_bid', methods=['POST', 'GET'])
def place_bid():
    # Get auction data
    auction_data = session.get('auction_data')
    #get bids data
    # listing_bids_data = session.get('listing_bids_data')

    if request.method == 'POST':
        bid_amount = float(request.form['bid_amount'])
        listing_id = auction_data[1]
        seller_email = auction_data[0]
        bidder_email = session.get('user')[0]
        print(f"bidder_email: {bidder_email}")
        # Check if bid amount and bidder is valid to auction
        last_bidder, curr_highest_bid = get_highest_bid(listing_id, seller_email)
        print(f"last_bidder: {last_bidder}")
        if curr_highest_bid is None: #no bids on the product made so set it to reserve price
            curr_highest_bid = auction_data[7]

        if curr_highest_bid is not None and bid_amount < curr_highest_bid + 1:
            flash('Your bid must be higher at least $1 higger than the current highest bid', category='error')
        elif last_bidder is not None and last_bidder == bidder_email:
            flash('You cannot bid unless a bid is placed by another bidder', category='error')
        elif auction_data[10] == 0:
            flash('This product has reached its maximum number of bids limit', category='error')
        else:#sucess

            #save the bid to the database
            bid_id = get_next_bid_id()
            save_bid(bid_id, seller_email, listing_id, bidder_email, bid_amount)

            #update remaining bids
            update_remaining_bids(listing_id, seller_email)
            updated_auction_data = get_auction_data(listing_id, seller_email)
            #check after updating if the remaining_bids are zero - if that case send notification to all bidder and winner
            if updated_auction_data[10] == 0: #remaining bid is 0
                # winner_email, winner_bid = get_highest_bid(listing_id, seller_email)
                print(updated_auction_data[10])
                send_notifications(listing_id, seller_email)
        
            flash('Your bid has been placed successfully!', category='error')

        
    return render_template('place_bid.html', auction_data = auction_data)

@app.route('/payment/<int:listing_id>', methods=['POST', 'GET'])
def payment(listing_id):
    bidder_email = session.get('user')[0]
    if request.method == 'GET':
        bidder_email = session.get('user')[0]
        stored_cards = get_stored_credit_cards(bidder_email)
        return render_template('payment.html', listing_id=listing_id, stored_cards=stored_cards)
    elif request.method == 'POST':
        selected_card = request.form['stored_card']
        record_transaction_and_status(listing_id, bidder_email)
        flash('Payment successfully submitted!', category='success')
        return render_template('payment.html', listing_id=listing_id)
    else:
        return "Invalid request method"

@app.route('/display_bids', methods=['POST', 'GET'])
def display_bids():
    bidder_email = session.get('user')[0]
    bids = get_bids_by_bidder_email(bidder_email)
    return render_template('display_bids.html', bids=bids)

@app.route('/add_card', methods=['POST', 'GET'])
def add_card():
    if request.method == 'POST':
        credit_card_number = request.form['credit_card_number']
        card_type = request.form['card_type']
        expire_month = request.form['expire_month']
        expire_year = request.form['expire_year']
        security_code = request.form['security_code']
        bidder_email = session.get('user')[0]

        #add card to the database
        connection = sql.connect('database.db')
        cursor = connection.cursor()

        cursor.execute('''INSERT INTO Credit_Cards (credit_card_num, card_type, expire_month, expire_year, security_code, Owner_email) VALUES (?, ?, ?, ?, ?, ?)''', (credit_card_number, card_type, expire_month, expire_year, security_code, bidder_email))

        connection.commit()
        connection.close()

        flash('Credit card successfully added!', category='success')
    return render_template('add_card.html')

@app.route('/purchases', methods=['POST', 'GET'])
def purchases():
    # Get the logged in user's email
    email = session.get('user')[0]

    # Get the purchases made by the user
    purchases = get_purchases_by_bidder(email)

    return render_template('purchases.html', purchases=purchases)



#################

def get_purchases_by_bidder(bidder_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM auction_listings a, transactions t WHERE a.Listing_ID = t.Listing_ID AND t.Bidder_email = ? AND a.Status = ?''', (bidder_email, 2))
    purchases = cursor.fetchall()
    connection.close()
    return purchases

def get_bids_by_bidder_email(bidder_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM Bids WHERE Bidder_email = ?''', (bidder_email,))
    bids = cursor.fetchall()
    connection.close()
    return bids


#helpers of auctions_bidding
def record_transaction_and_status(listing_id, bidder_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT Seller_Email FROM Bids WHERE Listing_ID = ? and Bidder_Email = ?''', (listing_id, bidder_email))
    seller_email = cursor.fetchone()[0]

    transaction_id = get_next_transaction_id()
    transaction_date = datetime.now().strftime('%-m/%-d/%y')

    winner_email, winning_bid_price = get_highest_bid(listing_id, seller_email)

    #record transaction
    cursor.execute('''INSERT INTO Transactions (Transaction_ID, Seller_Email, Listing_ID, Bidder_Email, Date, Payment)
                          VALUES (?, ?, ?, ?, ?, ?)''', (transaction_id, seller_email, listing_id, bidder_email, transaction_date, winning_bid_price))

    # Update status to "Sold"
    cursor.execute('''UPDATE auction_listings SET Status = 2 WHERE Listing_ID = ? AND Seller_Email = ?''', (listing_id,seller_email))

    connection.commit()
    connection.close()

def get_next_transaction_id():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(Transaction_ID) FROM Transactions')
    max_id = cursor.fetchone()[0]
    connection.close()
    return max_id + 1 if max_id else 1

def get_stored_credit_cards(bidder_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT credit_card_num, card_type, expire_month, expire_year, security_code, Owner_email
                      FROM Credit_Cards
                      WHERE Owner_email = ?''', (bidder_email,))

    credit_cards = cursor.fetchall()
    connection.close()
    return credit_cards



def send_notifications(listing_id, seller_email):
    winner_email, highest_bid = get_highest_bid(listing_id, seller_email)
    listing_bids_data = get_listing_bids_data(listing_id, seller_email)
    
    notifications = {}
    print(notifications)
    
    for listing in listing_bids_data:
        bidder_email = listing[3]
        print(bidder_email)
        message = f"Auction {listing_id} has ended. "
        if bidder_email == winner_email:
            message += f"Woho! Congratulations! You won with a bid of ${highest_bid}. "
            payment_url = url_for('payment', listing_id=listing_id)
            message += f"Click <a href='{payment_url}'> here </a> to enter the payment process."
        else:
            message += f"The winning bid was ${highest_bid} by {winner_email}. Better luck next time!"
        
        notifications[bidder_email] = message
        print(notifications[bidder_email])
    
    session['notifications'] = notifications
    print(session['notifications'])

def update_remaining_bids(listing_id, seller_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''UPDATE auction_listings SET Remaining_Bids = Remaining_Bids - 1 WHERE Listing_ID = ? AND Seller_Email = ?''', (listing_id, seller_email))
    connection.commit()
    cursor.execute('''SELECT Remaining_Bids FROM auction_listings WHERE Listing_ID = ? AND Seller_Email = ?''', (listing_id, seller_email))
    remaining_bids = cursor.fetchone()[0]
    connection.close()
    return remaining_bids

def save_bid(bid_id, seller_email, listing_id, bidder_email, bid_amount):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO Bids (Bid_ID, Seller_Email, Listing_ID, Bidder_email, Bid_price)
        VALUES (?, ?, ?, ?, ?)
    ''', (bid_id, seller_email, listing_id, bidder_email, bid_amount))
    connection.commit()
    connection.close()

def get_next_bid_id():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(Bid_ID) FROM Bids')
    max_id = cursor.fetchone()[0]
    connection.close()
    return max_id + 1 if max_id else 1

def get_listing_bids_data(listing_id, sellers_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM bids WHERE (Listing_ID, Seller_Email)= (?, ?)', (listing_id,sellers_email))
    listing_bids_data = cursor.fetchall()
    connection.close()
    return listing_bids_data

def get_highest_bid(listing_id, seller_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    #bids has been made before
    cursor.execute('SELECT Bidder_email, MAX(Bid_price) FROM Bids WHERE Listing_ID = ? AND Seller_Email = ? GROUP BY Listing_ID', (listing_id, seller_email))
    result = cursor.fetchone()
    bidder_email, highest_bid = result if result else (None, None)
    #no bids has been made before
    connection.close()
    return bidder_email, highest_bid

#helpers of auction_listing

#take off market helper
def update_auction_status(seller_email, auction_id, status, reason):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if reason:
        cursor.execute("UPDATE auction_listings SET Status = ?, Off_Reason = ? WHERE Listing_ID = ? AND Seller_Email = ?", (status, reason, auction_id, seller_email))
    else:
        cursor.execute("UPDATE auction_listings SET Status = ? WHERE Listing_ID = ? AND Seller_Email = ?", (status, auction_id, seller_email))
    connection.commit()
    connection.close()

def update_auction(listing_id, auction_title, product_name, product_description, quantity, reserve_price, max_bids, categories, seller_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    category = categories[0]
    cursor.execute('''UPDATE auction_listings SET Auction_Title = ?, Product_Name = ?, Product_Description = ?, Quantity = ?, Reserve_Price = ?, Max_bids = ?, Category = ? WHERE Listing_ID = ? AND Seller_Email = ?''',
                    (auction_title, product_name, product_description, quantity, reserve_price, max_bids, category, listing_id, seller_email))
    connection.commit()
    connection.close()

def get_auction_by_id(listing_id):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM uction_listings WHERE Listing_ID = ?", (auction_id,))
    auction = cursor.fetchone()
    connection.close()
    return auction

def get_auction_data(listing_id, sellers_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM auction_listings WHERE (Listing_ID, Seller_Email)= (?, ?)', (listing_id,sellers_email))
    auction_data = cursor.fetchone()
    connection.close()
    return auction_data

def get_auctions_by_status(seller_email, status):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM auction_listings WHERE Seller_Email = ? AND Status = ?", (seller_email, status))
    auctions = cursor.fetchall()
    connection.close()
    return auctions


def get_next_listing_id():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(Listing_ID) FROM auction_listings')
    max_id = cursor.fetchone()[0]
    connection.close()
    return max_id + 1 if max_id else 1
#********
#helper of auction_listing

def get_categories_name():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT category_name FROM categories')
    categories_name = cursor.fetchall()
    connection.close()
    return categories_name

#helper of categories
def get_root_categories():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM categories WHERE parent_category = ?', ('Root',))  
    root_categories = cursor.fetchall()
    connection.close()
    return root_categories

def get_subcategories(parent_category):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM categories WHERE parent_category = ?', (parent_category,))
    subcategories = cursor.fetchall()

    cursor.execute('SELECT parent_category FROM categories WHERE category_name = ?', (parent_category,))
    parent_of_parent = cursor.fetchone()

    connection.close()
    if subcategories is not None:
        return subcategories, parent_of_parent[0]
    else:
        return False

def get_items(category):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM auction_listings WHERE (Category, Status) = (?, ?)', (category,1))
    items = cursor.fetchall()
    connection.close()
    return items

def get_auction_data(listing_id, sellers_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM auction_listings WHERE (Listing_ID, Seller_Email)= (?, ?)', (listing_id,sellers_email))
    auction_data = cursor.fetchone()
    connection.close()
    return auction_data




#helper for login
def valid_email_password(email, password):
    connection = sql.connect('database.db')
    # connection.execute('CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, password TEXT);')
    cursor = connection.cursor()
    cursor.execute('select * FROM users WHERE (email, password) = (?, ?)', (email, password))
    user = cursor.fetchone()
    if user is not None:
        return user
    else:
        return False


#Check if the user is registered as a bidder, seller, helpdesk staff in the database if they are then only allow
def valid_role(email, role):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    if role == 'Bidder':
        cursor.execute('select * FROM bidders WHERE email = ?', (email,))
    if role == 'Seller':
        cursor.execute('select * FROM sellers WHERE email = ?', (email,))
    if role == 'Helpdesk':
        cursor.execute('select * FROM helpdesk WHERE email = ?', (email,))
    user = cursor.fetchone()
    if user is not None:
        return user
    else:
        return False

def make_pw_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

#function that was used to hash all the passwords stored in the database
def hash_password():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    i = 0
    for user, p in cursor:
        # print(p)
        # hash_password = hashlib.sha256(str.encode(p)).hexdigest()
        sha_password = hashlib.sha256(p.encode('UTF-8'))
        hash_password = (sha_password.hexdigest())
        connection.execute("UPDATE users SET password = ? WHERE email = ?", (hash_password, user)) 
        # print("new_p:", p, i)  
        # i += 1
    connection.commit()
    connection.close()


#personal information functions
def get_address_by_id(address_id):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM address A, zipcode_info Z WHERE A.address_id = ? AND A.zipcode = Z.zipcode', (address_id,))
    address = cursor.fetchone()
    connection.close()
    return address

def get_cardinfo_by_email(email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT credit_card_num FROM credit_cards WHERE Owner_email = ?', (email,))
    card_info = cursor.fetchall()#multiple cards
    connection.close()
    return card_info

def get_helpdesk_position(email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT Position FROM helpdesk WHERE email = ?''', (email,))
    position = cursor.fetchone()
    connection.close()
    return position[0] if position else None

if __name__== "__main__":
    app.run(debug = True)


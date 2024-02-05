## Background Information

Lion Auction is an online auction system that allows registered users to buy and sell goods and services via an online platform. The system offers a user-friendly interface for bidders and sellers to participate in online auctions. It offers a range of features such as bidding, auction listing, auction management, personal information management, payment management, and customer support. Lion Auction provides a secure and reliable platform for both buyers and sellers to participate in auctions, and offers a variety of goods and services across different categories.

## Features

- login.html is the main page that will be shown on the when you run on the server. This page will ask your email and password. If your email and password matches one stored in the database you will be directed to a profile page. Otherwise, you will be given an error message saying email or password are invalid. 
- database_hashed.db contains passwords that are hashed and and database.db contains passwords that are not hashed.
 - I was able to successfully hash the database but not able to use the hashed password to verify data. The commented code all over the app.py will show my attempts to find the hash password in the database and match it with password entered by user
 - Although, I finally was able to finish the project, and display invalid password and email error message when no matching data was their in database and I was able to take the user to their profile page and make them successfully login when the information entered was correct.
- User login with role-based access control for bidders, sellers, and helpdesk members.
- Create and manage auction listings, including editing and taking listings off the market.
- View categories and subcategories of items.
- Place bids and view auction details.
- Manage personal information, including address and credit card details.
- Make payments for won auctions.
- View and manage bids placed by the logged-in user.
- View purchases made by the logged-in user.

## Organization

- Template folder contains login.html, profile.html, add_card.html, auction_details.html, bidder_personal_info.html, bidder_welcome, categories.html, display_bids.html, edit_aution.html, helpdesk_welcome.html, login.html, manage_auction.html, payment.html, place_bid.html, publish_auction.html, seller_welcome.html, sub_categories.html, take_off_market.html
- static file design the same name html files
- env is the flask virtual environment 
- app.py contains all the functionality of pages, routes information(Flask and sqlite code)
Routes
- /: Login route with POST and GET methods.
- /change_role: Change the user's role with POST method.
- /bidder_welcome: Display the Bidder welcome page.
- /bidder_personal_info: Display and manage Bidder personal information.
- /seller_welcome: Display the Seller welcome page.
- /helpdesk_welcome: Display the Helpdesk welcome page.
- /categories: Display root categories.
- /sub_categories/<string:category_name>: Display subcategories and items in a category.
- /sub_categories/<string:category_name>/<int:listing_id>/<string:product_name>/<string:sellers_email>: Display auction details.
- /publish_auctions: Create and publish auction listings.
- /manage_auctions: Manage auction listings.
- /edit_auction/<int:auction_listing_id>: Edit an auction listing.
- /take_off_market/<int:auction_listing_id>: Take an auction listing off the market.
- /place_bid: Place a bid on an auction.
- /payment/<int:listing_id>: Make a payment for a won auction.
- /display_bids: Display bids placed by the logged-in user.
- /add_card: Add a credit card to the logged-in user's account.
- /purchases: Display the logged-in user's purchases.

## Instructions
- First Unpack the .zip file.
- open the unpacked folder in visual studio code or any other editor.
- then open the terminal and follow the steps below. 
- Run source env/bin/activate to activate the virtual environment
- Run python3 app.py then then application should start running on 'http://127.0.0.1:5000/'

## Sources

- https://www.geeksforgeeks.org/how-to-update-all-the-values-of-a-specific-column-of-sqlite-table-using-python/
- https://docs.python.org/3/library/sqlite3.html
- https://stackoverflow.com/questions/29582736/python3-is-there-a-way-to-iterate-row-by-row-over-a-very-large-sqlite-table-wi
- https://www.youtube.com/watch?v=YyUknBHcZB8
- https://www.youtube.com/watch?v=UZIhVmkrAEs
-Bootstrap documentation and Flask documentation

## Walkthrough

Because these are GIFs, I was not able to capture all the functionality in one video, so I decided to record different GIFs of selected functionalities. The GIFs don't include all the functionalities but focus on the main features of the application. The application has many more functionalities, so please download the app to play with it :)

Bidder's Basic Functionality - Navigating the Auction Platform

<img src="http://g.recordit.co/wCC2dvLXhq.gif" width=250><br>

Category Browsing and Bidding Functionality - Navigating Categories and Placing Bids Seamlessly

<img src="http://g.recordit.co/YQOwkSwLsh.gif" width=250><br>

Post-bidding, this GIF showcases notifications to all bidders, payment prompts for the winner, and updates to the bids and purchase history.

<img src="http://g.recordit.co/DwGpQHQB5y.gif" width=250><br>

Seller Interface: Managing Auctions and Viewing Listings

<img src="http://g.recordit.co/AhtAgwvg74.gif" width=250><br>


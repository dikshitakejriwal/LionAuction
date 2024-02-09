## Background Information

Lion Auction is an online auction system that allows registered users to buy and sell goods and services via an online platform. The system offers a user-friendly interface for bidders and sellers to participate in online auctions. It offers a range of features such as bidding, auction listing, auction management, personal information management, payment management, and customer support. Lion Auction provides a secure and reliable platform for both buyers and sellers to participate in auctions, and offers a variety of goods and services across different categories.

## Features

- Secure User Authentication: The login.html page is the first interaction users have with the platform. It prompts for an email and password, ensuring that access is granted only to users with credentials that match those in the database. Unsuccessful login attempts result in an error message.
- Role-Based Access Control: Users can log in with specific roles—be it bidders, sellers, or helpdesk members—each with tailored access permissions to different functionalities within the platform
- Auction Listing Management: Sellers have the ability to create, edit, and delist their auction items, providing complete control over their listings.
- Interactive Bidding System: Bidders can place bids on items of interest and view detailed auction information, including current bids and item descriptions.
- Personal Information Management: Users can update their personal details, including addresses and credit card information, ensuring all transactions are up to date.
- Payment Processing: Winners of auctions can proceed to secure payment gateways to complete their purchases, with all transactions handled safely and   efficiently.
- Bid and Purchase Histories: Users have access to their bidding history and purchased items, allowing them to track their activities and manage their acquisitions.
- Database with Security - Users passwords are hashed to safely store in the database. database_hashed.db stores hashed passwords, providing an extra layer of security for the users.

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


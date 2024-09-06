1. Project Overview

   - Project Name: Ebisco Clothings.
   - Description: Welcome to Ebisco Clothings Online Clothing Web App! This application is designed to provide a seamless online shopping experience for clothing and accessories. It features a user-friendly interface, secure authentication, product catalog management, and an integrated shopping cart and checkout system..
   - Purpose: Its main purpose is to make sure ordinary users can track their shipments.
   - Link to Demo: My github link ( https://github.com/thinkingtek/online-clothing-store.git )

2. Installation

   - Clone the repository:
     git clone https://github.com/thinkingtek/online-clothing-web-app.git

   - Change directory:
     cd yourproject

   - Create a virtual environment
     python -m venv env
   - Activate the virtual environment
     .\env\Scripts\activate (for windows)
     source env/bin/activate (for Mac)

   - Install dependencies:
     pip install -r reqs.txt

   - Set up the database:
     python manage.py migrate

3. Usage

   - Run "python manage.py runserver" to run the project

4. Instructions

   - After setup make you create three groups (customer, staff), although admin not setup yet.
   - categories and tags should be added.
   - Shipping methods (personal pickup FREE, Home delivery (#5,000), Express (#10,000)) should be added.
   - Staffs can be manually added through the Django admin page.
   - Email console is used for signup

5. Features

   - User creation, authentication, password reset and change.
   - Browse products by category or use the basic search filter functionality.
   - contact page
   - add to cart and update cart items
   - When item is added to cart the item price dosen't change unless the user tries to update the item himself
   - shipping fee updates each time the Order is saved
   - Order History and User Profiles.
   - order list and order details (users can see the list of items in a successful order)
   - integrated paystack payment system
   - Admin Dashboard for Managing Products, Categories, and Orders.
   - Responsive Design for Mobile and Desktop.
   - Modal for deleting specific cart item, and clearing of cart.
   - Total amount changes in on the frontend when you change shipping method.
   - Unit testing can be added later

6. Testing

   - "python manage.py test"

7. Created Accounts

   -------- ACCOUNTS -----------
   username: newuser
   email: newuser@gmail.com
   password: mypass123

   username: superuser
   email: superuser@gmail.com
   password: mypass123

   testuserpass (password for all ordinary user accounts)

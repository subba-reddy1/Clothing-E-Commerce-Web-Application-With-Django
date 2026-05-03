StyleHaven - Clothing E-Commerce Web Application
StyleHaven is a fully functional e-commerce web application built with Django. It features a complete shopping experience with user authentication, product management for managers, and a seamless checkout process.

🚀 Features
🛒 Customer Features
User Authentication: Secure Signup & Login system.
Product Browsing: Filter products by Category (Men, Women, Kids) and Price.
Shopping Bag: Add to cart, update quantities, and remove items.
Checkout System: Simple checkout flow to place orders.
Search Functionality: Find products instantly.
👨‍💼 Manager/Admin Features
Manager Dashboard: Dedicated panel to manage inventory.
Product Management: Add, Edit, and Delete products with image uploads.
Order Tracking: View and manage customer orders.
🛠️ Tech Stack
Backend: Python, Django 5.0
Frontend: HTML5, CSS3, Tailwind CSS, JavaScript
Database: SQLite (Default) / PostgreSQL (Production ready)
📂 Project Structure
A quick look at the codebase organization:

bash shop_project/ ├── adminApp/ # Manager dashboard & product logic ├── usersApp/ # Customer facing views (Home, Cart, Checkout) ├── templates/ # HTML files (Tailwind integrated) │ ├── adminApp/ # Admin specific templates │ ├── userApp/ # Customer specific templates │ └── base.html # Main layout wrapper ├── static/ # CSS, JavaScript, and Images ├── media/ # User uploaded product images ├── db.sqlite3 # Database file └── manage.py # Django command-line utility

Component Technology Backend Python 3.10, Django 5.0 Frontend HTML5, Tailwind CSS, JavaScript Database SQLite (Dev), PostgreSQL (Production ready) Version Control Git & GitHub

⚙️ Installation & Setup
Follow these steps to run the project locally:

Clone the repository:

git clone [https://github.com/RevanthKunala/Clothing-E-Commerce-Web-Application-With-Django.git](https://github.com/RevanthKunala/Clothing-E-Commerce-Web-Application-With-Django.git)
cd Clothing-E-Commerce-Web-Application-With-Django
Create a Virtual Environment (Optional but Recommended):

python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate
Install Dependencies:

pip install -r requirements.txt
Run Migrations:

python manage.py migrate
Create a Superuser (Admin):

python manage.py createsuperuser
Run the Server:

python manage.py runserver
Access the App: Open your browser and go to http://127.0.0.1:8000/

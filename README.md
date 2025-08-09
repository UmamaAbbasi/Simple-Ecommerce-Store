# E-Commerce Website (Django)

A fully functional e-commerce website built as part of my internship project using Django and HTML.  
The website includes product listings, shopping cart functionality, checkout process, and a responsive user interface.

## 🚀 Features
- Browse products by category
- Add products to cart
- Update or remove cart items
- Checkout and order processing
- User authentication (login/register)
- Responsive design for mobile and desktop

## 🛠 Tech Stack
- **Frontend:** HTML
- **Backend:** Django (Python)
- **Database:** SQLite
- **Tools:** VS Code

## 📂 Project Structure
ecommerce-website/
│── ecommerce/ # Main Django project folder
│── shop/ # App for managing products
│── cart/ # App for shopping cart
│── orders/ # App for orders and checkout
│── templates/ # HTML templates
│── static/ # CSS, JS, Images
│── db.sqlite3 # SQLite database
│── manage.py # Django management script
│── requirements.txt # Python dependencies
│── README.md # Project description

## ⚙️ Setup & Run
# Create virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver

License: This project was developed for educational purposes as part of an internship.

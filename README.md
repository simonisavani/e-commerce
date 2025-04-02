# E-Commerce Application

## 📌 Project Overview
This is a full-fledged **E-Commerce Application** built using **Flask** for the backend and **MongoDB** as the database. The application supports user authentication, product management, shopping cart functionality, and coupon-based discounts.

## 🚀 Features
- **User Authentication** (JWT-based login & registration)
- **Product Management** (CRUD operations)
- **Shopping Cart** (Add, remove, update products)
- **Coupon System** (Apply discount codes)
- **Secure APIs** (Protected routes using Flask-JWT-Extended)
- **Database**: MongoDB with Flask-PyMongo

## 🏗️ Tech Stack
- **Backend**: Flask, Flask-JWT-Extended, Flask-PyMongo
- **Database**: MongoDB
- **Authentication**: JSON Web Tokens (JWT)
- **Other Tools**: Docker, Postman (for API testing)

## 📂 Project Structure
```
├── app
│   ├── routes
│   │   ├── auth.py          # User authentication routes
│   │   ├── products.py      # Product management routes
│   │   ├── cart.py          # Shopping cart routes
│   │   ├── discount.py      # Coupon system
│   ├── models.py           # Database models
│   ├── config.py           # App configuration
├── tests                   # Unit tests
├── requirements.txt        # Required dependencies
├── run.py                  # Application entry point
└── README.md               # Project documentation
```

## 🔧 Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/simonisavani/e-commerce.git
   cd e-commerce
   ```
2. **Create a virtual environment & activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Create a `.env` file and add the following:
   ```
   SECRET_KEY=your_secret_key
   MONGO_URI=mongodb://localhost:27017/ecommerce
   JWT_SECRET_KEY=your_jwt_secret_key
   ```
5. **Run the application:**
   ```bash
   python wsgi.py
   ```
6. **API Testing:**
   - Use **Postman** or **cURL** to test the APIs.

## ✅ API Endpoints
| Method | Endpoint          | Description                     |
|--------|------------------|---------------------------------|
| POST   | /auth/register   | Register a new user            |
| POST   | /auth/login      | Login user & get JWT token     |
| GET    | /products        | Get all products               |
| POST   | /products        | Add a new product (Admin)      |
| PUT    | /cart/add        | Add a product to the cart      |
| POST   | /coupon          | Apply a discount code          |

## 🛠️ Deployment (Optional)
To deploy using **Docker**:
```bash
docker build -t ecommerce-app .
docker run -p 5000:5000 ecommerce-app
```

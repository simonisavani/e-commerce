# E-Commerce Backend

This is the backend for an e-commerce platform built using **Flask**, providing APIs for authentication, product management, cart functionality, orders, and discount coupons.

## Features
- **User Authentication** (Register/Login with JWT)
- **Product Management** (Add, Update, Delete, Fetch Products)
- **Cart Management** (Add to Cart, Remove, Fetch Cart Items)
- **Order Processing** (Place Order, Track Order)
- **Coupon System** (Apply Discount Coupons)

## Tech Stack
- **Flask** (Python Backend Framework)
- **Flask-JWT-Extended** (Authentication)
- **MongoDB** (Database)
- **Docker** (Optional - Containerization)

## Installation
### Prerequisites
- Python 3.x installed
- MongoDB installed and running

### Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/simonisavani/e-commerce.git
   cd e-commerce
   ```
2. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Environment Variables** (Create `.env` file)
   ```
   SECRET_KEY=your_secret_key
   MONGO_URI=mongodb://localhost:27017/ecommerce
   ```
5. **Run the Application**
   ```bash
   flask run
   ```

## API Endpoints
### Authentication
| Method | Endpoint       | Description          |
|--------|--------------|----------------------|
| POST   | /auth/register | Register User       |
| POST   | /auth/login    | User Login (JWT)    |

### Products
| Method | Endpoint                 | Description          |
|--------|---------------------------|----------------------|
| POST   | /api/products             | Add Product         |
| GET    | /api/products             | Get All Products    |
| GET    | /api/products/<product_id> | Get Single Product  |
| PUT    | /api/products/<product_id> | Update Product      |
| DELETE | /api/products/<product_id> | Delete Product      |

### Cart
| Method | Endpoint           | Description       |
|--------|-------------------|-----------------|
| POST   | /api/cart         | Add to Cart     |
| GET    | /api/cart         | Get Cart Items  |
| DELETE | /api/cart/<cart_id> | Remove Item    |

### Orders
| Method | Endpoint              | Description          |
|--------|----------------------|----------------------|
| POST   | /api/order           | Place Order         |
| GET    | /api/order/<order_id> | Track Order Status  |

### Discounts
| Method | Endpoint      | Description      |
|--------|--------------|------------------|
| POST   | /api/coupon  | Apply Coupon Code |

## Deployment
### Using Docker
1. **Build the Docker Image**
   ```bash
   docker build -t ecommerce-backend .
   ```
2. **Run the Container**
   ```bash
   docker run -p 5000:5000 ecommerce-backend
   ```

### Deployment to Cloud
- Can be deployed on **Heroku, AWS, Render, or DigitalOcean**.
- Use **Gunicorn** as WSGI server for production.
- Store environment variables securely.

## Contributing
Pull requests are welcome! For major changes, open an issue first to discuss improvements.




from app.config import db

# Users Collection
db.users.create_index("email", unique=True)

# Products Collection
db.products.create_index("name", unique=True)

# Orders Collection
db.orders.create_index("user_id")

# Cart Collection
db.cart.create_index("user_id")

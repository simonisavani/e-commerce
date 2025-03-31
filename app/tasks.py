# from celery import Celery

# celery = Celery('tasks', broker='redis://localhost:6379/0')

# @celery.task
# def send_order_notification(user_id):
#     print(f"Order notification sent to user {user_id}")
from celery import Celery
from app.config import CELERY_BROKER_URL

celery = Celery('tasks', broker=CELERY_BROKER_URL)

@celery.task
def send_order_notification(order_id, email):
    # Simulate sending email
    print(f"Sending email to {email} for order {order_id}")

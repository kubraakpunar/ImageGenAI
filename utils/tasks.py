from celery import shared_task
from .services import process_user_photo_service

@shared_task
def process_user_photo(user_id, prompt, original_photo_name):
    process_user_photo_service(user_id, prompt, original_photo_name)
from celery import shared_task
from image_generator.services import PhotoService

@shared_task
def process_user_photo(user_id, prompt, original_photo_name):
    PhotoService.process_user_photo_service(user_id, prompt, original_photo_name)
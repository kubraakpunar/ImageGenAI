from celery import shared_task
from .midjourney_api import MidjourneyApi
import os
import boto3
from django.conf import settings
import mimetypes

@shared_task
def process_user_photo(user_id, prompt, original_photo_name):
    from image_generator.models import User

    user_profile = User.objects.get(id=user_id)
    original_photo_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{original_photo_name}'

    full_prompt = f"{original_photo_url} {prompt}"

    midjourney = MidjourneyApi(
        prompt=full_prompt,
        application_id=os.getenv("MIDJOURNEY_APP_ID"),
        guild_id=os.getenv("MIDJOURNEY_GUILD_ID"),
        session_id=os.getenv("MIDJOURNEY_SESSION_ID"),
        channel_id=os.getenv("MIDJOURNEY_CHANNEL_ID"),
        version=os.getenv("MIDJOURNEY_VERSION"),
        id=os.getenv("MIDJOURNEY_ID"),
        authorization=os.getenv("MIDJOURNEY_AUTHORIZATION")
    )

    image_path = midjourney.image_path()
    if image_path:
        s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)
        with open(image_path, 'rb') as file:
            prompted_photo_name = f'prompted_photos/{os.path.basename(image_path)}'
            prompted_content_type, _ = mimetypes.guess_type(prompted_photo_name)

            s3.upload_fileobj(
                file,
                settings.AWS_STORAGE_BUCKET_NAME,
                prompted_photo_name,
                ExtraArgs={'ContentType': prompted_content_type, 'ACL': 'public-read'}
            )

            prompted_photo_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{prompted_photo_name}'
            user_profile.prompted_photo = prompted_photo_url
            user_profile.save()

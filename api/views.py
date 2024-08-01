from rest_framework import viewsets
from .serializers import UserSerializer
from image_generator.models import User
from utils.midjourney_api import MidjourneyApi
from django.core.files.base import ContentFile
import os
import boto3
from django.conf import settings
import mimetypes

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user_profile = serializer.save()
        text_prompt = os.getenv("text_prompt")
        original_photo_file = user_profile.original_photo.file
        original_photo_name = user_profile.original_photo.name
        content_type, _ = mimetypes.guess_type(original_photo_name)
        
        s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)
        
        s3.upload_fileobj(
            original_photo_file, 
            settings.AWS_STORAGE_BUCKET_NAME, 
            original_photo_name, 
            ExtraArgs={'ContentType': content_type}
        )
        
        original_photo_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{original_photo_name}'
        
        prompt = f"{original_photo_url} {text_prompt}"
        
        midjourney = MidjourneyApi(
            prompt=prompt,
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
            with open(image_path, 'rb') as file:
                prompted_photo_name = f'prompted_photos/{os.path.basename(image_path)}'
                prompted_content_type, _ = mimetypes.guess_type(prompted_photo_name)

                s3.upload_fileobj(
                    file, 
                    settings.AWS_STORAGE_BUCKET_NAME, 
                    prompted_photo_name, 
                    ExtraArgs={
                        'ContentType': prompted_content_type,  
                        'ACL': 'public-read'
                    }
                )
                
                prompted_photo_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{prompted_photo_name}'
                user_profile.prompted_photo = prompted_photo_url
                user_profile.save()

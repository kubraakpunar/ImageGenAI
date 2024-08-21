from rest_framework import viewsets
from .serializers import UserSerializer
from image_generator.models import User
from utils.tasks import process_user_photo
import os
import boto3
from django.conf import settings
import mimetypes

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user_profile = serializer.save()
        text_prompt1 = os.getenv("prompt_part1")
        text_prompt2 = os.getenv("prompt_part2")
        text_prompt3 = os.getenv("prompt_part3")
        text_prompt4 = os.getenv("prompt_part4")
        
        full_prompt = f"{text_prompt1} {text_prompt2} {text_prompt3} {text_prompt4}"

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

        process_user_photo.delay(user_profile.id, full_prompt, original_photo_name)

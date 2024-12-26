<h1 align="center">ImageGenAI</h1>

This mobile application leverages the power of AI to turn your special moments into unforgettable, high-quality images. Built with Django, the app integrates MidJourney AI for creative image generation and provides a seamless experience through a robust backend.

## Features

 • **AI-Powered Image Generation:** Transform user-uploaded photos into stunning, creative images using MidJourney AI. <br>
 • **Asynchronous Processing:** Utilize Celery with Redis to handle long-running tasks, ensuring a smooth user experience.  <br>
 • **Cloud Storage:** Store and retrieve images securely using AWS S3.  <br>
 • **API Integration:** Expose a comprehensive set of RESTful APIs using Django REST Framework (DRF).  <br>

## Technology Stack

 • **Django:** Backend framework used to develop the core application.  <br>
 • **Django REST Framework (DRF):** Simplifies the creation of RESTful APIs.  <br>
 • **Celery:** Manages asynchronous task queues for handling long-running operations.  <br>
 • **Redis:** Acts as a message broker for Celery tasks.  <br>
 • **AWS S3:** Provides secure storage and retrieval of user-generated images.  <br>

## Installation

 Prerequisites <br>
  • Python 3.12  <br>
  • Django  <br>
  • MidJourney AI Discord account  <br>
  • Redis  <br>
  • AWS S3 account  <br>

  Clone the Repository
  ```
  git clone https://github.com/kubraakpunar/ImageGenAI.git 
  ```
  Install Dependencies
   Create a virtual environment and install the required packages:
   ```
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
## Configuration
  AWS S3: Set up your AWS credentials and S3 bucket in your Django settings.  <br>
  Celery & Redis: Ensure Redis is running, and configure Celery in your Django settings.  <br>
  MidJourney API: Add your MidJourney API key and configuration details to the settings.  <br>

## Migrations
Run the following command to apply migrations:
```
py manage.py migrate
```
## Run the Application
Start the Django development server:

```
py manage.py runserver
```
Start Celery workers:
```
celery -A ImageGenAI worker --loglevel=info

#for windows
celery -A ImageGenAI worker -l info  --pool=solo
```

## Usage
  • Uploading a Photo: Users can upload a photo, which will be sent to the MidJourney API for transformation.  <br>
  • Processing: The app processes the photo asynchronously, storing the result in AWS S3.  <br>
  • Retrieval: Users can retrieve and view both the original and AI-generated images.  <br>
  

<p align="center">
  <img src="https://valasys.com/wp-content/uploads/2023/07/What-Is-Midjourney-AI-and-How-Does-It-Work-1.jpg" alt="" width="300" height="200">
</p>





  







  


import requests
from urllib.parse import urlparse
import os
import time
import json

class MidjourneyApi:
    def __init__(self, prompt, application_id, guild_id, session_id, channel_id, version, id, authorization):
        self.application_id = application_id
        self.guild_id = guild_id
        self.session_id = session_id
        self.channel_id = channel_id
        self.version = version
        self.id = id
        self.authorization = authorization
        self.prompt = prompt
        self.message_id = ""
        self.image_path_str = ""

        self.send_message()
        self.wait_for_image()
        self.download_image()

    def send_message(self):
        url = "https://discord.com/api/v9/interactions"
        data = {
            "type": 2,
            "application_id": self.application_id,
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "session_id": self.session_id,
            "data": {
                "version": self.version,
                "id": self.id,
                "name": "imagine",
                "type": 1,
                "options": [
                    {
                        "type": 3,
                        "name": "prompt",
                        "value": self.prompt
                    }
                ]
            }
        }
        headers = {
            'Authorization': self.authorization,
            'Content-Type': 'application/json',
        }
        response = requests.post(url, headers=headers, json=data)
        print(f"Request payload: {json.dumps(data, indent=2)}")
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")

        if response.status_code not in (200, 204):
            raise Exception(f"Failed to send message: {response.status_code} {response.text}")
        else:
            print("Message sent successfully.")

    def wait_for_image(self):
        headers = {
            'Authorization': self.authorization,
            "Content-Type": "application/json",
        }
        for i in range(20):
            time.sleep(30)
            try:
                response = requests.get(f'https://discord.com/api/v9/channels/{self.channel_id}/messages', headers=headers)
                if response.status_code != 200:
                    raise Exception(f"Failed to get messages: {response.status_code} {response.text}")

                messages = response.json()
                for message in messages:
                    if 'attachments' in message and len(message['attachments']) > 0:
                        self.message_id = message['id']
                        return
            except Exception as e:
                print(f"Error getting message: {e}")
                if i == 19:
                    raise ValueError("Timeout")
        raise ValueError("Timeout: Image not generated within the expected time frame.")

    def download_image(self):
        headers = {
            'Authorization': self.authorization,
            "Content-Type": "application/json",
        }
        if not os.path.exists('images'):
            os.makedirs('images')
        
        for i in range(10):
            time.sleep(15)
            try:
                response = requests.get(f'https://discord.com/api/v9/channels/{self.channel_id}/messages', headers=headers)
                if response.status_code != 200:
                    raise Exception(f"Failed to get messages: {response.status_code} {response.text}")
                
                messages = response.json()
                for message in messages:
                    if 'attachments' in message and len(message['attachments']) > 0:
                        image_url = message['attachments'][0]['url']
                        image_response = requests.get(image_url)
                        if image_response.status_code != 200:
                            raise Exception(f"Failed to download image: {image_response.status_code} {image_response.text}")

                        image_name = os.path.basename(urlparse(image_url).path)
                        self.image_path_str = os.path.join("images", image_name)
                        with open(self.image_path_str, "wb") as file:
                            file.write(image_response.content)
                        print(f"Image downloaded and saved at: {self.image_path_str}")
                        return
                print("No attachments found in the message.")
            except Exception as e:
                print(f"An error occurred: {e}")
                if i == 9:
                    raise ValueError("Timeout")
        raise ValueError("Timeout: Image not downloaded within the expected time frame.")

    def image_path(self):
        return self.image_path_str

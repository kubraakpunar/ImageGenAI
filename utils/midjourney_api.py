import requests
from urllib.parse import urlparse
import os
import random
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
        self.custom_id = ""
        self.image_path_str = ""

        self.send_message()
        self.wait_message()
        self.get_image()
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
    def wait_message(self):
        headers = {
            'Authorization': self.authorization,
            "Content-Type": "application/json",
        }
        for i in range(5):
            time.sleep(60)
            try:
                response = requests.get(f'https://discord.com/api/v9/channels/{self.channel_id}/messages', headers=headers)
                if response.status_code != 200:
                    raise Exception(f"Failed to get messages: {response.status_code} {response.text}")
                
                messages = response.json()
                print(f"Retrieved messages: {json.dumps(messages, indent=2)}")
                most_recent_message_id = messages[0]['id']
                self.message_id = most_recent_message_id
                components = messages[0]['components'][0]['components']
                buttons = [comp for comp in components if comp.get('label') in ['U1', 'U2', 'U3', 'U4']]
                custom_ids = [button['custom_id'] for button in buttons]
                if not custom_ids:
                    raise Exception("No buttons found to select from.")
                self.custom_id = random.choice(custom_ids)
                break
            except Exception as e:
                print(f"Error getting message: {e}")
                if i == 4:
                    raise ValueError("Timeout")

    def get_image(self):
        url = "https://discord.com/api/v9/interactions"
        headers = {
            "Authorization": self.authorization,
            "Content-Type": "application/json",
        }
        data = {
            "type": 3,
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_flags": 0,
            "message_id": self.message_id,
            "application_id": self.application_id,
            "session_id": self.session_id,
            "data": {
                "component_type": 2,
                "custom_id": self.custom_id,
            }
        }
        response = requests.post(url, headers=headers, json=data)
        print(f"Request payload: {json.dumps(data, indent=2)}")
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code not in (200, 204):
            raise Exception(f"Failed to choose images: {response.status_code} {response.text}")
        else:
            print("Images chosen successfully.")

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
                if 'attachments' in messages[0] and len(messages[0]['attachments']) > 0:
                    image_url = messages[0]['attachments'][0]['url']
                    image_response = requests.get(image_url)
                    if image_response.status_code != 200:
                        raise Exception(f"Failed to download image: {image_response.status_code} {image_response.text}")

                    image_name = os.path.basename(urlparse(image_url).path)
                    self.image_path_str = os.path.join("images", image_name)
                    with open(self.image_path_str, "wb") as file:
                        file.write(image_response.content)
                    break
                else:
                    print("No attachments found in the message.")
            except Exception as e:
                print(f"An error occurred: {e}")
                if i == 9:
                    raise ValueError("Timeout")

    def image_path(self):
        return self.image_path_str


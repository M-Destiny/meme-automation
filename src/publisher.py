import os
import requests
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

class InstaPublisher:
    def __init__(self, session_file="session.json"):
        self.cl = Client()
        self.session_file = session_file
        self.user = os.getenv("IG_USER")
        self.password = os.getenv("IG_PASS")

    def login(self):
        if not self.user or not self.password:
            print("IG_USER or IG_PASS not found in environment.")
            return False
        if os.path.exists(self.session_file):
            print(f"Loading session from {self.session_file}")
            self.cl.load_settings(self.session_file)
            try:
                self.cl.login(self.user, self.password)
            except Exception as e:
                print(f"Session login failed: {e}")
                self.cl.login(self.user, self.password)
        else:
            print(f"No session found, logging in for the first time.")
            self.cl.login(self.user, self.password)
            self.cl.dump_settings(self.session_file)
            print(f"Session saved to {self.session_file}")
        return True

    def upload_photo(self, path, caption="Check out this meme! #ai #meme"):
        print(f"Uploading {path} to Instagram (via instagrapi)...")
        media = self.cl.photo_upload(path, caption)
        print(f"Uploaded successfully! ID: {media.pk}")
        return media.pk

class MetaPublisher:
    def __init__(self):
        self.access_token = os.getenv("META_ACCESS_TOKEN")
        self.ig_user_id = os.getenv("IG_USER_ID")
        self.graph_url = "https://graph.facebook.com/v18.0/"

    def upload_photo(self, image_url, caption="Check out this meme! #ai #meme"):
        """
        Meta Graph API requires the image to be hosted on a public URL.
        This is a limitation of the official API for container creation.
        """
        if not self.access_token or not self.ig_user_id:
            print("META_ACCESS_TOKEN or IG_USER_ID not found in environment.")
            return None

        print(f"Uploading {image_url} to Instagram (via Meta Graph API)...")
        
        # 1. Create Media Container
        container_url = f"{self.graph_url}{self.ig_user_id}/media"
        payload = {
            'image_url': image_url,
            'caption': caption,
            'access_token': self.access_token
        }
        response = requests.post(container_url, data=payload)
        result = response.json()
        
        if 'id' not in result:
            print(f"Error creating container: {result}")
            return None
        
        creation_id = result['id']
        
        # 2. Publish Media Container
        publish_url = f"{self.graph_url}{self.ig_user_id}/media_publish"
        publish_payload = {
            'creation_id': creation_id,
            'access_token': self.access_token
        }
        publish_response = requests.post(publish_url, data=publish_payload)
        publish_result = publish_response.json()
        
        if 'id' not in publish_result:
            print(f"Error publishing media: {publish_result}")
            return None
            
        print(f"Published successfully! ID: {publish_result['id']}")
        return publish_result['id']

if __name__ == "__main__":
    # Example usage
    # p = InstaPublisher()
    # m = MetaPublisher()
    pass

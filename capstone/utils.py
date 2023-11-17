import os
import openai
from IPython.display import Image
from IPython import display
from base64 import b64decode
import utils

def generate_image(prompt):
    # Set your OpenAI API key here. Preferably use an environment variable for security.
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    try:
        # Call the OpenAI API to generate an image
        # Replace 'Image' with the appropriate function based on the OpenAI documentation
        response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
        if response.status_code == 200:
            # Process the response and extract the image data
            image_data = response.json()
            return image_data
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

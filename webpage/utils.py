#utils.py
import openai
import requests
import os
from openai import OpenAI
import tkinter as tk           # for GUI thumbnails of what we got
from PIL import ImageTk
import numpy as np
from PIL import Image

def generate_image(prompt):
    api_key = "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"
    endpoint = "https://api.openai.com/v1/images/generations"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "prompt": prompt
    }

    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        if isinstance(result, dict) and "data" in result and result["data"]:
            return result["data"][0].get("url")  # Assuming you want the first image URL
        else:
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None
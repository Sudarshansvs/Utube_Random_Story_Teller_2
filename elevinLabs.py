import os
import requests
#test
api_key="sk_ea094a9ff9df71460172a315e50b267e23b988c29ca3da16"
chunk_size= 1024
voice_id="21m00Tcm4TlvDq8ikWAM"
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

headers = {
    "Accept":"audio/mpeg",
    "Content-Type" : "application/json",
    "xi-api-key" :api_key
}

data  = {
    "text": "hi hello how are you !",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost" : 0.5
    }
}
response = requests.post(url, json=data, headers = headers)

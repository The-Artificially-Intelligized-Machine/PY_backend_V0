import requests
from pydub import AudioSegment
import io
import os
import uuid
from datetime import datetime


def download_elevenlabs_as_ogg(text, api_key):
    """
    Downloads audio from ElevenLabs API and converts it to OGG format.
    Creates an output folder if it doesn't exist and generates a unique filename.

    Args:
        text (str): Text to convert to speech
        voice_id (str): ElevenLabs voice ID
        api_key (str): Your ElevenLabs API key
        base_folder (str): Base folder name for outputs (default: "output")

    Returns:
        str: Filename of the created audio file, or None if there was an error
    """
    base_folder="output"
    # Create output folder if it doesn't exist
    os.makedirs(base_folder, exist_ok=True)

    # Generate unique filename using timestamp and UUID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    filename = f"audio_{timestamp}_{unique_id}.ogg"
    output_path = os.path.join(base_folder, filename)

    # ElevenLabs API endpoint
    url = f"https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb"

    # Request headers
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    # Request body
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    try:
        # Make the API request
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        # Convert the MP3 response to OGG
        audio = AudioSegment.from_mp3(io.BytesIO(response.content))

        # Export as OGG
        audio.export(output_path, format="ogg")

        print(f"Audio successfully downloaded and converted to OGG!")
        print(f"File saved in the output folder as: {filename}")

        return filename

    except requests.exceptions.RequestException as e:
        print(f"Error making request to ElevenLabs API: {e}")
        return(f"Error making request to ElevenLabs API: {e}")
    except Exception as e:
        return(f"Error converting audio: {e}")


# Example usage:
"""
api_key = "your_api_key_here"
voice_id = "your_voice_id_here"
text = "Hello, this is a test of the ElevenLabs API with OGG conversion."

filename = download_elevenlabs_as_ogg(text, voice_id, api_key)
if filename:
    print(f"Your audio file is named: {filename}")
"""

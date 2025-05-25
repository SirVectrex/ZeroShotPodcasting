import requests

class DiaTTSAPI:
    def __init__(self, api_url="http://localhost:8003/tts"):
        self.api_url = api_url

    def generate_audio(self, script, output_path="podcast_audio.wav"):
        payload = {
            "voice_mode": "dialogue",
            "text": script,
            "output_format": "wav",
            "cfg_scale": 3.0,
            "temperature": 1.2,
            "top_p": 0.95,
            "speed_factor": 1.0,
            "cfg_filter_top_k": 35,
            "seed": -1,
            "split_text": True,
            "chunk_size": 160
        }

        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

        print(f"Audio saved as {output_path}")

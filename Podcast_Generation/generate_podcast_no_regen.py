"""NoCheckPipeline.py
This script generates a podcast script using OpenAI's GPT-4o model and converts it to audio using Google's Gemini TTS.
It reads a text file containing a query, generates a script based on that query, and then synthesizes the script into audio format.

Unlike the original script, this version does not trigger regeneration of script but stops. This is useful for testing or when you want to generate a podcast without re-evaluating the script.

Sample usage:
python generate_podcast.py --input_file data/query.txt --output_file output_conversation.wav

"""


# Set the OpenAI API key
import wave
import argparse
from openai import OpenAI
import json
import requests
import os
os.environ["OPENAI_API_KEY"] = "sk-YOUR_OPENAI"
OPENAI_client = OpenAI()

# TTS setup 
from google import genai
from google.genai import types
Google_client = genai.Client(api_key="YOUR_GOOGLE_API_KEY")

# --- Config ---
WPM = 120  # Words per minute for word count check
EVAL_THRESHOLD = 0.9  # Minimum G-Eval average score

# --- Helper Functions ---

def read_query(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read().strip()

def extract_episode_length(query: str) -> int:
    match = re.search(r'"episode_length_minutes":\s*(\d+)', query)
    return int(match.group(1)) if match else None

def extract_target_ages(query: str) -> list:
    matches = re.findall(r'"age"\s*:\s*(\d+)', query)
    return list(map(int, matches)) if matches else []

def generate_script_from_openai(prompt: str) -> str:
    response = OPENAI_client.responses.create(model="gpt-4o", input=prompt)
    return response.output_text

def generate_audio_from_gemini(script: str) -> bytes:
    full_prompt = "TTS the following conversation in an engaging and fun way:\n" + script
    response = Google_client.generate_content(
        contents=full_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                        types.SpeakerVoiceConfig(
                            speaker='Speaker 1',
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Kore')
                            )
                        ),
                        types.SpeakerVoiceConfig(
                            speaker='Speaker 2',
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Puck')
                            )
                        )
                    ]
                )
            )
        )
    )
    return response.candidates[0].content.parts[0].inline_data.data

def save_wave_file(filename: str, pcm_data: bytes, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)

# --- Validation Checks ---

def check_word_count_limit(script: str, query: str) -> bool:
    episode_length = extract_episode_length(query)
    if episode_length is None:
        print("Could not determine episode length. Skipping word count check.")
        return False
    max_length = episode_length * WPM
    word_count = len(script.split())
    print(f"📝 Script length: {word_count} / {max_length} words")
    return word_count <= max_length

def check_readability(script: str, query: str) -> bool:
    clean_script = script.replace("Speaker 1:", "").replace("Speaker 2:", "").strip()
    readability = Readability(clean_script)
    ari = readability.ari()
    script_min_age, script_max_age = ari.ages

    listener_ages = extract_target_ages(query)
    if not listener_ages:
        print("No target listener ages found in query.")
        return False

    min_listener_age = min(listener_ages)
    max_listener_age = max(listener_ages)

    print(f"Script age range: {script_min_age}-{script_max_age}, Target audience: {min_listener_age}-{max_listener_age}")
    return (script_min_age <= max_listener_age and script_max_age >= min_listener_age)

def evaluate_podcast(input_text: str, output_text: str) -> float:
    criteria = [
        "Does the output fully and clearly address the input topic?",
        "Does the conversation flow naturally from one speaker to the next?",
        "Are transitions smooth, ideas logically connected, and no abrupt topic shifts?",
        "Penalize unclear, off-topic, or awkward parts."
    ]

    eval_prompt = f"""You are a conversation quality evaluator. Given an input and a generated podcast script, evaluate it against the following criteria:
    {chr(10).join(f"{i+1}. {c}" for i, c in enumerate(criteria))}

    Provide a score for each (0 to 1), followed by a one-line justification. Keep scores to one decimal point of precision.

    Input:
    {input_text}

    Output:
    {output_text}

    Respond in the following format:

    1. [score] - [short reason]
    2. [score] - [short reason]
    3. [score] - [short reason]
    4. [score] - [short reason]

    Then output the average score like this:
    Average: [score]
"""

    response = OPENAI_client.responses.create(model="gpt-4o", input=eval_prompt)
    lines = response.output_text.strip().splitlines()
    avg_line = [line for line in lines if "Average:" in line]
    if not avg_line:
        print("⚠️ Could not parse evaluation result.")
        return 0.0
    try:
        avg_score = float(re.findall(r"[\d.]+", avg_line[0])[0])
        print(f"🎯 G-Eval average score: {avg_score}")
        return avg_score
    except Exception:
        return 0.0

# --- Main Execution ---

def main():
    parser = argparse.ArgumentParser(description="Generate podcast script and audio if validation passes.")
    parser.add_argument('--input_file', required=True, help='Path to input .txt file')
    parser.add_argument('--output_file', required=True, help='Filename for output .wav file')
    args = parser.parse_args()

    print("Reading input query...")
    input_query = read_query(args.input_file)

    print("Generating podcast script...")
    script = generate_script_from_openai(input_query)

    print("Running validation checks...")

    if not check_word_count_limit(script, input_query):
        print("❌ Script is too long for target episode length. Skipping TTS.")
        return

    if not check_readability(script, input_query):
        print("❌ Script readability is not appropriate for the target audience. Skipping TTS.")
        return

    score = evaluate_podcast(input_query, script)
    if score < EVAL_THRESHOLD:
        print(f"❌ G-Eval score {score:.2f} is below threshold of {EVAL_THRESHOLD}. Skipping TTS.")
        return

    print("All checks passed. Generating audio...")
    audio_data = generate_audio_from_gemini(script)
    save_wave_file(args.output_file, audio_data)
    print(f"Podcast generated and saved to '{args.output_file}'")

if __name__ == "__main__":
    main()

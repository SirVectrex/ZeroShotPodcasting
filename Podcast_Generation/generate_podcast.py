import os
import re
import requests
import time
from DiaTTSAPI import DiaTTSAPI


# CONFIGURATION 
CHATGPT_API_URL = "https://api.openai.com/v1/chat/completions"
CHATGPT_API_KEY = os.getenv("OPENAI_API_KEY")  # Set your OpenAI API key as an environment variable
MAX_WORDS = 240  
MODEL = "gpt-o4-mini"


# INPUT 
def get_user_prompt():
    with open("query.txt", "r", encoding="utf-8") as f:
        return f.read()


# CHATGPT SCRIPT GENERATION 
def generate_script(prompt, max_words):
    headers = {
        "Authorization": f"Bearer {CHATGPT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }
    response = requests.post(CHATGPT_API_URL, headers=headers, json=data)
    response.raise_for_status()
    script = response.json()["choices"][0]["message"]["content"]
    return script

def count_words(text):
    return len(re.findall(r'\b\w+\b', text))

# CHATGPT G-EVAL 
def evaluate_script(script, prompt):
    headers = {
        "Authorization": f"Bearer {CHATGPT_API_KEY}",
        "Content-Type": "application/json"
    }
    eval_prompt = (
        "You are an expert podcast evaluator. Given the following script and prompt, "
        "evaluate the script for: (1) coherence, (2) age appropriateness for a general audience, "
        "(3) topic fitment. Respond with YES if all criteria are met, otherwise NO and a short reason.\n\n"
        f"Prompt: {prompt}\n\nScript:\n{script}\n\nEvaluation:"
    )
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a strict podcast script judge."},
            {"role": "user", "content": eval_prompt}
        ],
        "temperature": 0.0
    }
    response = requests.post(CHATGPT_API_URL, headers=headers, json=data)
    response.raise_for_status()
    evaluation = response.json()["choices"][0]["message"]["content"]
    return evaluation.strip()

# MAIN PIPELINE 
def main():
    prompt = get_user_prompt()
    print(f"Prompt:\n{prompt}\n")

    # Generate script, check word count, regenerate if needed
    for attempt in range(3):
        script = generate_script(prompt, MAX_WORDS)
        word_count = count_words(script)
        print(f"Generated script ({word_count} words):\n{script}\n")
        if word_count <= MAX_WORDS:
            break
        print(f"Script too long ({word_count} words). Regenerating...")
        time.sleep(2)
    else:
        print("Failed to generate script within word limit after 3 attempts.")
        return

    # Evaluate script
    evaluation = evaluate_script(script, prompt)
    print(f"Evaluation result:\n{evaluation}\n")
    if evaluation.lower().startswith("yes"):
        print("Script passed evaluation. Generating audio...")
        tts = DiaTTSAPI()
        tts.generate_audio(script)
    else:
        print("Script did not pass evaluation. Please revise the prompt or try again.")


if __name__ == "__main__":
    main()

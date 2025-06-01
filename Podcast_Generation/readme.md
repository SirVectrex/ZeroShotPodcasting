# Podcast Generation

This folder contains scripts and resources for generating podcasts using Large Language Models (LLMs) and the Dia 1.6B Text-to-Speech (TTS) server.

## Overview

The main pipeline works as follows:
1. **Input Prompt:**  
   The user provides a prompt describing the desired podcast topic (edit `query.txt`).
2. **Script Generation:**  
   The script calls the OpenAI ChatGPT API to generate a podcast script based on the prompt.
3. **Word Count Check:**  
   If the script exceeds the maximum word limit, it is regenerated (up to 3 attempts).
4. **Script Evaluation:**  
   The script is evaluated by ChatGPT (G-EVAL) for coherence, age appropriateness, and topic fitment. The script is further tested on age-appropiateness with ARI.
5. **Audio Generation:**  
   If the script passes evaluation, the Dia 1.6B TTS API is called locally to generate the podcast audio using voice cloning.

## Folder Structure

- 'generate_podcast.py': Main script to generate the podcast.
- 'generate_podcast_no_regen.py': Main script to generate the podcast without regeneration when checks fail.
- 'NotebookGeneration.ipynb': Jupyter notebook for interactive podcast generation and more detailed exploration.
- 'DiaTTSAPI.py': Python module for interacting with the Dia 1.6B TTS server as an alternative to the Google API.

## Usage

1. **Set Up Environment:**
   - Place your OpenAI API key in the `OPENAI_API_KEY` and `GOOGLE_API_KEY` environment variable.
   - Ensure the Dia 1.6B TTS server is running locally and your reference audio is available on the server.

2. **Edit Prompt:**
   - Write your podcast topic or question in `query.txt`.

3. **Run the Script:**
   ```sh
   python generate_podcast.py

4. **Output:**
The generated podcast audio will be saved as podcast_audio.wav in this directory.


## Requirements

- Python 3.x
- `requests` Python package
- Access to OpenAI API (ChatGPT)
- Access to Google TTS API (optional, if not using Dia TTS server)
- Running Dia 1.6B TTS server (see [Dia-TTS-Server documentation](https://github.com/devnen/Dia-TTS-Server/blob/main/documentation.md))

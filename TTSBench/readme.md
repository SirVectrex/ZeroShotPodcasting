# TTSBench: A Benchmarking Platform for Text-to-Speech Models

TTSBench is a web-based platform designed to evaluate and compare the performance of various Text-to-Speech (TTS) models. The platform enables users to listen to audio samples, distinguish between human and synthetic speech, and provide quality ratings. Aggregated results are displayed on leaderboards, offering insights into the strengths and weaknesses of different TTS systems.

## Features

- **Audio Evaluation:** Listen to both human and AI-generated speech samples.
- **Human vs. Synthetic Classification:** Identify whether a sample is human or machine-generated.
- **Quality Rating:** Rate the naturalness and intelligibility of each sample on a 1–5 scale.
- **Leaderboards:** View aggregated results and rankings for monologue and conversational TTS models.
- **Data Transparency:** All audio files and metadata are accessible for research and reproducibility.

## Usage

1. **Rate Audio Samples:**  
   Visit `rate.html` to participate in the evaluation. Listen to randomly selected audio, classify it, and submit your rating.

2. **View Leaderboards:**  
   - `leaderboard_standard.html`: Rankings for monologue samples.
   - `leaderboard_convo.html`: Rankings for conversational samples.

3. **Home Page:**  
   `index.html` provides an overview and navigation to all features.

## Technical Overview

- **Frontend:**  
  HTML, CSS, and JavaScript (no frameworks).

- **Backend:**  
  Node.js API endpoints (see `/api` directory).  
  PostgreSQL powered by NEON.
  Hosted on Vercel.

- **Audio Data:**  
  Audio files are stored in `public/audio/`.  
  Metadata is maintained in `data/audio_metadata.json`.

## Project Structure

```
/api
  get-audio.js             # Serves random unrated audio samples
  submit-rating.js         # Handles rating submissions
  get-leaderboard-*.js     # Leaderboard data endpoints
  get-ratings-count.js     # Returns total ratings count
/public
  /audio                   # Audio files (monologue & conversational)
/data
  audio_metadata.json      # Metadata for all audio samples
index.html                 # Home page
rate.html                  # Audio rating interface
leaderboard_*.html         # Leaderboards
public/style.css           # Stylesheet
```


## Running Locally

1. Clone the repository.
2. Install dependencies:
   ```sh
   npm install
   ```
3. Deploy on Vercel or run locally


## License
MIT License.

Developed for research and educational purposes.
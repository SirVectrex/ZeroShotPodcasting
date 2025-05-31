
# ZeroShotPodcasting Monorepo

Welcome to **ZeroShotPodcasting**, a comprehensive toolkit for zero-shot podcast script generation, evaluation, and text-to-speech (TTS) synthesis — all powered by advanced large language models (LLMs) and state-of-the-art TTS engines.



## 📂 Repository Structure

```

ZerShotPodcasting/
├── Podcast\_Generation/       # End-to-end podcast generation pipeline (LLM + TTS)
│   ├── ...
│   └── readme.md              # Detailed usage and setup for podcast generation
│
├── LLMBench/                  # Benchmarking and evaluation suite for LLMs
│   ├── ...          
│   └── readme.md              # LLMBench specific instructions and overview
│
├── TTSBench/                  # Benchmarking and analysis tools for TTS systems
│   ├── ...             
│   └── readme.md              # TTSBench usage, setup guide, explanation
│
└── README.md                  # (You are here!) Monorepo overview and setup guide

````


## 🚀 Key Features

- **Zero-shot Podcast Script Generation:** Generate engaging, natural podcast scripts from JSON-configured prompts without manual scripting.
- **Multi-speaker Dialogue TTS:** Produce high-quality audio using Dia 1.6B TTS with voice cloning and dialogue modes.
- **Automated Script Evaluation:** Evaluate podcast scripts for coherence, topic relevance, and audience appropriateness with GPT-powered judging.
- **Comprehensive Benchmarking:** Evaluate both LLMs and TTS systems for quality, readability, and audience fit.
- **Modular & Extensible:** Easily swap or add new LLMs or TTS engines with a clean modular design.



## 📚 Getting Started

### Prerequisites

- Python 3.x
- Install dependencies (see individual subfolder `readme.md` files for details)
- API keys and local servers:
  - OpenAI API key for LLM interactions (set environment variable `OPENAI_API_KEY`)
  - Dia-TTS server running locally or remotely (default: `http://localhost:8003/tts`)


## 🧩 Module Details

### LLMBench

* Measure readability (ARI, Flesch-Kincaid).
* Perform coherence and relevance evaluation.
* Analyze language complexity and audience fit.
* Visualize age appropriateness and linguistic features.

### TTSBench

* Benchmark TTS systems including Dia-TTS.

### Podcast Generation

* Generate podcast scripts from detailed prompts.
* Use multi-speaker dialogue voice cloning with Dia TTS.
* Evaluate generated scripts automatically with GPT-powered metrics.


---

## 💡 Acknowledgements

* OpenAI for GPT models and APIs
* Dia-TTS-Server, CSM for powerful voice cloning and dialogue TTS
* All contributors and open-source libraries powering this project


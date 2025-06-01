
# ZeroShotPodcasting Monorepo

Welcome to **ZeroShotPodcasting**, a comprehensive toolkit for zero-shot podcast script generation, evaluation, and text-to-speech (TTS) synthesis — all powered by advanced large language models (LLMs) and state-of-the-art TTS engines.

*Note:* The Google TTS API was introduced very shortly before paper submission - the Paper submission state of the repository was freezed as a release. The change after paper submission include: support of Google TTS API, Jupyter notebook for interactive podcast generation, and a few minor bug fixes. 



## 📂 Repository Structure

```

ZerShotPodcasting/
├── Podcast\_Generation/        # End-to-end podcast generation pipeline (LLM + TTS)
│   ├── generate\_podcast.py    # Main podcast generation script with Google TTS
│   ├── generate\_podcast\_no\_regen.py # Podcast generation without regeneration on failure
│   ├── NotebookGeneration.ipynb # Jupyter notebook for interactive podcast generation
│   ├── query.txt              # Example prompt input
│   └── readme.md              # Detailed usage and setup for podcast generation
│
├── LLMBench/                  # Benchmarking and evaluation suite for LLMs
│   ├── ARI\_Flesh.py           # Readability metrics
│   ├── GEval\_test.py          # Script evaluation using GPT-based methods
│   ├── age\_plot.py            # Age-appropriateness visualization
│   ├── print\_GEVAL\_stats.py   # Evaluation stats reporting
│   ├── wordanalysis.py        # Word and complexity analysis
│   ├── LLM\_interaction/       # Helper modules for LLM communication
│   ├── scripts/               # Additional scripts for benchmarking
│   ├── SVGs/                  # Visualization assets
│   └── readme.md              # LLMBench specific instructions
│
├── TTSBench/                  # Benchmarking and analysis tools for TTS systems
│   ├── scripts/               # Automation and benchmarking scripts
│   ├── plots/                 # Performance and analysis plots
│   └── readme.md              # TTSBench usage and setup guide
│
└── README.md                  # (You are here!) Monorepo overview and setup guide

````


## 🚀 Key Features

- **Zero-shot Podcast Script Generation:** Generate engaging, natural podcast scripts from JSON-configured prompts without manual scripting.
- **Multi-speaker Dialogue TTS:** Produce high-quality audio using Dia 1.6B TTS with voice cloning and dialogue modes.
- **Automated Script Evaluation:** Evaluate podcast scripts for coherence, topic relevance, and audience appropriateness with GPT-powered judging.
- **Comprehensive Benchmarking:** Evaluate both LLMs and TTS systems for quality, readability, and audience fit.
- **Visualization & Analysis:** Plot and analyze LLM outputs and TTS performance metrics.
- **Modular & Extensible:** Easily swap or add new LLMs or TTS engines with a clean modular design.



## 📚 Getting Started

### Prerequisites

- Python 3.x
- Install dependencies (see individual subfolder `readme.md` files for details)
- API keys and local servers:
  - OpenAI API key for LLM interactions (set environment variable `OPENAI_API_KEY`)
  - Google TTS API key (set environment variable `GOOGLE_API_KEY`)
  - optionally Dia-TTS server running locally or remotely (default: `http://localhost:8003/tts`)


## 🧩 Module Details

### LLMBench

* Measure readability (ARI, Flesch-Kincaid).
* Perform coherence and relevance evaluation.
* Analyze language complexity and audience fit.
* Visualize age appropriateness and linguistic features.

### TTSBench

* Benchmark TTS systems including Dia-TTS.
* Generate plots for audio quality metrics.
* Automate testing and comparisons across engines.

### Podcast Generation

* Generate podcast scripts from detailed prompts.
* Use multi-speaker dialogue voice cloning with Dia TTS.
* Evaluate generated scripts automatically with GPT-powered metrics.


---

## 💡 Acknowledgements

* OpenAI for GPT models and APIs
* Dia-TTS-Server for powerful voice cloning and dialogue TTS
* All contributors and open-source libraries powering this project


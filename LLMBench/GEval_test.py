import csv

from deepeval import evaluate
from deepeval.metrics import HallucinationMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams, ConversationalTestCase
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import ConversationalGEval

import json

import pandas as pd

df = pd.read_csv("scripts/scripts_utf8.csv", sep=";")
model_names = df["Model"].tolist()




podcast_instructions = """
🎙️ **Podcast Script Generator Instructions**

You are an AI assistant that generates engaging, natural, and professionally structured podcast scripts based on a JSON configuration.

---

🎯 **GOAL**
Write a podcast script featuring a two-person dialogue that:

* Explores the topic provided in the JSON
* Fits the duration **exactly**, using a maximum of `episode_length_minutes × 120` words
* Matches tone, language, and complexity to the audience's age
* Follows a friendly and conversational structure
* Feels like a real, unscripted podcast — without addressing the audience directly if `"audience_direct": "no"`

---

🧱 **SCRIPT STRUCTURE**

1. 🎬 **Creative Mini-Intro**
   Begin with something like "Welcome to..." or "You're listening to..." (1–2 lines)
2. 👋 **Friendly Guest Introduction**
   Host greets and introduces the guest
3. 🎓 **Main Topic Discussion**
   Explain key concepts with examples and analogies, depending on age
4. 🔄 **Back-and-Forth Engagement**
   Include light humor, surprises, or clarifications
5. 🧼 **Closing / Wrap-Up**
   End on a thoughtful, clever, or warm note

---

🔤 **OUTPUT FORMAT**
Use `[S1]` for the host and `[S2]` for the guest. Example:
[S1] Welcome to BrainSpark! I’m your host, Kent Brockman.
[S2] Thanks for having me, Kent — I brought a brain full of neural network facts!
[S1] That’s perfect, because today we’re diving into...

---

🎭 **CHARACTER DESIGN**

* Host: Use name from JSON
* Guest: Invent a name + use `"guest_role"` and `"guest_personality"` if provided
* Make their style engaging, natural, and age-appropriate

---

📏 **HARD LIMIT — WORD COUNT**
🛑 The **total script must NOT exceed `episode_length_minutes × 120 words`**.
Round slightly under if needed. Make every word count.

---

🗣️ **STYLE RULES**

* Use the `"language"` field
* Match tone to audience age:

  * Kids (under 12): playful, analogies, no jargon
  * Teens: friendly, structured, some humor
  * Adults: professional, conversational, clear
* Reflect optional `"style"`:

  * `"humorous"` → witty, energetic
  * `"educational"` → clear, factual
  * `"story-driven"` → immersive, dramatic
* Respect `"audience_direct": "no"` — don’t break the fourth wall

---

🧠 **RECAP**
✅ Max word limit enforced
✅ Start with a mini-intro
✅ Two speakers only
✅ Clear, structured, characterful script
✅ Age and tone aligned
✅ Use guest role/personality/style fields when available
✅ No references to this prompt or JSON

{
"podcast": {
"topic": "What is a neural network?",
"language": "en",
"host": "Kent Brockman",
"audience": \[
{
"name": "Bart Simpson",
"age" : 8
},
{
"name": "Lisa Simpson",
"age": 12
}
],
"audience\_direct": "no",
"episode\_length\_minutes": 2results = evaluate(test_cases=dataset.test_cases, metrics=[metric])
},
"style": "engaging",
"guest\_role": "scientist"
}
"""
def script_to_turns(script_text):
    # Split by lines, remove empty lines
    lines = [line.strip() for line in script_text.strip().splitlines() if line.strip()]
    
    return [LLMTestCase(input=podcast_instructions, actual_output=script_text)]

csv_path = "LLM_interaction/scripts_utf8.csv" 

test_cases = []

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        script_text = row['Text']
        turns = script_to_turns(script_text)
        convo_test_case = ConversationalTestCase(turns=turns)
        test_cases.append(convo_test_case)

dataset = EvaluationDataset(test_cases=test_cases)


metric = ConversationalGEval(
    name="Relevance and Coherence",
    evaluation_steps=[
        "Does the output fully and clearly address the input topic (neural networks)?",
        "Does the conversation flow naturally from one speaker to the next?",
        "Are transitions smooth, ideas logically connected, and no abrupt topic shifts?",
        "Penalize unclear, off-topic, or awkward parts."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
)

results = evaluate(test_cases=dataset.test_cases, metrics=[metric])

print("-------------------------------------")
print(results)
print("-------------------------------------")

scores = []

for idx, result in enumerate(results.test_results):
    try:
        score = result.metrics_data[0].score
        scores.append({
            "index": idx,
            "score": score,
            "reason": result.metrics_data[0].reason
        })
    except Exception as e:
        scores.append({
            "index": idx,
            "score": None,
            "error": str(e)
        })

# Print or save as JSON
import json
with open("scripts/evaluation_scores.json", "w") as f:
    json.dump(scores, f, indent=2)


with open("scripts/model_scores.json", "w", encoding="utf-8") as f:
    json.dump(scores, f, indent=2)




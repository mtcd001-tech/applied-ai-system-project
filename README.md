# 🎵 Applied AI Music Recommender System

> An evolution of the Module 1–3 Music Recommender Simulation, upgraded with an **Agentic Workflow** that plans, acts, evaluates, and reflects on its own recommendations.

---

## 📌 Original Project (Modules 1–3)

**Repo:** [ai110-module3show-musicrecommendersimulation-starter](https://github.com/mtcd001-tech/ai110-module3show-musicrecommendersimulation-starter)

The original project was a content-based music recommender simulation. It loaded a CSV of songs, scored each track against a user preference profile using weighted features (genre, mood, energy, tempo), and returned a ranked list of top recommendations via the command line. It demonstrated core recommendation logic but had no self-evaluation or retry mechanism.

---

## 🧠 What This Project Does

This upgraded system adds an **Agentic Workflow** on top of the original recommender. Instead of just scoring and returning results, the AI agent:

1. **Plans** — analyzes the user profile and describes its strategy
2. **Acts** — runs the recommender engine
3. **Evaluates** — checks if the top score meets a confidence threshold
4. **Reflects** — if results are poor, adjusts preferences and retries (up to 3 iterations)

This makes the system behave more like a real AI agent that is aware of its own output quality.

---

## 🏗️ Architecture Overview
User Preferences
│
▼
┌─────────────┐
│  agent.py   │  ← Agentic loop (Plan → Act → Evaluate → Reflect)
└──────┬──────┘
│
▼
┌──────────────────┐
│  recommender.py  │  ← Core scoring engine (load, score, rank)
└──────┬───────────┘
│
▼
data/songs.csv   ← 18 songs with 11 features each
│
▼
Ranked Results + Reasons + Agent Log

**Components:**
- `src/agent.py` — Agentic loop with plan/act/evaluate/reflect steps
- `src/recommender.py` — Core logic: load songs, score, rank
- `src/main.py` — Runs 3 user profiles through the agent
- `tests/test_recommender.py` — 9 automated tests
- `agent.log` — Full log of every agent decision

---

## ⚙️ Setup Instructions

**Requirements:** Python 3.8+

```bash
# 1. Clone the repo
git clone https://github.com/mtcd001-tech/applied-ai-system-project.git
cd applied-ai-system-project

# 2. (Optional) Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install pytest

# 4. Run the recommender agent
python -m src.main

# 5. Run automated tests
python -m pytest tests/ -v
```

No API keys or external services required. Runs fully offline.

---

## 💬 Sample Interactions

### Profile 1: Chill Lofi Listener
**Input:**
```python
{"genre": "lofi", "mood": "chill", "energy": 0.40, "tempo_bpm": 78, ...}
```
**Agent Output:**
[AGENT - PLAN] Goal: Find low-energy lofi songs with a chill mood.
[AGENT - EVALUATE] ✅ Good results (top score: 76.4). Accepting recommendations.
#1 - Midnight Coding by LoRoom        Score: 76.4/100
#2 - Library Rain by Paper Lanterns   Score: 75.8/100
#3 - Focus Flow by LoRoom             Score: 62.1/100
✅ Agent accepted results on first iteration.

---

### Profile 2: High Energy Pop Fan
**Input:**
```python
{"genre": "pop", "mood": "happy", "energy": 0.90, "tempo_bpm": 128, ...}
```
**Agent Output:**
[AGENT - PLAN] Goal: Find high-energy pop songs with a happy mood.
[AGENT - EVALUATE] ✅ Good results (top score: 75.0). Accepting recommendations.
#1 - Sunrise City by Neon Echo   Score: 75.0/100
#2 - Gym Hero by Max Pulse       Score: 62.3/100
✅ Agent accepted results on first iteration.

---

### Profile 3: Adversarial Edge Case
**Input:**
```python
{"genre": "metal", "mood": "aggressive", "energy": 1.0, "tempo_bpm": 210, ...}
```
**Agent Output:**
Iteration 1: ⚠️  Low confidence (49.5 < 60.0). Shifting energy toward middle.
Iteration 2: ⚠️  Low confidence (47.4 < 60.0). Dropping genre/mood filters.
Iteration 3: ⚠️  Low confidence (37.4 < 60.0). No good match found.
#1 - Digital Tension by Synth Pulse   Score: 37.4/100
⚠️ Agent reflected twice and honestly reported low confidence — correct behavior for impossible preferences.

---

## 🔧 Design Decisions

| Decision | Reason | Trade-off |
|---|---|---|
| Content-based filtering | Simple, explainable, no user data needed | No collaborative filtering; can't learn from other users |
| Score threshold at 60/100 | Balances strictness with dataset size | May be too strict for niche genres |
| Max 3 iterations | Prevents infinite loops | May not fully recover from extreme edge cases |
| Reflect by adjusting energy then dropping genre/mood | Progressive relaxation strategy | Later results are less personalized |
| Reasons list in output | Explainable AI — user knows why songs were chosen | Adds verbosity to output |

---

## 🧪 Testing Summary

**9 automated tests across 3 categories:**

| Test | Result |
|---|---|
| Songs CSV loads 18 songs | ✅ Pass |
| Each song has required fields | ✅ Pass |
| Numeric fields are float type | ✅ Pass |
| score_song returns (float, list) tuple | ✅ Pass |
| Genre-matching song scores higher | ✅ Pass |
| Reasons list is never empty | ✅ Pass |
| recommend_songs returns exactly k results | ✅ Pass |
| Results sorted highest score first | ✅ Pass |
| Top result for lofi prefs is a lofi song | ✅ Pass |

**What worked:** Core scoring logic is reliable and consistent across all profiles.  
**What didn't:** Adversarial profiles with out-of-dataset values (tempo 210 BPM, mood "aggressive") consistently scored below threshold — the agent's reflect mechanism could not recover because the dataset simply doesn't contain matching songs.  
**Learned:** Small datasets expose the limits of content-based filtering quickly.

---

## 🪞 Reflection

**What this project taught me about AI:**  
Adding an agentic loop changed how I think about AI systems. Instead of one-shot outputs, the agent monitors its own confidence and tries to improve — which is closer to how real AI pipelines behave. I learned that "good enough" thresholds matter as much as the algorithm itself.

**Limitations and ethics:**  
- The dataset of 18 songs creates filter bubbles — lofi and pop are overrepresented
- The system cannot learn or adapt over time; preferences must be manually defined
- No user data is collected, making this privacy-safe by design
- Potential misuse is low given this is a simulation, not a real platform
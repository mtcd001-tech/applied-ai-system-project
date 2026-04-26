"""
Agentic Workflow for Music Recommender.
The agent plans, acts, evaluates, and reflects on recommendations.
"""

import logging
from typing import Dict, List, Tuple

from recommender import load_songs, recommend_songs, score_song

# Setup logging
logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

MAX_ITERATIONS = 3
SCORE_THRESHOLD = 60.0  # Minimum acceptable top score out of 100


def plan(user_prefs: Dict) -> str:
    """Step 1: Analyze user preferences and describe the plan."""
    logging.info(f"[PLAN] User preferences received: {user_prefs}")

    genre = user_prefs.get("genre", "unknown")
    mood = user_prefs.get("mood", "unknown")
    energy = user_prefs.get("energy", 0.5)

    energy_label = "high-energy" if energy >= 0.7 else "low-energy" if energy <= 0.4 else "mid-energy"

    plan_text = (
        f"Goal: Find {energy_label} {genre} songs with a {mood} mood. "
        f"Will score all songs and return top 5. "
        f"Will retry with relaxed weights if top score < {SCORE_THRESHOLD}."
    )

    print(f"\n[AGENT - PLAN]\n  {plan_text}")
    logging.info(f"[PLAN] {plan_text}")
    return plan_text


def act(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple]:
    """Step 2: Run the recommender."""
    logging.info(f"[ACT] Running recommender for {len(songs)} songs, k={k}")
    results = recommend_songs(user_prefs, songs, k)
    logging.info(f"[ACT] Top result: {results[0][0]['title']} score={results[0][1]:.1f}")
    return results


def evaluate(results: List[Tuple], iteration: int) -> Tuple[bool, str]:
    """Step 3: Check if results are good enough."""
    top_score = results[0][1]
    top_title = results[0][0]['title']

    if top_score >= SCORE_THRESHOLD:
        verdict = f"✅ Good results (top score: {top_score:.1f}). Accepting recommendations."
        logging.info(f"[EVALUATE] Iteration {iteration}: PASS - {verdict}")
        return True, verdict
    else:
        verdict = f"⚠️  Low confidence (top score: {top_score:.1f} < {SCORE_THRESHOLD}). Will retry."
        logging.warning(f"[EVALUATE] Iteration {iteration}: FAIL - {verdict}")
        return False, verdict


def reflect(user_prefs: Dict, iteration: int) -> Dict:
    """Step 4: Adjust preferences to broaden search if results were poor."""
    logging.info(f"[REFLECT] Adjusting preferences for iteration {iteration}")

    adjusted = user_prefs.copy()

    # Broaden by relaxing genre/mood (clear them after 2 failed attempts)
    if iteration == 2:
        adjusted["genre"] = ""
        adjusted["mood"] = ""
        print(f"  [AGENT - REFLECT] Dropping genre/mood filter to broaden search.")
        logging.info("[REFLECT] Dropped genre and mood filters.")
    else:
        # Shift energy slightly toward middle
        adjusted["energy"] = (user_prefs["energy"] + 0.5) / 2
        print(f"  [AGENT - REFLECT] Shifting energy toward middle: {adjusted['energy']:.2f}")
        logging.info(f"[REFLECT] Energy adjusted to {adjusted['energy']:.2f}")

    return adjusted


def run_agent(user_prefs: Dict, songs: List[Dict]) -> List[Tuple]:
    """
    Main agentic loop: Plan → Act → Evaluate → Reflect (repeat if needed).
    Returns the best results found.
    """
    print("\n" + "="*70)
    print("AGENTIC MUSIC RECOMMENDER".center(70))
    print("="*70)

    current_prefs = user_prefs.copy()
    best_results = None

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- Iteration {iteration}/{MAX_ITERATIONS} ---")
        logging.info(f"[AGENT] Starting iteration {iteration}")

        # Step 1: Plan
        plan(current_prefs)

        # Step 2: Act
        results = act(current_prefs, songs)
        best_results = results

        # Step 3: Evaluate
        passed, verdict = evaluate(results, iteration)
        print(f"  [AGENT - EVALUATE] {verdict}")

        if passed:
            break

        # Step 4: Reflect (only if not last iteration)
        if iteration < MAX_ITERATIONS:
            current_prefs = reflect(current_prefs, iteration)

    return best_results
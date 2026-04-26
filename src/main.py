"""
Main runner - now uses Agentic Workflow.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs
from agent import run_agent


def print_results(results):
    print("\n" + "="*70)
    print("TOP MUSIC RECOMMENDATIONS FOR YOU".center(70))
    print("="*70)

    for rank, rec in enumerate(results, 1):
        song, score, reasons = rec
        print(f"\n#{rank} - {song['title']} by {song['artist']}")
        print(f"    Score: {score:.1f}/100")
        print("    Why:")
        for reason in reasons:
            print(f"      • {reason}")
        print("-" * 70)


def main():
    songs = load_songs("data/songs.csv")

    # Profile 1: Chill Lofi
    print("\n\n" + "█"*70)
    print(" PROFILE: Chill Lofi Listener".center(70))
    print("█"*70)
    chill_prefs = {
        "genre": "lofi", "mood": "chill",
        "energy": 0.40, "tempo_bpm": 78,
        "valence": 0.60, "danceability": 0.47,
        "acousticness": 0.80, "instrumentalness": 0.65,
        "liveness": 0.05,
    }
    print_results(run_agent(chill_prefs, songs))

    # Profile 2: High Energy Pop
    print("\n\n" + "█"*70)
    print(" PROFILE: High Energy Pop Fan".center(70))
    print("█"*70)
    pop_prefs = {
        "genre": "pop", "mood": "happy",
        "energy": 0.90, "tempo_bpm": 128,
        "valence": 0.85, "danceability": 0.88,
        "acousticness": 0.05, "instrumentalness": 0.01,
        "liveness": 0.10,
    }
    print_results(run_agent(pop_prefs, songs))

    # Profile 3: Adversarial (impossible preferences)
    print("\n\n" + "█"*70)
    print(" PROFILE: Adversarial (Edge Case)".center(70))
    print("█"*70)
    adversarial = {
        "genre": "metal", "mood": "aggressive",
        "energy": 1.0, "tempo_bpm": 210,
        "valence": 0.0, "danceability": 1.0,
        "acousticness": 0.0, "instrumentalness": 0.5,
        "liveness": 1.0,
    }
    print_results(run_agent(adversarial, songs))


if __name__ == "__main__":
    main()
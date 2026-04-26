# 🃏 Model Card — VibeFinder 1.0

## Model Name
VibeFinder 1.0 — Agentic Music Recommender Simulation

## Goal / Task
Suggest the top 5 songs from a catalog that best match a user's musical taste profile, using a weighted scoring algorithm. The agent monitors result quality and retries with adjusted preferences if confidence is low.

## Data Used
- **Source:** `data/songs.csv` (manually curated)
- **Size:** 18 songs
- **Features:** genre, mood, energy, tempo_bpm, valence, danceability, acousticness, instrumentalness, liveness
- **Limits:** Small dataset; pop and lofi genres are overrepresented (6 of 18 songs)

## Algorithm Summary
1. For each song, calculate a score out of ~100 points:
   - +12.5 for genre match
   - +15.0 for mood match
   - Up to 16 points for energy similarity (closest = full points)
   - Up to 8 points each for acousticness and instrumentalness
   - Smaller weights for valence, danceability, liveness, tempo
2. Sort all songs by score, return top 5
3. Agent checks if top score ≥ 60. If not, adjusts energy toward middle, then drops genre/mood filter, and retries up to 3 times.

## Observed Behavior / Biases
- **Genre dominance:** Even after halving genre weight to 12.5, genre match still heavily influences rankings because mood match adds another 15 points — songs matching both genre and mood almost always win.
- **Filter bubble:** With only 18 songs, users with niche preferences (metal, blues) get poor results since the dataset has only 1–2 songs per genre.
- **Adversarial failure:** Profiles with impossible preferences (tempo > 170 BPM, non-existent moods) always score below threshold. The reflect mechanism cannot fix what the data doesn't contain.

## Evaluation Process
Tested with 3 distinct user profiles:
- **Chill Lofi** — passed on iteration 1, top score 76.4
- **High Energy Pop** — passed on iteration 1, top score 75.0
- **Adversarial Edge Case** — failed all 3 iterations, top score 37.4

The adversarial profile correctly demonstrated that the agent honestly reports low confidence rather than returning misleading results.

**EDM vs Acoustic comparison:** A high-energy electronic profile (energy: 0.9, acousticness: 0.05) ranked Digital Tension and Gym Hero at top. An acoustic profile (energy: 0.35, acousticness: 0.90) ranked Library Rain and Spacewalk Thoughts at top. This confirms the energy and acousticness features are working correctly to differentiate musical vibes.

## Intended Use
- Educational simulation to demonstrate content-based filtering and agentic AI patterns
- Portfolio project showing AI system design with evaluation loops

## Non-Intended Use
- Not suitable as a real music recommendation platform
- Should not be used with real user listening data without privacy review
- Not designed for production deployment

## Ideas for Improvement
1. **Expand the dataset** to 100+ songs across all genres to reduce filter bubbles
2. **Add collaborative filtering** — incorporate what similar users liked
3. **Dynamic threshold** — adjust the 60-point threshold based on dataset size and genre coverage
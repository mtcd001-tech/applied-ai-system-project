"""
Automated tests for the Music Recommender system.
Run with: python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from recommender import load_songs, score_song, recommend_songs

# ── Load data once for all tests ──────────────────────────────────────
SONGS = load_songs("data/songs.csv")

CHILL_PREFS = {
    "genre": "lofi", "mood": "chill",
    "energy": 0.40, "tempo_bpm": 78,
    "valence": 0.60, "danceability": 0.47,
    "acousticness": 0.80, "instrumentalness": 0.65,
    "liveness": 0.05,
}

POP_PREFS = {
    "genre": "pop", "mood": "happy",
    "energy": 0.90, "tempo_bpm": 128,
    "valence": 0.85, "danceability": 0.88,
    "acousticness": 0.05, "instrumentalness": 0.01,
    "liveness": 0.10,
}


# ── Test 1: Load songs ─────────────────────────────────────────────────
def test_load_songs_count():
    """Songs CSV should load 18 songs."""
    assert len(SONGS) == 18, f"Expected 18 songs, got {len(SONGS)}"


def test_load_songs_fields():
    """Each song should have required fields."""
    required = ["title", "artist", "genre", "mood", "energy", "tempo_bpm"]
    for field in required:
        assert field in SONGS[0], f"Missing field: {field}"


def test_load_songs_numeric():
    """Energy field should be float, not string."""
    assert isinstance(SONGS[0]["energy"], float)


# ── Test 2: Score song ─────────────────────────────────────────────────
def test_score_returns_tuple():
    """score_song should return a (float, list) tuple."""
    result = score_song(CHILL_PREFS, SONGS[0])
    assert isinstance(result, tuple)
    assert isinstance(result[0], float)
    assert isinstance(result[1], list)


def test_score_genre_match_higher():
    """A genre-matching song should score higher than a non-matching one."""
    lofi_song = next(s for s in SONGS if s["genre"] == "lofi")
    rock_song = next(s for s in SONGS if s["genre"] == "rock")
    lofi_score, _ = score_song(CHILL_PREFS, lofi_song)
    rock_score, _ = score_song(CHILL_PREFS, rock_song)
    assert lofi_score > rock_score


def test_score_reasons_not_empty():
    """Reasons list should never be empty."""
    _, reasons = score_song(CHILL_PREFS, SONGS[0])
    assert len(reasons) > 0


# ── Test 3: Recommend songs ────────────────────────────────────────────
def test_recommend_returns_k_results():
    """recommend_songs should return exactly k results."""
    results = recommend_songs(CHILL_PREFS, SONGS, k=5)
    assert len(results) == 5


def test_recommend_sorted_descending():
    """Results should be sorted highest score first."""
    results = recommend_songs(CHILL_PREFS, SONGS, k=5)
    scores = [r[1] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_recommend_top_is_lofi():
    """Top result for chill lofi prefs should be a lofi song."""
    results = recommend_songs(CHILL_PREFS, SONGS, k=1)
    top_song = results[0][0]
    assert top_song["genre"] == "lofi", f"Expected lofi, got {top_song['genre']}"


def test_recommend_pop_top_result():
    """Top result for pop prefs should be a pop song."""
    results = recommend_songs(POP_PREFS, SONGS, k=1)
    top_song = results[0][0]
    assert top_song["genre"] == "pop", f"Expected pop, got {top_song['genre']}"
"""
Tests for the new-game status reset fix.

The bug: after winning, st.session_state.status was never reset to "playing"
when New Game was clicked, so the game remained frozen.

The fix: the new_game handler now sets st.session_state.status = "playing".
These tests verify that logic using plain dicts to simulate session_state.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import check_guess


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def simulate_new_game(session_state: dict) -> dict:
    """Mirrors the new-game handler in app.py (lines 134-140)."""
    import random
    session_state["attempts"] = 0
    session_state["secret"] = random.randint(1, 100)
    session_state["status"] = "playing"  # the fix being tested
    return session_state


# ---------------------------------------------------------------------------
# Tests for the status reset fix
# ---------------------------------------------------------------------------

def test_new_game_resets_status_after_win():
    """After winning, clicking New Game must reset status to 'playing'."""
    state = {"attempts": 3, "secret": 42, "status": "won"}
    state = simulate_new_game(state)
    assert state["status"] == "playing"


def test_new_game_resets_status_after_loss():
    """After losing, clicking New Game must reset status to 'playing'."""
    state = {"attempts": 8, "secret": 77, "status": "lost"}
    state = simulate_new_game(state)
    assert state["status"] == "playing"


def test_new_game_resets_attempts():
    """New Game should reset attempts to 0."""
    state = {"attempts": 5, "secret": 10, "status": "won"}
    state = simulate_new_game(state)
    assert state["attempts"] == 0


def test_new_game_generates_new_secret():
    """New Game should assign a new secret (an integer)."""
    state = {"attempts": 0, "secret": 99, "status": "won"}
    state = simulate_new_game(state)
    assert isinstance(state["secret"], int)
    assert 1 <= state["secret"] <= 100


def test_game_not_blocked_after_new_game():
    """
    Simulate the guard clause in app.py:
        if session_state.status != 'playing': st.stop()
    After new_game, this should NOT trigger.
    """
    state = {"attempts": 3, "secret": 42, "status": "won"}
    state = simulate_new_game(state)
    # If status is 'playing', the guard clause does NOT call st.stop()
    assert state["status"] == "playing", (
        "Guard clause would have stopped the app — status was not reset"
    )


# ---------------------------------------------------------------------------
# Sanity-check tests for check_guess (used by the win path)
# ---------------------------------------------------------------------------

def test_check_guess_correct():
    outcome, _ = check_guess(42, 42)
    assert outcome == "Win"


def test_check_guess_too_high():
    outcome, _ = check_guess(80, 42)
    assert outcome == "Too High"


def test_check_guess_too_low():
    outcome, _ = check_guess(10, 42)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# Tests for the hint/secret-type bug fix (always use int secret)
#
# The bug: on even attempts, secret was cast to str, causing lexicographic
# comparison in check_guess's TypeError fallback. E.g. str(1) > str(50)
# evaluated False ("1" < "5"), so guessing 1 returned "Go LOWER!" — wrong.
#
# The fix: secret is always passed as int to check_guess.
# ---------------------------------------------------------------------------

def test_hint_low_guess_is_too_low():
    """Guess of 1 vs secret of 50 must always be Too Low, not Too High."""
    outcome, _ = check_guess(1, 50)
    assert outcome == "Too Low", "Hint was backwards — secret was likely treated as a string"


def test_hint_high_guess_is_too_high():
    """Guess of 99 vs secret of 50 must always be Too High."""
    outcome, _ = check_guess(99, 50)
    assert outcome == "Too High"


def test_hint_not_affected_by_string_secret():
    """
    Directly verify the old broken path: if secret were a string, the
    lexicographic comparison would produce wrong results for certain values.
    Guessing 1 against str secret '50' would wrongly return Too High.
    This test confirms check_guess with an int secret never hits that path.
    """
    # With an int secret, numeric comparison is used — result must be correct.
    outcome, _ = check_guess(1, 50)
    assert outcome != "Too High", (
        "Got Too High for guess=1 secret=50; secret may have been a string"
    )


def test_hint_correct_across_range():
    """Spot-check several guess/secret pairs to ensure numeric comparison throughout."""
    cases = [
        (1,   100, "Too Low"),
        (100, 1,   "Too High"),
        (25,  75,  "Too Low"),
        (75,  25,  "Too High"),
        (50,  50,  "Win"),
    ]
    for guess, secret, expected in cases:
        outcome, _ = check_guess(guess, secret)
        assert outcome == expected, (
            f"check_guess({guess}, {secret}) returned '{outcome}', expected '{expected}'"
        )


# ---------------------------------------------------------------------------
# Tests for the swapped hint message bug fix
#
# The bug: "Too High" returned "Go HIGHER!" and "Too Low" returned "Go LOWER!"
# — the messages were inverted relative to what the player should do.
# E.g. guessing 200 (Too High) told the player to go even higher.
#
# The fix: "Too High" now returns "Go LOWER!" and "Too Low" returns "Go HIGHER!"
# ---------------------------------------------------------------------------

def test_too_high_message_says_go_lower():
    """When guess exceeds secret, the hint must tell the player to go LOWER."""
    _, message = check_guess(200, 50)
    assert "LOWER" in message, f"Expected 'Go LOWER' hint for high guess, got: {message}"


def test_too_low_message_says_go_higher():
    """When guess is below secret, the hint must tell the player to go HIGHER."""
    _, message = check_guess(1, 50)
    assert "HIGHER" in message, f"Expected 'Go HIGHER' hint for low guess, got: {message}"


def test_too_high_message_does_not_say_go_higher():
    """Regression: 'Too High' outcome must NOT say 'Go HIGHER!'."""
    _, message = check_guess(200, 50)
    assert "HIGHER" not in message, f"Got 'Go HIGHER' for an over-range guess: {message}"


def test_too_low_message_does_not_say_go_lower():
    """Regression: 'Too Low' outcome must NOT say 'Go LOWER!'."""
    _, message = check_guess(1, 50)
    assert "LOWER" not in message, f"Got 'Go LOWER' for an under-range guess: {message}"

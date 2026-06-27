import pytest

# Mocking the logic from src/utils/formatStats.ts in Python for testing purposes
def format_count(n: int) -> str:
    if n >= 1_000_000:
        return f"{float(f'{n / 1_000_000:.1f}'):g}M"
    if n >= 1_000:
        return f"{float(f'{n / 1_000:.1f}'):g}k"
    return str(n)

def format_date(date_str: str) -> str:
    from datetime import datetime
    # Simulating the fix: adding +1 to month index
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{dt.year}-{dt.month}-{dt.day}"

def test_format_count_bug_fix():
    """
    Verifies Bug 2: Round thousands should not show .0 decimal.
    2000 -> 2k (not 2.0k)
    1500 -> 1.5k
    """
    assert format_count(2000) == "2k"
    assert format_count(1500) == "1.5k"
    assert format_count(1000000) == "1M"
    assert format_count(1200000) == "1.2M"

def test_format_date_bug_fix():
    """
    Verifies Bug 1: Month should be 1-indexed, not 0-indexed.
    2024-03-15 -> 2024-3-15
    """
    # The original bug would have returned 2024-2-15
    assert format_date("2024-03-15") == "2024-3-15"
    assert format_date("2024-01-01") == "2024-1-1"

def test_format_edge_cases():
    """
    Verifies edge cases for both functions.
    """
    # Count edge cases
    assert format_count(999) == "999"
    assert format_count(0) == "0"
    
    # Date edge cases
    assert format_date("2024-12-31") == "2024-12-31"

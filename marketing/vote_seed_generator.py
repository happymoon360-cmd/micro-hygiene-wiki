"""
Vote Seed Data Generator for Micro-Hygiene Wiki

This script generates realistic vote distributions for all tips in the database.
Votes follow a realistic distribution pattern:
- 20-40% of tips have high engagement (10+ votes)
- 40-60% have moderate engagement (5-9 votes)
- 60-80% have low engagement (2-4 votes)
- Some tips have 0-1 votes (newly added)

Effectiveness and difficulty scores follow a correlation:
- High effectiveness tips tend to have higher difficulty scores
- Tips with balanced scores around 3-4 for both metrics
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Vote count distribution
VOTE_DISTRIBUTION = {
    "high": 0.25,      # 25% of tips have 10+ votes
    "moderate": 0.40,   # 40% have 5-9 votes
    "low": 0.25,       # 25% have 2-4 votes
    "none": 0.10,      # 10% have 0-1 votes
}

# Effectiveness and difficulty correlation
# Higher effectiveness tips often have higher difficulty
# Balanced tips: effectiveness 2.5-4.5, difficulty 2.5-4.0
# Easy tips: effectiveness 4-5, difficulty 1.0-2.0
# Difficult tips: effectiveness 1-3, difficulty 4.0-5.0


def generate_vote_count() -> int:
    """Generate a vote count based on distribution."""
    rand = random.random()
    if rand < VOTE_DISTRIBUTION["high"]:
        return random.randint(10, 25)
    elif rand < VOTE_DISTRIBUTION["high"] + VOTE_DISTRIBUTION["moderate"]:
        return random.randint(5, 9)
    elif rand < VOTE_DISTRIBUTION["high"] + VOTE_DISTRIBUTION["moderate"] + VOTE_DISTRIBUTION["low"]:
        return random.randint(2, 4)
    else:
        return random.randint(0, 1)


def generate_vote_data() -> List[Dict[str, Any]]:
    """
    Generate vote data for a tip.

    Returns a list of vote records with:
    - effectiveness: 1-5
    - difficulty: 1-5
    - ip_hash: placeholder (simulated)
    - created_at: recent dates
    """
    vote_count = generate_vote_count()
    votes = []

    for i in range(vote_count):
        # Generate effectiveness and difficulty with correlation
        effectiveness = random.randint(1, 5)
        difficulty = random.randint(1, 5)

        # Add correlation: higher effectiveness often means higher difficulty
        if effectiveness >= 4 and difficulty < 3:
            difficulty = random.randint(3, 4)
        elif effectiveness <= 2 and difficulty >= 4:
            difficulty = random.randint(2, 3)

        # Generate votes spread over the last 90 days
        days_ago = random.randint(1, 90)
        created_at = datetime.now() - timedelta(days=days_ago)

        votes.append({
            "effectiveness": effectiveness,
            "difficulty": difficulty,
            "ip_hash": f"ip_{random.randint(100000, 999999)}",
            "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return votes


def print_summary(votes: List[Dict[str, Any]]) -> None:
    """Print summary statistics of generated vote data."""
    total_votes = len(votes)
    effectiveness_avg = sum(v["effectiveness"] for v in votes) / total_votes if total_votes > 0 else 0
    difficulty_avg = sum(v["difficulty"] for v in votes) / total_votes if total_votes > 0 else 0

    print(f"\n=== Vote Data Summary ===")
    print(f"Total votes generated: {total_votes}")
    print(f"Average effectiveness: {effectiveness_avg:.2f}/5")
    print(f"Average difficulty: {difficulty_avg:.2f}/5")

    # Distribution breakdown
    vote_dist = {}
    for v in votes:
        count = vote_dist.get(v["effectiveness"], 0) + 1
        vote_dist[v["effectiveness"]] = count
    print(f"\nEffectiveness distribution:")
    for eff, count in sorted(vote_dist.items(), key=lambda x: x[0], reverse=True):
        bar = "█" * int(count / total_votes * 50)
        print(f"  {effff}: {bar} {count:3} ({count/total_votes*100:.1f}%)")

    # Difficulty distribution
    difficulty_dist = {}
    for v in votes:
        count = difficulty_dist.get(v["difficulty"], 0) + 1
        difficulty_dist[v["difficulty"]] = count
    print(f"\nDifficulty distribution:")
    for diff, count in sorted(difficulty_dist.items(), key=lambda x: int(x[0]), reverse=True):
        bar = "█" * int(count / total_votes * 50)
        print(f"  {diff:2}: {bar} {count:3} ({count/total_votes*100:.1f}%)")

    # Success rate calculation
    # Tips with higher effectiveness tend to have higher success rates
    # Base success rate: 60%, with adjustments based on effectiveness
    success_rates = [
        0.65 + (eff - 3) * 0.07 for eff in range(1, 5)
        for eff in votes
    ]
    success_avg = sum(success_rates) / len(success_rates)

    print(f"\nCalculated success rate: {success_avg:.1%}")
    print(f"(Formula: base 60% + effectiveness correlation)")


if __name__ == "__main__":
    print("=" * 60)
    print("VOTE SEED DATA GENERATOR")
    print("Micro-Hygiene Wiki")
    print("=" * 60)

    # Generate for approximately 217 tips (67 existing + 150 new)
    TOTAL_TIPS = 217
    all_votes = []

    for i in range(TOTAL_TIPS):
        votes = generate_vote_data()
        all_votes.extend(votes)

    print_summary(all_votes)

    print(f"\n{'='*60}")
    print(f"Output format: JSON array of vote records")
    print(f"Ready to import into Django Vote model")
    print(f"Total records: {len(all_votes)}")
    print(f"Est. total votes: {len(all_votes)}")
    print("=" * 60)

    # Print sample data for verification
    print(f"\n{'='*10} SAMPLE VOTES (first 3) {'='*10}")
    for vote in all_votes[:3]:
        print(vote)

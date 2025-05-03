import math
from typing import List, Tuple, Dict
import enum

RATING_TIERS = (
    (math.inf, 3.7),
    (1010000, 3.7),
    (1009999, 3.6),
    (1008000, 3.4),
    (1004000, 2.4),
    (1000000, 2.0),
    (980000, 1.0),
    (950000, 0.0),
    (900000, -1.0),
    (800000, -2.0),
    (700000, -3.0),
    (600000, -4.0),
    (500000, -5.0),
    (0, -9999.0),
    (-math.inf, -9999.0),
)


class Difficulty(enum.IntEnum):
    I = enum.auto()
    II = enum.auto()
    III = enum.auto()
    IV = enum.auto()
    IV_alpha = enum.auto()


def get_all_level_v2_ratings(
        song: Dict[Difficulty, Tuple[int, float, bool]]) -> List[float]:
    if Difficulty.IV_alpha not in song:
        return [calculate_single(*charts) for charts in song.values()]

    iv_ratings: List[float] = [
        calculate_single(
            *song[Difficulty.IV]) if Difficulty.IV in song else 0.0,
        calculate_single(*song[Difficulty.IV_alpha])
        if Difficulty.IV_alpha in song else 0.0,
    ]

    charts_without_iv: List[Tuple[int, float, bool]] = [
        chart for difficulty, chart in song.items()
        if difficulty not in (Difficulty.IV, Difficulty.IV_alpha)
    ]
    return [calculate_single(*chart)
            for chart in charts_without_iv] + [max(iv_ratings)]


def calculate_single(score: int, innerDifficulty: float,
                     isCleared: bool) -> float:
    tier = len(RATING_TIERS) - 1
    for i in range(len(RATING_TIERS)):
        if RATING_TIERS[i][0] <= score:
            tier = i
            break

    l_score, l_bonus = RATING_TIERS[tier]
    h_score, h_bonus = RATING_TIERS[tier - 1]

    rating = l_bonus + innerDifficulty + (h_bonus - l_bonus) * (
        (score - l_score) / (h_score - l_score))

    rating = max(0, rating)
    if rating <= 6.0 or isCleared:
        return rating
    return 6.0


def calculate_player_rating(
        songs: List[Dict[Difficulty, Tuple[int, float, bool]]]) -> float:
    ratings: List[float] = []
    for song in songs:
        ratings.extend(get_all_level_v2_ratings(song))
    print(ratings)
    ratings.sort(reverse=True)

    first10_ratings = ratings[:10]
    second10_ratings = ratings[10:20]
    third20_ratings = ratings[20:40]

    total_rating = (sum(first10_ratings) / 10.0 * 0.6 +
                    sum(second10_ratings) / 10.0 * 0.2 +
                    sum(third20_ratings) / 20.0 * 0.2)
    return math.floor(total_rating * 1000) / 1000.0


if __name__ == "__main__":
    # Example usage
    example_songs = [
        {  # Suito
            Difficulty.I: (1010000, 5, True),  # 8.7
            Difficulty.II: (1010000, 9.3, True),  # 13.0
            Difficulty.III: (1009966, 12.4, True),  # 15.997
            Difficulty.IV: (1006900, 14.5, True),  # 17.625
        },
        {  # Heaven's Cage
            Difficulty.I: (1010000, 3, True),  # 6.7
            Difficulty.II: (1010000, 7, True),  # 10.7
            Difficulty.III: (1010000, 10.4, True),  # 14.1
            Difficulty.IV: (1009916, 13.1, True),  # 16.692
            Difficulty.IV_alpha: (1009925, 13.9, True),  # 17.493
        },
        {  # Alfheim's faith
            Difficulty.I: (1010000, 4, True),  # 7.7
            Difficulty.II: (1010000, 7, True),  # 10.7
            Difficulty.III: (1010000, 10.5, True),  # 14.2
            Difficulty.IV: (1010000, 12.5, True),  # 16.2
            Difficulty.IV_alpha: (0, 13.2, False),  # 0.0
        }
    ]
    print(calculate_player_rating(example_songs))  # Output: 8.610
    '''
    first 10: 17.625 17.493 16.2 15.997 14.2 14.1 13.0 10.7 10.7 8.7 --> 8.3228...
    second 10: 7.7 6.7 --> 0.288
    8.3228... + 0.288 = 8.6108... ==> 8.610
    8.610 is the final rating
    '''

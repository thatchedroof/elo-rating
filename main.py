#%%

import pandas as pd

from typing import cast, List, Dict, Type, Tuple

# %%

def expected_outcome(own_rating: float,
                     opponent_rating: float,
                     s: float
                     ) -> float:
    return 1 / (1 + 10 ** ((opponent_rating - own_rating) / s))

def new_rating(old_rating: float,
               actual_outcome: float,
               expected_outcome: float,
               k: float
               ) -> float:
    return old_rating + k * (actual_outcome - expected_outcome)

def elo(score_frame:    pd.DataFrame,
        k:              float,
        s:              float,
        initial_rating: float = 1000,
        rating_input:   Dict[str, float] = {}
        ) ->            Dict[str, float]:

    if score_frame.empty:
        return rating_input

    #assert type(tuple(score_frame.iloc[0])) is Tuple[str, str, int, str]

    winner, loser, score, platform = cast(Tuple[str, str, int, str],
                                          tuple(score_frame.iloc[0]))

    ratings = rating_input

    if winner not in rating_input.keys():
        ratings = {**ratings, winner: initial_rating}

    if loser not in rating_input.keys():
        ratings = {**ratings, loser: initial_rating}

    updated_winner = new_rating(
        old_rating = ratings[winner],
        actual_outcome = 1 - (score/10),
        expected_outcome = expected_outcome(
            own_rating = ratings[winner],
            opponent_rating = ratings[loser],
            s = s
        ),
        k = k
    )

    updated_loser = new_rating(
        old_rating = ratings[loser],
        actual_outcome = score/10,
        expected_outcome = expected_outcome(
            own_rating = ratings[loser],
            opponent_rating = ratings[winner],
            s = s
        ),
        k = k
    )

    updated_ratings = {
        **ratings,
        winner: updated_winner,
        loser: updated_loser
        }

    return elo(
        score_frame = score_frame.iloc[1:, :],
        k = k,
        s = s,
        initial_rating = initial_rating,
        rating_input = updated_ratings
    )

#%%

if __name__ == "__main__":

    scores = pd.read_csv('scores.csv')

    k = 50
    s = 400

    ratings = elo(
            score_frame = scores,
            k = k,
            s = s
        )

    #print(sum(ratings.values()))

    for key, value in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
        print(f'{key}: {int(value)}')

# %%

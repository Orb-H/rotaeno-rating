# Rotaeno Rating Calculator Logic

This repository contains the refined logic for calculating the player's rating. It follows the logic in **2.8.41** version.

## Terms

There are terms related to rating calculation, but here I introduce some terms for better understanding.

- `Chart`: A unique item which has score and difficulty value.
- `Song`: A single song. It can contain several charts, by difficulty.
- `Score`: The calculated score value of chart by playing it.
- `Rating`: This can indicate both of below:
  - Individual rating value, which is determined by the score and difficulty value of each chart.
  - Total rating value, which is calculated by the calculated individual rating values.
- `Difficulty` or `Difficulty Name`: The display name for difficulty of each chart. For example, `I`, `II`, `III`, `IV`, and `IV-α`.
- `Difficulty Value`: A float value which indicates the quantitative difficulty of each chart.
- `Bonus`: An additional value used for calculating the individual rating value. It is determined by the score value.

## Calculating the rating of a single chart

Rotaeno introduces the tiers and bonus values according to the score value as below:

|   Score Range   |   Bonus Range    | Slope(1e-6) |
| :-------------: | :--------------: | :---------: |
|     1010000     |      `+3.7`      |             |
| 1008000~1009999 |  `+3.4`~`+3.6`   |   100.05    |
| 1004000~1008000 |  `+2.4`~`+3.4`   |   **250**   |
| 1000000~1004000 |  `+2.0`~`+2.4`   |     100     |
| 980000~1000000  |  `+1.0`~`+2.0`   |     50      |
|  950000~980000  |  `±0.0`~`+1.0`   |    33.33    |
|  900000~950000  |  `-1.0`~`±0.0`   |     20      |
|  800000~900000  |  `-2.0`~`-1.0`   |     10      |
|  700000~800000  |  `-3.0`~`-2.0`   |     10      |
|  600000~700000  |  `-4.0`~`-3.0`   |     10      |
|  500000~600000  |  `-5.0`~`-4.0`   |     10      |
|    0~500000     | `-9999.0`~`-5.0` |    19988    |

Base of these tier values, the rating is calculated as below:

- For 1010000, `(Difficulty Value) + 3.7`
- For the score `s` in the range in `s1~s2`,
  - Let bonus range be `b1~b2`, then rating is `(Difficulty Value) + b1 + (s - s1) / (s2 - s1) * (b2 - b1)`.
  - In other words, rating is linear in each range.

After calculating the rating value, there are more post-processing steps as below:

- If the calculated value is negative, consider it as 0.
- If the player didn't clear the chart, rating value cannot exceed 6.0.

## Calculating the total rating

Now we know how to calculate the individual rating value. Based on these values, total rating is calculated as below:

1. Collect all the songs.
1. Collect score data according to the difficulty, by songs.
   - For difficulty IV and IV-α, pick the one with the higher rating value.
   - In other words, collected score data contains I, II, III, and the higher value between IV and IV-α.
1. Sort the rating values in a descending order. (Higher first)
1. Pick the first 40 of them and calculate the rating as below:
   ```
     (Sum of first 10 ratings) / 10.0 * 0.6
   + (Sum of next 10 ratings) / 10.0 * 0.2
   + (Sum of last 20 ratings) / 20.0 * 0.2
   ```
1. Finally, keep three digits after decimal point and truncate the rest.

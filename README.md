# Rotaeno Rating Calculator Logic

[Korean](https://github.com/Orb-H/rotaeno-rating/blob/main/README_ko.md)

This repository contains the refined logic for calculating the player's rating. It follows the logic in **2.8.41** version.

## Terms

I introduce some terms to use in this page. Some of them could have different meanings from the common ones.

- **Chart**: A unique item which exists by the song and the difficulty. It consists of play result including score.
- **Song**: A single song. It contains several charts by difficulty.
- **Score**: The calculated score value of chart by playing it.
- **Rating**: This can indicate either of below:
  - **Chart Rating** or **Individual Rating** is determined by the score and difficulty value of each chart.
  - **Total Rating** or **Rating** is calculated with the individual rating values through a specific formula.
- **Difficulty**: The display name for difficulty of each chart. It is one of `I`, `II`, `III`, `IV`, and `IV-α`.
- **Chart Constant** or **Inner Difficulty**: A float value which indicates the quantitative difficulty of each chart. For example, the highest value is **14.5** from 翠杜(Suito).
- **Bonus**: An additional value used for calculating the individual rating value. It is determined by the score.

## Calculating the chart rating value

Rotaeno introduces the tiers and bonus values according to the score value as below:

|     Score Range     |   Bonus Range    | Slope(1e-6) |
| :-----------------: | :--------------: | :---------: |
|      `1010000`      |      `+3.7`      |             |
| `1008000`~`1009999` |  `+3.4`~`+3.6`   |   100.05    |
| `1004000`~`1008000` |  `+2.4`~`+3.4`   |   **250**   |
| `1000000`~`1004000` |  `+2.0`~`+2.4`   |     100     |
| ` 980000`~`1000000` |  `+1.0`~`+2.0`   |     50      |
| ` 950000`~` 980000` |  `±0.0`~`+1.0`   |    33.33    |
| ` 900000`~` 950000` |  `-1.0`~`±0.0`   |     20      |
| ` 800000`~` 900000` |  `-2.0`~`-1.0`   |     10      |
| ` 700000`~` 800000` |  `-3.0`~`-2.0`   |     10      |
| ` 600000`~` 700000` |  `-4.0`~`-3.0`   |     10      |
| ` 500000`~` 600000` |  `-5.0`~`-4.0`   |     10      |
| `      0`~` 500000` | `-9999.0`~`-5.0` |    19988    |

Base of these tier values, the rating is calculated as below:

- For pure perfect, (1010000)
  $$(Chart\  Constant) + 3.7$$
- For the score $s$ in the score range in $s_1~s_2$ and bonus range in $b_1~b_2$,
  $$(Chart\ Constant)+b_1+(b_2-b_1)\times\frac{s-s_1}{s_2-s_1}$$

After calculating the rating value, there are more post-processing steps as below:

- If the calculated value is negative, consider it as 0.
- If the player didn't clear the chart, rating value cannot exceed 6.0.

## Calculating the total rating

Now we know how to calculate the individual rating value. Based on these values, total rating is calculated as below:

1. Collect all the charts from each song.
1. Collect score data from each song, according to the rule below.
   - Collect `I`, `II`, and `III` charts.
   - If both `IV` and `IV-α` exist, pick the one with the higher chart rating value.
1. Sort the chart rating values in a descending order. (Higher first)
1. Pick the first 40 of them and calculate the rating as below: ($c_i$ is the chart rating of $i$-th chart)
   $$
   \frac{c_1+...+c_{10}}{10}\times0.6+\frac{c_{11}+...+c_{20}}{10}\times0.2+\frac{c_{21}+...+c_{40}}{20}\times0.2
   $$
1. Finally, keep three digits after decimal point and truncate the rest.

# 🏆 FIFA World Cup 2026 Statistical Predictor

A Python-based statistical simulation of the **2026 FIFA World Cup** (the expanded 48-team tournament hosted by the USA, Canada, and Mexico). The predictor uses a combination of historical match data (from 1970 to 2022) and the official **June 11, 2026 FIFA World Rankings** to run a **20,000-trial Monte Carlo simulation** of the entire tournament structure.

---

## 📁 Repository Structure

* `data/`
  * `fifa_wc_mens_match_dataset_1970_2022.csv`: The historical match dataset used to calibrate goal-scoring rates and compute team pedigree.
* `simulate_wc.py`: The main simulation script. Runs 20,000 simulated World Cups, ranks groups using official tiebreakers, pairs third-placed teams, runs knockout stages, and outputs `predictions.csv`.
* `calculate_stats.py`: Calculates historical World Cup aggregates (win rate, average goals scored, and conceded) for all countries.
* `fit_poisson.py`: Performs a Poisson regression on historical matches to optimize goal-scoring coefficients.
* `predictions.csv`: The generated output table containing the probability of every team reaching each stage.
* `.gitignore`: Excludes Python cache and temporary files.
* `README.md`: This file.

---

## 📊 Methodology & Modeling

Matches are simulated using a **Poisson goal-scoring distribution** driven by team strength:

1. **Composite Rating ($R$)**:
   * **Modern Strength (80% weight)**: Calibrated from the latest June 2026 FIFA Coca-Cola rankings. FIFA points are interpolated across a continuous curve.
   * **Historical Pedigree (20% weight)**: Based on the average goal difference per match from World Cups between 1970 and 2022.
   * **Standardization**: Both components are converted to $Z$-scores and standardized so that the final rating $R$ has a mean of $0.0$ and a standard deviation of $1.0$ across the 48 teams.

2. **Goal Expectancy (Poisson Regression)**:
   * Goal expectation parameters $\lambda_A$ and $\lambda_B$ are calculated using the optimized coefficients from `fit_poisson.py`:
     $$\lambda_A = 1.2632 \times e^{0.25 \times (R_A - R_B)}$$
     $$\lambda_B = 1.2632 \times e^{0.25 \times (R_B - R_A)}$$
     * *Note*: $1.2632$ represents the average goals scored per team in a World Cup match since 1970.
   * Knockout draws are resolved through a 30-minute extra time simulation ($\lambda_{ET} = \lambda / 3$), followed by a penalty shootout with probabilities slightly adjusted by team ratings ($0.50 + 0.05 \times (R_A - R_B)$).

3. **Tournament Rules**:
   * Simulates all 12 groups (A to L) of 4 teams.
   * Applies official group tiebreakers: Points $\rightarrow$ Goal Difference $\rightarrow$ Goals Scored $\rightarrow$ Wins $\rightarrow$ Rating.
   * Implements a backtracking bipartite matching algorithm to dynamically pair the 8 best third-placed teams to their Round of 32 opponents in compliance with the Annex C regulations.
   * Tracks progression through the Round of 32, Round of 16, Quarterfinals, Semifinals, Third Place match, and Final.

---

## 🚀 How to Run

This project runs using **only standard Python libraries** (no external packages like `numpy` or `pandas` are required).

### Prerequisite
* Python 3.x

### Executing the Simulation
To run the 20,000-trial simulation and regenerate `predictions.csv`, execute:
```bash
python simulate_wc.py
```

To run the Poisson parameter optimization:
```bash
python fit_poisson.py
```

To calculate the historical statistics of countries in past World Cups:
```bash
python calculate_stats.py
```

---

## 🔮 Predictions (Top 15 Contenders)

Based on a 20,000-trial simulation run, here are the top 15 contenders to win the 2026 World Cup:

| Rank | Team | Group | FIFA Rank | Advance Group % | Reach QF % | Reach Final % | Win World Cup % |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **France** | I | 3 | 96.67% | 55.34% | 28.57% | **16.98%** |
| 2 | **Argentina** | J | 1 | 97.17% | 45.97% | 18.34% | **12.12%** |
| 3 | **Spain** | H | 2 | 98.33% | 46.73% | 18.44% | **11.74%** |
| 4 | **England** | L | 4 | 96.85% | 45.09% | 15.62% | **9.20%** |
| 5 | **Brazil** | C | 6 | 97.20% | 43.03% | 12.72% | **6.68%** |
| 6 | **Germany** | E | 10 | 94.48% | 34.86% | 11.51% | **5.24%** |
| 7 | **Netherlands** | F | 8 | 91.14% | 34.85% | 10.37% | **5.00%** |
| 8 | **Belgium** | G | 9 | 94.33% | 36.34% | 9.32% | **4.34%** |
| 9 | **Portugal** | K | 5 | 94.50% | 30.96% | 7.80% | **4.21%** |
| 10 | **Morocco** | C | 7 | 95.01% | 35.53% | 8.84% | **4.00%** |
| 11 | **Croatia** | L | 11 | 90.81% | 26.62% | 5.53% | **2.61%** |
| 12 | **Senegal** | I | 15 | 79.82% | 25.85% | 5.85% | **2.20%** |
| 13 | **Colombia** | K | 13 | 90.72% | 22.69% | 4.47% | **2.11%** |
| 14 | **Mexico** | A | 14 | 88.74% | 25.25% | 4.53% | **1.91%** |
| 15 | **Switzerland** | B | 19 | 90.11% | 25.79% | 4.90% | **1.79%** |

*Note: Probabilities are subject to statistical fluctuations within $\pm 0.35\%$ margin of error.*

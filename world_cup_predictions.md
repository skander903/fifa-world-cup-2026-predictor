# 🏆 2026 FIFA World Cup Predictions & Statistical Analysis

This report presents a comprehensive statistical prediction of the **2026 FIFA World Cup** using historical match data (from 1970 to 2022) combined with modern FIFA rankings to run a **20,000-trial Monte Carlo simulation** of the entire tournament structure.

---

## 📊 Methodology & Logical Framework

To predict the outcome of every team, we built a composite rating system and simulated matches using a Poisson regression goal-scoring model:

1. **Composite Rating ($R$)**:
   - **Modern Strength (80% weight)**: Based on the latest **June 11, 2026 FIFA Coca-Cola Men's World Rankings**. FIFA points are dynamically mapped to a continuous point scale.
   - **Historical Pedigree (20% weight)**: Based on historical World Cup goal difference per match from the 1970–2022 dataset. This captures tournament culture and pedigree.
   - **Standardization**: Both metrics are standardized ($Z$-scores) and combined. The final rating $R$ is standardized to have a mean of $0$ and a standard deviation of $1$ across the 48 teams.

2. **Match Simulation Model**:
   - Matches are simulated using a **Poisson goal-scoring distribution**.
   - Expected goals for Team A ($\lambda_A$) and Team B ($\lambda_B$) are modeled as:
     $$\lambda_A = 1.2632 \times e^{0.25 \times (R_A - R_B)}$$
     $$\lambda_B = 1.2632 \times e^{0.25 \times (R_B - R_A)}$$
     - *Note*: $1.2632$ is the historical average number of goals scored by a team in World Cup matches, calibrated from the dataset.
     - The scaling factor of $0.25$ is calibrated from historical matches.
   - In knockout stages, if a match ends in a draw, extra time is simulated using the same Poisson model scaled down to 30 minutes ($\lambda / 3$). If still tied, a penalty shootout is simulated with a win probability slightly biased by the team ratings ($0.50 + 0.05 \times (R_A - R_B)$).

3. **Tournament Rules**:
   - Complete group stage simulation of 12 groups (A to L) of 4 teams.
   - Exact tiebreakers: Points $\rightarrow$ Goal Difference $\rightarrow$ Goals Scored $\rightarrow$ Wins $\rightarrow$ Rating.
   - Bipartite matching algorithm to dynamically pair the 8 best third-placed teams to their Round of 32 opponents according to the 2026 FIFA Regulations.
   - Full knockout bracket progression from the Round of 32 to the Final.

---

## 🥇 Global Prediction Standings (Full 48-Team Table)

The table below lists all 48 qualified nations sorted by their probability of winning the 2026 FIFA World Cup, along with their probabilities of reaching key knockout stages.

| Rank | Team | Group | FIFA Rank | Composite Rating | Advance Group % | Reach R16 % | Reach QF % | Reach SF % | Reach Final % | Win World Cup % |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **France** | I | 3 | +1.87 | 96.69% | 75.39% | 55.16% | 39.62% | 28.27% | **16.66%** |
| 2 | **Spain** | H | 2 | +1.88 | 98.31% | 70.49% | 47.66% | 29.93% | 19.55% | **12.35%** |
| 3 | **Argentina** | J | 1 | +1.85 | 97.08% | 67.59% | 46.54% | 28.39% | 18.05% | **11.36%** |
| 4 | **England** | L | 4 | +1.58 | 96.95% | 70.52% | 44.80% | 27.76% | 15.05% | **8.94%** |
| 5 | **Brazil** | C | 6 | +1.32 | 96.88% | 61.77% | 42.26% | 23.23% | 12.70% | **6.51%** |
| 6 | **Germany** | E | 10 | +1.16 | 94.64% | 62.20% | 34.80% | 20.96% | 11.80% | **5.38%** |
| 7 | **Netherlands** | F | 8 | +1.19 | 91.21% | 51.74% | 35.30% | 18.54% | 10.28% | **5.00%** |
| 8 | **Belgium** | G | 9 | +1.04 | 94.18% | 64.03% | 36.68% | 21.01% | 9.57% | **4.54%** |
| 9 | **Morocco** | C | 7 | +1.00 | 95.36% | 55.69% | 35.81% | 18.23% | 9.17% | **4.28%** |
| 10 | **Portugal** | K | 5 | +1.21 | 94.53% | 61.77% | 30.93% | 15.50% | 8.07% | **4.25%** |
| 11 | **Croatia** | L | 11 | +0.89 | 90.66% | 53.91% | 26.49% | 12.45% | 5.23% | **2.62%** |
| 12 | **Senegal** | I | 15 | +0.64 | 80.53% | 46.35% | 25.41% | 13.72% | 5.67% | **2.05%** |
| 13 | **Mexico** | A | 14 | +0.64 | 88.07% | 53.92% | 24.70% | 10.92% | 4.35% | **1.97%** |
| 14 | **Colombia** | K | 13 | +0.82 | 90.83% | 51.14% | 22.16% | 9.20% | 4.21% | **1.92%** |
| 15 | **Switzerland** | B | 19 | +0.42 | 90.23% | 52.09% | 25.34% | 11.58% | 4.99% | **1.71%** |
| 16 | **United States** | D | 17 | +0.47 | 79.58% | 45.27% | 22.43% | 11.43% | 4.50% | **1.62%** |
| 17 | **Japan** | F | 18 | +0.46 | 78.57% | 34.64% | 18.98% | 8.15% | 3.35% | **1.21%** |
| 18 | **Türkiye** | D | 22 | +0.34 | 76.28% | 40.80% | 19.30% | 9.14% | 3.55% | **1.11%** |
| 19 | **Uruguay** | H | 16 | +0.53 | 86.04% | 36.63% | 16.86% | 5.97% | 2.46% | **1.05%** |
| 20 | **Ecuador** | E | 23 | +0.19 | 80.84% | 38.77% | 17.10% | 7.88% | 2.89% | **0.92%** |
| 21 | **Iran** | G | 20 | +0.14 | 80.55% | 41.05% | 18.82% | 7.85% | 2.54% | **0.82%** |
| 22 | **South Korea** | A | 25 | +0.00 | 74.92% | 38.41% | 13.35% | 4.61% | 1.52% | **0.51%** |
| 23 | **Australia** | D | 27 | -0.10 | 63.14% | 27.73% | 11.27% | 4.46% | 1.29% | **0.40%** |
| 24 | **Egypt** | G | 29 | -0.18 | 72.08% | 32.98% | 13.13% | 5.03% | 1.44% | **0.40%** |
| 25 | **Ivory Coast** | E | 33 | -0.16 | 70.75% | 29.25% | 11.07% | 4.24% | 1.26% | **0.36%** |
| 26 | **Austria** | J | 24 | +0.12 | 69.55% | 25.62% | 10.22% | 3.43% | 1.11% | **0.34%** |
| 27 | **Norway** | I | 31 | -0.08 | 58.97% | 26.14% | 10.58% | 4.26% | 1.22% | **0.27%** |
| 28 | **Canada** | B | 30 | -0.39 | 73.57% | 31.10% | 10.50% | 3.20% | 1.05% | **0.25%** |
| 29 | **Algeria** | J | 28 | -0.08 | 63.00% | 21.23% | 7.80% | 2.50% | 0.71% | **0.23%** |
| 30 | **Sweden** | F | 38 | -0.27 | 55.92% | 18.90% | 7.39% | 2.41% | 0.68% | **0.21%** |
| 31 | **Scotland** | C | 42 | -0.43 | 67.56% | 22.91% | 7.88% | 2.25% | 0.71% | **0.17%** |
| 32 | **Czech Republic** | A | 40 | -0.40 | 63.14% | 27.10% | 7.89% | 2.10% | 0.56% | **0.14%** |
| 33 | **Paraguay** | D | 41 | -0.40 | 53.89% | 20.49% | 7.66% | 2.60% | 0.68% | **0.14%** |
| 34 | **Tunisia** | F | 45 | -0.64 | 43.58% | 12.28% | 4.12% | 1.10% | 0.25% | **0.06%** |
| 35 | **South Africa** | A | 60 | -0.90 | 44.94% | 15.71% | 3.40% | 0.77% | 0.19% | **0.06%** |
| 36 | **Bosnia and Herzegovina** | B | 64 | -0.93 | 56.59% | 19.09% | 4.92% | 1.17% | 0.27% | **0.05%** |
| 37 | **Uzbekistan** | K | 50 | -0.62 | 52.95% | 14.32% | 3.96% | 0.97% | 0.22% | **0.04%** |
| 38 | **Panama** | L | 34 | -0.75 | 45.86% | 13.36% | 2.73% | 0.48% | 0.11% | **0.03%** |
| 39 | **Qatar** | B | 56 | -1.11 | 49.89% | 15.01% | 3.32% | 0.76% | 0.10% | **0.02%** |
| 40 | **Jordan** | J | 63 | -0.90 | 33.45% | 7.80% | 1.97% | 0.41% | 0.07% | **0.01%** |
| 41 | **Saudi Arabia** | H | 61 | -1.14 | 34.30% | 6.68% | 1.46% | 0.27% | 0.06% | **0.01%** |
| 42 | **Curaçao** | E | 82 | -1.55 | 23.15% | 4.92% | 0.92% | 0.17% | 0.04% | **0.01%** |
| 43 | **Iraq** | I | 57 | -0.94 | 28.77% | 8.82% | 2.41% | 0.63% | 0.11% | **0.01%** |
| 44 | **Cape Verde** | H | 67 | -1.04 | 38.20% | 8.00% | 1.67% | 0.36% | 0.03% | **0.01%** |
| 45 | **Ghana** | L | 73 | -1.31 | 26.35% | 5.49% | 0.83% | 0.11% | 0.03% | **0.00%** |
| 46 | **DR Congo** | K | 46 | -1.42 | 25.63% | 4.45% | 0.86% | 0.10% | 0.01% | **0.00%** |
| 47 | **New Zealand** | G | 85 | -1.66 | 23.14% | 5.35% | 1.05% | 0.18% | 0.02% | **0.00%** |
| 48 | **Haiti** | C | 83 | -2.37 | 8.70% | 1.08% | 0.13% | 0.02% | 0.01% | **0.00%** |

---

## 📦 Detailed Group-by-Group Predictions

Below is the probability breakdown for each team to advance from their respective groups. In the 2026 format, the top two teams in each group and the eight best third-placed teams advance.

### Group A

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Mexico** | 14 | +0.64 | 88.07% | 53.92% | 24.70% | **1.97%** |
| **South Korea** | 25 | +0.00 | 74.92% | 38.41% | 13.35% | **0.51%** |
| **Czech Republic** | 40 | -0.40 | 63.14% | 27.10% | 7.89% | **0.14%** |
| **South Africa** | 60 | -0.90 | 44.94% | 15.71% | 3.40% | **0.06%** |

### Group B

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Switzerland** | 19 | +0.42 | 90.23% | 52.09% | 25.34% | **1.71%** |
| **Canada** | 30 | -0.39 | 73.57% | 31.10% | 10.50% | **0.25%** |
| **Bosnia and Herzegovina** | 64 | -0.93 | 56.59% | 19.09% | 4.92% | **0.05%** |
| **Qatar** | 56 | -1.11 | 49.89% | 15.01% | 3.32% | **0.02%** |

### Group C

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Brazil** | 6 | +1.32 | 96.88% | 61.77% | 42.26% | **6.51%** |
| **Morocco** | 7 | +1.00 | 95.36% | 55.69% | 35.81% | **4.28%** |
| **Scotland** | 42 | -0.43 | 67.56% | 22.91% | 7.88% | **0.17%** |
| **Haiti** | 83 | -2.37 | 8.70% | 1.08% | 0.13% | **0.00%** |

### Group D

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **United States** | 17 | +0.47 | 79.58% | 45.27% | 22.43% | **1.62%** |
| **Türkiye** | 22 | +0.34 | 76.28% | 40.80% | 19.30% | **1.11%** |
| **Australia** | 27 | -0.10 | 63.14% | 27.73% | 11.27% | **0.40%** |
| **Paraguay** | 41 | -0.40 | 53.89% | 20.49% | 7.66% | **0.14%** |

### Group E

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Germany** | 10 | +1.16 | 94.64% | 62.20% | 34.80% | **5.38%** |
| **Ecuador** | 23 | +0.19 | 80.84% | 38.77% | 17.10% | **0.92%** |
| **Ivory Coast** | 33 | -0.16 | 70.75% | 29.25% | 11.07% | **0.36%** |
| **Curaçao** | 82 | -1.55 | 23.15% | 4.92% | 0.92% | **0.01%** |

### Group F

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Netherlands** | 8 | +1.19 | 91.21% | 51.74% | 35.30% | **5.00%** |
| **Japan** | 18 | +0.46 | 78.57% | 34.64% | 18.98% | **1.21%** |
| **Sweden** | 38 | -0.27 | 55.92% | 18.90% | 7.39% | **0.21%** |
| **Tunisia** | 45 | -0.64 | 43.58% | 12.28% | 4.12% | **0.06%** |

### Group G

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Belgium** | 9 | +1.04 | 94.18% | 64.03% | 36.68% | **4.54%** |
| **Iran** | 20 | +0.14 | 80.55% | 41.05% | 18.82% | **0.82%** |
| **Egypt** | 29 | -0.18 | 72.08% | 32.98% | 13.13% | **0.40%** |
| **New Zealand** | 85 | -1.66 | 23.14% | 5.35% | 1.05% | **0.00%** |

### Group H

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Spain** | 2 | +1.88 | 98.31% | 70.49% | 47.66% | **12.35%** |
| **Uruguay** | 16 | +0.53 | 86.04% | 36.63% | 16.86% | **1.05%** |
| **Cape Verde** | 67 | -1.04 | 38.20% | 8.00% | 1.67% | **0.01%** |
| **Saudi Arabia** | 61 | -1.14 | 34.30% | 6.68% | 1.46% | **0.01%** |

### Group I

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **France** | 3 | +1.87 | 96.69% | 75.39% | 55.16% | **16.66%** |
| **Senegal** | 15 | +0.64 | 80.53% | 46.35% | 25.41% | **2.05%** |
| **Norway** | 31 | -0.08 | 58.97% | 26.14% | 10.58% | **0.27%** |
| **Iraq** | 57 | -0.94 | 28.77% | 8.82% | 2.41% | **0.01%** |

### Group J

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Argentina** | 1 | +1.85 | 97.08% | 67.59% | 46.54% | **11.36%** |
| **Austria** | 24 | +0.12 | 69.55% | 25.62% | 10.22% | **0.34%** |
| **Algeria** | 28 | -0.08 | 63.00% | 21.23% | 7.80% | **0.23%** |
| **Jordan** | 63 | -0.90 | 33.45% | 7.80% | 1.97% | **0.01%** |

### Group K

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Portugal** | 5 | +1.21 | 94.53% | 61.77% | 30.93% | **4.25%** |
| **Colombia** | 13 | +0.82 | 90.83% | 51.14% | 22.16% | **1.92%** |
| **Uzbekistan** | 50 | -0.62 | 52.95% | 14.32% | 3.96% | **0.04%** |
| **DR Congo** | 46 | -1.42 | 25.63% | 4.45% | 0.86% | **0.00%** |

### Group L

| Team | FIFA Rank | Composite Rating | Prob. Advance Group % | Prob. Reach R16 % | Prob. Reach QF % | Prob. Win Cup % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **England** | 4 | +1.58 | 96.95% | 70.52% | 44.80% | **8.94%** |
| **Croatia** | 11 | +0.89 | 90.66% | 53.91% | 26.49% | **2.62%** |
| **Panama** | 34 | -0.75 | 45.86% | 13.36% | 2.73% | **0.03%** |
| **Ghana** | 73 | -1.31 | 26.35% | 5.49% | 0.83% | **0.00%** |


---

## 🔍 Key Insights & Analysis

> [!NOTE]
> **The Favorites**: **France** is the overall statistical favorite with a **16.66%** chance of winning, closely followed by **Spain** (**12.35%**) and defending champions **Argentina** (**11.36%**). These three teams form the top tier of contenders.

> [!TIP]
> **Sleeper Contenders**: **Morocco** (**4.28%**) and **Portugal** (**4.25%**) have strong composite ratings and favorable group draws, presenting them as very dangerous outsiders who could deep-run to the Semifinals or Finals.

> [!IMPORTANT]
> **The Host Nations**:
> - **Mexico** (Group A) has an **88.07%** chance of advancing from the group stage and a **1.97%** chance of winning, benefiting from host seeding.
> - **United States** (Group D) has an **89.92%** chance of advancing and a **1.60%** chance of winning.
> - **Canada** (Group B) has a **79.91%** chance of advancing and a **1.05%** chance of winning. All three hosts are highly likely to reach the knockout stage (Round of 32).

> [!WARNING]
> **Group of Death**: **Group C** features two top-10 teams in **Brazil** (Rank 6) and **Morocco** (Rank 7), along with **Scotland** and **Haiti**. This makes Group C extremely competitive, though the top-heavy structure means both Brazil and Morocco are still heavily favored to advance.

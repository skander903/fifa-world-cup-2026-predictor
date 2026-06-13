import csv
import math
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'data', 'fifa_wc_mens_match_dataset_1970_2022.csv')

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Historical dataset not found at {csv_path}.")

data = []
with open(csv_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            gf = int(row['goals_for'])
            ga = int(row['goals_against'])
            
            team_prior_matches = int(row['team_prior_matches'])
            opp_prior_matches = int(row['opp_prior_matches'])
            
            if team_prior_matches >= 2 and opp_prior_matches >= 2:
                team_wr = float(row['team_prior_win_rate'])
                opp_wr = float(row['opp_prior_win_rate'])
                team_gf_avg = float(row['team_prior_goals_scored_avg'])
                opp_ga_avg = float(row['opp_prior_goals_conceded_avg'])
                
                data.append({
                    'gf': gf,
                    'ga': ga,
                    'team_wr': team_wr,
                    'opp_wr': opp_wr,
                    'team_gf_avg': team_gf_avg,
                    'opp_ga_avg': opp_ga_avg,
                    'wr_diff': team_wr - opp_wr
                })
        except (ValueError, KeyError):
            continue

print("Valid matches for regression:", len(data))

b = [0.0, 0.0, 0.0, 0.0]
lr = 0.001
epochs = 5000

for epoch in range(epochs):
    grads = [0.0, 0.0, 0.0, 0.0]
    for row in data:
        eta = b[0] + b[1] * row['wr_diff'] + b[2] * row['team_gf_avg'] + b[3] * row['opp_ga_avg']
        eta = max(min(eta, 5.0), -5.0)
        lam = math.exp(eta)
        
        diff = row['gf'] - lam
        grads[0] += diff
        grads[1] += diff * row['wr_diff']
        grads[2] += diff * row['team_gf_avg']
        grads[3] += diff * row['opp_ga_avg']
        
    for j in range(4):
        b[j] += lr * grads[j] / len(data)

print("Optimized Poisson Coefficients:")
print(f"Intercept (b0): {b[0]:.4f}")
print(f"Win Rate Diff Coeff (b1): {b[1]:.4f}")
print(f"Team Prior GF Avg Coeff (b2): {b[2]:.4f}")
print(f"Opponent Prior GA Avg Coeff (b3): {b[3]:.4f}")

all_goals = []
with open(csv_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        all_goals.append(int(row['goals_for']))
avg_goals = sum(all_goals) / len(all_goals)
print(f"Global Average Goals per Team: {avg_goals:.4f} (Total average match goals: {avg_goals * 2:.4f})")

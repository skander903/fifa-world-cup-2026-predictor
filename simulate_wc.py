import csv
import math
import random
import os
from collections import defaultdict

# Resolve paths relative to this script
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'data', 'fifa_wc_mens_match_dataset_1970_2022.csv')
output_csv_path = os.path.join(base_dir, 'predictions.csv')

# ---------------------------------------------------------
# 1. Load historical match dataset and calculate stats
# ---------------------------------------------------------
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Historical dataset not found at {csv_path}. Make sure to put the dataset file in the data/ directory.")

hist_stats = defaultdict(list)
with open(csv_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        team = row['team_name']
        gf = int(row['goals_for'])
        ga = int(row['goals_against'])
        hist_stats[team].append(gf - ga)

historical_mapping = {
    "Türkiye": "Turkey",
    "DR Congo": "Zaire"
}

team_hist_gd = {}
for team, gd_list in hist_stats.items():
    team_hist_gd[team] = sum(gd_list) / len(gd_list)

def get_historical_gd(team_name):
    mapped_name = historical_mapping.get(team_name, team_name)
    if mapped_name in team_hist_gd:
        return team_hist_gd[mapped_name]
    return 0.0

# ---------------------------------------------------------
# 2. Define 2026 FIFA World Cup Groups and FIFA Rankings
# ---------------------------------------------------------
groups = {
    'A': ['Mexico', 'South Africa', 'South Korea', 'Czech Republic'],
    'B': ['Canada', 'Bosnia and Herzegovina', 'Qatar', 'Switzerland'],
    'C': ['Brazil', 'Morocco', 'Haiti', 'Scotland'],
    'D': ['United States', 'Paraguay', 'Australia', 'Türkiye'],
    'E': ['Germany', 'Curaçao', 'Ivory Coast', 'Ecuador'],
    'F': ['Netherlands', 'Japan', 'Sweden', 'Tunisia'],
    'G': ['Belgium', 'Egypt', 'Iran', 'New Zealand'],
    'H': ['Spain', 'Cape Verde', 'Saudi Arabia', 'Uruguay'],
    'I': ['France', 'Senegal', 'Iraq', 'Norway'],
    'J': ['Argentina', 'Algeria', 'Austria', 'Jordan'],
    'K': ['Portugal', 'DR Congo', 'Uzbekistan', 'Colombia'],
    'L': ['England', 'Croatia', 'Ghana', 'Panama']
}

all_teams_list = []
for grp_teams in groups.values():
    all_teams_list.extend(grp_teams)

fifa_rankings = {
    "Argentina": 1, "Spain": 2, "France": 3, "England": 4, "Portugal": 5,
    "Brazil": 6, "Morocco": 7, "Netherlands": 8, "Belgium": 9, "Germany": 10,
    "Croatia": 11, "Colombia": 13, "Mexico": 14, "Senegal": 15, "Uruguay": 16,
    "United States": 17, "Japan": 18, "Switzerland": 19, "Iran": 20,
    "Türkiye": 22, "Ecuador": 23, "Austria": 24, "South Korea": 25,
    "Australia": 27, "Algeria": 28, "Egypt": 29, "Canada": 30, "Norway": 31,
    "Ivory Coast": 33, "Panama": 34, "Sweden": 38, "Czech Republic": 40,
    "Paraguay": 41, "Scotland": 42, "Tunisia": 45, "DR Congo": 46,
    "Uzbekistan": 50, "Qatar": 56, "Iraq": 57, "South Africa": 60,
    "Saudi Arabia": 61, "Jordan": 63, "Bosnia and Herzegovina": 64,
    "Cape Verde": 67, "Ghana": 73, "Curaçao": 82, "Haiti": 83, "New Zealand": 85
}

exact_points = {
    1: 1877.27, 2: 1874.71, 3: 1870.70, 4: 1828.02, 5: 1767.85,
    6: 1765.86, 7: 1755.10, 8: 1753.57, 9: 1742.24, 10: 1735.77,
    11: 1714.87, 13: 1698.35, 14: 1687.48, 15: 1684.07, 16: 1673.07,
    17: 1671.23, 18: 1661.58, 19: 1650.06, 20: 1619.58, 27: 1579.0,
    30: 1559.0, 50: 1458.73, 60: 1428.0, 85: 1275.0
}

def rank_to_points(rank):
    if rank in exact_points:
        return exact_points[rank]
    ranks = sorted(exact_points.keys())
    for i in range(len(ranks) - 1):
        r1, r2 = ranks[i], ranks[i+1]
        if r1 < rank < r2:
            p1, p2 = exact_points[r1], exact_points[r2]
            return p1 + (p2 - p1) * (rank - r1) / (r2 - r1)
    if rank < 1:
        return 1900.0
    return 1275.0 - (rank - 85) * 5.0

fifa_points = {team: rank_to_points(fifa_rankings[team]) for team in all_teams_list}

# ---------------------------------------------------------
# 3. Build composite ratings and standardize
# ---------------------------------------------------------
raw_fifa = [fifa_points[t] for t in all_teams_list]
mean_fifa = sum(raw_fifa) / len(raw_fifa)
std_fifa = math.sqrt(sum((x - mean_fifa)**2 for x in raw_fifa) / len(raw_fifa))

raw_hist = [get_historical_gd(t) for t in all_teams_list]
mean_hist = sum(raw_hist) / len(raw_hist)
std_hist = math.sqrt(sum((x - mean_hist)**2 for x in raw_hist) / len(raw_hist))

composite_ratings = {}
for team in all_teams_list:
    z_fifa = (fifa_points[team] - mean_fifa) / std_fifa
    z_hist = (get_historical_gd(team) - mean_hist) / std_hist
    composite_ratings[team] = 0.80 * z_fifa + 0.20 * z_hist

mean_comp = sum(composite_ratings.values()) / len(composite_ratings)
std_comp = math.sqrt(sum((x - mean_comp)**2 for x in composite_ratings.values()) / len(composite_ratings))

for team in all_teams_list:
    composite_ratings[team] = (composite_ratings[team] - mean_comp) / std_comp

# ---------------------------------------------------------
# 4. Define Match Simulation Logic
# ---------------------------------------------------------
BASE_GOAL_RATE = 1.2632
ALPHA = 0.25

def poisson_random(lam):
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1

def simulate_goals(rating_a, rating_b):
    lam_a = BASE_GOAL_RATE * math.exp(ALPHA * (rating_a - rating_b))
    lam_b = BASE_GOAL_RATE * math.exp(ALPHA * (rating_b - rating_a))
    g_a = poisson_random(lam_a)
    g_b = poisson_random(lam_b)
    return g_a, g_b

def simulate_match(team_a, team_b, knockout=False):
    r_a = composite_ratings[team_a]
    r_b = composite_ratings[team_b]
    g_a, g_b = simulate_goals(r_a, r_b)
    
    if not knockout:
        return g_a, g_b, None
        
    if g_a != g_b:
        winner = team_a if g_a > g_b else team_b
        return g_a, g_b, winner
        
    et_lam_a = (BASE_GOAL_RATE * math.exp(ALPHA * (r_a - r_b))) / 3.0
    et_lam_b = (BASE_GOAL_RATE * math.exp(ALPHA * (r_b - r_a))) / 3.0
    et_g_a = poisson_random(et_lam_a)
    et_g_b = poisson_random(et_lam_b)
    
    g_a_total = g_a + et_g_a
    g_b_total = g_b + et_g_b
    
    if g_a_total != g_b_total:
        winner = team_a if g_a_total > g_b_total else team_b
        return g_a_total, g_b_total, winner
        
    win_prob_a = 0.5 + 0.05 * (r_a - r_b)
    win_prob_a = max(0.3, min(0.7, win_prob_a))
    
    if random.random() < win_prob_a:
        return g_a_total, g_b_total, team_a
    else:
        return g_a_total, g_b_total, team_b

# ---------------------------------------------------------
# 5. Third-place Team Allocation Logic
# ---------------------------------------------------------
slots = {
    74: {'A', 'B', 'C', 'D', 'F'},
    77: {'C', 'D', 'F', 'G', 'H'},
    78: {'C', 'E', 'F', 'H', 'I'},
    79: {'E', 'H', 'I', 'J', 'K'},
    80: {'A', 'E', 'H', 'I', 'J'},
    81: {'E', 'F', 'G', 'I', 'J'},
    83: {'B', 'E', 'F', 'I', 'J'},
    87: {'D', 'E', 'I', 'J', 'L'}
}

def find_matching(teams, slot_ids, idx, current_matching, used_teams):
    if idx == len(slot_ids):
        return current_matching.copy()
    
    slot = slot_ids[idx]
    allowed = slots[slot]
    
    for i, team in enumerate(teams):
        if i not in used_teams and team in allowed:
            current_matching[slot] = team
            used_teams.add(i)
            
            res = find_matching(teams, slot_ids, idx + 1, current_matching, used_teams)
            if res is not None:
                return res
                
            used_teams.remove(i)
            del current_matching[slot]
            
    return None

def allocate_third_places(third_placed_groups):
    slot_ids = list(slots.keys())
    matching = find_matching(third_placed_groups, slot_ids, 0, {}, set())
    return matching

# ---------------------------------------------------------
# 6. Monte Carlo Simulation of the World Cup
# ---------------------------------------------------------
NUM_SIMULATIONS = 20000
stage_counts = {team: defaultdict(int) for team in all_teams_list}

def sim_tournament():
    group_results = {}
    third_place_candidates = []
    
    for grp, grp_teams in groups.items():
        pts = {t: 0 for t in grp_teams}
        gd = {t: 0 for t in grp_teams}
        gf = {t: 0 for t in grp_teams}
        wins = {t: 0 for t in grp_teams}
        
        for i in range(4):
            for j in range(i + 1, 4):
                t_a, t_b = grp_teams[i], grp_teams[j]
                g_a, g_b, _ = simulate_match(t_a, t_b, knockout=False)
                
                gf[t_a] += g_a
                gf[t_b] += g_b
                gd[t_a] += (g_a - g_b)
                gd[t_b] += (g_b - g_a)
                
                if g_a > g_b:
                    pts[t_a] += 3
                    wins[t_a] += 1
                elif g_b > g_a:
                    pts[t_b] += 3
                    wins[t_b] += 1
                else:
                    pts[t_a] += 1
                    pts[t_b] += 1
                    
        ranked = sorted(
            grp_teams,
            key=lambda t: (pts[t], gd[t], gf[t], wins[t], composite_ratings[t]),
            reverse=True
        )
        
        group_results[grp] = ranked
        
        third_team = ranked[2]
        third_place_candidates.append({
            'team': third_team,
            'group': grp,
            'pts': pts[third_team],
            'gd': gd[third_team],
            'gf': gf[third_team],
            'wins': wins[third_team],
            'rating': composite_ratings[third_team]
        })
        
        stage_counts[ranked[3]]['Group Stage'] += 1
        
    ranked_thirds = sorted(
        third_place_candidates,
        key=lambda x: (x['pts'], x['gd'], x['gf'], x['wins'], x['rating']),
        reverse=True
    )
    
    advancing_thirds = ranked_thirds[:8]
    eliminated_thirds = ranked_thirds[8:]
    
    for item in eliminated_thirds:
        stage_counts[item['team']]['Group Stage'] += 1
        
    adv_thirds_groups = [x['group'] for x in advancing_thirds]
    group_to_third_team = {x['group']: x['team'] for x in advancing_thirds}
    
    matching = allocate_third_places(adv_thirds_groups)
    match_third_team = {slot: group_to_third_team[matching[slot]] for slot in slots}

    winners = {grp: group_results[grp][0] for grp in groups}
    runners = {grp: group_results[grp][1] for grp in groups}
    
    r32_matches = {
        73: (runners['A'], runners['B']),
        74: (winners['E'], match_third_team[74]),
        75: (winners['F'], runners['C']),
        76: (winners['C'], runners['F']),
        77: (winners['I'], match_third_team[77]),
        78: (winners['A'], match_third_team[78]),
        79: (winners['L'], match_third_team[79]),
        80: (winners['G'], match_third_team[80]),
        81: (winners['B'], match_third_team[81]),
        82: (runners['D'], runners['G']),
        83: (winners['D'], match_third_team[83]),
        84: (runners['E'], runners['I']),
        85: (winners['J'], runners['H']),
        86: (winners['H'], runners['J']),
        87: (winners['K'], match_third_team[87]),
        88: (runners['K'], runners['L'])
    }
    
    r32_winners = {}
    for match_id, (t1, t2) in r32_matches.items():
        _, _, winner = simulate_match(t1, t2, knockout=True)
        r32_winners[match_id] = winner
        
        loser = t2 if winner == t1 else t1
        stage_counts[loser]['Round of 32'] += 1
        
    r16_matches = {
        89: (r32_winners[74], r32_winners[77]),
        90: (r32_winners[73], r32_winners[75]),
        91: (r32_winners[76], r32_winners[78]),
        92: (r32_winners[79], r32_winners[80]),
        93: (r32_winners[83], r32_winners[84]),
        94: (r32_winners[81], r32_winners[82]),
        95: (r32_winners[86], r32_winners[88]),
        96: (r32_winners[85], r32_winners[87])
    }
    
    r16_winners = {}
    for match_id, (t1, t2) in r16_matches.items():
        _, _, winner = simulate_match(t1, t2, knockout=True)
        r16_winners[match_id] = winner
        
        loser = t2 if winner == t1 else t1
        stage_counts[loser]['Round of 16'] += 1
        
    qf_matches = {
        97: (r16_winners[89], r16_winners[90]),
        98: (r16_winners[93], r16_winners[94]),
        99: (r16_winners[91], r16_winners[92]),
        100: (r16_winners[95], r16_winners[96])
    }
    
    qf_winners = {}
    for match_id, (t1, t2) in qf_matches.items():
        _, _, winner = simulate_match(t1, t2, knockout=True)
        qf_winners[match_id] = winner
        
        loser = t2 if winner == t1 else t1
        stage_counts[loser]['Quarter-finals'] += 1
        
    sf_matches = {
        101: (qf_winners[97], qf_winners[98]),
        102: (qf_winners[99], qf_winners[100])
    }
    
    sf_winners = {}
    sf_losers = {}
    for match_id, (t1, t2) in sf_matches.items():
        _, _, winner = simulate_match(t1, t2, knockout=True)
        sf_winners[match_id] = winner
        sf_losers[match_id] = t2 if winner == t1 else t1
        
    t1, t2 = sf_losers[101], sf_losers[102]
    _, _, winner_3rd = simulate_match(t1, t2, knockout=True)
    loser_3rd = t2 if winner_3rd == t1 else t1
    
    stage_counts[winner_3rd]['3rd'] += 1
    stage_counts[loser_3rd]['4th'] += 1
    
    t1, t2 = sf_winners[101], sf_winners[102]
    _, _, champion = simulate_match(t1, t2, knockout=True)
    runner_up = t2 if champion == t1 else t1
    
    stage_counts[champion]['Winner'] += 1
    stage_counts[runner_up]['Runner-up'] += 1

print(f"Running {NUM_SIMULATIONS} tournament simulations...")
for sim in range(NUM_SIMULATIONS):
    sim_tournament()

results = []
for team in all_teams_list:
    group_letter = [g for g, teams in groups.items() if team in teams][0]
    c = stage_counts[team]
    total_sims = float(NUM_SIMULATIONS)
    
    p_group = c['Group Stage'] / total_sims
    p_r32 = c['Round of 32'] / total_sims
    p_r16 = c['Round of 16'] / total_sims
    p_qf = c['Quarter-finals'] / total_sims
    p_sf = c['Semi-finals'] / total_sims
    p_4th = c['4th'] / total_sims
    p_3rd = c['3rd'] / total_sims
    p_runner = c['Runner-up'] / total_sims
    p_winner = c['Winner'] / total_sims
    
    prob_advance = 1.0 - p_group
    prob_r16 = p_r16 + p_qf + p_sf + p_4th + p_3rd + p_runner + p_winner
    prob_qf = p_qf + p_sf + p_4th + p_3rd + p_runner + p_winner
    prob_sf = p_sf + p_4th + p_3rd + p_runner + p_winner
    prob_final = p_runner + p_winner
    prob_win = p_winner
    
    results.append({
        'Team': team,
        'Group': group_letter,
        'FIFA_Rank': fifa_rankings[team],
        'FIFA_Points': fifa_points[team],
        'Composite_Rating': composite_ratings[team],
        'Prob_Advance': prob_advance,
        'Prob_R16': prob_r16,
        'Prob_QF': prob_qf,
        'Prob_SF': prob_sf,
        'Prob_Final': prob_final,
        'Prob_Winner': prob_win
    })

results_sorted = sorted(results, key=lambda x: (x['Prob_Winner'], x['Composite_Rating']), reverse=True)

with open(output_csv_path, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results_sorted[0].keys())
    writer.writeheader()
    for row in results_sorted:
        writer.writerow(row)

print("Predictions successfully written to:", output_csv_path)

print("\nTop 15 Teams by Prediction to Win the 2026 World Cup:")
print(f"{'Team':<20} | {'Group':<5} | {'FIFA Rank':<9} | {'Advance %':<9} | {'QF %':<7} | {'Final %':<7} | {'Win %':<7}")
print("-" * 75)
for r in results_sorted[:15]:
    print(f"{r['Team']:<20} | {r['Group']:<5} | {r['FIFA_Rank']:<9} | {r['Prob_Advance']*100:<8.2f}% | {r['Prob_QF']*100:<6.2f}% | {r['Prob_Final']*100:<6.2f}% | {r['Prob_Winner']*100:<6.2f}%")

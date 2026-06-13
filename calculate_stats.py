import csv
import os
from collections import defaultdict

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'data', 'fifa_wc_mens_match_dataset_1970_2022.csv')

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Historical dataset not found at {csv_path}.")

team_stats = defaultdict(list)

with open(csv_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        team = row['team_name']
        gf = int(row['goals_for'])
        ga = int(row['goals_against'])
        outcome = row['outcome']
        team_stats[team].append((gf, ga, outcome))

team_aggregates = {}
for team, matches in team_stats.items():
    total_matches = len(matches)
    total_gf = sum(m[0] for m in matches)
    total_ga = sum(m[1] for m in matches)
    wins = sum(1 for m in matches if m[2].lower() == 'win')
    draws = sum(1 for m in matches if m[2].lower() == 'draw')
    losses = sum(1 for m in matches if m[2].lower() == 'loss')
    
    win_rate = wins / total_matches
    gf_avg = total_gf / total_matches
    ga_avg = total_ga / total_matches
    gd_avg = gf_avg - ga_avg
    
    team_aggregates[team] = {
        'matches': total_matches,
        'win_rate': win_rate,
        'gf_avg': gf_avg,
        'ga_avg': ga_avg,
        'gd_avg': gd_avg,
        'wins': wins,
        'draws': draws,
        'losses': losses
    }

sorted_teams = sorted(
    [t for t in team_aggregates.items() if t[1]['matches'] >= 5],
    key=lambda x: x[1]['gd_avg'],
    reverse=True
)

print(f"{'Team':<20} | {'Matches':<7} | {'Win Rate':<8} | {'GF Avg':<6} | {'GA Avg':<6} | {'GD Avg':<6}")
print("-" * 65)
for team, stats in sorted_teams[:20]:
    print(f"{team:<20} | {stats['matches']:<7} | {stats['win_rate']:<8.3f} | {stats['gf_avg']:<6.3f} | {stats['ga_avg']:<6.3f} | {stats['gd_avg']:<6.3f}")

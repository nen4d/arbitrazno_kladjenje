import pandas as pd

# Load CSV files into DataFrames
file1 = pd.read_csv('admiralbet.csv')
file2 = pd.read_csv('maxbet.csv')
file3 = pd.read_csv('merkur.csv')
file4 = pd.read_csv('pinnbet.csv')
file5 = pd.read_csv('soccerbet.csv')

# Combine all DataFrames into one for easier processing
combined_df = pd.concat([file1, file2, file3, file4])

def find_arbitrage_opportunities(df):
    arbitrage_opportunities = []
    
    # Group by the match (home team and away team)
    grouped = df.groupby(['home', 'away'])
    
    for (home, away), group in grouped:
        # Find the best odds for home win, draw, and away win
        best_home_win_odds = group['odds_1'].max()
        best_draw_odds = group['odds_x'].max()
        best_away_win_odds = group['odds_2'].max()
        
        # Calculate the arbitrage condition
        arbitrage_condition = (1 / best_home_win_odds) + (1 / best_draw_odds) + (1 / best_away_win_odds)
        
        if arbitrage_condition < 1:
            arbitrage_opportunities.append({
                'home': home,
                'away': away,
                'best_home_win_odds': best_home_win_odds,
                'best_draw_odds': best_draw_odds,
                'best_away_win_odds': best_away_win_odds,
                'arbitrage_condition': arbitrage_condition
            })
    
    return arbitrage_opportunities

def calculate_profit(opportunity, total_stake=100):
    # Extract the best odds
    best_home_win_odds = opportunity['best_home_win_odds']
    best_draw_odds = opportunity['best_draw_odds']
    best_away_win_odds = opportunity['best_away_win_odds']
    
    # Calculate the individual stakes
    stake_home = total_stake / (best_home_win_odds * opportunity['arbitrage_condition'])
    stake_draw = total_stake / (best_draw_odds * opportunity['arbitrage_condition'])
    stake_away = total_stake / (best_away_win_odds * opportunity['arbitrage_condition'])
    
    # Calculate the potential profit for each outcome
    profit_home = (stake_home * best_home_win_odds) - total_stake
    profit_draw = (stake_draw * best_draw_odds) - total_stake
    profit_away = (stake_away * best_away_win_odds) - total_stake
    
    return {
        'stake_home': stake_home,
        'stake_draw': stake_draw,
        'stake_away': stake_away,
        'profit_home': profit_home,
        'profit_draw': profit_draw,
        'profit_away': profit_away
    }

# Find arbitrage opportunities
arbitrage_opportunities = find_arbitrage_opportunities(combined_df)

if len(arbitrage_opportunities) == 0:
    print("No arbitrage opportunities found.")
else:
    # Calculate and display profit for each arbitrage opportunity
    for opportunity in arbitrage_opportunities:
        profit = calculate_profit(opportunity)
        print(f"Match: {opportunity['home']} vs {opportunity['away']}")
        print(f"Stakes: Home - {profit['stake_home']:.2f}, Draw - {profit['stake_draw']:.2f}, Away - {profit['stake_away']:.2f}")
        print(f"Profits: Home - {profit['profit_home']:.2f}, Draw - {profit['profit_draw']:.2f}, Away - {profit['profit_away']:.2f}")
        print("-" * 40)
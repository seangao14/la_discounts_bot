import pandas as pd
from src.discounts.baseball import get_mlb_discounts

def get_daily_discounts(today):
    """
    Get all discounts for today.
    """

    baseball_triggered = get_mlb_discounts(today)
    baseball_triggered_df = pd.DataFrame(baseball_triggered, columns=['Team', 'Trigger'])

    deals = pd.read_csv('deals.csv')

    today_deals = pd.merge(
        baseball_triggered_df, deals, how='inner', on=['Team', 'Trigger']
    )

    ret = ''
    for _, row in today_deals.iterrows():
        ret += (
            f'```\n'
            f'{row["Restaurant"]}\n'
            f'{row["Deal"]}\n'
            f'Condition: {row["Team"]} {row["Trigger"]}'
            f'```'
        )
        
    return ret

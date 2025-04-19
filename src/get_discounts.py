import pandas as pd
from src.helpers import table_to_message
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

    ret = table_to_message(today_deals)

    if ret == '':
        ret = 'No discounts today :('
    else:
        ret = "Discounts for today:\n" + ret
        
    return ret

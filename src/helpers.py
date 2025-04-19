def table_to_message(df):
    ret = ''
    for _, row in df.iterrows():
        ret += (
            f'```\n'
            f'{row["Restaurant"]}\n'
            f'{row["Deal"]}\n'
            f'{row["Redemption"]}\n'
            f'Condition: {row["Team"]} {row["Trigger"]}'
            f'```'
        )
    
    return ret
def table_to_message(df):
    """
    Convert a DataFrame to a message string.
    """

    ret = ''
    for _, row in df.iterrows():
        ret += (
            f'```\n'
            f'{row["Restaurant"]}\n'
            f'{row["Deal"]}\n'
            f'{row["Redemption"]}\n'
            f'Condition: {row["Team"]} - {row["Trigger"]}'
            f'```'
        )
    
    return ret


async def send_message(o, message, type="ctx"):
    """
    Send a message to the user.
    
    Args:
        o (object): The object to send the message to.
        message (str): The message to send.
        type (str): The type of object to send the message to. Default is "ctx".
    """

    try:
        if type == "ctx":
            await o.author.send(message)
        elif type == "user":
            await o.send(message)
    except Exception as e:
        print(f"Error sending message: {e}")

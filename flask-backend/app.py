from flask import Flask, jsonify, request                 # The Main thing
import pandas                           # Dataframe reading and manipulation
import json
from datetime import datetime
import re

from sympy import per

import users                            # list of all currency things and their relevant properties
from explorer import Explorer           # explores data on the blockchain


######### INITIALISING APP #########
app = Flask(__name__)
explorer = Explorer()


######### API ROUTES #########
# Fetching the Blockchain as JSON
@app.route('/blockchain')
def blockchain():
    blockchain = get_blockchain()                   # reading and formatting the Blockchain as a DataFrame
    return blockchain.to_json(orient='records')     # returns the Blockchain to the client as JSON


# Fetching user trades as JSON
@app.route('/blockchain/@<username>')
def user(username: str):
    descending = request.args.get('descending', None)   # whether the trades should be in ascending or descending order
    user = users.get_user(username)                     # fetching the User object by name
    trades = get_user_trades(username)                  # gets all of the user's trades by Username

    # sorting by newest trade first if there's a descending parameter with any value. why? -> https://stackoverflow.com/questions/65575796/why-does-the-flask-bool-query-parameter-always-evaluate-to-true
    if descending:
        trades.sort_index(axis=0, ascending=False, inplace=True)

    return trades.to_json(orient='records')             # returns the filtered Blockchain to the client as JSON


# Mining Milestones
@app.route('/blockchain/milestones')
def milestones():
    ms = explorer.get_mining_milestones()

    # dict format
    ms.set_index('TXID', inplace=True) # setting the TX ID as key for the dict
    return ms.to_dict()['MILESTONE']

    # json list format
    return ms.to_json(orient='records')


# Blockchain Statistics
@app.route('/blockchain/stats')
def stats():
    # getting a query parameter ?period=xxx as int, with a default value of 0
    period = request.args.get('period', 0, type=int)

    return get_blockchain_stats(period)


# User specific statistics
@app.route('/blockchain/stats/@<username>')
def stats_user(username: str):
    user = users.get_user(username)                     # fetching the User object by name
    stats = get_user_stats(user)

    return stats

# testing optional parameters ex: ?key=value
@app.route('/test')
def test():
    optional_value = request.args.get('reversed', False)
    return f'<code>Reversed: {optional_value}</code>'


######### BLOCKCHAIN FUNCTIONS / PANDAS #########
# Loading the Blockchain from disk
def get_blockchain() -> pandas.DataFrame:
    '''
    Loading the latest version of the blockchain from disk with appropriate formatting.\n
    Returns a pandas DataFrame.
    '''
    # Reading the blockchain
    blockchain = explorer.blockchain

    # Replacing user IDs with usernames
    blockchain.replace(users.replace_thing('mention', 'name'), inplace=True)

    # Extracing emote names from the discord emote code
    blockchain['PREV_HASH'] = blockchain['PREV_HASH'].apply(get_emote_name)

    # Renaming the columns
    blockchain.columns = ['ID', 'INPUT', 'SIZE', 'OUTPUT', 'EMOTE', 'DATE']
    
    print('[APP.PY] >>> Fetching Blockchain')

    # Returns the Blockchain as a DataFrame
    return blockchain



# Getting general Blockchain Statistics by time period
def get_blockchain_stats(period: int) -> dict[str, any]:
    supply          = explorer.supply
    mined           = explorer.things_mined_by_time(days=period)
    trades          = explorer.num_of_trades(days=period)
    user_trades     = explorer.num_of_trades(days=period, users_only=True)
    biggest_trade   = explorer.biggest_trade(days=period)
    usernames       = [users.replace_thing('mention', 'name')[u] for u in explorer.users] # converting from discord @mentions to plain usernames

    return {
        'supply'        : supply,
        'mined'         : mined,
        'trades'        : trades,
        'user_trades'   : user_trades,
        'users'         : usernames,
        'biggest_trade' : biggest_trade,
        'period': period
    }



######### USER SPECIFIC #########
# Gets all trades a user was involved in using their Username
def get_user_trades(username: str) -> pandas.DataFrame:
    '''
    Filtered Blockchain containing only trades by a specific user.\n
    Returns a pandas DataFrame.
    '''
    blockchain = get_blockchain()

    # Filtering all rows where User is either Input or Output
    user_txs = blockchain.loc[(blockchain['INPUT'] == username) | (blockchain['OUTPUT'] == username)]

    return user_txs

# Gets all number statistics relative to the chosen user
def get_user_stats(user: users.User):
    '''
    Gets interesting statistics about a user's experience with Currency Things!
    '''
    balance             = explorer.get_balance(user.mention)
    trades              = explorer.num_of_trades(days=0, specific_user=user.mention)
    user_trades         = explorer.num_of_trades(days=0, specific_user=user.mention, users_only=True)
    mined               = explorer.mined_by_user(user.mention)
    sent                = explorer.user_things_sent(user.mention)
    received            = explorer.user_things_received(user.mention)
    biggest_sent        = explorer.biggest_trade(user_sent=user.mention)
    biggest_received    = explorer.biggest_trade(user_received=user.mention)

    return {
        'name'              : user.name,
        'balance'           : balance,
        'trades'            : trades,
        'user_trades'       : user_trades,
        'mined'             : mined,
        'things_sent'       : sent,
        'things_received'   : received,
        'biggest_sent'      : biggest_sent,
        'biggest_received'  : biggest_received
    }



######### HELPER FUNCTIONS #########
def get_emote_name(emote_code: str) -> str:
    '''Extracts only the emote name from the discord emote code (if the emote is valid)'''
    # Does no formating if the code doesn't start with <
    if not(emote_code.startswith('<')):
        return emote_code
    
    # extracts the text from the emote code
    return re.findall(r'[a-zA-Z]+', emote_code)[0]


# Runs the server
if __name__ == '__main__':
    app.run(debug=True)
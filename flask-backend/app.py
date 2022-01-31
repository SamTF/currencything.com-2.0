from flask import Flask, jsonify                 # The Main thing
import pandas                           # Dataframe reading and manipulation
import json
from datetime import datetime
import re

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
    user = users.get_user(username)                 # fetching the User object by name
    trades = get_user_trades(username)              # gets all of the user's trades by Username

    return trades.to_json(orient='records')         # returns the filtered Blockchain to the client as JSON

# Mining Milestones
@app.route('/blockchain/milestones')
def milestones():
    ms = explorer.get_mining_milestones()

    # dict format
    ms.set_index('TXID', inplace=True) # setting the TX ID as key for the dict
    return ms.to_dict()['MILESTONE']

    # json list format
    return ms.to_json(orient='records')


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


# Gets all trades a user was involved in using their discord @mention
def get_user_trades(mention: str) -> pandas.DataFrame:
    '''
    Filtered Blockchain containing only trades by a specific user.\n
    Returns a pandas DataFrame.
    '''
    blockchain = get_blockchain()

    # Filtering all rows where User is either Input or Output
    filtered = blockchain.loc[(blockchain['INPUT'] == mention) | (blockchain['OUTPUT'] == mention)]

    print(f'[APP.PY] >>> Fetching trades for user: {mention}')

    return filtered






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
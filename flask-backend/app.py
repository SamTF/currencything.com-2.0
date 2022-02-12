from debugpy import trace_this_thread
from flask import Flask, jsonify, request                   # The Main thing
import pandas                                               # Dataframe reading and manipulation
import re                                                   # REGEX for emote codes

import users                                                # list of all currency things and their relevant properties
from explorer import Explorer                               # explores data on the blockchain
import graph_dealer as gd                                   # generating static graphs with matplotlib


######### INITIALISING APP #########
app = Flask(__name__)
explorer = Explorer()


######### API ROUTES #########
# Fetching the Blockchain as JSON
@app.route('/blockchain')
def blockchain():
    blockchain = get_blockchain()                   # reading and formatting the Blockchain as a DataFrame
    # TEMP!!!!
    graphs()
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


# Getting Stat Graphs
@app.route('/blockchain/stats/graphs')
def graphs():
    # Graphing the stats data with matplotlib
    ### THIS MUST NOT BE DONE HERE
    ### IT SLOWS DOWN THE PAGE BY A FULL SECOND!!!
    ### put the graph generation for the main page on a cron job every 24h
    gd.plot_chart(explorer.supply_over_time(),              gd.GraphType.LINE,  'supply',           'Supply Over Time',         'Date',         '₡urrency Things',  True)
    gd.plot_chart(explorer.mined_per_day(),                 gd.GraphType.LINE,  'mined',            'Things Mined Per Day',     'Date',         '₡urrency Things',  True)
    gd.plot_chart(explorer.num_of_trades_per_day(),         gd.GraphType.LINE,  'trades',           'Trades Over Time',         'Date',         '# Of Trades',      True)
    gd.plot_chart(explorer.num_of_trades_per_day(True),     gd.GraphType.LINE,  'user_trades',      'User Trades Over Time',    'Date',         '# Of Trades',      True)
    gd.plot_chart(explorer.biggest_trade_over_time(),       gd.GraphType.BAR,   'biggest_trade',    'Biggest Trade Over Time',  'Trade ID',     '₡urrency Things',  False)
    

    holders = explorer.get_balance_all().rename(index=users.replace_thing('mention', 'name')) # changes the index values from discord mentions to usernames
    gd.plot_chart(holders,               gd.GraphType.BAR,   'holders',          'Currency Thing Holders',   'User',         '₡urrency Things',  False)
    
    
    print('[APP.PY] >>> Calling all graphs!')

    return {'message' : 'all graphs successfully generated!'}


# Getting User-specific graphs
@app.route('/blockchain/stats/@<username>/graphs')
def user_graphs(username):
    # fetching the User object by name
    user = users.get_user(username)

    # getting the dataframes required for the graphs
    user_trades = explorer.num_of_trades_per_day(True, specific_user=user.mention)
    networth_over_time = explorer.balance_over_time(user.mention, True)

    # fetching the graphs as a SVG string to embed in the HTML
    trades_graph_svg    = gd.plot_chart(user_trades,        gd.GraphType.LINE,  f'{username}_trades',   'Trades Per Day',       'Day',  '# Of Trades',      True, gd.Method.STRING_BUFFER)
    networth_graph      = gd.plot_chart(networth_over_time, gd.GraphType.LINE,  f'{username}_networth', 'Networth Over Time',   'Date', '₡urrency Things',  True, gd.Method.STRING_BUFFER)

    # return supply
    return {'trades' : trades_graph_svg, 'networth' : networth_graph}
    

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
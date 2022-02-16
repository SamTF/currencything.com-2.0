### This utility script generates all homepage graphs for the Currency Thing Explorer
# run this on a cron job every 24h

import users                                                # list of all currency things and their relevant properties
from explorer import Explorer                               # explores data on the blockchain
import graph_dealer as gd                                   # generating static graphs with matplotlib


explorer = Explorer()

def generate_graphs() -> None:
    gd.plot_chart(explorer.supply_over_time(),              gd.GraphType.LINE,  'supply',           'Supply Over Time',         'Date',         '₡urrency Things',  True)
    gd.plot_chart(explorer.mined_per_day(),                 gd.GraphType.LINE,  'mined',            'Things Mined Per Day',     'Date',         '₡urrency Things',  True)
    gd.plot_chart(explorer.num_of_trades_per_day(),         gd.GraphType.LINE,  'trades',           'Trades Over Time',         'Date',         '# Of Trades',      True)
    gd.plot_chart(explorer.num_of_trades_per_day(True),     gd.GraphType.LINE,  'user_trades',      'User Trades Over Time',    'Date',         '# Of Trades',      True)
    gd.plot_chart(explorer.biggest_trade_over_time(),       gd.GraphType.BAR,   'biggest_trade',    'Biggest Trade Over Time',  'Trade ID',     '₡urrency Things',  False)
    

    holders = explorer.get_balance_all().rename(index=users.replace_thing('mention', 'name')) # changes the index values from discord mentions to usernames
    gd.plot_chart(holders,               gd.GraphType.BAR,   'holders',          'Currency Thing Holders',   'User',         '₡urrency Things',  False)
    
    
    print('[APP.PY] >>> Calling all graphs!')
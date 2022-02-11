### This script only explores the data currently on the blockchain.

import pandas as pd
from datetime import datetime, timedelta

pd.options.mode.chained_assignment = None


### CONSTANTS
BLOCKCHAIN  = 'block.chain'             # the name of the local blockchain file stored on disk
CREATOR_ID  = 840976021687762955        # The Currency Thing Discord user ID
CREATOR     = f'<@{CREATOR_ID}>'        # formats the Bot's ID as a Discord mention


###### THE BLOCKCHAIN EXPLORER CLASS ##############################################################################################################
class Explorer:
    def __init__(self) -> None:
        self._last_updated = datetime.strptime('1970-01-01', '%Y-%m-%d')
        self._blockchain = self.blockchain

    @property
    def blockchain(self) -> pd.DataFrame:
        # Only reloads the blockchain from disk every 5 mins
        # if (datetime.now() - self._last_updated).total_seconds() <= (5 * 60):
        #     return self._blockchain

        b = pd.read_csv(BLOCKCHAIN)
        b['SIZE'] = pd.to_numeric(b['SIZE'])    # Converts the SIZE column into INT type; otherwise it assumes STRING type
        b['TIME'] = pd.to_datetime(b['TIME'])   # Converts the TIME column into datetime format
        self._last_updated = datetime.now()

        return b
    
    @property
    def mined(self) -> pd.DataFrame:
        '''
        Returns the Blockchain including only mining rewards (where Currency Thing is the Input)
        '''
        return self.blockchain.loc[self.blockchain['INPUT'] == CREATOR]                     # All currency things sent by the Currency Thing bot (mined)
    

    ### GENERAL STATS ######
    @property
    def supply(self) -> int:
        '''How many Currency Things have been mined in total.'''
        b = self.blockchain.groupby(['INPUT']).sum()                                        # Groups df by Input then sums all currency things SENT BY each user - where the user is on the INPUT side of the trade
        supply = b.loc[CREATOR]['SIZE']                                                     # Sums all currency things sent by the discord bot - aka total supply

        return int(supply)                                                                  # Converting numpy int64 to int
    

    @property
    def users(self) -> list[str]:
        '''Returns a list of all Currency Thing users.'''
        return self.blockchain.groupby(['OUTPUT']).sum().index.to_list()                    # getting a list of all the users that own currency things as discord @mentions
    

    def num_of_trades(self, days = 0, users_only = False, specific_user: str = None) -> int:
        '''
        Returns the total number of trades on the Blockchain.

        days: if specified, only counts TXs from the last X days.
        users_only: only displays trades executed by users and not by the Currency Thing bot
        specific_user: only count trades involving the mentioned user (by discord @mention)
        '''
        trades = self.blockchain if days < 1 else self.tx_by_time(days)                     # checks entire blockchain, or last few days if "days" value is specified

        if users_only:
            trades = trades.loc[trades['INPUT'] != CREATOR]                                 # Only count rows where the Currency Thing Bot was not involved
        
        if specific_user:                                                                   # Filtering all trades where the specified User is either Input or Output
            trades = trades.loc[(trades['INPUT'] == specific_user) | (trades['OUTPUT'] == specific_user)]

        if trades.empty: return 0                                                           # checking if there have been any trades in the given timeframe

        return len(trades.index)                                                            # returns the number of rows in the (filtered?) dataframe

    
    def things_mined_by_time(self, days = 0) -> int:
        '''
        Returns the total amount of currency things mined in the last X days as an INT.

        days: if specified, only counts TXs from the last X days.
        '''
        rows = self.blockchain if days < 1 else self.tx_by_time(days)                       # checks entire blockchain, or last few days if "days" value is specified
        mined = rows.loc[rows['INPUT'] == CREATOR]                                          # Gets all trades where the Currency Thing Bot is the one sending things

        # checking if any things have been mined in the given timeframe
        if mined.empty: return 0

        mined = mined['SIZE'].sum()                                                         # Sums the size of currency things sent

        return int(mined)                                                                   # converting numpy.int64 to regular int


    def biggest_trade(self, days = 0, user_sent:str = None, user_received:str = None) -> int:
        '''
        Returns the trade with the largest size.

        days: if specified, only counts TXs from the last X days.
        user_sent: if specified, only counts TXs sent BY the user.
        user_received: if specified, only counts TXs sent TO the user.
        '''
        rows = self.blockchain if days < 1 else self.tx_by_time(days)                       # checks entire blockchain, or last few days if "days" value is specified

        # checking for user specific txs
        if user_sent:                                                                       # Gets all trades where the user was on the INPUT
            rows = rows[rows['INPUT'] == user_sent]
            if rows.empty: return 0                                                         # Returns 0 if user was never the input (bots)
            
        elif user_received:                                                                 # Filters rows where Currency Thing was NOT the INPUT, and the user was the OUTPUT
            rows = rows[(rows['INPUT'] != CREATOR) & (rows['OUTPUT'] == user_received)]
        
        # checking if there have been any trades in the given timeframe
        if rows.empty: return 0

        # Getting the value now
        rows.sort_values('SIZE', ascending=False, inplace=True)                             # Sorts rows by trade size in descending order
        biggest_trade = rows.iloc[0]['SIZE']                                                # the first row: biggest size
        return int(biggest_trade)                                                           # converting numpy int64 to int


    ### HELPER FUNCTIONS ######
    # helper function to filter blockchain txs by latest X days
    def tx_by_time(self, days:int = 1) -> pd.DataFrame:
        '''
        Returns the transactions that occured in the last X days.

        days: amount of days to subtract from current datetime. (default = 1)
        '''
        date = datetime.now() - timedelta(days=days)                                        # Gets the datetime value a specified amount of hours ago
        filtered_tx = self.blockchain.loc[self.blockchain['TIME'] > date]                   # Gets all blockchain trades with a time greater than that value

        return filtered_tx


    ### CUMULATIVE STATS ######
    # Cumulative sum of currency things at each transastion
    def supply_over_tx(self) -> pd.DataFrame:
        '''
        Returns a DataFrame with the total amount of currency things in circulation at each transaction ID.\n
        [ ID | SUPPLY ]
        '''
        print('[EXPLORER] >>> SUPPLY OVER TX')
        mined = self.mined.drop(['ID', 'INPUT', 'OUTPUT', 'PREV_HASH', 'TIME'], axis=1)     # Gets mining rewards and removes unnecessary column
        supply = mined.cumsum().rename(columns={'SIZE': 'SUPPLY'})                          # cumulative sums the mining rewards, and renames the col to Supply

        return supply
    
    # Cumulative sum of currency things at per day
    def supply_over_time(self) -> pd.DataFrame:
        '''
        Returns the total amount of currency things in circulation per day.
        [ ID | SUPPLY ]
        '''
        mined = self.mined.drop(['ID', 'INPUT', 'OUTPUT', 'PREV_HASH'], axis=1)             # Gets mining rewards and removes unnecessary column         
        mined['TIME'] = mined['TIME'].dt.date                                               # Converts the datetime to date
        supply = mined.groupby('TIME').sum()                                                # Sums all currency things mined per day
        supply = supply.cumsum(axis=0).rename(columns={'SIZE': 'SUPPLY'})                   # Gets the cumulative sum by date

        return supply

    
    ### DAILY STATS ######
    # Currency Things mined on each day
    def mined_per_day(self) -> pd.DataFrame:
        '''
        Returns a DataFrame with the amount of currency things made every day
        [ TIME | SIZE ]
        '''
        mined = self.mined
        mined['TIME'] = mined['TIME'].dt.date                                               # Converts the datetime to date
        mined = mined.groupby('TIME').sum().drop(['ID'], axis=1)                            # Groups by date and sums all size values at each day, and removes the ID column

        return mined
    
    # Number of trades per day
    def num_of_trades_per_day(self, users_only = False, specific_user: str = None) -> pd.DataFrame:
        '''
        Returns the quantity of transactions PER DAY on the blockchain as a DataFrame.\n
        [ TIME | SIZE ]

        users_only: only displays trades executed by users and not by the Currency Thing bot
        specific_user: only count trades involving the mentioned user (by discord @mention)
        '''
        trades = self.blockchain

        if users_only:
            trades = trades.loc[trades['INPUT'] != CREATOR]                                 # Only count rows where the Currency Thing Bot was not involved
        
        if specific_user:                                                                   # Filtering all trades where the specified User is either Input or Output
            trades = trades.loc[(trades['INPUT'] == specific_user) | (trades['OUTPUT'] == specific_user)]

        trades['TIME'] = trades['TIME'].dt.date
        trades = trades.groupby('TIME').count()
        trades.drop(['ID', 'INPUT', 'OUTPUT', 'PREV_HASH'], axis=1, inplace=True)

        return trades


    # Biggest Trades
    def biggest_trade_over_time(self):
        '''
        Tracks the biggest trade size at every moment in the blockchain.
        Returns a pandas dataframe [ ID | SIZE ]
        '''
        big_trades = []
        biggest_trade = 0

        for index, row in self.blockchain.iterrows():
            size = row['SIZE']

            # checking if the current trade is bigger than the current biggest
            if size > biggest_trade:
                data = (row['ID'], size)
                biggest_trade = size
                big_trades.append(data)
        
        # Returns a dataframe of the biggest trades
        big_trades_df = pd.DataFrame(big_trades, columns=['ID', 'SIZE'])
        big_trades_df.set_index('ID', inplace=True)

        return big_trades_df


    ### USER STATS ######
    # Gets the amount of currency things held by a user
    def get_balance(self, user: str) -> int:
        '''
        Gets the amount of currency things held by a user.

        user : discord @mention : <@123456789>
        '''

        output = self.blockchain.groupby(['OUTPUT']).sum()                              # OUTPUT Dataframe - sums all currency things SENT TO each user - where the user is on the OUTPUT side of the trade
        input = self.blockchain.groupby(['INPUT']).sum()                                # INPUT  Dataframe - sums all currency things SENT BY each user - where the user is on the INPUT  side of the trade

        try:    sent = input.loc[user]['SIZE']                                          # Check in case a user has only received and never sent to avoid Key Errors in the INPUT table
        except: sent = 0       

        balance = output.loc[user]['SIZE'] - sent                                       # Subtracts the amount sent (INPUT table) from the amount received (OUTPUT table) to get the current balance
        return int(balance)                                                             # Converting numpy int64 to int
    

    # Getting the balance of all Currency Thing users
    def get_balance_all(self) -> pd.DataFrame:
        '''
        Returns the balance of every currency thing user as a DataFrame.\n
        [ USER | SIZE ]
        '''
        received = self.blockchain.groupby(['OUTPUT']).sum()                            # OUTPUT Dataframe - sums all currency things SENT TO each user
        sent = self.blockchain.groupby(['INPUT']).sum()                                 # INPUT  Dataframe - sums all currency things SENT BY each user

        balances = pd.DataFrame(index=received.index, columns=['SIZE'])                 # Creating an empty dataframe with a Size column using the Users from the received dataframe
        balances['SIZE'] = received['SIZE'].sub(sent['SIZE'], fill_value=0)             # Subtracts the Sent col from the Received Col, treating null values as 0
        balances = balances.astype(int)                                                 # Converts SIZE from float to int
        balances.index.names = ['USER']                                                 # Sets the Index title as USER

        return balances
    

    def mined_by_user(self, user: str) -> int:
        '''
        Returns how many currency things a user has mined in total.
        user: discord @mention
        '''
        b = self.blockchain
        user_mined = b.loc[(b['INPUT'] == CREATOR) & (b['OUTPUT'] == user)]             # All currency things sent by the Currency Thing bot to the requested User : mined by user
        total_mined = user_mined.groupby(['OUTPUT']).sum()['SIZE']                      # Summing up the total mining output

        return int (total_mined)
    

    def user_things_sent(self, user: str) -> int:
        '''
        Gets the total amount of currency things that a user has sent to others.
        user : discord @mention : <@123456789>
        '''
        input = self.blockchain.groupby(['INPUT']).sum()                                # INPUT Dataframe - sums all currency things SENT BY each user - where the user is on the INPUT side of the trade

        try:    sent = input.loc[user]['SIZE']                                          # Check in case a user has only received and never sent to avoid Key Errors in the Input table
        except: sent = 0

        return int(sent)
    

    def user_things_received(self, user: str) -> int:
        '''
        Gets the amount of currency things sent to this user by others.
        user : discord @mention : <@123456789>
        '''
        # Filters rows where the INPUT was NOT Currency Thing AND the OUTPUT was the desired user
        b = self.blockchain
        filtered = b.loc[(b['INPUT'] != CREATOR) & (b['OUTPUT'] == user)]

        # Sums the results
        things_received = filtered['SIZE'].sum()
        
        return int(things_received)
    

    ### CUMULATIVE USER STATS ######
    def balance_over_time(self, user: str, date_index = False) -> pd.DataFrame:
        '''
        The cumulative amount of currency things held by the user over time.\n
        Returns a dataframe [ ID | SIZE | TIME ]

        user : discord @mention : <@123456789>
        '''
        b = self.blockchain
        received = b.loc[b['OUTPUT'] == user]                       # All currency things received by this user
        sent = b.loc[b['INPUT'] == user]                           # All currency things sent by this user

        sent['SIZE'] = sent['SIZE'] * - 1                                               # Turns sent things into negtaive transactions

        networth = pd.concat([received, sent])                                          # Combines both dataframes

        if date_index:
            networth.set_index('TIME', drop=True, inplace=True)                         # Sets the Datetime column as Index
            networth.drop(['ID'], axis=1, inplace=True)                                 # Removes the TX ID column
        else:
            networth.set_index('ID', drop=True, inplace=True)                           # Sets the ID column as Index
            networth.drop(['TIME'], axis=1, inplace=True)                               # Removes the datetime column

        networth.drop(['INPUT', 'OUTPUT', 'PREV_HASH'], axis=1, inplace=True)           # Removes all other unnecessary columns
        # networth = networth.sort_index(axis=0)                                          # Sorts the values chronologically by ID

        networth = networth.cumsum()                                                    # Finally, the cumulative amount of currency things held at each point

        return networth


 

    ### MILESTONES ######
    def who_mined_nth_thing(self, thing: int, cum_supply: pd.DataFrame) -> tuple[int, int]:
        '''
        Finds the TX ID where the nth Currency Thing was mined.\n
        Returns tuple (nth thing, TX ID)
        '''
        # Getting all trades where the supply is EQUAL OR MORE than the amount we're looking for (the first trade after the thousandth milestone is the winner)
        tx = cum_supply.loc[cum_supply['SUPPLY'] >= thing].head(1)
        id = tx.index[0]
        
        return (thing, id)
        

    def get_mining_milestones(self) -> pd.DataFrame:
        '''
        Looks up who mined each Milestone thing.\n
        Returns a DataFrame with milestone, tx id at which it was reached. (and TODO who mined it)
        '''
        print('[EXPLORER] >>> Getting Mining Milestones')

        # getting the latest thousandth thing milestone - ROUNDED DOWN
        latest = (self.supply // 1000) * 1000
        milestones = [1] + list(range(1000, latest + 1000, 1000)) # generating a list of all the thousands, but starting at 1

        supply_over_tx = self.supply_over_tx()

        # A list of tuples containing the Milestone reached, and the Trade ID where it was reached, for each milestone specified above
        mile_txs = [self.who_mined_nth_thing(thing, supply_over_tx) for thing in milestones]

        # Converting the list of tuples into a dataframe and saving it to disk
        milestones_df = pd.DataFrame(mile_txs, columns=['MILESTONE', 'TXID'])#.set_index('MILESTONE')
        return milestones_df
            






if __name__ == '__main__':
    print('hello?')
    ex = Explorer()
    # print(ex.supply)
    # print(ex.supply_over_tx(ex.blockchain))
    # print(ex.tx_by_time(100))
    # print(ex.biggest_trade(-5))
    print(ex.mined_by_user('<@216972321099874305>'))
    # print(ex.mined_per_day())
    # print(ex.mined)
    # print(ex.biggest_trade_over_time())
    # print(ex.get_balance_all())
    print(ex.balance_over_time('<@216972321099874305>', True))
    print(ex.get_balance('<@216972321099874305>'))
    print(ex.get_balance_all())
else:
    print('[EXPLORER.PY IMPORTED]')
    
    

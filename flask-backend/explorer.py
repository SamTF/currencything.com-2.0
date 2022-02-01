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
    

    def num_of_trades(self, days = 0, user_only = False) -> int:
        '''
        Returns the total number of trades on the Blockchain.

        days: if specified, only counts TXs from the last X days.
        user_only: only displays trades executed by users and not by the Currency Thing bot
        '''
        trades = self.blockchain if days < 1 else self.tx_by_time(days)                     # checks entire blockchain, or last few days if "days" value is specified
        print(trades)

        if user_only:
            trades = trades.loc[trades['INPUT'] != CREATOR]                                 # Only count rows where the Currency Thing Bot was not involved

        return len(trades.index)                                                            # returns the number of rows in the (filtered?) dataframe
    
    def things_mined_by_time(self, days = 0) -> int:
        '''
        Returns the total amount of currency things mined in the last X days as an INT.

        days: if specified, only counts TXs from the last X days.
        '''
        rows = self.blockchain if days < 1 else self.tx_by_time(days)                       # checks entire blockchain, or last few days if "days" value is specified
        mined = rows.loc[rows['INPUT'] == CREATOR]                                          # Gets all trades where the Currency Thing Bot is the one sending things
        mined = mined['SIZE'].sum()                                                         # Sums the size of currency things sent

        return int(mined)


    def biggest_trade(self, days = 0) -> int:
        '''
        Returns the trade with the largest size.

        days: if specified, only counts TXs from the last X days.
        '''
        rows = self.blockchain if days < 1 else self.tx_by_time(days)                       # checks entire blockchain, or last few days if "days" value is specified

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


    # Cumulative sum of currency things at each transastion
    def supply_over_tx(self, blockchain: pd.DataFrame) -> pd.DataFrame:
        '''
        Returns a DataFrame with the total amount of currency things in circulation at each transaction ID.\n
        [ ID | SUPPLY ]
        '''
        print('[EXPLORER] >>> SUPPLY OVER TX')
        mints = blockchain.loc[blockchain['INPUT'] == CREATOR]                              # All currency things sent by the Currency Thing bot (mined)
        mints.drop(['ID', 'INPUT', 'OUTPUT', 'PREV_HASH', 'TIME'], axis=1, inplace=True)    # Removes unnecessary columns

        supply = mints.cumsum().rename(columns={'SIZE': 'SUPPLY'})                          # cumulative sums the mining rewards, and renames the col to Supply
        return supply
    
    

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

        supply_over_tx = self.supply_over_tx(self.blockchain)

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
    print(ex.biggest_trade(-5))
    
    

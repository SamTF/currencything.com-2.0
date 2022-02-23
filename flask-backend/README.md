# Currency Thing API

This API powered by Flask is what the frontend uses to communicate with the Currency Thing blockchain. It reads the blockchain data directly from disk, updated in real-time, and manipulates it in any way required. It can also draw SVG graphs using this data and return the SVG code.

**Base URL: http://v2.currencything.com/api/**

## API Routes

 - **/blockchain**
	 - Returns the entire blockchain as an array of JSON objects in chronological order.
	 - optional arg: `?descending=true` to sort by newest transaction
	##
 - **/blockchain/@[username]**
	 - Returns every transactions involving the given user
	 - `username`: Discord username of the person. Ex: /blockchain/@Sam
	 - optional arg: `?descending=true` to sort by newest transaction
	##
 - **/blockchain/milestones**
	 - Returns a dictionary of every 1000<sup>th</sup> currency thing mined.
	 - Key: TX ID; value: n<sup>th</sup> thing mined
	##
 - **/blockchain/stats**
	 - Returns cool stats, like total supply, things mined, user trades, and biggest trade
	 - optional arg: `?period=[int]` to filter stats to only the last [int] days
	 ##
 - **/blockchain/stats/@[username]**
	 - Same as above, but featuring user=specific stats
	##
 - **/blockchain/stats/@[username]/graphs**
	 - This one is interesting. It renders two graphs, currencything balance and number of trades over time, and returns them as SVG code


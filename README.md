# Backtesting-Framework

pnl.py computes the pnl (Profit & Loss) for our OHLC (Open, High, Low, Close) financial dataset.

At time t, it checks Close price. From Close price, with the hyperparameters (A, k, sigma, gamma, etc) it computes an ideal bid and ask quote.
At time t, it checks if the previous bid and ask quotes are filled with the simple heuristic: if low < bid_quote < high it is filled. Similarly for ask_quote.

If the above conditions are true (bid_filled, ask_filled), it adjust the following 4 variables : 
- the inventory q
- the inventory_value ( = q*price)
- the cash amount
- the pnl ( = inventory_value + cash)

It adds these 4 variables to the dataframe and saves it to a new .csv

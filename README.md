# Backtesting-Framework

pnl.py computes the pnl (Profit & Loss) for our OHLC (Open, High, Low, Close) financial dataset.

At time t, it checks Close price. From Close price, with the hyperparameters (A, k, sigma, gamma, etc) it computes a best bid and ask quote.
At time t+1, it checks if the previous bid and ask quotes are filled with the simple heuristic: if low < bid_quote < high, it means the bid would have been filled (in which case q(t+1) = q(t) +1, and similarly we re-adjust the variables below). Similarly for ask_quote.

If the above conditions are true (bid_filled, ask_filled), it adjust the following 4 variables : 
- the inventory q
- the inventory_value ( = q*price)
- the cash amount
- the pnl ( = inventory_value + cash)

It adds these 4 variables to the dataframe and saves it to a new .csv

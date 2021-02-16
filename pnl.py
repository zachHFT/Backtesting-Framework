import math
import pandas as pd
import run


def compute_pnl(file_path):

    # setting the hyperparameters
    k = 0.1
    a = 0.03
    gamma = 1
    delta = 0.001
    sigma = 0.0015
    q = 0

    df = pd.read_csv(file_path, delimiter=',')
    df = df[['time', 'open', 'high', 'low', 'close', 'Volume', 'Volume MA']]
    df = df.rename(columns={"time": "timestamp"})

    n = len(df['timestamp'])
    print('len(dataset[timestamp])q: ', n)

    # choose for how many data points you want to run the simulation on
    # starting point and endpoint of the dataset
    i = 0
    end = 5000
    dataset = df.iloc[i:end]

    dataset['delta_bid'] = 0.0
    dataset['bid_quote'] = 0.0
    dataset['delta_ask'] = 0.0
    dataset['ask_quote'] = 0.0
    dataset['cash'] = 0.0
    dataset['inventory_value'] = 0.0
    dataset['q'] = 0.0
    dataset['pnl'] = 0.0

    dataset['q'][0] = 0
    dataset['cash'][0] = 0
    dataset['inventory_value'][0] = dataset['q'][0] * dataset['close'][0]
    dataset['pnl'][0] = dataset['inventory_value'][0] + dataset['cash'][0]

    for index in range(i + 1, len(dataset['timestamp'])):

        # print('index %i' % index)
        dataset['delta_bid'] = 1.0 / k
        # print('delta_bid_%i: %f' % (index, (dataset['delta_bid'][index])))

        dataset['bid_quote'][index] = dataset['close'][index - 1] - dataset['delta_bid'][index]
        # print('bid_quote_%i: %f' % (index, (dataset['bid_quote'][index])))

        dataset['delta_ask'] = 1.0 / k
        # print('delta_ask_%i: %f' % (index, dataset['delta_ask'][index]))

        dataset['ask_quote'][index] = dataset['close'][index - 1] + dataset['delta_ask'][index]
        # print('ask_quote_%i: %f' % (index, (dataset['ask_quote'][index])))

        # define boolean variables if bid was filled and ask was filled
        bid_filled = (dataset['bid_quote'][index] > dataset['low'][index])
        # print('bid_filled:', bid_filled)
        ask_filled = (dataset['ask_quote'][index] < dataset['high'][index])
        # print('ask_filled:', ask_filled)

        if bid_filled and ask_filled:
            # print('bid and ask filled at step %i' % index)
            dataset['q'][index] = dataset['q'][index - 1]
            dataset['cash'][index] = dataset['cash'][index - 1] + delta * (dataset['ask_quote'][index] - (dataset['bid_quote'][index]))
            dataset['inventory_value'][index] = dataset['q'][index] * dataset['close'][index]
            dataset['pnl'][index] = dataset['inventory_value'][index] + dataset['cash'][index]

        elif bid_filled and not ask_filled:
            # print('bid filled and ask NOT filled at step %i' % index)
            dataset['q'][index] = dataset['q'][index - 1] + delta
            dataset['cash'][index] = dataset['cash'][index - 1] + delta * (0 - (dataset['bid_quote'][index]))
            dataset['inventory_value'][index] = dataset['q'][index] * dataset['close'][index]
            dataset['pnl'][index] = dataset['inventory_value'][index] + dataset['cash'][index]

        elif ask_filled and not bid_filled:
            # print('bid NOT filled and ask filled at step %i' % index)
            dataset['q'][index] = dataset['q'][index - 1] - delta
            dataset['cash'][index] = dataset['cash'][index - 1] + delta * (dataset['ask_quote'][index] - 0)
            dataset['inventory_value'][index] = dataset['q'][index] * dataset['close'][index]
            dataset['pnl'][index] = dataset['inventory_value'][index] + dataset['cash'][index]

        else:
            # print('bid NOT filled and ask NOT filled at step %i' % index)
            dataset['q'][index] = dataset['q'][index - 1]
            dataset['cash'][index] = dataset['cash'][index - 1]
            dataset['inventory_value'][index] = dataset['q'][index] * dataset['close'][index]
            dataset['pnl'][index] = dataset['inventory_value'][index] + dataset['cash'][index]

        # print('cash_%i: %f' % (index, dataset['cash'][index]))
        # print('inventory_value_%i: %f' % (index, dataset['inventory_value'][index]))
        print('step n°%i: cash = %f | inventory_value = %f | q = %f | pnl: = %f' % (index, dataset['cash'][index], dataset['inventory_value'][index], dataset['q'][index], dataset['pnl'][index]))
        if bid_filled:
            print('bid!')
        if ask_filled:
            print('ask!')

    dataset.to_csv(file_path[:-4] + '-pnl-estimation-v1.csv')

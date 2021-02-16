import pandas as pd
import pnl
import os


def main():

    # build the file_path
    current_directory = os.getcwd()
    print('current directory: %s' % current_directory)
    data_directory = current_directory + '/Data/Tradingview/ISOtime'
    print('data directory: %s' % data_directory)
    filename = 'BINANCE BTCEUR, 1S.csv'
    print('filename: %s' % filename)
    file_path = data_directory + '/' + filename

    # run the pnl (profit & loss) back-testing engine
    pnl.compute_pnl(file_path)


if __name__ == '__main__':
    main()

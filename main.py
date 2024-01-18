import os
import json
import pandas as pd
from datetime import datetime as dt
 

req_columns = [
    "Trade Id",
    "Version",
    "Counter Party Id",
    "Book Id",
    "Maturity Date",
    "Created Date",
    "Expired"
    ]

store_path = "./trade_store/trade_store.csv"
new_trades_path = "./new_trades"
date_fmt = "%d/%m/%Y"
today = dt.now()


def create_store():
    """ If store csv file doesn't exists. This function creates empty file"""

    if not os.path.isfile(store_path):
        with open(store_path, 'w') as store:
            store.write(",".join(req_columns))


def get_trade_versions(trade_id: str, trade_store: pd.DataFrame):
    """ Get all versions for given trade id
    
        Parameters
            trade_id (str): Trade Id for which version list is required
            trade_store (pd.DataFrame): Trade Store DataFrame

        Returns
            cur_versions (pd.DataFrame): List of all trades for given trade id
    """

    cur_versions = trade_store.loc[trade_store['Trade Id'] == trade_id]
    return cur_versions


def valid_version(trade: dict, trade_store: pd.DataFrame):
    """ Check whether given trade has valid version or not

        Parameters
            trade (dict): Trade which needs to be validated
            trade_store (pd.DataFrame): Trade Store DataFrame

        Returns
            str: Type of the trade (New/Existing/Rejected)
    """

    trade_id = trade['trade_id']
    trade_version = trade['version']

    cur_trade_versions = get_trade_versions(trade_id, trade_store)
    max_cur_version = cur_trade_versions['Version'].max()

    if max_cur_version < trade_version or cur_trade_versions.empty:
        return "New Trade"
    elif max_cur_version == trade_version:
        return "Existing Trade"
    else:
        return "Rejected Trade"


def valid_maturity_date(trade: dict):
    """ Check whether given trade is valid maturity date or not
    
        Parameters
            trade (dict): Trade which needs to be validated

        Returns
            bool: Whether trade is valid or not
    """

    trade_mat_date = dt.strptime(trade['maturity_date'], date_fmt)
    if trade_mat_date.date() < today.date():
        return False
    return True


def add_trade(trade: dict, trade_store: pd.DataFrame):
    """ Add new trade to Trade Store DataFrame

        Parameters
            trade (dict): Trade which needs to be added
            trade_store (pd.DataFrame): Trade Store DataFrame in which trade 
                                        needs to be added

        Returns
            trade_store (pd.DataFrame): Updated Trade Store DataFrame
    """

    new_trade = [
        trade['trade_id'],
        trade['version'],
        trade['counter_party_id'],
        trade['book_id'],
        trade['maturity_date'],
        today.strftime(date_fmt),
        'N'
    ]
    trade_store.loc[len(trade_store.index)] = new_trade
    return trade_store


def update_trade(trade: dict, trade_store: pd.DataFrame):
    """ Update existing trade to Trade Store DataFrame

        Parameters
            trade (dict): Trade which needs to be updated
            trade_store (pd.DataFrame): Trade Store DataFrame in which trade 
                                        needs to be added

        Returns
            trade_store (pd.DataFrame): Updated Trade Store DataFrame
    """

    new_trade = [
        trade['counter_party_id'],
        trade['book_id'],
        trade['maturity_date'],
        today.strftime(date_fmt),
        'N'
    ]
    trade_store.loc[(trade_store['Trade Id'] == trade['trade_id']) & 
                    (trade_store['Version'] == trade['version']), 
                    ["Counter Party Id", "Book Id", "Maturity Date", 
                     "Created Date", "Expired"]] = new_trade
    return trade_store


def main():
    """ Main Function
    """

    create_store()
    trade_store = pd.read_csv(store_path)

    trades_list = os.listdir(new_trades_path)
    for trade_file in trades_list:
        with open(f"{new_trades_path}/{trade_file}", 'r') as trd_file:
            trades = json.loads(trd_file.read())

        for trd in trades:
            if not valid_maturity_date(trd):
                continue
            ver_validity = valid_version(trd, trade_store)
    
            if ver_validity == 'Rejected Trade':
                try:
                    raise Exception(f"Invalid Version of trade {trd['trade_id']}"\
                                    f"in file {trade_file}")
                except:
                    continue
            elif ver_validity == "Existing Trade":
                trade_store = update_trade(trd, trade_store)
            else:
                trade_store = add_trade(trd, trade_store)

    trade_store.to_csv(store_path, index = False)


def update_expiry():
    """ Update Exipry Flag for the Trades"""

    trade_store = pd.read_csv(store_path)
    trade_store.loc[pd.to_datetime(trade_store["Maturity Date"], format=date_fmt) < 
                    today, 'Expired'] = 'Y'
    trade_store.to_csv(store_path, index = False)

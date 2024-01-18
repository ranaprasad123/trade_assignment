import os
import pandas as pd
import main



def test_create_store():
    """ Test create_store function"""

    if os.path.isfile(main.store_path):
        os.remove(main.store_path)
    main.create_store()
    assert os.path.isfile(main.store_path)


def test_valid_version_1():
    """ Test valid_version function for new trade"""

    test_trade = {
        "trade_id": "T2",
	  "version": 1,
        "counter_party_id": "CP-1",
	  "book_id": "B1",
	  "maturity_date": "18/01/2024"
    }

    test_data = {
        "Trade Id": ["T1"],
        "Version": [1],
        "Counter Party Id": ["CP-1"],
        "Book Id": ["B1"],
        "Maturity Date": ["18/01/2025"],
        "Created Date": ["18/01/2024"],
        "Expired": ["N"]
    }

    test_trade_store = pd.DataFrame.from_dict(test_data)

    assert main.valid_version(test_trade, test_trade_store) == 'New Trade'


def test_valid_version_2():
    """ Test valid_version function for overwrite existing trade"""

    test_trade = {
        "trade_id": "T1",
	  "version": 1,
        "counter_party_id": "CP-2",
	  "book_id": "B1",
	  "maturity_date": "18/01/2024"
    }

    test_data = {
        "Trade Id": ["T1"],
        "Version": [1],
        "Counter Party Id": ["CP-1"],
        "Book Id": ["B1"],
        "Maturity Date": ["18/01/2025"],
        "Created Date": ["18/01/2024"],
        "Expired": ["N"]
    }

    test_trade_store = pd.DataFrame.from_dict(test_data)

    assert main.valid_version(test_trade, test_trade_store) == 'Existing Trade'

def test_valid_version_3():
    """ Test valid_version function for rejected trade"""

    test_trade = {
        "trade_id": "T1",
	  "version": 1,
        "counter_party_id": "CP-1",
	  "book_id": "B1",
	  "maturity_date": "18/01/2024"
    }

    test_data = {
        "Trade Id": ["T1", "T1"],
        "Version": [1, 2],
        "Counter Party Id": ["CP-1", "CP-1"],
        "Book Id": ["B1", "B1"],
        "Maturity Date": ["18/01/2025", "18/01/2025"],
        "Created Date": ["17/01/2024", "18/01/2024"],
        "Expired": ["N", "N"]
    }

    test_trade_store = pd.DataFrame.from_dict(test_data)

    assert main.valid_version(test_trade, test_trade_store) == 'Rejected Trade'
    
    
def test_valid_maturity_date_1():
    """ Test valid_maturity_date function for valid trade"""

    test_trade = {
        "trade_id": "T1",
	  "version": 1,
        "counter_party_id": "CP-1",
	  "book_id": "B1",
	  "maturity_date": "18/01/2025"
    }

    assert main.valid_maturity_date(test_trade) == True

def test_valid_maturity_date_2():
    """ Test valid_maturity_date function for invalid trade"""

    test_trade = {
        "trade_id": "T1",
	  "version": 1,
        "counter_party_id": "CP-1",
	  "book_id": "B1",
	  "maturity_date": "18/01/2023"
    }

    assert main.valid_maturity_date(test_trade) == False


def test_add_trade():
    """ Test add_trade function"""

    test_trade = {
        "trade_id": "T2",
	  "version": 1,
        "counter_party_id": "CP-1",
	  "book_id": "B1",
	  "maturity_date": "18/01/2025"
    }

    test_data = {
        "Trade Id": ["T1", "T1"],
        "Version": [1, 2],
        "Counter Party Id": ["CP-1", "CP-1"],
        "Book Id": ["B1", "B1"],
        "Maturity Date": ["17/01/2024", "18/01/2025"],
        "Created Date": ["17/01/2023", "18/01/2024"],
        "Expired": ["Y", "N"]
    }

    test_trade_store = pd.DataFrame.from_dict(test_data)

    expected_data = {
        "Trade Id": ["T1", "T1", "T2"],
        "Version": [1, 2, 1],
        "Counter Party Id": ["CP-1", "CP-1", "CP-1"],
        "Book Id": ["B1", "B1", "B1"],
        "Maturity Date": ["17/01/2024", "18/01/2025", "18/01/2025"],
        "Created Date": ["17/01/2023", "18/01/2024", "18/01/2024"],
        "Expired": ["Y", "N", "N"]
    }

    expected_trade_store = pd.DataFrame.from_dict(expected_data)
    actual_trade_store = main.add_trade(test_trade, test_trade_store)

    assert actual_trade_store.equals(expected_trade_store)


def test_update_trade():
    """ Test update_trade function"""

    test_trade = {
        "trade_id": "T1",
	  "version": 2,
        "counter_party_id": "CP-1",
	  "book_id": "B2",
	  "maturity_date": "18/01/2026"
    }

    test_data = {
        "Trade Id": ["T1", "T1"],
        "Version": [1, 2],
        "Counter Party Id": ["CP-1", "CP-1"],
        "Book Id": ["B1", "B1"],
        "Maturity Date": ["17/01/2024", "18/01/2025"],
        "Created Date": ["17/01/2023", "18/01/2024"],
        "Expired": ["Y", "N"]
    }

    test_trade_store = pd.DataFrame.from_dict(test_data)

    expected_data = {
        "Trade Id": ["T1", "T1"],
        "Version": [1, 2],
        "Counter Party Id": ["CP-1", "CP-1"],
        "Book Id": ["B1", "B2"],
        "Maturity Date": ["17/01/2024", "18/01/2026"],
        "Created Date": ["17/01/2023", "18/01/2024"],
        "Expired": ["Y", "N"]
    }

    expected_trade_store = pd.DataFrame.from_dict(expected_data)
    actual_trade_store = main.update_trade(test_trade, test_trade_store)

    assert actual_trade_store.equals(expected_trade_store)


def test_main():
    """ Test main function"""

    if os.path.isfile(main.store_path):
        os.remove(main.store_path)

    test_data = {
        "Trade Id": ["T1", "T1"],
        "Version": [1, 2],
        "Counter Party Id": ["CP-1", "CP-1"],
        "Book Id": ["B1", "B1"],
        "Maturity Date": ["17/01/2024", "18/06/2024"],
        "Created Date": ["14/01/2023", "14/01/2024"],
        "Expired": ["Y", "N"]
    }

    test_trade_store = pd.DataFrame.from_dict(test_data)
    test_trade_store.to_csv(main.store_path, index = False)

    expected_data = {
        "Trade Id": ["T1", "T1", "T2"],
        "Version": [1, 2, 1],
        "Counter Party Id": ["CP-1", "CP-1", "CP-1"],
        "Book Id": ["B1", "B1", "B1"],
        "Maturity Date": ["17/01/2024", "18/01/2025", "18/01/2025"],
        "Created Date": ["14/01/2023", "18/01/2024", "18/01/2024"],
        "Expired": ["Y", "N", "N"]
    }

    expected_trade_store = pd.DataFrame.from_dict(expected_data)

    main.main()

    actual_trade_store = pd.read_csv(main.store_path)

    assert actual_trade_store.equals(expected_trade_store)


def test_update_expiry():
    """ Test update_expiry function"""

    if os.path.isfile(main.store_path):
        os.remove(main.store_path)

    test_data = {
        "Trade Id": ["T1", "T1"],
        "Version": [1, 2],
        "Counter Party Id": ["CP-1", "CP-1"],
        "Book Id": ["B1", "B1"],
        "Maturity Date": ["17/01/2024", "18/01/2025"],
        "Created Date": ["17/01/2023", "18/01/2024"],
        "Expired": ["N", "N"]
    }

    test_trade_store = pd.DataFrame.from_dict(test_data)
    test_trade_store.to_csv(main.store_path, index = False)

    expected_data = {
        "Trade Id": ["T1", "T1"],
        "Version": [1, 2],
        "Counter Party Id": ["CP-1", "CP-1"],
        "Book Id": ["B1", "B1"],
        "Maturity Date": ["17/01/2024", "18/01/2025"],
        "Created Date": ["17/01/2023", "18/01/2024"],
        "Expired": ["Y", "N"]
    }

    expected_trade_store = pd.DataFrame.from_dict(expected_data)

    main.update_expiry()

    actual_trade_store = pd.read_csv(main.store_path)

    assert actual_trade_store.equals(expected_trade_store)

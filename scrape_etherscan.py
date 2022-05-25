"""Module used for getting vault contract addresses"""

import sys
import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

ETHERSCAN_EXPORT_CSV_PATH = "./etherscan_export.csv"
VAULT_ADDRESSES_CSV = "./vault_addresses.csv"

METHOD_INDEX = 15
METHOD_VAL = "Create Vault"

STATUS_INDEX = 13
STATUS_VAL = ''


def get_all_txn_hashes_to_visit():
    """Open etherscan vault csv and collect all hashes to visit"""
    transaction_hashes = []
    with open(ETHERSCAN_EXPORT_CSV_PATH, 'r') as in_file:
        csv_reader = csv.reader(in_file)
        for row in csv_reader:
            
            if row[METHOD_INDEX] == METHOD_VAL:
                if row[STATUS_INDEX] == STATUS_VAL:
                    transaction_hashes.append(row[0]) #Hash value

    return transaction_hashes

def visit_hash_and_get_vault_address(driver, txn_hash):
    url = f"https://etherscan.io/tx/{txn_hash}#internal"
    driver.get(url)

    time.sleep(1)

    #Get vault_address
    wait = WebDriverWait(driver, 10)
    try:
        vault_address = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4) > a:nth-child(3)")))
        vault_address = vault_address.text
        assert vault_address, "No vault address!"
        return [txn_hash, vault_address]

    except TimeoutException:
        return [txn_hash, "TIMEOUT"]

def save_addresses_to_csv(address_hash_pairings):
    print("Saving progress...")
    with open(VAULT_ADDRESSES_CSV, 'a') as save_file:
        csv_writer = csv.writer(save_file)
        csv_writer.writerows(address_hash_pairings)
    print("Progress saved!")

def return_visited_hashes():
    hash_list = []
    try:
        with open(VAULT_ADDRESSES_CSV, 'r') as save_file:
            csv_reader = csv.reader(save_file)
            for row in csv_reader:
                hash_list.append(row[0]) #[hash, vault_address]
        return hash_list

    except FileNotFoundError:
        return hash_list

def return_all_vault_addresses():
    vault_addresses = []

    #Get txn hashes
    txn_hashes = get_all_txn_hashes_to_visit()

    hashes_already_visited = return_visited_hashes()

    new_hashes = [h for h in txn_hashes if h not in hashes_already_visited]

    print(f"{len(new_hashes)} new transaction(s) to collect info for")
    
    #Setup driver
    chrome_options = Options()
    #chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)

    for ct, _hash in enumerate(new_hashes):
        print(f"Visiting hash number {ct}...")
        hash_address_list = visit_hash_and_get_vault_address(driver, _hash)
        vault_addresses.append(hash_address_list)

        if ct % 15 == 0:
            save_addresses_to_csv(vault_addresses)
            vault_addresses = []

    if len(vault_addresses) > 0:
        save_addresses_to_csv(vault_addresses)

    driver.quit()
    

if __name__ == "__main__":
    return_all_vault_addresses()

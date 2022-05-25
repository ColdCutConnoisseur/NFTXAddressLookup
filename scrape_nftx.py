"""Module to visit NFTX.io and retrieve contract addresses"""

import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException

VAULT_ADDRESSES_CSV = "./vault_addresses.csv"
ALL_DATA_CSV = "./nftx_vaults_info.csv"
NFT_ADDRESS_SELECTOR = "a.ml-2:nth-child(2)"
WETH_ADDRESS_SELECTOR = "h4.inline-flex:nth-child(5) > span:nth-child(2) > a:nth-child(1)"
ETHERSCAN_BASE_URL = "https://etherscan.io/address/"

def retrieve_vault_addresses_from_csv(csv_file, col_num):
    vault_addresses = []

    try:
        with open(csv_file, 'r') as in_file:
            csv_reader = csv.reader(in_file)
            for row in csv_reader:
                vault_addresses.append(row[col_num])
        return vault_addresses

    except FileNotFoundError:
        return vault_addresses

def visit_nftx_info_page_and_retrieve_data(driver, vault_address):
    url = f"https://nftx.io/vault/{vault_address}/info/"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 30)
        nft_address_element = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, NFT_ADDRESS_SELECTOR)))
        
        nft_address_href = nft_address_element.get_attribute('href')
        nft_address = nft_address_href.replace(ETHERSCAN_BASE_URL, '')

        weth_address_element = driver.find_element(By.CSS_SELECTOR, WETH_ADDRESS_SELECTOR)
        weth_address_href = weth_address_element.get_attribute('href')
        weth_address = weth_address_href.replace(ETHERSCAN_BASE_URL, '')

    except (TimeoutException, NoSuchElementException):
        nft_address = 'ERROR'
        weth_address = 'ERROR'

    return [nft_address, weth_address]

def write_results_to_csv(data_queue):
    print("Writing to csv...")
    with open(ALL_DATA_CSV, 'a') as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerows(data_queue)
    print("Done writing to csv.")
    
def scrape_all():
    """Main"""
    vault_addresses = retrieve_vault_addresses_from_csv(VAULT_ADDRESSES_CSV, 1)

    #Clean 'TIMEOUT's
    vault_addresses = [a for a in vault_addresses if a != "TIMEOUT"]

    existing_vault_addresses =  retrieve_vault_addresses_from_csv(ALL_DATA_CSV, 0)

    new_vault_addresses = [a for a in vault_addresses if a not in existing_vault_addresses]

    if new_vault_addresses:

        print(f"{len(new_vault_addresses)} to retrieve info for.  Retrieving...")

        new_data = []

        driver = webdriver.Chrome()

        for ct, new_vault_address in enumerate(new_vault_addresses):
            print(f"Retrieving info for new vault address num {ct}")
            collection_address, weth_account_address = visit_nftx_info_page_and_retrieve_data(driver, new_vault_address)
            new_data.append([new_vault_address, weth_account_address, collection_address])

            if ct % 15 == 0:
                write_results_to_csv(new_data)
                new_data = []

        if len(new_data) > 0:
            write_results_to_csv(new_data)

        driver.quit()

if __name__ == "__main__":
    scrape_all()

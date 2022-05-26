"""Main script to update Vault addresses"""

from scrape_etherscan import return_all_vault_addresses
from scrape_nftx import scrape_all
from add_collection_slugs_to_csv import update_csv


def main():
    return_all_vault_addresses()
    scrape_all()
    update_csv()


if __name__ == "__main__":
    main()


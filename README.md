# NFTX ADDRESS LOOKUP

##SETUP

Visit https://etherscan.io/exportData?type=address&a=0xbe86f647b167567525ccaafcd6f881f1ee558216 to download all
transaction hashes for the NFTX contract. NOTE: Make sure to set the data start date back a bit.
After the file is downloaded, etiher rename the file to __etherscan_export.csv__ or go into the __scrape_etherscan.py__ file
and change the __ETHERSCAN_EXPORT_CSV_PATH = "./etherscan_export.csv"__ to match the csv file name.
Also don't forget to place the csv file in this project's directory!

Next, run the following...

'''
python scrape_etherscan.py
'''

This will check for any new transaction hashes since the last running of this script.  If any new transaction hashes are found, the script will print out how many new transactions need to be processed, and the script will visit those transaction pages.  If those transactions are not errors (e.g. 'out of gas') and the executed method is 'Create Vault', the script will write the [transaction_hash, NFTX vault contract address] for that transaction to an internal csv file named __vault_addresses.csv__. 

In order to finish pulling data for the new vault addresses run...

'''
python scrape_nftx.py
'''

This script visits the NFTX.io website for each of the new vault addresses in the __vault_addresses.csv__ and will scrape the underlying NFT contract address as well as the sushiswap address.

Finally, run the following in order to get collection slugs for each of the NFT contract addresses.  The final output will be nftx_vaults_info.csv and nftx_vaults_info_w_slugs.csv.

'''
python add_collection_slugs_to_csv.py
'''

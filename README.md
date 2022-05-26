# NFTX ADDRESS LOOKUP

## SETUP

Visit https://etherscan.io/exportData?type=address&a=0xbe86f647b167567525ccaafcd6f881f1ee558216 to download all
transaction hashes for the NFTX contract. NOTE: Make sure to set the data start date back a bit.
After the file is downloaded, etiher rename the file to __etherscan_export.csv__ or go into the __nftx_constants.py__ file
and change the __ETHERSCAN_EXPORT_CSV_PATH = "./csvs/etherscan_export.csv"__ to match the csv file name.
Also don't forget to place the csv file in this project's directory in the __csvs__ folder!

If you have an OpenSea API key, put that in the __nftx_constants.py__ file under the constant __OPENSEA_API_KEY__. NOTE: that if you do provide an 
OpenSea API key that the constant __SLEEP_PERIOD__ can be reduced from 3 seconds.

## Running

Next, run the following...

```
python update_vault_csv.py
```

This will check for any new transaction hashes since the last running of this script.  If any new transaction hashes are found, the script will print out how many new transactions need to be processed, and the script will visit those transaction pages.  If those transactions are not errors (e.g. 'out of gas') and the executed method is 'Create Vault', the script will write the [transaction_hash, NFTX vault contract address] for that transaction to an internal csv file named __vault_addresses.csv__ located in the __csvs__ folder. 

Next, the script visits the NFTX.io website for each of the new vault addresses in the __vault_addresses.csv__ and will scrape the underlying NFT contract address as well as the sushiswap address.

Finally, the OpenSea API is used to return collection slugs for each of the NFT contract addresses.  The final output will be __nftx_vaults_info.csv__ and __nftx_vaults_info_w_slugs.csv__.

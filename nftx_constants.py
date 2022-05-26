"""Hold constants for NFTX"""

#[CONFIGURATION]-----------------------------------------------------------------------------------

OPENSEA_API_KEY = ""
SLEEP_PERIOD = 3     #Time to wait between requests to fetch collection slugs
                     #NOTE: if you provide an API_KEY, this sleep period can be reduced

#--------------------------------------------------------------------------------------------------

#scrape_etherscan.py
ETHERSCAN_EXPORT_CSV_PATH = "./csvs/etherscan_export.csv"
VAULT_ADDRESSES_CSV = "./csvs/vault_addresses.csv"

METHOD_INDEX = 15
METHOD_VAL = "Create Vault"

STATUS_INDEX = 13
STATUS_VAL = ''

VAULT_ADDRESS_SELECTOR = ".table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4) > a:nth-child(3)"

#scrape_nftx.py
VAULT_ADDRESSES_CSV = "./csvs/vault_addresses.csv"
ALL_DATA_CSV = "./csvs/nftx_vaults_info.csv"
NFT_ADDRESS_SELECTOR = "a.ml-2:nth-child(2)"
WETH_ADDRESS_SELECTOR = "h4.inline-flex:nth-child(5) > span:nth-child(2) > a:nth-child(1)"
ETHERSCAN_BASE_URL = "https://etherscan.io/address/"

#add_collection_slugs_to_csv.py
DATA_CSV_PATH = "./csvs/nftx_vaults_info.csv"       #Input
COMBINED_CSV = "./csvs/nftx_vaults_info_w_slug.csv" #With slugs present / Output

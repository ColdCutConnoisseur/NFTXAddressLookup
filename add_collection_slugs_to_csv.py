"""Module for translating collection addresses to collection-slug (OpenSea)"""

import sys
import csv
import time

import requests

import nftx_constants


class SkipError(Exception):
    pass

def return_collections_already_called():
    contract_address_index = 2
    already_called = []
    
    try:
        with open(nftx_constants.COMBINED_CSV, 'r') as outfile:
            csv_reader = csv.reader(outfile)
            for row in csv_reader:
                already_called.append(row[contract_address_index])

        return already_called

    except FileNotFoundError:
        return already_called

def find_data_to_alter(already_called_list):
    data_add_in = []

    collection_address_index = 2
    with open(nftx_constants.DATA_CSV_PATH, 'r') as in_file:
        csv_reader = csv.reader(in_file)
        for row in csv_reader:
            if row[collection_address_index] not in already_called_list:
                data_add_in.append(row)

    return data_add_in


def retrieve_collection_slug(session, asset_contract_address):
    api_endpoint = f"https://api.opensea.io/api/v1/asset_contract/{asset_contract_address}"
    r = session.get(api_endpoint)
    
    if r.status_code == 200:
        as_json = r.json()
        #print(as_json)
        collection_data = as_json['collection']
        if not collection_data:
            raise SkipError
        slug = collection_data['slug']
        print(slug)
        return slug

    else:
        print(f"Bad return code in 'retrieve_collection_slug' call. Status: {r.status_code}")
        if r.status_code == 404 or r.status_code == 406:
            print("Skipping 404/406")
            raise SkipError

        else:
            print("Exiting...")
            sys.exit(0)

def save_to_out_file(revised_data):
    print("Writing to csv...")
    with open(nftx_constants.COMBINED_CSV, 'a') as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerows(revised_data)
    print("Write finished.")

def update_csv():
    already_called_list = return_collections_already_called()

    session = requests.Session()

    session.headers = {'X-API-KEY' : nftx_constants.OPENSEA_API_KEY}

    data_to_alter = find_data_to_alter(already_called_list)

    print(f"{len(data_to_alter)} new transaction(s) to alter")

    revised_data = []

    for ct, record in enumerate(data_to_alter):
        print(record)

        try:
            collection_slug = retrieve_collection_slug(session, record[2])
            revised_data.append(record + [collection_slug])
            #print(revised_data)

        except SkipError:
            time.sleep(nftx_constants.SLEEP_PERIOD)
            continue

        time.sleep(nftx_constants.SLEEP_PERIOD)

        if ct % 15 == 0:
            save_to_out_file(revised_data)
            revised_data = []

    #Write to out file
    if len(revised_data) > 0:
        save_to_out_file(revised_data)
            


if __name__ == "__main__":
    update_csv()

import requests
import json
import time

def generate_url(walletAddress: str) -> str:
    url = f"http://api-mainnet.magiceden.dev/v2/wallets/{walletAddress}/activities?offset=0&limit=100"
    return url

def get_magic_eden_link(tokenMint) -> str:
    base_url = "https://magiceden.io/item-details"
    token_url = f"{base_url}/{tokenMint}"
    return token_url

def recent_activity_check(activitiesList, walletAddress):
    while True:
        new_req = requests.get(generate_url(walletAddress))
        activitiesListCurrent = json.loads(new_req.text)
        if activitiesList[0] != activitiesListCurrent[0]:
            if activitiesListCurrent[0]['type'] != 'bid':
                if activitiesListCurrent[0]['type'] == 'buyNow' and walletAddress != activitiesListCurrent[0]['buyer']:
                    activitiesList[0] = activitiesListCurrent[0]
                    print(f'NFT token was sold for {activitiesListCurrent[0]["price"]} ◎\n Collection: {activitiesListCurrent[0]["collection"]}\nME link: {get_magic_eden_link(activitiesListCurrent[0]["tokenMint"])}\n')
                elif activitiesListCurrent[0]['type'] == 'buyNow' and walletAddress == activitiesListCurrent[0]['buyer']:
                    activitiesList[0] = activitiesListCurrent[0]
                    print(f'NFT token was purchased for {activitiesListCurrent[0]["price"]} ◎\n Collection: {activitiesListCurrent[0]["collection"]}\nME link: {get_magic_eden_link(activitiesListCurrent[0]["tokenMint"])}\n')
                elif activitiesListCurrent[0]['type'] == 'list':
                    activitiesList[0] = activitiesListCurrent[0]
                    print(f'NFT token was listed for {activitiesListCurrent[0]["price"]} ◎\n Collection: {activitiesListCurrent[0]["collection"]}\nME link: {get_magic_eden_link(activitiesListCurrent[0]["tokenMint"])}\n')
                elif activitiesListCurrent[0]['type'] == 'delist':
                    activitiesList[0] = activitiesListCurrent[0]
                    print(f'NFT token was delisted! Collection: {activitiesListCurrent[0]["collection"]}\nME link: {get_magic_eden_link(activitiesListCurrent[0]["tokenMint"])}\n')
        else:
            time.sleep(15)

if __name__ == "__main__":
    walletAddress = input("Enter your wallet here: ")
    req = requests.get(generate_url(walletAddress))
    activitiesList = json.loads(req.text)
    recent_activity_check(activitiesList, walletAddress)

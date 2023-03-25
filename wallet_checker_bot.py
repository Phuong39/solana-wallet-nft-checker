import discord
import asyncio
import requests
import json
from discord.ext import commands
from discord import app_commands

TOKEN = "YOUR TOKEN"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.tree.sync()

def generate_url(walletAddress: str):
    url = f"http://api-mainnet.magiceden.dev/v2/wallets/{walletAddress}/activities?offset=0&limit=100"
    return url

def get_magic_eden_link(tokenMint):
    base_url = "https://magiceden.io/item-details"
    token_url = f"{base_url}/{tokenMint}"
    return token_url

@bot.tree.command(name="check", description="Checks real-time wallet activity")
@app_commands.describe(wallet_address="Enter the wallet adress")
async def check(interaction: discord.Integration, wallet_address: str):
    req = requests.get(generate_url(walletAddress=wallet_address))
    activitiesListOnStart = json.loads(req.text)
    await interaction.response.send_message(f"The wallet {interaction.user.name} has entered is being checked.")
    while True:
        new_req = requests.get(generate_url(wallet_address))
        activitiesListCurrent = json.loads(new_req.text)
        if activitiesListOnStart[0] != activitiesListCurrent[0]:
            if activitiesListCurrent[0]['type'] != 'bid':
                if activitiesListCurrent[0]['type'] == 'buyNow' and wallet_address != activitiesListCurrent[0]['buyer']:
                    await interaction.channel.send(f'NFT token was sold for {activitiesListCurrent[0]["price"]} ◎\nCollection: {activitiesListCurrent[0]["collection"]}\nME link: {get_magic_eden_link(activitiesListCurrent[0]["tokenMint"])}\n')
                    activitiesListOnStart = activitiesListCurrent
                elif activitiesListCurrent[0]['type'] == 'buyNow' and wallet_address == activitiesListCurrent[0]['buyer']:
                    await interaction.channel.send(f'NFT token was purchased for {activitiesListCurrent[0]["price"]} ◎\nCollection: {activitiesListCurrent[0]["collection"]}\nME link: {get_magic_eden_link(activitiesListCurrent[0]["tokenMint"])}\n')
                    activitiesListOnStart = activitiesListCurrent
                elif activitiesListCurrent[0]['type'] == 'list':
                    await interaction.channel.send(f'NFT token was listed for {activitiesListCurrent[0]["price"]} ◎\nCollection: {activitiesListCurrent[0]["collection"]}\nME link: {get_magic_eden_link(activitiesListCurrent[0]["tokenMint"])}\n')
                    activitiesListOnStart = activitiesListCurrent
                elif activitiesListCurrent[0]['type'] == 'delist':
                    await interaction.channel.send(f'NFT token was delisted! Collection: {activitiesListCurrent[0]["collection"]}\nME link: {get_magic_eden_link(activitiesListCurrent[0]["tokenMint"])}\n')
                    activitiesListOnStart = activitiesListCurrent
        else:
            asyncio.sleep(15)

if __name__ == "__main__":
    bot.run(TOKEN)

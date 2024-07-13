from flask import Flask
from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
import os
import re

load_dotenv()

# OpenAI client
oai_client = OpenAI(
    organization=os.getenv("OAI_ORG"),
    project=os.getenv("OAI_PROJECT"),
)

def get_parsed_transaction(tx_hash):
    response = requests.get(f'https://pikespeak.ai/api/contract/parsed-execution-by-hash?hash={tx_hash}')
    return response.json()

def get_account_info(account_id):
    response = requests.get(f'https://pikespeak.ai/api/infos/{account_id}')
    return response.json()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/tx/<tx_hash>")
def explain_tx(tx_hash):
    # Get tx data from pikespeak
    parsed_tx = get_parsed_transaction(tx_hash)
    parsed_tx_str = json.dumps(parsed_tx)

    completion = oai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "extract a list of all wallet addresses appearing in this blockchain transaction data. Addresses must be comma-separated and in one line"},
            {
                "role": "user", "content": f"{parsed_tx_str}"}
        ]
    )

    addresses = completion.choices[0].message.content.split(",")
    # Get some data about the addresses from PikesPeak
    addr_to_info = {}
    for addr in addresses:
        addr_to_info[addr] = get_account_info(addresses)

    completion = oai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eli5 and summarize what a NEAR blockchain transaction is doing based on its data, do not mention technical details. Be concise, and only include details relevant to the main intention behind the transaction"},
            {
                "role": "user",
                "content": f"""Helpful information:\nTx data: {parsed_tx_str}\nAddress info: {addr_to_info}\nClub info: CLUB	WEALTH RANGE
                        WHALE	Over $1M
                        SHARK	From $100k to $1M
                        DOLPHINS	From $10k to $100K
                        OCTOPUS	From $1k to $10K
                        CRAB	From $100 to $1K
                        SEAWEED	From $10 to $100
                        SAND	Above $0"""
            }
        ]
    )
    return { "gpt_res": completion.choices[0].message.content }
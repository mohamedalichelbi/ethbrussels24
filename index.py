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

#NEAR_ACCOUNT_ID_REGEX = ^(?=.{2,64}$)(([a-z\d]+[-_])*[a-z\d]+\.)*([a-z\d]+[-_])*[a-z\d]+$

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/tx/<tx_hash>")
def explain_tx(tx_hash):
    # Get tx data from pikespeak
    parsed_tx = get_parsed_transaction(tx_hash)

    completion = oai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eli5 and summarize what a NEAR blockchain transaction is doing based on its data, do not mention technical details. Be concise, and only include details relevant to the main intention behind the transaction"},
            {"role": "user", "content": json.dumps(parsed_tx)}
        ]
    )
    return { "gpt_res": completion.choices[0].message.content }
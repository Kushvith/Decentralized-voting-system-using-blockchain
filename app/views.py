import datetime
import json
from database.database import PeersDb
import requests
from flask import render_template, redirect, request
from flask import flash
from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.
peerdb = PeersDb()
CONNECTED_SERVICE_ADDRESS = peerdb.read()
POLITICAL_PARTIES = ["Democratic Party","Republican Party","Socialist party"]
VOTER_IDS=[
        'VOID001','VOID002','VOID003',
        'VOID004','VOID005','VOID006',
        'VOID007','VOID008','VOID009',
        'VOID010','VOID011','VOID012',
        'VOID013','VOID014','VOID015']

vote_check=[]

posts = []

# def vot_check():
    
def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    current_len = 0
    for node in CONNECTED_SERVICE_ADDRESS:
        response = requests.get('{}/chain'.format(node))
        length = response.json()['len']
        chain = response.json()['chain']
        if length > current_len:
            current_len = length
            longest_chain = chain
        if longest_chain:
            content = []
            vote_count = []
            chain = json.loads(response.content.decode(encoding="UTF-8"))
            print(chain)
            for block in chain['chain']:
                for tx in block["transactions"]:
                    tx["index"] = block["index"]
                    tx["hash"] = block["previous_hash"]
                    content.append(tx)
                    if block['index'] !=0:
                        if tx['voter_id'] not in vote_check:
                            vote_check.append(tx['voter_id'])

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    fetch_posts()

    vote_gain = []
    for post in posts:
        vote_gain.append(post["party"])
    print(vote_check)
    return render_template('index.html',
                           title='E-voting system '
                                 'using Blockchain and python',
                           posts=posts,
                           vote_gain=vote_gain,
                           node_address=CONNECTED_SERVICE_ADDRESS,
                           readable_time=timestamp_to_string,
                           political_parties=POLITICAL_PARTIES,
                           voter_ids=VOTER_IDS)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    party = request.form["party"]
    voter_id = request.form["voter_id"]

    post_object = {
        'voter_id': voter_id,
        'party': party,
    }
    if voter_id not in VOTER_IDS:
        flash('Voter ID invalid, please select voter ID from sample!', 'error')
        return redirect('/')
    if voter_id in vote_check:
        flash('Voter ID ('+voter_id+') already vote, Vote can be done by unique vote ID only once!', 'error')
        return redirect('/')
    else:
        vote_check.append(voter_id)
        for node in CONNECTED_SERVICE_ADDRESS:
            new_tx_address = "{}/new_transaction".format(node)
            requests.post(new_tx_address,
                    json=post_object,
                    headers={'Content-type': 'application/json'})
            print(vote_check)
            flash('Voted to '+party+' successfully!', 'success')
        return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M')

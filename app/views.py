import datetime
import json
from database.database import PeersDb
import requests
from flask import render_template, redirect, request
from flask import flash
import urllib.parse
from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.

POLITICAL_PARTIES = ["Democratic Party","Republican Party","Socialist party"]
VOTER_IDS=[
        'VOID001','VOID002','VOID003',
        'VOID004','VOID005','VOID006',
        'VOID007','VOID008','VOID009',
        'VOID010','VOID011','VOID012',
        'VOID013','VOID014','VOID015']

vote_check=[]

posts = []


    
def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    peerdb = PeersDb()
    parsed_url = urllib.parse.urlparse(request.host_url)

    new_port = 8000

    parsed_url = parsed_url._replace(netloc=parsed_url.netloc.replace(':5000', ':' + str(new_port)))

    new_url = urllib.parse.urlunparse(parsed_url)

    print(new_url)
    if new_url not in peerdb.read():
        peerdb.write([new_url])
    current_len = 0
    for node in peerdb.read():
        try:
            print(node)
            response = requests.get('{}/chain'.format(node), timeout=3)
            print(f"{node} {response.content}")
            length = response.json().get('len', 0)
            chain = response.json().get('chain', [])
            
            if length > current_len:
                current_len = length
                longest_chain = chain
                
            if longest_chain:
                content = []
                vote_count = []
                chain = response.json().get('chain', [])
                
                for block in chain:
                    for tx in block.get("transactions", []):
                        tx["index"] = block.get("index")
                        tx["hash"] = block.get("previous_hash")
                        content.append(tx)
                        
                        if block.get('index', 0) != 0:
                            if tx.get('voter_id') not in vote_check:
                                print("vote_check", vote_check)
                                vote_check.append(tx.get('voter_id'))
                
                global posts
                posts = sorted(content, key=lambda k: k.get('timestamp', 0), reverse=True)
    
        except requests.exceptions.RequestException:
            # If the node is not reachable, remove it from the peers database
            print("last nodes",node)
            peerdb.remove_node(node)
            

        



@app.route('/')
def index():
    fetch_posts()
    print("fetching the post........")
    vote_gain = []
    for post in posts:
        vote_gain.append(post["party"])
    print(vote_check)
    return render_template('index.html',
                           title='E-voting system '
                                 'using Blockchain and python',
                           posts=posts,
                           vote_gain=vote_gain,
                           node_address="",
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
    peerdb = PeersDb()
    
    if voter_id not in VOTER_IDS:
        flash('Voter ID invalid, please select voter ID from sample!', 'error')
        return redirect('/')
    if voter_id in vote_check:
        flash('Voter ID ('+voter_id+') already vote, Vote can be done by unique vote ID only once!', 'error')
        return redirect('/')
    else:
        for node in peerdb.read():
            new_tx_address = "{}/new_transaction".format(node)
            requests.post(new_tx_address,
                    json=post_object,
                    headers={'Content-type': 'application/json'})
            vote_check.append(voter_id)
            flash('Voted to '+party+' successfully!', 'success')
        return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M')

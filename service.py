from hashlib import sha256
import json
import time

from flask import Flask, redirect, request,render_template, url_for
import requests

from database.database import BlockChainDb, PeersDb


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self,block):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(block.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain():
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        super().__init__

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], 0, "0")
        genesis_block.hash = genesis_block.compute_hash(genesis_block)
        self.write_on_disk([genesis_block.__dict__])
    def write_on_disk(self,block):
        blockchainDb = BlockChainDb()
        blockchainDb.write(block)
    def last_block(self):
        blockchaindb = BlockChainDb()
        return blockchaindb.lastBlock()
   

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        print(block)
        previous_hash = self.last_block()['hash']

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.write_on_disk([block.__dict__])
        return True

    @staticmethod
    def proof_of_work(block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash(block)

        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash(block)

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash(block))

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block['hash']
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            print(block)
            delattr(block, block['hash'])

            if not cls.is_valid_proof(block, block_hash) or \
                    previous_hash != block['previous_hash']:
                result = False
                break

            block['hash'], previous_hash = block_hash, block_hash

        return result

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block()
        print(last_block)
        new_block = Block(index=last_block['index'] + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block['hash'])

        proof = self.proof_of_work(block=new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []

        return True


app = Flask(__name__)

# the node's copy of blockchain
blockchain = Blockchain()
blockchaindb = BlockChainDb()

if not blockchaindb.lastBlock():
    blockchain.create_genesis_block()

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["voter_id", "party"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

    tx_data["timestamp"] = time.time()

    blockchain.add_new_transaction(tx_data)

    return "Success", 201

@app.route('/clean_data', methods=['GET'])
def clean_data():
    block = BlockChainDb()
    block.remove_data()
    return "cleared",200 
# endpoint to return the node's copy of the chain.
# Our application will be using this endpoint to query
# all the posts to display.
@app.route('/chain', methods=['GET'])
def get_chain():
    blockchaindb = BlockChainDb()
    peer = PeersDb()
    #a = consensus()
    return json.dumps({'len':len(blockchaindb.read()),'chain':blockchaindb.read(),'peers':peer.read()})
    # return render_template("chain.html",chain= {'len':len(blockchaindb.read()),'chain':blockchaindb.read(),'peers':peer.read()})
   
@app.route('/chain_ui', methods=['GET'])
def ui_chain():
    blockchaindb = BlockChainDb()
    peer = PeersDb()
    #a = consensus()
    # return json.dumps({'len':len(blockchaindb.read()),'chain':blockchaindb.read(),'peers':peer.read()})
    return render_template("chain.html",chain= {'len':len(blockchaindb.read()),'chain':blockchaindb.read(),'peers':peer.read()})
 

# endpoint to request the node to mine the unconfirmed
# transactions (if any). We'll be using it to initiate
# a command to mine from our application itself.

@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    length = len(blockchain.unconfirmed_transactions)
    message = ""
    if not result:
        message = "No transactions to mine"
    else:
        blockchaindb = BlockChainDb()
        # Making sure we have the longest chain before announcing to the network
        chain_length = len(blockchaindb.read())
        consensus()
        if chain_length == len(blockchaindb.read()):
            # announce the recently mined block to the network
            announce_new_block(blockchain.last_block())
        message = "Block #{} is mined.".format(blockchain.last_block()['index'])
        # Redirect to /minedash with parameters length and message
        return redirect(url_for('mine_unconfirm', length=length, message=message))

@app.route('/minedash', methods=['GET'])
def mine_unconfirm():
    length = request.args.get('length') 
    if not length:
        length = len(blockchain.unconfirmed_transactions)
    message = request.args.get('message') 
    return render_template("mine.html", length=int(length), message=message)

@app.route("/register_node",methods=['POST'])
def register_new_node():
    node_address = request.get_json()["node_address"]
    host_url = request.get_json()["host_url"]
    if not node_address:
        return "invalid data",400
    peerdb = PeersDb()
    if host_url not in peerdb.read():
        peerdb.write([host_url])
    if node_address not in peerdb.read():
        peerdb.write([node_address])
    return get_chain()



@app.route('/register_with', methods=['GET','POST'])
def register_with_existing_node():
    """
    Internally calls the `register_node` endpoint to
    register current node with the node specified in the
    request, and sync the blockchain as well as peer data.
    """
    message = ""
    peerdb = PeersDb()
    if request.method == "POST":
        node_address = request.form["node_address"]
        if node_address not in peerdb.read():
            peerdb.write([node_address])
        if not node_address:
            return "Invalid data", 400
        if request.host_url not in peerdb.read():
            peerdb.write([request.host_url])
        data = {"node_address":node_address,"host_url":request.host_url}
        headers={'Content-Type':"application/json"}
        response = requests.post(node_address+"/register_node",data=json.dumps(data),headers=headers)
    # update(node_address)
    
        if response.status_code == 200:
            chain_dump = response.json()['chain']
            
            blockchain = create_chain_from_dump(chain_dump)
                                                
            message = "Registration successful" 
    return render_template('peers.html',message=message)

def create_chain_from_dump(chain_dump):
    blockchaindb = BlockChainDb()
    blockchaindb.remove_all()
    generated_blockchain = Blockchain()
    generated_blockchain.create_genesis_block()
    
  
    for idx, block_data in enumerate(chain_dump):
        if block_data['index'] == 0:
            continue  # skip genesis block
        
        block = Block(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"],
                      block_data["nonce"])
        proof = block_data['hash']
        print(block_data)
        added = generated_blockchain.add_block(block, proof)
        if not added:
            raise Exception("The chain dump is tampered!!")
    return generated_blockchain



# endpoint to add a block mined by someone else to
# the node's chain. The block is first verified by the node
# and then added to the chain.
@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["transactions"],
                  block_data["timestamp"],
                  block_data["previous_hash"],
                  block_data["nonce"])

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400
    blockchain.unconfirmed_transactions = []
    return "Block added to the chain", 201


# endpoint to query unconfirmed transactions
@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)


def consensus():
    """
    Our naive consnsus algorithm. If a longer valid chain is
    found, our chain is replaced with it.
    """
    blockchaindb = BlockChainDb()
    blockchain = {'chain':blockchaindb.read()}
    blockchai = Blockchain()
    longest_chain = None
    peerdb = PeersDb()
    peers = peerdb.read()
    current_len = len(blockchain['chain'])
    for node in peers:
        response = requests.get('{}/chain'.format(node))
        length = response.json()['len']
        chain = response.json()['chain']
        if length > current_len:
            current_len = length
            longest_chain = chain
    
    if longest_chain:
        blockchaindb.write(longest_chain)
        return True

    return False


def announce_new_block(block):
    """
    A function to announce to the network once a block has been mined.
    Other blocks can simply verify the proof of work and add it to their
    respective chains.
    """
    peerdb = PeersDb()
    for peer in peerdb.read():
        url = "{}/add_block".format(peer)
        headers = {'Content-Type': "application/json"}
        requests.post(url,
                      data=json.dumps(block, sort_keys=True),
                      headers=headers)
        print(peer)

# Uncomment this line if you want to specify the port number in the code
if  __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=8000)

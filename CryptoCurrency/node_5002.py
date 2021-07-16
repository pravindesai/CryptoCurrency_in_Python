# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 12:42:35 2021

@author: Pravin Desai
"""
# http://127.0.0.1:5000/

from flask import Flask, jsonify, request
from CryptoCurrency.Blockchain import Blockchain
import requests
from uuid import uuid4
from urllib.parse import urlparse


app = Flask(__name__)

node_address = str(uuid4()).replace('_', '')

blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)

    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transactions(sender= node_address, receiver= 'Miner2', amount= 1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'msg': 'Congratulations block mined succesfully',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response)


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200


@app.route('/add_transactions', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'elements Missing', 400
    index = blockchain.add_transactions(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to block{index}'}
    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No nodes found", 401
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All nodes connected ',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The chain is replace by longest chain',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All Good, Chain is already longest one',
                    'new_chain': blockchain.chain}
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5002)


# decentralizing

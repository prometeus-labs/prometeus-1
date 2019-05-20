import sys

sys.path.insert(0, '..')

from flask import Flask, Response, request
from web3 import Web3, IPCProvider
import validator, core, time, json, hashlib
from core.utils import eth_create_new_account

app = Flask(__name__)

time.sleep(3)


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Page not found</h1>', 404


@app.route('/init_data_validator')
def init_data_validator():
    my_provider = IPCProvider("../node/chaindata/geth.ipc")
    web3 = Web3(my_provider)
    default_account = web3.eth.accounts[0]
    web3.personal.unlockAccount(default_account, "", 30000)

    eth_account = core.utils.eth_create_new_account(web3, '../node/chaindata/keystore')
    eth_account_check_summ = web3.toChecksumAddress(eth_account["account"])

    tx = web3.eth.sendTransaction(
        {'from': default_account, 'to': eth_account_check_summ, 'value': web3.toWei(1, "ether"), 'gas': 21000})

    time.sleep(2)  # while for node done transaction

    eth_account['balance'] = web3.eth.getBalance(eth_account_check_summ)

    ret = {
        'blockchain_account': eth_account,
    }

    return Response(json.dumps(ret), mimetype='application/json')


@app.route('/init_data_owner', methods=['POST'])
def init_data_owner():
    my_provider = IPCProvider("../node/chaindata/geth.ipc")
    web3 = Web3(my_provider)
    # data = {"data": "data owner data",
    #        "data_validator": "0x" + secrets.token_bytes(20).hex()}
    data = request.get_json()
    if data.get("data") == None or data.get("data_validator") == None:
        return Response('{"error": "Bad request"}', status=400, mimetype='application/json')

    data_validator = data['data_validator']
    encrypted = validator.encrypt2(str(data['data']))
    encrypted_body = encrypted['encrypted']
    encrypted_private_key = encrypted['private_key']
    blockchain_account = eth_create_new_account(web3, '../node/chaindata/keystore')
    encrypted_file_name = f"{blockchain_account['account'].split('0x')[1]}_{data_validator.split('0x')[1]}".lower()
    url_encrypted_file = f"http://storage.prometeus.io/{encrypted_file_name}"

    new_file = open(f"../storage/{encrypted_file_name}", "wb")
    new_file.write(encrypted_body)
    new_file.close()

    ret = {
        'blockchain_account': blockchain_account,
        'storage_url': url_encrypted_file,
        'data_validator': data_validator,
        'private_key': encrypted_private_key.hex(),
        'md5': hashlib.md5(encrypted_body).hexdigest()
    }
    return Response(json.dumps(ret), mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080)

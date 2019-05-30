# Prometeus PoC Quick start

## Install

### Dependencies

```
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install ethereum solc

git clone git@github.com:prometeus-labs/prometeus.git
cd prometeus

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


### Init and start dev node with contract

```
cd node
./init.sh
```

or to start already initialized node

```
geth --dev --datadir chaindata/ --minerthreads 1 console
```

Now dev node with preloaded smart contract is runing on localhost.

Open second terminal and run DataValidator function to initialize new DataOwner
in local dev node.

It will create new blockchain accoount, save encrypted DataOwner for more details see the [link](..)

```
cd ../tests
python transactions.py
``` 
### Install and run own endpoint

```
cd web/src
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```

All dev local endpoints are avaleable now by address

```
curl http://127.0.0.1:8000/
```

### IPFS
TODO


## Prometeus roles 
There are three roles Mart, Validator and Owner in the system. Bellow roles action and tools described.

### DataValidator

To act as Validator role init new Validator account first just after bringing up dev node and endpoints. You are able to create many Validators as you like by call API method:

```
curl http://127.0.0.1:8000/create_account/?type=validator
```

Method returns structure like 

```json
{"blockchain_account": {"account": "0x9e2c064cfb29017445ac2a9d61bd2aa1fd2dbbae", 
                        "identity": "Npo9yyg9Kh2Eb1eog6dwimNRG6Ob9vOmja4KZdFWhs4", 
                        "private": "0xa060f56f7cd0c2462f0db8f94f38adf320690f5fe9ba9f941888e097aec5f81c",
                        "balance": 1000000000000000000}, 
 "system_account": {"login": "login", "password": "password"}}
```
where

*blockchain_account* - is a new Validator account in a blockcahin

*system_account* - system user and password to login into webservice http://127.0.0.1:8000

Initializing data Owner call API POST method */init_owner*

```
curl -H "Content-Type: application/json" --request POST --data '{"data":"xyzsdfsdfsfdsfdsf", "data_validator":"0xb19542ea90295401ed7558077d582b70f208bfba"}' http://127.0.0.1:8000/init_owner
```

Params

```json
{
    "data":"DataOwner data to store",
    "validator": "0x9e2c064cfb29017445ac2a9d61bd2aa1fd2dbbae"
}
```

Method will process data with bellow flow

- creates blokchain account for data Owner and link it with Validator blokchain account
- maps Validator->Owner and store mapping in blockcahin and local DB
- encrypt data Owner data set and save file to the store

Returns


```json
{
    "blockchain_account": {"account": "0x9e2c064cfb29017445ac2a9d61bd2aa1fd2dbbae", 
                           "identity": "CaeguhpOwchd86a_7JXBbBYtWg0JtS7oiTjR6lE7DJQ",
                           "private": "0xd649203af334415a04ab464356bd13b7d26d275456bf97b90549f51a03b3cf7e"},
    "storage_url": "https://storage.prometeus.io/9e2c064cfb29017445ac2a9d61bd2aa1fd2dbbae_9e2c064cfb29017445ac2a9d61bd2aa1fd2dbbae",
    "validator":  "0x9e2c064cfb29017445ac2a9d61bd2aa1fd2dbbae",
    "private_key": "3-j1I7hUZXgymbGL6wZysN_f-7rCfkD72fIDy8hMEE8=",
    "md5": "9a6d26641a37729b316df6b21412e73a"
}
```




## Using Prometeus PoC live endpoint

The system has deployed with local dev geth node and have no any transactions with main blockchain.



*  [https://api.prometeus.io](https://api.prometeus.io) 
* [ https://storage.prometeus.io]( https://storage.prometeus.io)
* [ https://scanner.prometeus.io]( https://scanner.prometeus.io)


### Using API endpoint

[https://api.prometeus.io](https://api.prometeus.io) usage is the same as described in above chapter 'Prometeus roles'.
It aims to play any roles like Mart, Validator or Owner

Some ideas how to use live dev demo. Create accounts:

```
curl https://api.prometeus.io/create_account/?type=validator
curl https://api.prometeus.io/create_account/?type=mart
```
Initialize data Owner

```
curl -H "Content-Type: application/json" --request POST --data '{"data":"xyzsdfsdfsfdsfdsf", "data_validator":"0xb19542ea90295401ed7558077d582b70f208bfba"}' https://api.prometeus.io/init_owner
```

To obtain relatedt to Prometeus account data 

```
curl http://api.prometeus.io/scanner/?blockchain_address=0x60a7e2a4080c91662f4b85245edce83736797013
```

returns json structure like

```json
{"blockchain_address": "0x60a7e2a4080c91662f4b85245edce83736797013", 
 "type": "data_owner", 
 "updated": "2019-05-28T04:42:23.801Z", 
 "storage": null, 
 "storage_md5": null, 
 "validator": "0xa3fea70386bd87ede44a6d6d2bff874ce09b9596"}
```

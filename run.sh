#!/bin/sh

cd web/src

./manage.py runserver 0.0.0.0:8000 &

cd -

cd node

mkdir  chaindata
echo "var promTokenOutput=`solc --optimize --combined-json abi,bin,interface ../lib/contract/PromToken.sol`" > promtoken.js
geth --dev --datadir chaindata/ --minerthreads 1 --preload "init.js"

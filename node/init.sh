#!/bin/sh

mkdir chaindata

echo "var prometeusOutput=`solc --optimize --combined-json abi,bin,interface ../contract/prometeus.sol`" > prometeus.js
echo "var promTokenOutput=`solc --optimize --combined-json abi,bin,interface ../contract/PromToken.sol`" > promtoken.js

# dev
# geth --dev --datadir chaindata/ --minerthreads 1 --preload "init.js"  console

geth --dev --datadir chaindata/ --minerthreads 1 --preload "init.js"

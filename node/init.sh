#!/bin/sh
echo "var promTokenOutput=`solc --optimize --combined-json abi,bin,interface ../lib/contract/PromToken.sol`" > promtoken.js
geth --dev --datadir chaindata/ --minerthreads 1 --preload "init.js"


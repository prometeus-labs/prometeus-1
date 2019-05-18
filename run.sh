#! /bin/sh

cd api
python3 api.py &

cd ../node
./init.sh

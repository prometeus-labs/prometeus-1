FROM golang

WORKDIR /go/src

# RUN mkdir -p github.com/ethereum
# RUN git clone https://github.com/ethereum/go-ethereum github.com/ethereum/go-ethereum
RUN go get github.com/ethereum/go-ethereum
RUN go install -v github.com/ethereum/go-ethereum/cmd/geth && \
    go install -v github.com/ethereum/go-ethereum/cmd/swarm

COPY . .

RUN mkdir node1

RUN geth --datadir node1 --password ./password.txt account new >  account.txt && \
    geth --datadir node1 init genesis.json

RUN go get -d -v ./...
RUN go install -v ./...

RUN go build -v -o run app

CMD geth --datadir node1 --nodiscover --mine --minerthreads 1 --maxpeers 0 --verbosity 3 --networkid 98765 --rpc --rpcapi="db,eth,net,web3,personal,web3"


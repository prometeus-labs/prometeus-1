

loadScript('promtoken.js')
promtoken_abi = promTokenOutput.contracts['./contract/PromToken.sol:StandardToken'].abi
promtoken_bin = "0x"+promTokenOutput.contracts['./contract/PromToken.sol:StandardToken'].bin
promtoken_contract = eth.contract(JSON.parse(promtoken_abi))
personal.unlockAccount(eth.accounts[0], "", 300000)
deployTransationObject = { from: eth.accounts[0], data: promtoken_bin, gas: 2000000 }
promtoken_instance = promtoken_contract.new(deployTransationObject)
promtoken_instance.address
promtoken = promtoken_contract.at(promtoken_instance.address)

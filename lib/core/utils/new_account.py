import secrets
import glob

def eth_create_new_account(web3, keystore_path, password=None):
        ret = {}
        if not password:
                password = secrets.token_urlsafe(32)  
                password = password.split('0x')[0]
             

        account = web3.personal.newAccount(password)
        account = account.split('0x')[1].lower()
             

        keystore_file = glob.glob(f"{keystore_path}/*{str(account)}*")
      

        if keystore_file:
                with open(keystore_file[0]) as keyfile:
                        encrypted_key = keyfile.read()
                        private_key = web3.eth.account.decrypt(encrypted_key, password)
                
                ret = {'account': '0x'+account.lower(), 'identity': password, 'private': private_key.hex()}
        else:
            ret = {'info': "Somthing went wrong"}
        return ret
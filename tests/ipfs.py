import json
import requests

ipfs_server_name = 'http://ipfs:5001'


def send_file_to_ipfs(file_name):
    url = ipfs_server_name + '/api/v0/add?pin=false&wrapWithDirectory=false&progress=true&wrap-with-directory=false&stream-channels=true'
    with open(file_name, 'rb') as f:
        r = requests.post(url, files={"file": f})

        if r.status_code != 200:
            raise Exception(r.content.decode('utf8'))

        result = json.loads(r.content.decode('utf8').split('\n')[1])
        file_hash = result['Hash']

        request = f'arg=/ipfs/{file_hash}&arg=/{file_name}&stream-channels=true'

        cp_url = ipfs_server_name + f'/api/v0/files/cp?' + request
        r = requests.post(cp_url)
        if r.status_code != 200:
            raise Exception(r.content.decode('utf8'))

        return {
            "hash": file_hash,
            "name": file_name
        }


def get_file_from_ipfs(name):
    url = ipfs_server_name + f'/api/v0/files/read?arg=/{name}&stream-channels=true'
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(r.content)
    return r.content.decode('utf8')

try:
    data = send_file_to_ipfs('ipfs_test_file.txt')
    print("File is uploading: ", data["hash"])
    print(get_file_from_ipfs(data['name']))

except Exception as e:
    print(str(e))

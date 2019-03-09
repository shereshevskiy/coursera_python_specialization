
import argparse
import os
import tempfile
import json

# initialization
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')


# argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key", help="input key name")
parser.add_argument("-v", "--value", help="input value")
parser.add_argument('--clear', action='store_true', help='Clear')
args = parser.parse_args()

key = args.key
value = args.value
clear = args.clear

if clear:
    os.remove(storage_path)
else:
    if not os.path.exists(storage_path):
        with open(storage_path, 'w') as fp:
            json.dump({}, fp)


    with open(storage_path, 'r') as fp:
        raw_data = fp.read()
        if raw_data:
            data = json.loads(raw_data)
        else:
            data = {}
        # print(data)
        if key and value:
            data.setdefault(key, []).append(value)
        elif key and not value:
            print(', '.join(data.get(key, '')))
        else:
            print('Error: You need input key')
    with open(storage_path, 'w') as fp:
        json.dump(data, fp)


import argparse
import os
import tempfile
import json

# initialization
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

if not os.path.exists(storage_path):
    with open(storage_path, 'w') as fp:
        json.dump({}, fp)

# argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key", help="input key name")
parser.add_argument("-v", "--val", help="input value")
args = parser.parse_args()

key = args.key
value = args.val

with open(storage_path, 'r') as fp:
    data = json.load(fp)
    if key and value:
        if key in data:
            data[key].append(value)
        else:
            data[key] = [value]
    elif key and not value:
        if key in data:
            print(', '.join(data[key]))
        else:
            print(None)
with open(storage_path, 'w') as fp:
    json.dump(data, fp)

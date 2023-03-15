import atexit
import subprocess
import json
import requests
from k8sfinalizer.cli import parse_args

args = parse_args()

namespace = args.namespace

# Get the namespace object in JSON format
p = subprocess.Popen(['kubectl', 'get', 'namespace', args.namespace, '-o', 'json'], stdout=subprocess.PIPE)
if p is None:
    print(f"Error: Failed to get namespace {args.namespace}")
    exit(1)
p.wait()
data = json.load(p.stdout)

# Print the namespace data
print('Namespace data:')
print(json.dumps(data, indent=4))

# Ask for confirmation before continuing
confirmation = input('Do you want to remove all finalizers from this namespace? [y/n]: ')
if confirmation.lower() != 'y':
    print('Aborted.')
    exit(0)

#Start kubectl proxy and register cleanup function
proxy_process = subprocess.Popen(['kubectl', 'proxy'])
atexit.register(proxy_process.kill)

#Remove all finalizers from the namespace object
data['spec']['finalizers'] = []

#Send the updated namespace object back to the API server
requests.put('http://127.0.0.1:8001/api/v1/namespaces/{}/finalize'.format(args.namespace), json=data).raise_for_status()

print('Finalizers removed successfully!')

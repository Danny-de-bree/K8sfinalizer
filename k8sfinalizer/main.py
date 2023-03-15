import atexit
import subprocess
import json
import requests
import sys
import argparse
from colorama import Fore, Style

def parse_args():
    parser = argparse.ArgumentParser(description='Welcome to the tool that will help you delete annoying terminating namespaces')
    parser.add_argument('--namespace', help='Namespace to use')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    namespace = args.namespace

    # Start the kubectl proxy process
    proxy_process = subprocess.Popen(['kubectl', 'proxy'])

    # Register an exit handler to kill the kubectl proxy process
    atexit.register(proxy_process.kill)

    # Get the namespace data as JSON
    p = subprocess.Popen(['kubectl', 'get', 'namespace', namespace, '-o', 'json'], stdout=subprocess.PIPE)
    p.wait()
    data = json.load(p.stdout)

    # Print the namespace data in red color
    print(f"{Fore.RED}Feyenoord 1#{Style.RESET_ALL} Namespace data: {Fore.WHITE}{namespace}{Style.RESET_ALL}")
    print(json.dumps(data, indent=4))

    # Remove the finalizers from the namespace data
    data['spec']['finalizers'] = []

    # Send a PUT request to the Kubernetes API to update the namespace data
    response = requests.put('http://127.0.0.1:8001/api/v1/namespaces/{}/finalize'.format(namespace), json=data)
    response.raise_for_status()

    # Ask for confirmation before deleting the namespace
    confirmation = input('Are you sure you want to delete the namespace "{}"? (y/n) '.format(namespace)).lower()
    if confirmation != 'y':
        print('Aborting...')
        sys.exit()

    # Delete the namespace using kubectl
    subprocess.run(['kubectl', 'delete', 'namespace', namespace])

if __name__ == '__main__':
    main()

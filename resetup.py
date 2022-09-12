import argparse
import re
arg = argparse.ArgumentParser()
arg.add_argument('--version', type=str)
args = arg.parse_args()
vers = re.search(r'\/?([0-9][0-9A-Za-z\.]+)', args.version)
if args.version and vers:
    new = open('setup.py').read().replace(
        '0.1.6',
        vers.group(1)
    )
    with open('setup.py', 'w') as fil:
        print(new)
        fil.write(new)
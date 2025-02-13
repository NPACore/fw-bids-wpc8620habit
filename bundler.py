#!/usr/bin/env python3
import json
import os
import re
import sys
from glob import glob
import json
import argparse
import pyjson5 # read json w/c style comments

def args(in_args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Combine folder of json rules into single json file for flywheel.")
    parser.add_argument('--jsondir','-d', required=True,
                        help='Path to the directory containing JSON file. One for each rule.')
    parser.add_argument('--combined', '-c', type=str,
                        help='Path to the combined json file. Output of bundle, input for exploder')
    parser.add_argument('--template','-t', type=str,
                        help='Path to the template file')
    parser.add_argument('--explode','-e', action='store_true', default=False,
                        help='Create per rule files from combined.json. Opposite of default: combining rules into single file.')
    args = parser.parse_args(in_args)
    # TODO: remove hard jsondir requirement from argparse
    if args.explode and not args.jsondir:
        args.jsondir = os.path.basename(args.combined[:-5])

    elif not args.explode and not args.combined:
        args.jsondir = re.sub('/$','', args.jsondir)
        args.combined = f"{args.jsondir}.json"

    return args


## bundle
def combine(template, in_dir) -> dict:
    with open(template) as tmpl:
        json_out = pyjson5.load(tmpl)

    json_out['rules'] = []
    for js in [*glob(f"{in_dir}/*.json"),*glob(f"{in_dir}/*.jsonc")]:
        # template might be in teh same directory
        # ignore it
        if os.path.abspath(template) == os.path.abspath(js):
            continue

        with open(js) as jsfh:
            json_out['rules'].append(pyjson5.load(jsfh))
    return json_out

## split
def explode(in_json, out_dir, template):
    with open(in_json) as f:
        full = json.load(f)
    os.makedirs(out_dir, exist_ok=True)
    for rule in full['rules']:
        id = rule.get('id', 'BADID')
        out_name = f'{out_dir}/{id}.json'
        print(f"# {out_name}")
        with open(out_name, 'w') as out:
            out.write(json.dumps(rule, indent=2))
    del full['rules']
    print(f"# {template}")
    with open(template, 'w') as out:
        out.write(json.dumps(full, indent=2))

if __name__ == "__main__":
    args = args(sys.argv[1:])
    if args.explode:
        explode(args.combined, args.jsondir, args.template)
    else:
        # default path
        json_dict = combine(args.template, args.jsondir)
        with open(args.combined, 'w') as outfh:
            json.dump(json_dict, outfh, indent=2)

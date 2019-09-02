#!/usr/bin/python

import sys
import re
import json
from collections import OrderedDict

def load_dirty_json(dirty_json):

    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    
    regex_replace = [
        # (r",(\s+[\}\]])", r'\1'), # Remove trailing commas
        (r'(,)\s*}(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)', r'}'), # Remove trailing object commas
        (r'(,)\s*\](?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)', r']'), # Remove trailing array commas
        (r"\/\*[\s\S]*?\*\/", r''), # Remove block comments
        (re.compile(r"(\".*?(?<!\\)\"|\'.*?(?<!\\)\')|(/\*.*?\*/|//[^\r\n]*$)", re.MULTILINE|re.DOTALL), _replacer), # Remove line comments
        (re.compile(r"^[ \s]+$[\n\r]+", re.MULTILINE), r'') # Remove empty lines
    ]

    for r, s in regex_replace:
        dirty_json = re.sub(r, s, dirty_json)
    
    clean_json = json.loads(dirty_json, object_pairs_hook=OrderedDict)

    return clean_json



def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True



if (len(sys.argv) != 2) or (is_empty(sys.argv[1])):
    sys.exit(1)


try:
    with open(str(sys.argv[1]), "r") as read_file:
        rawdata = read_file.read().decode('utf-8')
except:
    sys.exit(1)


try:
    data = load_dirty_json(rawdata)
except:
    sys.exit(1)

try:
    # If we have a match, clean it and return the results
    if "peacock.color" in data.keys():
        del data["peacock.color"]
        del data["workbench.colorCustomizations"]
        for key in data.keys():
            if key.startswith("peacock"):
                del data[key]

        if not is_empty(data):
            sys.stdout.write(json.dumps(data, indent=2))
            sys.stdout.flush()

    else:
        sys.exit(1)

except:
    sys.exit(1)

sys.exit()
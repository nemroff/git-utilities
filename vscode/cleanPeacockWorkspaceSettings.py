import re
import json

def load_dirty_json(dirty_json):

    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    
    regex_replace = [
        (r",(\s+[\}\]])", r'\1'), # Remove trailing commas
        (r"\/\*[\s\S]*?\*\/", r''), # Remove block comments
        (re.compile(r"(\".*?(?<!\\)\"|\'.*?(?<!\\)\')|(/\*.*?\*/|//[^\r\n]*$)", re.MULTILINE|re.DOTALL), _replacer), # Remove line comments
        (re.compile(r"^[ \s]+$[\n\r]+", re.MULTILINE), r'') # Remove empty lines
    ]

    for r, s in regex_replace:
        dirty_json = re.sub(r, s, dirty_json)
    
    clean_json = json.loads(dirty_json)

    return clean_json

# with open(".vscode/settings.json", "w") as write_file:
#     json.dump(data, write_file)

def is_not_empty(any_structure):
    if any_structure:
        # print('Structure is not empty.')
        return True
    else:
        # print('Structure is empty.')
        return False

with open(".vscode/settings.json", "r") as read_file:
    data = load_dirty_json(read_file.read())

# print(json.dumps(data, indent=2))

if "peacock.color" in data.keys():
    del data["peacock.color"]
    del data["workbench.colorCustomizations"]
    for key in data.keys():
        if key.startswith("peacock"):
            del data[key]

if is_not_empty(data):
    print(json.dumps(data, indent=2))
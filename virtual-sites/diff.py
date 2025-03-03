import json
from pprint import pprint

import xmltodict
from deepdiff import DeepDiff


def postprocessor(path, key, value):
    try:
        return key, int(value) if "." not in value else float(value)
    except (ValueError, TypeError):
        return key, value


smiles = json.load(open("results/vs-molecules/toolkit-v0.10.2/indices.json", "r"))

for index in smiles:
    with open(f"results/vs-molecules/toolkit-v0.10.2/systems/{index}.xml") as f:
        system1 = xmltodict.parse(f.read(), postprocessor=postprocessor)

    with open(
        f"results/vs-molecules/toolkit-v0.10.1+42.gd7f02367/systems/{index}.xml",
    ) as f:
        system2 = xmltodict.parse(f.read(), postprocessor=postprocessor)

    diff = DeepDiff(system1, system2, ignore_order=True, significant_digits=6)
    print(index, len(diff["values_changed"]))
    pprint(diff)

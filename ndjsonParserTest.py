import ndjson

with open('raw_ndjson/full_simplified_smiley face.ndjson', 'r') as f:
    smiley_dict = ndjson.load(f)

for smiles in smiley_dict:
	print(smiles['drawing'])
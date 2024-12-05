See combined output file [`out/combined_template.json`](out/combined_template.json) sutible for flywheel's bids-curate.

It is built by removing any comments and combining all the rules within the template.

Importatnly, `00_template.json` is named with leading `00` so it always sorted first. All other json files are expected to be rules.

The crux of the combination is this jq command.
```
jq -s '.[0] + {rules: .[1:]}' *.json
```

The [`Makefile`](Makefile) documents the actual process.

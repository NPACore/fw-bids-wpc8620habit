## Iterating

 1. change e.g. `LunaHabit/SEFieldMap.json`
 2. run [`./bundler.py`](./bundler.py) (or `make`, see [`Makefile`](Makefile) for bundler.py syntax)
 3. upload bundle to flywheel (e.g `fw upload LunaHabit_curate.json fw://mrrc/playground`)
 4. rerun BIDS. [`./run_curate-gear.py`](./run_curate-gear.py). prints log, writes to `/tmp/nii.csv`.
 5. look at output: `grep nii.gz /tmp/nii.csv| cut -d, -f5,6,9|column -ts,`
 6. repeat

## TODO
intendedFor regex pairs. can be set in [`./run_curate-gear.py`](./run_curate-gear.py)

## Flywheel documentation
https://docs.flywheel.io/Developer_Guides/dev_bids_template_file/

[Watch out for [missing currly's and parrens](https://docs.flywheel.io/Developer_Guides/dev_bids_template_file/#__codelineno-4-17)]


Flywheel examples can be found in 
https://gitlab.com/flywheel-io/public/bids-client/
within `flywheel_bids/templates/flywheel_curated/`

### Format
```
"$replace": {
  "$pattern": "bad",
  "$replacement": "good"}
}
```

Next steps: IntendedFor
https://docs.flywheel.io/Developer_Guides/dev_bids_curation_6_fmaps_and_intendedfors/#how-to-include-regular-expressions-during-bids-curation

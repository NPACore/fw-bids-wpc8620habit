# Bids curation in mulitple JSON files
## Motivation
One giant json config file is hard to inspect.
Breaking rules into their own file makes debuging more managable. And we can add comments.

## Iterating

 1. change e.g. `LunaHabit/SEFieldMap.json`
 2. run [`./bundler.py`](./bundler.py) (or `make`, see [`Makefile`](Makefile) for bundler.py syntax)
 3. upload bundle to flywheel (e.g `fw upload LunaHabit_curate.json fw://mrrc/playground`)
 4. rerun BIDS. [`./run_curate-gear.py`](./run_curate-gear.py). prints log, writes to `/tmp/nii.csv`.
 5. look at output: `grep nii.gz /tmp/nii.csv| cut -d, -f5,6,9|column -ts,`
 6. repeat


## Offline Check
As of 2024-12, `fw-template-check` is out-of-date with upstream `curate-bids`. Use the old version like (likely in a dedicate python virtual machine):
```
pip install git+https://gitlab.com/will.foran/curate-bids.git@check-cli-old
```

```
fw-template-check -t LunaHabit_curate.json "33 - dMRI_b0_AP" "37 - dMRI_b0_AP"

33 - dMRI_b0_AP dMRI_b0 sub-{session.info.BIDS.Subject}_acq-b0_epi.nii.gz
37 - dMRI_b0_AP dMRI_b0 sub-{session.info.BIDS.Subject}_acq-b0_epi.nii.gz
```

## TODO
intendedFor regex pairs. can be set in [`./run_curate-gear.py`](./run_curate-gear.py)

https://docs.flywheel.io/Developer_Guides/dev_bids_curation_6_fmaps_and_intendedfors/#how-to-include-regular-expressions-during-bids-curation
## Flywheel documentation
https://docs.flywheel.io/Developer_Guides/dev_bids_template_file/

[Watch out for [missing currly's and parrens](https://docs.flywheel.io/Developer_Guides/dev_bids_template_file/#__codelineno-4-17)]


Flywheel examples can be found in 
https://gitlab.com/flywheel-io/public/bids-client/
within `flywheel_bids/templates/flywheel_curated/`

## Bids Curate Notes
### $run_counter
From [`LunaHabit/dMRI_b0.json`](LunaHabit/dMRI_b0.json)
```
    "run": {
        // bids-client/tests/test_templates_unittest.py
        // + always increments?
        "$value": "+",
        // flywheel_curated/nyu-bair-vfs-project-template.json
        "$run_counter": {
            "key": "field_map.{file.info.BIDS.Dir}.{file.info.BIDS.Acq}.{file.info.BIDS.Suffix}"
          }
    },
```

[`bids-client/flywheel_bids/supporting_files/templates.py`](https://gitlab.com/flywheel-io/public/bids-client/-/blob/master/flywheel_bids/supporting_files/templates.py#L370) appears to only update the `$run_couter` if the current value is `"+"`.
The only place I've found this referenced is in [`bids-client/tests/test_templates_unittest.py`](https://gitlab.com/flywheel-io/public/bids-client/-/blob/master/tests/test_templates_unittest.py#L407).

### Format
Format can be used with `auto_update` defnitiions, espeically for session and subject: `definitions.session.{Label,Subject}.auto_update`.

```
"$format":[{
 "$replace": {
  "$pattern": "bad",
  "$replacement": "good"}
 }]
}
```

from [LunaHabit/template.jsonc](LunaHabit/template.jsonc)
```
    "definitions": {
        "session": {
            "properties": {
                "Label": {
                    "auto_update": {
                        "$process": true,
                        "$value": "<session.label>", // this is yyyymmddhhmmss... '<>' is autoformat lowercase + rm spaces; {} is literal value
                        "$format": [{
                            "$replace": { // keep only the first 8 digits
                                "$pattern": "(?<=[0-9]{8}).*",
                                "$replacement": ""}
                        }]
                    }
```




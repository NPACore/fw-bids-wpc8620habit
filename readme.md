
## Flywheel documentation
https://docs.flywheel.io/Developer_Guides/dev_bids_template_file/

(watch out for [missing currly's and parrens](https://docs.flywheel.io/Developer_Guides/dev_bids_template_file/#__codelineno-4-17))

Flywheel examples can be found in 
https://gitlab.com/flywheel-io/public/bids-client/
within `flywheel_bids/templates/flywheel_curated/`
### Format
```
"$replace": {
  "$pattern": "[a-z]",
  "$replacement": "Character"}
}
```

Next steps: IntendedFor
https://docs.flywheel.io/Developer_Guides/dev_bids_curation_6_fmaps_and_intendedfors/#how-to-include-regular-expressions-during-bids-curation

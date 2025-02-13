#! /usr/bin/env python3
"""Run curate-bids on session "2024-10-18 08_08_15"

    This script was created to run Job ID 67ad4fff0d4e5d6d3679f9d8
    In project "mrrc/playground"
    On Flywheel Instance https://fw.mrrc.upmc.edu/api
"""

import os
import time
import argparse
from datetime import datetime


import flywheel


input_files = {
    "template": {
        "container_path": "mrrc/playground",
        "location_name": "LunaHabit_curate.json",
    }
}


fw = flywheel.Client("")
gear = fw.lookup("gears/curate-bids")
destination = fw.lookup("mrrc/playground/12112_20241018/2024-10-18 08_08_15")

inputs = dict()
for key, val in input_files.items():
    if val["container_path"][:8] == "analysis":
        path = val["container_path"][9:]
        parent_of_analysis = fw.lookup(path)
        # find analysis that has the right file
        analyses = parent_of_analysis.reload().analyses
        for analysis in analyses:
            for file in analysis.files:
                if file.name == val["location_name"]:
                    container = analysis
    else:
        container = fw.lookup(val["container_path"])
    inputs[key] = container.get_file(val["location_name"])

print(inputs)
config = {
    "base_template": "reproin",
    "intendedfor_regexes": "",
    "reset": True,
    "save_sidecar_as_metadata": "auto",
    "use_or_save_config": "",
    "verbosity": "INFO",
}

tags = ["curate-bids"]

now = datetime.now()
analysis_label = (
    f'{gear.gear.name} {now.strftime("%m-%d-%Y %H:%M:%S")} SDK launched'
)
print(f"analysis_label = {analysis_label}")

analysis_id = gear.run(
    analysis_label=analysis_label,
    tags=tags,
    config=config,
    inputs=inputs,
    destination=destination,
)
print(f"analysis_id = {analysis_id}")

###
# wait for job. if nothing else is running, expect 12s to run
print("# waiting 30s for job to finish")
time.sleep(30)

# log has 'msg' and 'fd'. dont care about file descriptor (STDERR=2)
job = fw.jobs.find_one(f"_id={analysis_id}")
print("\n".join([l['msg'] for l in job.get_logs() ]))
# analysis output includes acquisiton list
dest = fw.get(job['destination']['id'])
dest.download_file("mrrc_playground_acquisitions.csv","/tmp/acq.csv")
dest.download_file("mrrc_playground_niftis.csv","/tmp/nii.csv")
print("# see /tmp/acq.csv and /tmp/nii.csv")
print("#   grep nii.gz /tmp/nii.csv| cut -d, -f5,6,9|column -ts,")
# [x['name'] for x in dest['files']]
# ['mrrc_playground_acquisitions.csv',
#  'mrrc_playground_acquisitions_details_1.csv',
#  'mrrc_playground_acquisitions_details_2.csv',
#  'mrrc_playground_intendedfors.csv',
#  'mrrc_playground_niftis.csv']



print(f"download {analysis_label}")

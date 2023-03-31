import argparse
import json
import logging
import sys

import isamples_core
import isamples_core_records
import linkml_runtime.dumpers
import linkml_runtime.loaders

target_classes = {
    "PhysicalSampleRecord":isamples_core.PhysicalSampleRecord,
    "PhysicalSampleRecordList":isamples_core_records.PhysicalSampleRecordList,
    "PhysicalSampleRecordDict":isamples_core_records.PhysicalSampleRecordDict,
}


def validate_content(fn_src:str, target_class_name:str):
    content = linkml_runtime.loaders.json_loader.load(fn_src, target_class=target_classes[target_class_name])
    print(linkml_runtime.dumpers.json_dumper.dumps(content))


def validate_source(fn_src:str):
    data = {}
    with open(fn_src) as src:
        data = json.load(src)
    _type = data.get("@type", None)
    if _type in target_classes:
        return validate_content(fn_src, _type)
    if "samples" in data:
        if isinstance(data["samples"], list):
            return validate_content(fn_src, "PhysicalSampleRecordList")
        else:
            return validate_content(fn_src, "PhysicalSampleRecordDict")
    else:
        return validate_content(fn_src, "PhysicalSampleRecord")


def main()->int:
    logging.basicConfig(level=logging.INFO)
    L = logging.getLogger()
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    args = parser.parse_args()
    validate_source(args.source)
    return 0

if __name__ == "__main__":
    sys.exit(main())
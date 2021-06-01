import json
import os
import sys

from isamples_metadata.SESARTransformer import SESARTransformer

ISAMPLES_FILE_PREFIX = "iSamples_"

# assume these have been pulled down at some other time
dir = "/Users/mandeld/iSamples/tmprecords/"


def test_local_records():
    for file in os.listdir(dir):
        if file.startswith(ISAMPLES_FILE_PREFIX):
            continue
        full_path = os.path.join(dir, file)
        with open(full_path) as source_file:
            source_record = json.load(source_file)
            try:
                transformer = SESARTransformer(source_record)
                transformed_to_isamples_record = transformer.transform()
                filename_no_ext = os.path.splitext(file)[0]
                with open(
                    dir + ISAMPLES_FILE_PREFIX + filename_no_ext + ".json", "w"
                ) as outfile:
                    json.dump(transformed_to_isamples_record, outfile)
            except:
                e = sys.exc_info()[0]
                print("Exception in file " + full_path)
                raise e

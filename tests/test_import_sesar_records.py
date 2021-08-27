import json
import os
import sys

from isamples_metadata.SESARTransformer import SESARTransformer

ISAMPLES_FILE_PREFIX = "iSamples_"

# assume these have been pulled down at some other time
dir = "/Users/mandeld/iSamples/tmprecords/"


@pytest.mark.skip(reason="This is a one-off script not intended to be run as part of a CI process")
def test_local_records():
    for file in os.listdir(dir):
        if file.startswith(ISAMPLES_FILE_PREFIX):
            continue
        filename_no_ext = os.path.splitext(file)[0]
        dest_path = dir + ISAMPLES_FILE_PREFIX + filename_no_ext + ".json"
        if os.path.exists(dest_path):
            continue
        full_path = os.path.join(dir, file)
        with open(full_path) as source_file:
            try:
                source_record = json.load(source_file)
                transformer = SESARTransformer(source_record)
                transformed_to_isamples_record = transformer.transform()
                with open(
                    dest_path, "w"
                ) as outfile:
                    json.dump(transformed_to_isamples_record, outfile)
            except:
                e = sys.exc_info()[0]
                print("Exception in file " + full_path)
                raise e

# Adapted from https://github.com/isamplesorg/vocabulary_learning/blob/develop/fasttext_interface/DwC_predict.py

import fasttext
import os.path
import typing
import re

from fasttext.FastText import _FastText

MODEL_FILENAME = "./sampledFeature.bin"
THIS_PATH = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(THIS_PATH, MODEL_FILENAME)
MODEL = None
RESULT_PREFIX = "__label__"


def _model() -> _FastText:
    global MODEL
    if MODEL is None:
        MODEL = fasttext.load_model(MODEL_PATH)
    return MODEL


def predict_sampled_feature(context: typing.List[typing.AnyStr]) -> typing.AnyStr:
    """
    Invoke the pre-trained fasttext model to predict the sampledFeature label for the specified string inputs
    :param context: The unprocessed inputs to the model, taken from a source record
    :return: String label to be used as the sampled feature for the source record
    """

    # Do a bit of formatting to ensure the input is as the model expects
    string_input = " ".join(context)
    string_input = string_input.lower()
    string_input = re.sub(r"[^\w\s]", "", string_input)
    model = _model()
    result = model.predict(string_input)

    # The model output looks like this:
    # (('__label__Marine_water_body',), array([1.00001001]))
    # So get the first item's first item and do some string munging to get the actual label to use
    raw_result = result[0][0]
    processed_result = raw_result.removeprefix(RESULT_PREFIX)
    processed_result = processed_result.replace("_", " ")
    return processed_result

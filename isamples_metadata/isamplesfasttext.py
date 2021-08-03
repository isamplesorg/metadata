# Adapted from https://github.com/isamplesorg/vocabulary_learning/blob/develop/fasttext_interface/DwC_predict.py

import fasttext
import os.path
import typing
import re
import logging
from isamples_metadata import config
from fasttext.FastText import _FastText

from isamples_metadata.Transformer import Transformer

_MODEL = None
_MODEL_PATH = config.Settings().fasttext_model_path
if not os.path.exists(_MODEL_PATH):
    logging.error(
        "Unable to locate fasttext model at path %s.  All predictions will return NOT_PROVIDED.",
        _MODEL_PATH,
    )
else:
    _MODEL = fasttext.load_model(_MODEL_PATH)


class SampledFeaturePredictor:
    RESULT_PREFIX = "__label__"

    def __init__(self, name: typing.AnyStr, model: _FastText):
        self._name = name
        self._model = model
        self._model_valid = model is not None

    def predict_sampled_feature(
        self, context: typing.List[typing.AnyStr]
    ) -> typing.AnyStr:
        """
        Invoke the pre-trained fasttext model to predict the sampledFeature label for the specified string inputs.
        Prerequisite: In order to use this, make sure that there is a pydantic settings file on the
        environment path, named "isamples_metadata.env" with at least this variable set:

        FASTTEXT_MODEL_PATH = "/absolute/path/to/model"

        :param context: The unprocessed inputs to the model, taken from a source record
        :return: String label to be used as the sampled feature for the source record. If the model couldn't be loaded Transformer.NOT_PROVIDED will be returned.
        """
        if not self._model_valid:
            logging.error(
                "Returning Transformer.NOT_PROVIDED since we couldn't load the model at path %s.",
                _MODEL_PATH,
            )
            return Transformer.NOT_PROVIDED

        # Do a bit of formatting to ensure the input is as the model expects
        string_input = " ".join(context)
        string_input = string_input.lower()
        string_input = re.sub(r"[^\w\s]", "", string_input)
        result = self._model.predict(string_input)

        # The model output looks like this:
        # (('__label__Marine_water_body',), array([1.00001001]))
        # So get the first item's first item and do some string munging to get the actual label to use
        raw_result = result[0][0]
        processed_result = raw_result.removeprefix(self.RESULT_PREFIX)
        processed_result = processed_result.replace("_", " ")
        return processed_result


SMITHSONIAN_FEATURE_PREDICTOR = SampledFeaturePredictor("Smithsonian", _MODEL)

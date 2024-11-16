from typing import Dict, List, Any

from optimum.intel import OVModelForSeq2SeqLM
from transformers import AutoTokenizer


INSTRUCTION = "rewrite: "
generation_config = {
    "max_new_tokens": 8,
    "use_cache": True,
    "temperature": 0.6,
    "do_sample": True,
    "top_p": 0.95,
}


class EndpointHandler:
    def __init__(self, path="."):
        # Preload all the elements you are going to need at inference.
        # pseudo:
        self.model = OVModelForSeq2SeqLM.from_pretrained(
            path, use_cache=True, use_io_binding=False
        )
        self.tokenizer = AutoTokenizer.from_pretrained(path, use_fast=True)

    def __call__(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
         data args:
              inputs (:obj: `str` | `PIL.Image` | `np.array`)
              kwargs
        Return:
              A :obj:`list` | `dict`: will be serialized and returned
        """
        inputs = data.pop("inputs", data)
        parameters = data.pop("parameters", generation_config)
        inputs = self.tokenizer(
            ["{} {}".format(INSTRUCTION, inputs)],
            padding=False,
            return_tensors="pt",
            max_length=20,
            truncation=True,
        )

        outputs = self.model.generate(**inputs, **parameters)
        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True)

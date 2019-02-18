import requests
from summ_support.summarization import get_summarised


def post(payload):
    input_text = payload['input_text']

    response = get_summarised(input_text)
    summary = eval(response)

    return {
        "input_text": input_text,
        "Summary": summary['result']
    }
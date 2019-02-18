"""
    Machine translation API
"""
import textract
from google.cloud import translate


def read_data(file_path):
    text = textract.process(file_path)
    return text


def post(payload):
    file_path = payload['file_path']

    text = read_data(file_path)

    translate_client = translate.Client()


    # The target language
    target = 'ru' # for more go to https://cloud.google.com/translate/docs/languages

    translation = translate_client.translate(
        text,
        target_language=target)

    return {
        "Text_given" : text,
        "Translated_text" : translation['translatedText'],
        "Language": target
    }

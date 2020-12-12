import re

import django

django.setup()
import nltk.data
from google.cloud import translate_v2 as translate

from dictionary.models import EngToGerDict


def translate_text(text):
    if len(text) > 1000:
        try:
            raise ValueError  # something bad...
        except ValueError as err:
            err.message = "Text length cannot be more than 1000 chars because of Google API restrictions."
            raise
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    print("Source: " + text)
    sentences = tokenizer.tokenize(text)
    translate_client = translate.Client()
    # разбиваем на предложения
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        # разбиваем на слова
        for word in words:
            # если не пунктуация - переводим
            if not re.match('\W', word):
                try:
                    # сначало ищем в бд
                    word_trans = EngToGerDict.objects.get(source=word)
                    text = text.replace(word, word_trans.translation)
                except EngToGerDict.DoesNotExist:
                    # если в бд нет, обращаемся к гуглу и сохраняем перевод в бд.
                    gcp_api_result = translate_client.translate(word, source_language="en", target_language="de")
                    word_trans = EngToGerDict(source=word, translation=gcp_api_result["translatedText"])
                    word_trans.save()
                    text = text.replace(word, word_trans.translation)
    print("Translated: " + text)
    return text


def translate_file(path):
    pass


translate_text(
    'Hello world. How are you?')

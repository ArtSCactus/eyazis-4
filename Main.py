"""Translates text into the target language.

Target must be an ISO 639-1 language code.
See https://g.co/cloud/translate/v2/translate-reference#supported_languages
"""
import six
from google.cloud import translate_v2 as translate

translate_client = translate.Client()

print("Приветствую!\n")
while True:
    text = input("Введите текст (или 0 чтобы выйти): ")
    if text is None or len(text) == 0:
        print("Текст не был введён. Пожалуйста, попробуйте снова")
        continue
    if text == "0":
        print("До встречи!")
        exit(0)
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, source_language="ru", target_language="en")

    print(u"Исходный: {}".format(result["input"]))
    print(u"Перевод: {}".format(result["translatedText"]))
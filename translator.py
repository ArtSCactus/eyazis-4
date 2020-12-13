import operator
import re

import django
from nltk import FreqDist

from printDocumets import printExpectation
from saveInFile import SaveFile

django.setup()
import nltk.data
from google.cloud import translate_v2 as translate

from dictionary.models import EngToGerDict


def translate_text(text):
    if len(text) > 1000:
        try:
            raise ValueError
        except ValueError as err:
            err.message = "Text length cannot be more than 1000 chars because of Google API restrictions."
            raise
    result_str = ''
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    print("Source: " + text)
    result_str = result_str + "Source: " + text
    sentences = tokenizer.tokenize(text)
    translate_client = translate.Client()
    analytics = {}
    # разбиваем на предложения
    for sentence in sentences:
        # разбиваем предложения на слова
        words = nltk.word_tokenize(sentence)
        # подсчитываем количество вхождений слов
        counted_words = FreqDist(words)
        # проходим по каждому слову
        for word in words:
            # если не пунктуация - переводим и обрабатываем
            if not re.match('\W', word):
                # проверяем наличие слова в аналитике. Если есть - увеличиваем счётчик вхождения слова.
                # Если нет - инициализируем
                try:
                    analytics[word]['counter'] = analytics[word]['counter'] + counted_words[word]
                except KeyError:
                    analytics[word] = {'counter': counted_words[word],
                                       'word_type': list(filter(lambda item: item[0] == word, nltk.pos_tag(words)))[0][
                                           1]}
                try:
                    # сначало ищем в бд
                    word_trans = EngToGerDict.objects.get(source=word)
                    # если нашло в бд, заменяем в тексте слово на перевод
                    text = text.replace(word, word_trans.translation)
                except EngToGerDict.DoesNotExist:
                    # если в бд нет, обращаемся к гуглу и сохраняем перевод в бд.
                    gcp_api_result = translate_client.translate(word, source_language="en", target_language="de")
                    word_trans = EngToGerDict(source=word, translation=gcp_api_result["translatedText"])
                    word_trans.save()
                    text = text.replace(word, word_trans.translation)

    # выводим перевод в консоль
    print("\nTranslated: " + text)
    result_str = result_str + "\nTranslated: " + text
    # сортируем аналитику по количеству вхождений слов
    analytics = dict(sorted(analytics.items(),
                            key=operator.itemgetter(0),
                            reverse=False))
    # выводим аналитику в консоль
    print('\nAnalytics: ')
    result_str = result_str + '\nAnalytics: '
    for key, value in analytics.items():
        result_str = result_str + key + ' -> amount of entrances: ' + str(value['counter']) + ', word type: ' + value[
            'word_type'] + '\n'
    print(result_str)
    # сохраняем в файл, если эотого хочет пользователь
    SaveFile(result_str, 1)
    printExpectation()


def translate_file(path):
    pass

# translate_text(
#    'Hello Hello world. How are you?')

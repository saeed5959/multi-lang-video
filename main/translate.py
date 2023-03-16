from translate import Translator


def translate_text_func(text_list: list, lang:str):

    text_trans_list = []
    for text in text_list:
        translator= Translator(to_lang=lang)
        text_trans_list.append(translator.translate(text))

    return text_trans_list 
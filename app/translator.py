from googletrans import Translator
translator = Translator()

def translate_to_en(text):
    detected_language = translator.detect(text)
    translation = translator.translate(text, dest='en')
    return translation.text, detected_language.lang


def translate_to_hi(text):
    detected_language = translator.detect(text)
    translation = translator.translate(text, dest='hi')
    return translation.text, detected_language.lang

def lang_checker(text):
    detect_language=translator.detect(text)
    return detect_language.lang



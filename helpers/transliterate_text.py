from polyglot.detect import Detector
from polyglot.text import Text

# arabic_script = set(['\u0621', '\u0622', '\u0623', '\u0624', '\u0625', '\u0626', '\u0627', '\u0628', '\u0629', '\u062A', '\u062B', '\u062C', '\u062D', '\u062E', '\u062F', '\u0630', '\u0631', '\u0632', '\u0633', '\u0634', '\u0635', '\u0636', '\u0637', '\u0638', '\u0639', '\u063A', '\u0640', '\u0641', '\u0642', '\u0643', '\u0644', '\u0645', '\u0646', '\u0647', '\u0648', '\u0649',
#                     '\u064A', '\u064B', '\u064C', '\u064D', '\u064E', '\u064F', '\u0650', '\u0651', '\u0652', '\u0653', '\u0654', '\u0655', '\u0656', '\u0657', '\u0658', '\u0659', '\u065A', '\u065B', '\u065C', '\u065D', '\u065E', '\u065F', '\u0660', '\u0661', '\u0662', '\u0663', '\u0664', '\u0665', '\u0666', '\u0667', '\u0668', '\u0669', '\u066A', '\u066B', '\u066C', '\u066D', '\u066E', '\u066F'])


def transliterate_text(text_ar, text_en, language, primary_language='en', mapped_words={}):
    MIN_TEXT_LENGTH = 2
    # if any(char in arabic_script for char in text):
    if text_en == text_en or len(text_ar) < MIN_TEXT_LENGTH:
        return text_en
    if language != primary_language:
        detector = Detector(text_ar)
        if detector.language.code == 'ar':
            new_text = Text(text_ar)
            transliterated_words = []
            # translate_text = ''
            list_text = new_text.transliterate("en")
            for index, value in enumerate(list_text):
                # for x in new_text.transliterate("en"):
                original = new_text.words[index]
                for no_transliterate_word in mapped_words.keys():
                    if no_transliterate_word in original:
                        transliterated_words.append(
                            mapped_words[no_transliterate_word])
                        break
                        # translate_text = translate_text + mapped_words[x] + ' '
                else:
                    transliterated_words.append(value)
                    # translate_text = translate_text + x + ''
            # if language == 'ar':
            # translator = Transliterator(
            #     source_lang=language, target_lang=primary_language)
            # translate_text = translator.transliterate(text)
            transliterated_words.reverse()
            unique_list = []
            [unique_list.append(x)
             for x in transliterated_words if x not in unique_list]

            return ' '.join(unique_list)
        # return translate_text
    return text_ar

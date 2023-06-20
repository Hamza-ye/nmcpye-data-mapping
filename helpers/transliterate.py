import pandas as pd
import unicodedata
from langdetect import detect
from googletrans import Translator
from polyglot.downloader import downloader
from polyglot.transliteration import Transliterator
from polyglot.detect import Detector
from polyglot.text import Text

MIN_TEXT_LENGTH = 2  # minimum length

def detect_language(text):
    if len(text) < MIN_TEXT_LENGTH:
        return None  # text is too short
    try:
        return detect(text)
    except LangDetectException:
        return None  # language cannot be detected


# language models
downloader.download("transliteration2.ar")

# file path
file_path = 'hfs-list/Health_Facilities.xlsx'

df = pd.read_excel(file_path)


df['HFNameSourceEditable'] = df['HFNameSourceEditable'].fillna('')
df['language'] = df['HFNameSourceEditable'].astype(str).apply(detect_language)

# no_transliterate_words = ['مركز', 'صحي', 'وحدة', 'مستشفى', 'مستوصف','عيادة','مختبر', 'طوارى']
mapped_words = {'الوحدة الصحية': 'HU',
                'المركز الصحي': 'HC',
                'المجمع الصحي': 'Complex',
                'الصحية': 'HU',
                'وحدة': 'HU',
                'صحي': 'HC',
                'مستشفى': 'H',
                'مستوصف': 'Dispensary',
                'عيادة': 'Clinic',
                'طوارى': 'emergancy',
                'امومة': 'Maternity',
                'طفولة': 'Childhood',
                'الهلال': 'Crescent',
                'الصليب': 'Cross',
                'الأحمر': 'Red',
                'الطبي': 'Medical',
                'سجن مركزي': 'Central Jail',
                'سجن المركزي': 'Central Jail',
                'المركزي': 'Central',
                'مركز': 'HC',
                'النفسية': 'Psychological',
                'الجامعي': 'educational',
                'التعليمي': 'educational',
                'مختبر': 'Laboratory',
                'الوطني': 'National',
                'العامة': 'Public',
                'الخاص': 'Private',
                }


def transliterate_text2(text_ar, text_en, language, primary_language='en'):
    # if any(char in arabic_script for char in text):
    if len(text_ar) < MIN_TEXT_LENGTH:
    # if text_en == text_en or len(text_ar) < MIN_TEXT_LENGTH:
        return text_ar
    if language != primary_language:
        detector = Detector(text_ar, quiet=True)
        if detector.language.code == 'ar':
            new_text = Text(text_ar)
            transliterated_words = []
            # translate_text = ''
            list_text = new_text.transliterate("en")
            for index, value in enumerate(list_text):
                # for x in new_text.transliterate("en"):
                original = new_text.words[index]
              
                for no_transliterate_word_key, no_transliterate_word_value in mapped_words.items():
                    if no_transliterate_word_key in original:
                        transliterated_words.append(
                            no_transliterate_word_value)
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
            [unique_list.append(x) for x in transliterated_words if x not in unique_list]

            return ' '.join(unique_list)
        # return translate_text
    return text_ar
    # return text


# to primary language
df['HFNameSourceARENTrans'] = df.apply(
    lambda x: transliterate_text2(x['HFNameSourceEditable'], x['NameEN'], x['language']), axis=1)

df.to_excel("hfs_list_all_transliterated.xlsx", index=False)

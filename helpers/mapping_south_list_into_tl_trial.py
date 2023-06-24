import pandas as pd
from langdetect import detect
from googletrans import Translator
from polyglot.downloader import downloader
from polyglot.transliteration import Transliterator
from polyglot.detect import Detector
from polyglot.text import Text
from fuzzywuzzy import fuzz


# data needs Preprocessing. and introducing a better idea, try Weighted matching later
# token-based and character-based matching, exact match on district level

downloader.download("transliteration2.ar")

MIN_TEXT_LENGTH = 2

THRESHOLD = 50  # Set the threshold for fuzzy matching

def detect_language(text):
    if len(str(text)) < MIN_TEXT_LENGTH:
        return None
    try:
        return detect(text)
    except LangDetectException:
        return None


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


def transliterate_text(text, language, primary_language='en'):
    # print(f"transliterate_text: input={text}")
    if not isinstance(text, str) or len(text) < MIN_TEXT_LENGTH:
        return ""
    if language != primary_language:
        detector = Detector(text, quiet=True)
        if detector.language.code == 'ar':
            new_text = Text(text)
            transliterated_words = []
            list_text = new_text.transliterate("en")
            for index, value in enumerate(list_text):
                original = new_text.words[index]

                for no_transliterate_word_key, no_transliterate_word_value in mapped_words.items():
                    if no_transliterate_word_key in original:
                        # transliterated_words.append(
                        #     no_transliterate_word_value)
                        break
                else:
                    transliterated_words.append(value)

            transliterated_words.reverse()
            unique_list = []
            [unique_list.append(x) for x in transliterated_words if x not in unique_list]

            result = ' '.join(unique_list)
            # print(f"transliterate_text: output={result}")
            return result
    result = text
    # print(f"transliterate_text: output={result}")
    return result


def fuzzy_match(row, col1, col2, threshold):
    match_ratio = 0
    if isinstance(row[col2], str):
        match_ratio = fuzz.token_set_ratio(row[col1], row[col2].lower())

    if match_ratio >= threshold:
        return f"{match_ratio}%"
    else:
        return ""


def trans_and_calculate_fuzzyness(file_path, cols_to_transliterate, match_col):
    df = pd.read_excel(file_path)
    for col in cols_to_transliterate:
        new_col_name = f"transliterated_{col}"
        df[new_col_name] = df[col].apply(lambda x: transliterate_text(x, detect_language(x)) if pd.notnull(x) else x)
    for col in cols_to_transliterate:
        transliterated_col = f"transliterated_{col}"
        match_result_col = f"match_percentage_{transliterated_col}"
        df[match_result_col] = df.apply(lambda x: fuzzy_match(x, match_col, transliterated_col, THRESHOLD), axis=1)
    df.to_excel("transliterated_output.xlsx", index=False)

# Define the file path to the Excel file
file_path = 'unified_translitrated.xlsx'
trans_and_calculate_fuzzyness(file_path, ['hf_name_north_using_s_id_3','hf_name_north_using_7chars_4','hf_name_digit_5'], 'hf_name_ar_south_trans')

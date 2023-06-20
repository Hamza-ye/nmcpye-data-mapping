import pandas as pd
from fuzzywuzzy import fuzz

file_path = 'data/master-data/md_health_facilities.xlsx'

df = pd.read_excel(file_path)

exact_cols = ['district_id_unified_s_n']
fuzzy_cols = ['hf_name']

fuzzy_threshold = 10

exact_duplicates = df[df.duplicated(subset=exact_cols, keep=False)]

exact_groups = exact_duplicates.groupby(exact_cols)

#possible fuzzy duplicates within each group
fuzzy_duplicates = []
for name, group in exact_groups:
    for i, row1 in group.iterrows():
        for j, row2 in group.iterrows():
            if i < j:
                fuzzy_ratio = fuzz.token_set_ratio(
                    row1[fuzzy_cols[0]], row2[fuzzy_cols[0]])
                if fuzzy_ratio >= fuzzy_threshold:
                    fuzzy_duplicates.append((i, j, fuzzy_ratio))

df['Possible Duplicates'] = ''
for i, j, ratio in fuzzy_duplicates:
    df.at[i, 'Possible Duplicates'] = str(ratio) + '%'
    df.at[j, 'Possible Duplicates'] = str(ratio) + '%'


df.to_excel('table_with_duplicates_flagged.xlsx', index=False)

# import pandas as pd

# df_left = pd.read_csv('./data/master-data/md_catchment_locations.csv')
# df_right = pd.read_csv('./data/master-data/md_health_facilities.csv')

# df = pd.merge(df_left, df_right, how='left', on='hf_code_link')

# ...
# ...
# ...

# non_matching_rows = df[df['hf_code_link'].isnull()]

# # fail if non-matching rows are above a 10084 cms
# max_non_matching_rows = 10
# if len(non_matching_rows) > max_non_matching_rows:
#     raise ValueError('Number of cms non-matching rows exceeds maximum')

import pandas as pd
import math

# Load the two CSV files into Pandas dataframes
df1 = pd.read_csv('./data/master-data/md_catchment_locations.csv')
df2 = pd.read_csv('./data/master-data/md_health_facilities.csv')

# Define the column names to use for joining and grouping
join_col = 'hf_code_link'
group_cols = ['gov_id', 'gov', 'district']

# Perform the left join
merged_df = pd.merge(df1, df2, on=join_col, how='left')

# Calculate the percentage, mapped count, and unmapped count
total_rows = len(merged_df)
mapped_rows = len(merged_df.dropna(subset=['hf_code_link']))
unmapped_rows = total_rows - mapped_rows
percentage_matched = round(mapped_rows / total_rows * 100)

# Group the merged dataframe by the specified columns and calculate the counts
grouped_df = merged_df.groupby(group_cols).agg(
    {'mapping_status': 'count'}).reset_index()
grouped_df = grouped_df.rename(columns={'mapping_status': 'MAPPED'})

# Add the unmapped counts to the grouped dataframe
unmapped_df = merged_df[pd.isna(merged_df['hf_code_link'])].groupby(
    group_cols).agg({'mapping_status': 'count'}).reset_index()
unmapped_df = unmapped_df.rename(columns={'mapping_status': 'UNMAPPED'})
grouped_df = pd.merge(grouped_df, unmapped_df,
                      on=group_cols, how='outer').fillna(0)

# Format the percentage as a string and create the markdown table
percentage_str = str(percentage_matched)
table_df = grouped_df.copy()
table_df['Percentage'] = '![{}](https://geps.dev/progress/{})'.format(
    percentage_str, math.ceil(percentage_matched/10)*10)
table_df = table_df[group_cols + ['Percentage', 'MAPPED', 'UNMAPPED']]
table_str = table_df.to_markdown(index=False)

print(table_str)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load the dataset
file_path = "ERT-Spreadsheet-01.xlsx"
df = pd.read_excel(file_path)

# Define key column groups from inspection
device_columns = df.columns[3:10]
platform_columns = df.columns[11:23]
challenge_columns = df.columns[34:43]
satisfaction_col = df.columns[43]
benefits_col = df.columns[44]
learning_pref_col = df.columns[74]

# Step 1: Combine multi-select fields into single strings
df['Devices_Used'] = df[device_columns].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
df['Platforms_Used'] = df[platform_columns].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
df['Challenges_Faced'] = df[challenge_columns].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)

# Rename columns for clarity
df_cleaned = df[['Devices_Used', 'Platforms_Used', 'Challenges_Faced', satisfaction_col, benefits_col, learning_pref_col]].copy()
df_cleaned.columns = ['Devices_Used', 'Platforms_Used', 'Challenges_Faced', 'Support_Rating', 'Remote_Benefits', 'Learning_Preference']

# Step 2: Data Cleaning
df_cleaned.dropna(how='all', inplace=True) # Remove rows where all selected fields are NaN
df_cleaned['Support_Rating'] = pd.to_numeric(df_cleaned['Support_Rating'], errors='coerce')
df_cleaned['Remote_Benefits'] = pd.to_numeric(df_cleaned['Remote_Benefits'], errors='coerce')

# Step 3: Visualization

# Device Usage - Bar Chart
plt.figure(figsize=(10, 6))
device_counts = pd.Series(', '.join(df_cleaned['Devices_Used'].dropna()).split(', ')).value_counts()
sns.barplot(y=device_counts.index, x=device_counts.values, palette="viridis")
plt.title('Devices Used for Remote Learning')
plt.xlabel('Count')
plt.ylabel('Device')
plt.tight_layout()
plt.show()

# Platforms Used - Horizontal Bar Chart
plt.figure(figsize=(10, 6))
platform_counts = pd.Series(', '.join(df_cleaned['Platforms_Used'].dropna()).split(', ')).value_counts()
sns.barplot(y=platform_counts.index, x=platform_counts.values, palette="magma")
plt.title('Platforms Used for Remote Learning')
plt.xlabel('Count')
plt.ylabel('Platform')
plt.tight_layout()
plt.show()

# Challenges Faced - Word Cloud
challenge_text = ', '.join(df_cleaned['Challenges_Faced'].dropna())
wordcloud = WordCloud(width=1000, height=400, background_color='white').generate(challenge_text)
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Common Challenges Faced")
plt.tight_layout()
plt.show()

# Support Rating - Histogram
plt.figure(figsize=(8, 5))
sns.histplot(df_cleaned['Support_Rating'].dropna(), bins=5, kde=True, color='skyblue')
plt.title('Support Rating from Institution')
plt.xlabel('Rating (1 = Poor to 5 = Excellent)')
plt.ylabel('Number of Students')
plt.tight_layout()
plt.show()

# Remote Benefits - Pie Chart
plt.figure(figsize=(6, 6))
benefit_counts = df_cleaned['Remote_Benefits'].value_counts().rename({1: "Yes", 0: "No"})
plt.pie(benefit_counts, labels=benefit_counts.index, autopct='%1.1f%%', colors=["#66c2a5", "#fc8d62"])
plt.title('Did Students See Benefits in Remote Learning?')
plt.tight_layout()
plt.show()

# Learning Preference - Bar Chart
plt.figure(figsize=(10, 6))
pref_counts = df_cleaned['Learning_Preference'].value_counts()
sns.barplot(y=pref_counts.index, x=pref_counts.values, palette="cubehelix")
plt.title('Preferred Learning Mode Post-Pandemic')
plt.xlabel('Count')
plt.ylabel('Preference')
plt.tight_layout()
plt.show()
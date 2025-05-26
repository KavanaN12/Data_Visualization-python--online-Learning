import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from scipy.stats import ttest_ind
#1st program
# Set up styling
sns.set(style='whitegrid')

# === LOAD DATA ===
# Update path as needed if you're not in notebook or script with these files locally
traditional_file = 'ThirdCaseStudy_Both_Traditional_2019-2020.txt'
online_file = 'ThirdCaseStudy_Both_online_2020-2021.txt'

# Assign column names based on file structure
traditional_cols = ['A1','A2','A3','A4','A5','A6','A7','Exam','FinalScore','Lab','PartialScore','Grade']
online_cols = ['A1','A2','A3','A4','A5','A6','A7','Lab','FinalScore','Grade']

# Load data
df_trad = pd.read_csv(traditional_file, names=traditional_cols)
df_online = pd.read_csv(online_file, names=online_cols)

# Add learning mode labels
df_trad['Learning_Mode'] = 'Face-to-Face'
df_online['Learning_Mode'] = 'Online'

# Select relevant columns
df_trad = df_trad[['FinalScore', 'Grade', 'Learning_Mode']]
df_online = df_online[['FinalScore', 'Grade', 'Learning_Mode']]

# Combine datasets
df = pd.concat([df_trad, df_online], ignore_index=True)

# Clean data
df['FinalScore'] = pd.to_numeric(df['FinalScore'], errors='coerce')
df.dropna(subset=['FinalScore'], inplace=True)

# === SUMMARY STATISTICS ===
print("=== Summary Statistics ===")
print(df.groupby('Learning_Mode')['FinalScore'].describe())

# === SCATTER PLOT ===
plt.figure(figsize=(10, 5))
sns.stripplot(data=df, x='Learning_Mode', y='FinalScore', jitter=True, alpha=0.7)
plt.title('Scatter Plot of Final Scores by Learning Mode')
plt.ylabel('Final Score')
plt.xlabel('Learning Mode')
plt.tight_layout()
plt.show()

# === BAR CHART OF GRADE DISTRIBUTION ===
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Grade', hue='Learning_Mode',
              order=sorted(df['Grade'].unique()))
plt.title('Grade Distribution by Learning Mode')
plt.xlabel('Grade')
plt.ylabel('Number of Students')
plt.legend(title='Learning Mode')
plt.tight_layout()
plt.show()

# === PIE CHARTS FOR EACH MODE ===
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Face-to-Face Grades
ftf_counts = df[df['Learning_Mode'] == 'Face-to-Face']['Grade'].value_counts()
axs[0].pie(ftf_counts, labels=ftf_counts.index, autopct='%1.1f%%',
           colors=sns.color_palette("Blues", len(ftf_counts)))
axs[0].set_title('Grades - Face-to-Face')

# Online Grades
online_counts = df[df['Learning_Mode'] == 'Online']['Grade'].value_counts()
axs[1].pie(online_counts, labels=online_counts.index, autopct='%1.1f%%',
           colors=sns.color_palette("Reds", len(online_counts)))
axs[1].set_title('Grades - Online')

plt.tight_layout()
plt.show()

# === T-TEST ===
ftf_scores = df[df['Learning_Mode'] == 'Face-to-Face']['FinalScore']
online_scores = df[df['Learning_Mode'] == 'Online']['FinalScore']

t_stat, p_value = ttest_ind(ftf_scores, online_scores, equal_var=False)

print("\n=== T-Test Result ===")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")
if p_value < 0.05:
    print("Conclusion: Statistically significant difference between learning modes.")
else:
    print("Conclusion: No statistically significant difference.")
#2nd program
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
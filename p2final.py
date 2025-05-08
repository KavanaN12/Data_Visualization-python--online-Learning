import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

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

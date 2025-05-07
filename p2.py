import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Seed for reproducibility
np.random.seed(42)

# Generate synthetic data
n_students = 1000
nim = [f"S{i:03d}" for i in range(1, n_students + 1)]
ftf_scores = np.random.normal(loc=84, scale=5, size=n_students).clip(70, 100)
online_scores = np.random.normal(loc=73, scale=8, size=n_students).clip(50, 99)

# Grade calculation function
def calculate_grade(score):
    if score >= 85:
        return 'A'
    elif score >= 75:
        return 'B'
    elif score >= 55:
        return 'C'
    else:
        return 'D'

# Create DataFrame
df = pd.DataFrame({
    "NIM": nim,
    "FTF_score": ftf_scores.round(1),
    "Online_score": online_scores.round(1)
})

# Grades and preferences
df["FTF_grade"] = df["FTF_score"].apply(calculate_grade)
df["Online_grade"] = df["Online_score"].apply(calculate_grade)

# Simulated survey preference
df["Preferred"] = np.where(np.random.rand(n_students) < 0.93, "Face-to-Face", "Online")

print(df.head())

# --- Visualizations ---

# 1. Scatter plot
plt.figure(figsize=(10, 5))
sns.scatterplot(x="NIM", y="FTF_score", data=df, color="blue", label="FTF Score")
sns.scatterplot(x="NIM", y="Online_score", data=df, color="red", label="Online Score")
plt.title("Student Scores: Face-to-Face vs Online")
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()
plt.show()

# 2. Bar chart of grades
ftf_grade_counts = df["FTF_grade"].value_counts().sort_index()
online_grade_counts = df["Online_grade"].value_counts().sort_index()

grade_df = pd.DataFrame({
    "Grade": ["A", "B", "C", "D"],
    "FTF": ftf_grade_counts.reindex(["A", "B", "C", "D"], fill_value=0),
    "Online": online_grade_counts.reindex(["A", "B", "C", "D"], fill_value=0)
}).melt(id_vars="Grade", var_name="Method", value_name="Count")

plt.figure(figsize=(8, 6))
sns.barplot(x="Grade", y="Count", hue="Method", data=grade_df)
plt.title("Grade Distribution by Learning Method")
plt.show()

# 3. Pie chart for preferences
plt.figure(figsize=(6, 6))
df["Preferred"].value_counts().plot.pie(autopct='%1.1f%%', colors=["skyblue", "lightgreen"])
plt.title("Student Learning Method Preferences")
plt.ylabel("")
plt.show()

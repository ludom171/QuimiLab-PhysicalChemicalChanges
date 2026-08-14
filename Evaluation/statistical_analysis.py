import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import kruskal, spearmanr
from decimal import Decimal, ROUND_HALF_UP

path_data = 'anonymized_responses.csv'

df = pd.read_csv(path_data, delimiter=';', encoding='cp1252',decimal=',')

df = df.iloc[:, :35].copy() 

df.columns = [
    "Experience", "Profile",
    "U1", "U2", "U3", "U4", "U5", "Usability_original",
    "TQ1", "TQ2", "TQ3", "TQ4", "TQ5", "TechnicalQuality_original",
    "PEF1", "PEF2", "PEF3", "PEF4", "PEF5", "PEF_original",
    "AAP1", "AAP2", "AAP3", "AAP4", "AAP5", "AAP_original",
    "Student1", "Student2", "Student3",
    "LabStaff1", "LabStaff2", "LabStaff3",
    "Faculty1", "Faculty2", "Faculty3"
    ]

dimensions = {
    "Usability": ["U1", "U2", "U3", "U4", "U5"],
    "Technical Quality": ["TQ1", "TQ2", "TQ3", "TQ4", "TQ5"],
    "Perceived Experimental Fidelity": ["PEF1", "PEF2", "PEF3", "PEF4", "PEF5"],
    "Acceptance and Adoption Potential": ["AAP1", "AAP2", "AAP3", "AAP4", "AAP5"]
}

for name, items in dimensions.items():
    df[name] = df[items].mean(axis=1)

common_items = [item for items in dimensions.values() for item in items]

df["Overall"] = df[common_items].mean(axis=1)

def cronbach_alpha(data):
    """
    Calculate Cronbach's alpha for a given dataset.
    """
    K = data.shape[1]
    variances = data.var(axis=0, ddof=1).sum()
    total_variance = data.sum(axis=1).var(ddof=1)
    return (K / (K - 1)) * (1 - (variances / total_variance))

def ftm(value, decimals=2):
    """
    Format a float value to a string with specified decimal places.
    """
    pattern = "0." + "0" * decimals
    return str(Decimal(str(value)).quantize(Decimal(pattern), rounding=ROUND_HALF_UP))

print(f"Participants: {len(df)}")

print(f"\nOverall perception:"
      f"\nM = {ftm(df['Overall'].mean())},"
      f"\nSD = {ftm(df['Overall'].std())}"
      )

print("\nDimension Results:")
for name, items in dimensions.items():
    print(f"{name}: "
          f"\nM = {ftm(df[name].mean())},"
          f"\nSD = {ftm(df[name].std())},"
          f"\nCronbach's alpha = {ftm(cronbach_alpha(df[items]))}"
          )

item_table ={
    "Academic Integration": "AAP1",
    "Continuity": "AAP4",
    "Expansion Potential": "AAP5",
    "Recommendation": "AAP3",
    "Reuse Intention": "AAP2",

    "Virtual Interaction": "U4",
    "Ease of Adoption": "U5",
    "Navigation": "U1",
    "Interface Organization": "U2",
    "Technical Quality": "TQ5"
}

print("\nItem Level Results:")
for label, column in item_table.items():
    print(f"{label}: "
          f"\nM = {ftm(df[column].mean())},"
          f"\nSD = {ftm(df[column].std())}"
          )

profile_map = {
    "Estudiante" : "Students",
    "Instructor de laboratorio" : "Laboratory Staff",
    "Docente" : "Faculty Members"
}

profile_order = ["Students", "Laboratory Staff", "Faculty Members"]

df["Profile_EN"] = df["Profile"].replace(profile_map)

profile_summary = (df.groupby("Profile_EN")["Acceptance and Adoption Potential"].agg(["mean", "std", "count"]).reindex(profile_order))

profile_groups = [df.loc[df["Profile_EN"] == profile, "Acceptance and Adoption Potential"] for profile in profile_order]

H, p_kw = kruskal(*profile_groups)

print("\nAcceptance and Adoption Potential by Participant Profile:")
for profile, row in profile_summary.iterrows():
    print(f"{profile}: "
          f"M = {ftm(row['mean'])}, "
          f"SD = {ftm(row['std'])}, "
          f"n = {int(row['count'])}")

print(f"\nKruskal-Wallis Test:"
      f"\nH = {ftm(H)}, "
      f"\np = {ftm(p_kw, 3)}"
      )

experience_map = {
    "Ninguna": "None",
    "Básica": "Basic",
    "Intermedia": "Intermediate",
    "Avanzada": "Advanced"
}

experience_order = ["None", "Basic", "Intermediate", "Advanced"]

experience_code = {
    "None": 0,
    "Basic": 1,
    "Intermediate": 2,
    "Advanced": 3
}

df["Experience_EN"] = df["Experience"].replace(experience_map)

df["Experience_Code"] = df["Experience_EN"].map(experience_code)

experience_summary = (df.groupby("Experience_EN")["Overall"].agg(["mean", "std", "count"]).reindex(experience_order))

rho, p_spearman = spearmanr(df["Experience_Code"], df["Overall"])

print("\nOverall Perception by Previous Experience Level:")
for experience, row in experience_summary.iterrows():
    print(f"{experience}: "
          f"M = {ftm(row['mean'])}, "
          f"SD = {ftm(row['std'])}, "
          f"n = {int(row['count'])}"
          )

print(f"\nSpearman's Rank Correlation:"
      f"\nrho = {ftm(rho, 3)}, "
      f"\np = {ftm(p_spearman, 3)}"
      )

#Figure 5

dimension_order = [
    "Acceptance and Adoption Potential",
    "Perceived Experimental Fidelity",
    "Technical Quality",
    "Usability"
]

means = [df[name].mean() for name in dimension_order]
sds = [df[name].std() for name in dimension_order]

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(dimension_order, means, xerr=sds, capsize=4)
ax.invert_yaxis()
ax.set_xlim(0, 5.6)
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xlabel("Mean perception score (1-5)")
ax.grid(axis='x', linestyle='--', alpha=0.25)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for bar, mean in zip(bars, means):
    ax.text(mean - 0.15, bar.get_y() + bar.get_height() * 0.28,
            f"{ftm(mean)}", va='center', ha='right', color='white', fontsize=10, fontweight='bold')

fig.tight_layout()
fig.savefig("figure_5.pdf", bbox_inches='tight')

plt.close(fig)

# Figure 6

fig, ax = plt.subplots(figsize=(8, 4.2))
bars = ax.barh(profile_summary.index, profile_summary['mean'], xerr=profile_summary['std'], capsize=4)
ax.invert_yaxis()
ax.set_xlim(0, 5.6)
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xlabel("Mean Acceptance and Adoption Potential score (1–5)")
ax.grid(axis='x', linestyle='--', alpha=0.25)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for bar, mean, n in zip(bars, profile_summary['mean'], profile_summary['count']):
    ax.text(mean - 0.15, bar.get_y() + bar.get_height() * 0.28,
            f"{ftm(mean)}", va='center', ha='right', color='white', fontsize=10, fontweight='bold')
    ax.text(0.10, bar.get_y() + bar.get_height() / 2,
            f"n={int(n)}", va='center', ha='left', color='white', fontsize=10)

fig.tight_layout()
fig.savefig("figure_6.pdf", bbox_inches='tight')
plt.close(fig)

#Figure 7

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(experience_summary.index, experience_summary['mean'], xerr=experience_summary['std'], capsize=4)
ax.invert_yaxis()
ax.set_xlim(0, 5.6)
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xlabel("Overall perception score (1–5)")
ax.grid(axis='x', linestyle='--', alpha=0.25)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for bar, mean, n in zip(bars, experience_summary['mean'], experience_summary['count']):
    ax.text(mean - 0.15, bar.get_y() + bar.get_height() * 0.28,
            f"{ftm(mean)}", va='center', ha='right', color='white', fontsize=10, fontweight='bold')
    ax.text(0.10, bar.get_y() + bar.get_height() / 2,
            f"n={int(n)}", va='center', ha='left', color='white', fontsize=10)

fig.tight_layout()
fig.savefig("figure_7.pdf", bbox_inches='tight')
plt.close(fig)


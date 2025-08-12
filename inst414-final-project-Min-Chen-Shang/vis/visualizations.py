# vis/visualizations.py

import matplotlib.pyplot as plt
import seaborn as sns

def generate_visualizations(model, data_dict):
    """
    Generate basic EDA visualizations from cleaned data.
    
    Args:
        model: trained model (not used yet)
        data_dict: dictionary containing cleaned 'appointments' and 'cms' DataFrames
    """
    print("Generating visualizations...")

    df = data_dict["appointments"]

    # No-show rate by gender
    plt.figure(figsize=(6, 4))
    sns.countplot(x='gender', hue='no_show', data=df)
    plt.title("No-show Count by Gender")
    plt.xlabel("Gender")
    plt.ylabel("Count")
    plt.legend(title="No-show", labels=["Show", "No-show"])
    plt.tight_layout()
    plt.show()

    # No-show rate by age
    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x='age', hue='no_show', multiple='stack', bins=20)
    plt.title("Age Distribution by Show/No-show")
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()
#
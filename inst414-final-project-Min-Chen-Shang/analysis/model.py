# analysis/model.py

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

def train_model(data_dict, model_type="logistic"):
    """
    Train a classification model to predict no-shows.
    
    Args:
        data_dict (dict): Dictionary containing the processed 'appointments' DataFrame.
        model_type (str): 'logistic' or 'random_forest'
    
    Returns:
        model: trained model
        X_test, y_test: testing set for evaluation
    """
    df = data_dict["appointments"]

    # Features and target
    X = df[["age", "lead_time"]]  
    y = df["no_show"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_type == "logistic":
        model = LogisticRegression(max_iter=1000)
    elif model_type == "random_forest":
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        raise ValueError("Unsupported model type.")

    model.fit(X_train, y_train)

    return model, X_test, y_test
#
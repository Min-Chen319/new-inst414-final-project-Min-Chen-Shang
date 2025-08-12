# main.py
# Entry point for the Patient No-Show Prediction Pipeline

from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

from analysis.model import train_model
from analysis.evaluate import evaluate_model

from vis.visualizations import generate_visualizations

def main():
    print("Starting ETL pipeline...")
    raw_data_paths = extract_data()
    processed_data = transform_data(raw_data_paths)
    load_data(processed_data)

    print("Running analysis...")
    model, X_test, y_test = train_model(processed_data)
    evaluate_model(model, X_test, y_test)

    print("Generating visualizations...")
    generate_visualizations(model, processed_data)

    print("Pipeline execution complete.")

if __name__ == "__main__":
    main()
#Remove cvs file to allow push
#update 08/03

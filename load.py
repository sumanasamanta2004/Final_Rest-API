import joblib
import pandas as pd

# Load the saved model
loaded_model = joblib.load("iris_regression_model.pkl")

# Example: predict on new data
# Make sure new_data has same structure (same columns as training X)
new_data = pd.DataFrame({
    'sepal_length': [5.1],
    'sepal_width': [3.5],
    'petal_width': [0.2]
})

# Predict
prediction = loaded_model.predict(new_data)
print("Predicted petal_length:", prediction[0])

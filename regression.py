import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load CSV file
df = pd.read_csv(r"D:\OneDrive\Desktop\model-2(Rest API last project)\iris.csv")

# Show data and column names
print("Iris Dataset:")
print(df.head())
print("\nColumn names:", df.columns.tolist())

# Use only numeric columns as features
X = df.drop(columns=['petal_length', 'species'])
y = df['petal_length']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("\nModel Evaluation:")
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R^2 Score:", r2_score(y_test, y_pred))

# Show predictions
results = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print("\nActual vs Predicted:")
print(results.head())




#save the model

import joblib

# Save the model to a file
joblib.dump(model, "iris_regression_model.pkl")

print("Model saved as iris_regression_model.pkl")

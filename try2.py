#pip install scikit-learn
# Import necessary libraries

#RANDOM FOREST 


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.exceptions import NotFittedError

# Load your dataset
# Assuming your dataset is already cleaned
try:
    data = pd.read_csv("dataset/laptops.csv")
except FileNotFoundError:
    print("Dataset not found. Ensure the file path is correct.")
    exit()

# Ensure the dataset has the required columns
required_columns = ['ram', 'processor', 'os', 'storage', 'laptop_brand', 'usecases']
if not all(col in data.columns for col in required_columns):
    print("Dataset missing required columns. Please check your dataset.")
    exit()

# Features (X) and Target (y)
X = data[['ram', 'processor', 'os', 'storage', 'laptop_brand']]
y = data['usecases']

# Preprocessing: One-Hot Encoding for categorical features
X_encoded = pd.get_dummies(X, drop_first=True)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestClassifier(random_state=42)
try:
    model.fit(X_train, y_train)
except ValueError:
    print("Error training the model. Check your data consistency.")
    exit()

# User Input Function
def get_user_input():
    print("\nPlease enter your laptop preferences:")
    ram = input("Enter RAM size (e.g., 8GB, 16GB): ").strip().lower()
    processor = input("Enter Processor type (e.g., i5, Ryzen 5): ").strip().lower()
    os = input("Enter Operating System (e.g., Windows, Linux): ").strip().lower()
    storage = input("Enter Storage size (e.g., 512GB SSD, 1TB HDD): ").strip().lower()
    laptop_brand = input("Enter Laptop Brand (e.g., Dell, HP): ").strip().lower()
    return {
        'ram': ram,
        'processor': processor,
        'os': os,
        'storage': storage,
        'laptop_brand': laptop_brand
    }

# Recommendation Function
def recommend_laptop():
    try:
        user_input = get_user_input()
        user_df = pd.DataFrame([user_input])
        user_encoded = pd.get_dummies(user_df, drop_first=True)
        # Align columns with training data
        user_encoded = user_encoded.reindex(columns=X_encoded.columns, fill_value=0)
        prediction = model.predict(user_encoded)
        print(f"\nRecommended laptop use case: {prediction[0]}")
    except NotFittedError:
        print("The model is not trained yet. Train the model before making predictions.")
    except ValueError as e:
        print(f"An error occurred during prediction: {e}")

# Call Recommendation
recommend_laptop()

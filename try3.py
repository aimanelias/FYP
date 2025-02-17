#TF IDF AND RANDOM FOREST INTERFACE

#python try3.py
import pickle

try:
    with open('model/rf_model.pkl', 'rb') as file:
        rf_model = pickle.load(file)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error: {e}")
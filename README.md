# Laptop Recommender System

A Content-Based Laptop Recommendation system that leverages **TF-IDF**, **Cosine Similarity**, and **Random Forest** for accurate laptop type prediction and personalized recommendations.

## Features

- **Laptop Type Prediction:** Predicts the most suitable laptop type (e.g., Office, Gaming) based on user preferences.
- **Top 5 Recommendations:** Provides the top 5 laptops matching user-specified criteria.
- **Interactive Web App:** User-friendly interface built with Streamlit.
- **Data Visualization:** Compare recommended laptops with interactive tables and images.
- **High Accuracy:** Achieved 98.75% accuracy and 95.44% cross-validation score.
- **Agile Development:** Developed using Agile methodology for iterative improvement.

## Tech Stack

- **Python**
- **Streamlit** (Web UI)
- **scikit-learn** (TF-IDF, Random Forest, Cosine Similarity)
- **Plotly** (Visualization)
- **Jupyter Notebook** (Development & Analysis)

## Dataset

- The system uses curated datasets of laptops and use cases, located in the `dataset/` directory.

## Getting Started

### 1. Clone the Repository

```bash
git clone <repo-url>
cd <repo-directory>
```

### 2. Set Up a Virtual Environment

```bash
# Install virtualenv if you don't have it
pip install virtualenv

# Create a new environment named 'env'
python -m venv env

# Activate the environment (Windows)
.\env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser. Fill in your laptop preferences to get predictions and recommendations.

## File Structure

- `app.py` — Main entry point for the Streamlit app.
- `pages/` — Contains additional Streamlit pages (About, Project, Analysis, Recommendation logic).
- `model/` — Pre-trained models and vectorizers.
- `dataset/` — CSV files with laptop data and use cases.
- `templates/` — Images and static assets.
- `requirements.txt` — Python dependencies.
- `HOW TO.txt` — Step-by-step setup instructions.

## Screenshots

*(Add screenshots of the app interface and recommendations here)*

## Methodology

- **TF-IDF Vectorization:** Converts laptop specifications into feature vectors.
- **Cosine Similarity:** Finds laptops most similar to user preferences.
- **Random Forest Classifier:** Predicts the laptop type (e.g., Office, Gaming).
- **Streamlit UI:** Collects user input and displays results interactively.

## Results

- **Model Accuracy:** 98.75%
- **Cross-Validation Score:** 95.44%

## License

*(Specify your license here, e.g., MIT, if applicable)*

## Acknowledgements

- Developed as part of a degree project using Agile methodology.
- Special thanks to open-source contributors and dataset providers.

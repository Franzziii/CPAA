import nltk
import os
import shutil

# Define paths
CUSTOM_NLTK_DIR = os.path.join(os.getcwd(), "nltk_data")
DEFAULT_NLTK_DIR = os.path.join(os.path.expanduser("~"), "nltk_data")

print(f"Downloading NLTK data to: {CUSTOM_NLTK_DIR}")

# Create directory if it doesn't exist
os.makedirs(CUSTOM_NLTK_DIR, exist_ok=True)

# Download required datasets
nltk.download('punkt', download_dir=CUSTOM_NLTK_DIR)
nltk.download('stopwords', download_dir=CUSTOM_NLTK_DIR)
nltk.download('punkt_tab', download_dir=CUSTOM_NLTK_DIR)

print("NLTK data downloaded successfully!")
print("You can now run app.py without internet connection.")
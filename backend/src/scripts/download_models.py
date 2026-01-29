import os
import urllib.request

# -----------------------------
# Config
# -----------------------------
MODEL_URL = "https://huggingface.co/orel12/ggml-gpt4all-j-v1.3-groovy/resolve/main/ggml-gpt4all-j-v1.3-groovy.bin?download=true"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "ggml-gpt4all-j-v1.3-groovy.bin")

# -----------------------------
# Create models folder
# -----------------------------
os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# Download
# -----------------------------
if os.path.exists(MODEL_PATH):
    print(f"Model already exists at {MODEL_PATH}, skipping download.")
else:
    print(f"Downloading GPT4All-J 3B to {MODEL_PATH} ...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Download complete!")

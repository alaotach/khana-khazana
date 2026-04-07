# Khana Khazana

Khana Khazana is a social recipe sharing platform where you can share your amazing and delicious special recipes with the world and become a popular chef among the world haha.

It is a Flask app that allows you to easily create and browse recipes, upload images, and format your culinary ideas with a nice text editor.

## Features
- **create and browse recipes**: easily add new dishes with detailed ingredients and instructions.
- **image uploads**: image uploading directly into the editor and the max upload size is capped at 5MB.
- **spam protection**: rate limited endpoints to prevent spam on recipe creation and uploads.
- **storage cleanup**: session based tracker clean up for non used images that get uploaded but aren't published with a submitted recipe.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alaotach/khana-khazana
   cd khana-khazana
   ```

2. **Install packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```
   The app will run locally at `http://localhost:3459` (or `http://0.0.0.0:3459`).
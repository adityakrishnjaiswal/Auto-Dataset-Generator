# AutoDatasetGenerator

**AutoDatasetGenerator** is a powerful tool designed to streamline the process of generating datasets for YOLO (You Only Look Once), an object detection framework. This tool helps create annotated datasets needed for training YOLO models, simplifying data preparation and boosting productivity for computer vision projects.

## Features

- **Easy-to-Use Interface**: A user-friendly frontend for seamless dataset generation.
- **Efficient Data Handling**: Manage and annotate images for training in real-time.
- **YOLO Compatibility**: Generates dataset formats compatible with YOLO for immediate use.

## Project Structure

- **frontend/**: Contains the React-based frontend application.
- **backend/**: Python-based backend that handles data processing and annotation tasks.
- **node_modules/**: Node.js dependencies (ignored by Git).
- **env/**: Python virtual environment (ignored by Git).

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.x
- Node.js and npm

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/adityakrishnjaiswal/Auto-Dataset-Generator/
   cd Auto-Dataset-Generator
   ```

2. **Set up the backend**:
   ```bash
   cd backend
   python -m venv env
   source env/bin/activate  # For macOS/Linux
   .\env\Scripts\activate  # For Windows
   pip install -r requirements.txt
   ```

3. **Set up the frontend**:
   ```bash
   cd ../frontend
   npm install
   ```

## Running the Application

### Backend

Start the backend server:
   ```bash
   cd backend
   python app.py
   ```

The backend should now be running, and you can access it on `http://localhost:5000` (or the port specified in your `app.py`).

### Frontend

Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

The frontend should now be running on `http://localhost:3000` (or the port specified in your `package.json`).

## Usage

1. Open the frontend application in your web browser.
2. Upload images for annotation.
3. Use the annotation tools to label objects in the images.
4. Save and export the annotated dataset in YOLO format.

## Contributing

Contributions are welcome! If you would like to contribute, please fork the repository and submit a pull request. Ensure your code is well-documented and tested before submitting.

### Steps to contribute:

1. Fork the repository.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/adityakrishnjaiswal/Auto-Dataset-Generator/
   ```
3. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```
5. Push your changes:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Create a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **YOLO Framework**: Special thanks to the YOLO object detection framework for making advanced object detection accessible.
- **Contributors**: We appreciate the contributions from the open-source community.


from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import shutil
import zipfile
from frameextractor import extract_frames
from annotate import YOLOAnnotationGenerator
from createyaml import DatasetYamlCreator

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Define folder paths
uploads_folder = r"C:\Users\Admin\Desktop\AutoDataset-Generator\uploads"
video_folder = os.path.join(uploads_folder, 'videos')
reference_folder = os.path.join(uploads_folder, 'reference-images')
frames_folder = os.path.join(uploads_folder, 'frames')
output_folder = r'C:\Users\Admin\Desktop\AutoDataset-Generator\output'
labels_folder = os.path.join(output_folder, 'labels')

# Ensure the necessary folders exist
os.makedirs(video_folder, exist_ok=True)
os.makedirs(reference_folder, exist_ok=True)
os.makedirs(frames_folder, exist_ok=True)
os.makedirs(labels_folder, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_files():
    """
    Handles file uploads for video and reference images.
    Returns a JSON response indicating the status of the upload.
    """
    try:
        # Retrieve video and reference images from the request
        video_file = request.files.get('video')
        reference_images = request.files.getlist('references')

        # Validate video file
        if not video_file:
            return jsonify({"error": "No video file uploaded."}), 400
        if not video_file.filename.endswith(('.mp4', '.avi', '.mov')):
            return jsonify({"error": "Invalid video file format. Only .mp4, .avi, or .mov are allowed."}), 400

        # Save video file to the designated folder
        video_path = os.path.join(video_folder, video_file.filename)
        if os.path.exists(video_path):
            return jsonify({"error": "Video file already exists."}), 409
        video_file.save(video_path)

        # Save reference images
        reference_paths = []
        for img in reference_images:
            if not img.filename.endswith(('.png', '.jpg', '.jpeg')):
                return jsonify({"error": f"Invalid image file format: {img.filename}. Only .png, .jpg, or .jpeg are allowed."}), 400

            reference_path = os.path.join(reference_folder, img.filename)
            if os.path.exists(reference_path):
                return jsonify({"error": f"Image {img.filename} already exists."}), 409

            img.save(reference_path)
            reference_paths.append(reference_path)

        return jsonify({
            "message": "Files uploaded successfully. Click 'Generate' to start processing.",
            "video_path": video_path,
            "reference_images": reference_paths
        })

    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route('/process', methods=['POST'])
def generate_dataset():
    """
    Processes the uploaded video and reference images to generate the dataset.
    Returns a JSON response indicating the status of dataset generation.
    """
    try:
        # Check for existing video files in the video folder
        video_files = os.listdir(video_folder)
        if not video_files:
            return jsonify({"error": "No video file found for processing."}), 400

        # Process the first video file found
        video_name, video_extension = os.path.splitext(video_files[0])
        video_path = os.path.join(video_folder, video_name)
        os.makedirs(video_path, exist_ok=True)

        # Check for existing reference images
        if not os.listdir(reference_folder):
            return jsonify({"error": "No reference images found for processing."}), 400

        # Extract frames from the video
        extract_frames(video_folder, frames_folder)

        # Generate class labels and annotations
        generator = YOLOAnnotationGenerator(reference_folder, frames_folder, labels_folder)
        generator.create_class_labels()
        generator.generate_annotations()

        # Create dataset YAML file
        yaml_output_path = os.path.join(output_folder, 'dataset.yaml')
        creator = DatasetYamlCreator(reference_folder, output_folder, yaml_output_path)
        creator.generate_yaml()

        return jsonify({
            "message": "Dataset generated successfully!",
            "yaml_file": yaml_output_path
        })

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

@app.route('/download', methods=['GET'])
def download_dataset():
    """
    Creates a ZIP file containing the generated dataset and returns it as a download.
    """
    try:
        # Define paths for dataset subdirectories
        dataset_dirs = ['train', 'val', 'test']
        subfolders = ['images', 'labels']
        zip_file_path = os.path.join(output_folder, 'datasets.zip')

        # Ensure dataset subdirectories exist
        for dataset_dir in dataset_dirs:
            for subfolder in subfolders:
                folder_path = os.path.join(output_folder, dataset_dir, subfolder)
                os.makedirs(folder_path, exist_ok=True)

        # Copy image and label files to their respective dataset subdirectories
        for dataset_dir in dataset_dirs:
            for file in os.listdir(frames_folder):
                if file.endswith(('.jpg', '.jpeg', '.png')):
                    src_path = os.path.join(frames_folder, file)
                    dest_path = os.path.join(output_folder, dataset_dir, 'images', file)
                    shutil.copy(src_path, dest_path)
            for file in os.listdir(labels_folder):
                if file.endswith(('.txt')):
                    src_path = os.path.join(labels_folder, file)
                    dest_path = os.path.join(output_folder, dataset_dir, 'labels', file)
                    shutil.copy(src_path, dest_path)

        # Remove the original labels folder after copying
        shutil.rmtree(labels_folder)
        
        # Create a ZIP file containing all dataset files
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for root, _, files in os.walk(output_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_folder)
                    zipf.write(file_path, arcname)

        # Return the ZIP file as an attachment
        return send_file(zip_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 500

if __name__ == "__main__":
    try:
        # Run the Flask application on port 5000 with debug mode enabled
        app.run(debug=True, port=5000)
    except SystemExit as e:
        print(f"SystemExit caught: {e}")
    except Exception as e:
        print(f"Error starting the server: {e}")
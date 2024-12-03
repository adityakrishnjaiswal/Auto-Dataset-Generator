import os
import yaml

class DatasetYamlCreator:
    def __init__(self, reference_folder, dataset_directory, yaml_file_path):
        """
        Initializes the DatasetYamlCreator instance with provided paths.
        
        Parameters:
        reference_folder (str): Path to the folder containing reference images.
        dataset_directory (str): Path to the directory where the dataset folders will be created.
        yaml_file_path (str): Path for the output YAML file.
        """
        self.reference_folder = reference_folder
        self.dataset_directory = dataset_directory
        self.yaml_file_path = yaml_file_path

    def create_folders(self):
        """
        Creates the necessary subdirectories for training, validation, and testing datasets.
        Each dataset folder includes subfolders for images and labels.
        """
        # List of main dataset folders (train, val, test)
        folders = ['train', 'val', 'test']
        # Subfolders for storing images and labels
        subfolders = ['images', 'labels']

        for folder in folders:
            for subfolder in subfolders:
                path = os.path.join(self.dataset_directory, folder, subfolder)
                os.makedirs(path, exist_ok=True)  # Create directories if they do not exist

    def process_image_names(self):
        """
        Processes the image filenames in the reference folder to extract unique base names.
        
        Returns:
        list: Sorted list of unique image names without extensions.
        """
        # Extract base names from the image files, ignoring file extensions and extra parts
        image_names = [os.path.splitext(os.path.splitext(file)[0].split('-')[0])[0]
                       for file in os.listdir(self.reference_folder)
                       if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

        # Remove duplicates and sort the names
        unique_modified_names = set(image_names)
        sorted_names = sorted(unique_modified_names)
        return sorted_names

    def create_yaml_file(self, sorted_names):
        """
        Creates a YAML file containing the dataset configuration.
        
        Parameters:
        sorted_names (list): Sorted list of unique image names for dataset classes.
        """
        # Construct the YAML data structure
        yaml_data = {
            "names": sorted_names,
            "namescount": len(sorted_names),  # Count of unique image names
            "train": "dataset/train/images",
            "val": "dataset/val/images",
            "test": "dataset/test/images",
        }

        # Write the YAML data to the specified file
        with open(self.yaml_file_path, 'w') as yaml_file:
            yaml.dump(yaml_data, yaml_file, default_flow_style=False, allow_unicode=True)

    def generate_yaml(self):
        """
        Generates the dataset YAML file by calling the necessary methods to create folders,
        process image names, and write the YAML file.
        """
        # Create the required directory structure for the dataset
        self.create_folders()
        # Get sorted image names from the reference folder
        sorted_names = self.process_image_names()
        # Create the YAML file with the processed image names
        self.create_yaml_file(sorted_names)

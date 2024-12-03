import os
import cv2

class YOLOAnnotationGenerator:
    def __init__(self, reference_folder, frames_folder, labels_folder):
        """
        Initializes the YOLOAnnotationGenerator with paths for reference images, frames to process, and labels output folder.
        """
        self.reference_folder = reference_folder
        self.frames_folder = frames_folder
        self.labels_folder = labels_folder
        self.class_labels = self.create_class_labels()

    def find_partial_in_full(self, partial_img, full_img):
        """
        Finds the location of the partial image (template) within the full image using template matching.
        Returns the bounding box coordinates if a match with sufficient confidence is found.
        """
        if partial_img is None or full_img is None:
            raise ValueError("One or both images are not loaded correctly.")

        # Convert images to grayscale for template matching
        partial_gray = cv2.cvtColor(partial_img, cv2.COLOR_BGR2GRAY)
        full_gray = cv2.cvtColor(full_img, cv2.COLOR_BGR2GRAY)

        # Resize the partial image if it is larger than the full image
        if partial_gray.shape[0] > full_gray.shape[0] or partial_gray.shape[1] > full_gray.shape[1]:
            scale_factor = min(full_gray.shape[0] / partial_gray.shape[0], full_gray.shape[1] / partial_gray.shape[1])
            partial_gray = cv2.resize(partial_gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)

        # Apply template matching
        res = cv2.matchTemplate(full_gray, partial_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # Check if the confidence threshold is met
        if max_val > 0.8:  # Confidence threshold set at 0.8
            top_left = max_loc
            h, w = partial_gray.shape
            return (top_left[0], top_left[1], w, h)
        else:
            return None

    def convert_to_yolo_format(self, bbox, image_shape):
        """
        Converts the bounding box coordinates from pixel values to YOLO format.
        YOLO format uses normalized values (x_center, y_center, width, height).
        """
        if image_shape[1] == 0 or image_shape[0] == 0:
            raise ValueError("Image dimensions are invalid for YOLO conversion.")
        
        dw = 1.0 / image_shape[1]
        dh = 1.0 / image_shape[0]
        
        x, y, w, h = bbox
        x_center = x + w / 2.0
        y_center = y + h / 2.0
        return [x_center * dw, y_center * dh, w * dw, h * dh]

    def create_class_labels(self):
        """
        Creates a dictionary of class labels from the reference folder.
        The dictionary maps the class name to a unique numeric ID.
        """
        class_labels = {}
        label_count = 1  # Start class labels from 1
        for filename in os.listdir(self.reference_folder):
            # Extract label from the filename and ensure uniqueness
            label_name = os.path.splitext(os.path.splitext(filename)[0].split('-')[0])[0]
            if label_name not in class_labels:
                class_labels[label_name] = label_count
                label_count += 1
        return class_labels

    def save_annotations(self, annotation_filepath, annotations):
        """
        Saves the annotations in YOLO format to a text file.
        """
        with open(annotation_filepath, 'w') as annotations_file:
            for annotation in annotations:
                annotations_file.write(f"{annotation}\n")

    def generate_annotations(self):
        """
        Generates YOLO annotations for all frames in the frames folder by matching with reference images.
        Saves the generated annotations as text files in the labels folder.
        """
        if not os.path.exists(self.labels_folder):
            os.makedirs(self.labels_folder)

        for frame in os.listdir(self.frames_folder):
            full_img_path = os.path.join(self.frames_folder, frame)
            full_img = cv2.imread(full_img_path)
            if full_img is None:
                continue  # Skip frames that fail to load

            annotations = []  # List to hold the annotations for the current frame

            for reference_image in os.listdir(self.reference_folder):
                reference_img_path = os.path.join(self.reference_folder, reference_image)
                partial_img = cv2.imread(reference_img_path)
                if partial_img is None:
                    continue  # Skip reference images that fail to load

                label_name = os.path.splitext(reference_image)[0]
                if label_name in self.class_labels:
                    class_label = self.class_labels[label_name]

                    # Find the bounding box of the partial image in the full image
                    bbox = self.find_partial_in_full(partial_img, full_img)
                    if bbox:
                        # Convert the bounding box to YOLO format and append to annotations
                        yolo_bbox = self.convert_to_yolo_format(bbox, full_img.shape)
                        annotations.append(f"{class_label} {' '.join(map(str, yolo_bbox))}")

            # Save annotations if any are found for the current frame
            if annotations:
                annotation_filepath = os.path.join(self.labels_folder, f"{os.path.splitext(frame)[0]}.txt")
                self.save_annotations(annotation_filepath, annotations)

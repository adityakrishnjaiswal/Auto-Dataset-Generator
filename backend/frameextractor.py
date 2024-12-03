import cv2
import os

def extract_frames(video_folder, output_folder):
    """
    Extracts frames from all video files in the specified folder and saves them to the output folder.
    
    Parameters:
    video_folder (str): Path to the folder containing video files.
    output_folder (str): Path to the folder where extracted frames will be saved.
    """
    # Ensure the output directory exists; create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all video files in the folder with supported formats
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv'))]

    # Loop through each video file for frame extraction
    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)

        # Initialize a VideoCapture object to read the video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            # Log an error if the video file cannot be opened
            return f"Error opening video file: {video_path}"

        # Retrieve total frame count and frames per second (FPS) of the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = cap.get(cv2.CAP_PROP_FPS)

        # Calculate the duration of the video in seconds
        duration = total_frames / frame_rate

        # Determine the frames to be extracted based on the video duration and frame rate
        frames_to_extract = [int(frame_rate * t) for t in range(int(duration))]

        # Loop through each specified frame index and extract the frame
        for frame_idx in frames_to_extract:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)  # Move to the specific frame position
            ret, frame = cap.read()

            if not ret:
                # Stop processing if a frame could not be read
                break

            # Construct a filename for the frame with zero-padded indexing
            frame_filename = f"Frame_{frame_idx:04d}.jpg"
            frame_path = os.path.join(output_folder, frame_filename)

            # Save the extracted frame as a JPEG image
            cv2.imwrite(frame_path, frame)

        # Release the video capture object after processing
        cap.release()

        # Clean up by removing the original video file after extraction
        os.remove(video_path)

    # Indicate successful completion of frame extraction
    return "Frame extraction completed successfully."

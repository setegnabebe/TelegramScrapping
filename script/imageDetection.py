import os
import cv2
import torch
import logging
import pandas as pd
from pathlib import Path

# Set up logging
logging.basicConfig(
    filename="object_detection.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Started Object Detection Process.")

# Directory paths
image_dir = "raw_telegram_data"  # Directory containing images to process
output_dir = "detection_results"  # Directory to store detection results
os.makedirs(output_dir, exist_ok=True)

# YOLO model setup
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Use YOLOv5 small model
    logging.info("YOLOv5 model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load YOLOv5 model: {e}")
    raise

# Function to perform object detection on a single image
def detect_objects(image_path):
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image not found or cannot be read: {image_path}")

        # Perform detection
        results = model(image)

        # Extract detection results
        detections = results.pandas().xyxy[0]  # Bounding boxes in Pandas DataFrame
        logging.info(f"Detections made on image {image_path}: {len(detections)} objects found.")

        # Save the annotated image
        annotated_image_path = os.path.join(output_dir, Path(image_path).stem + "_annotated.jpg")
        results.save(save_dir=output_dir)
        logging.info(f"Annotated image saved to {annotated_image_path}.")

        return detections

    except Exception as e:
        logging.error(f"Error during object detection on {image_path}: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error

# Process all images in the image directory
detection_data = []
for image_file in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_file)
    if os.path.isfile(image_path):
        detections = detect_objects(image_path)
        if not detections.empty:
            # Add image file name to the detection results
            detections["image_file"] = image_file
            detection_data.append(detections)

# Combine all detection results into a single DataFrame
if detection_data:
    combined_detections = pd.concat(detection_data, ignore_index=True)

    # Save detections to a CSV file
    detection_csv_path = os.path.join(output_dir, "detection_results.csv")
    combined_detections.to_csv(detection_csv_path, index=False)
    logging.info(f"All detection results saved to {detection_csv_path}.")
else:
    logging.warning("No detections were made on any images.")

logging.info("Object Detection Process Completed Successfully.")

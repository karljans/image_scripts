#!/usr/bin/env python3

# import the necessary packages
import os
import glob
import argparse
import cv2
from detector import ObjectDetection


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input_dir", required=True,
	help="raw/un-annotated sources of image file directory")

ap.add_argument("-w", "--weight_file", required=True,
	help="path to weight file")

ap.add_argument("-o", "--output_dir", default=None,
	help="output directory of processed/annotated image files (default: None)")

ap.add_argument("-ct", "--conf_thresh", default=0.6,
	help="confidence threshold value for detection (default: 0.6)")

ap.add_argument("-iout", "--iou_thresh", default=0.3,
	help="intersection of union threshold value for detection (default: 0.3)")

ap.add_argument("-objs", "--objects", default=[0,1],
	help="desired objects to detect (default: [0, 1]")

ap.add_argument("-msize", "--model_size", default=1280,
	help="size of the model for detection (default: 1280)")

ap.add_argument("-ext", "--image_extension", default="jpg",
	help="extension of the image image file (default: jpg)")

ap.add_argument("-nc", "--number_of_classes", default=2,
	help="denotes how many classes in that dataset (default: 2)")

ap.add_argument("-cn", "--class_names", default=["buoy","vessel"],
	help="name of classes (default: [buoy,vessel])")

ap.add_argument("-cf_name", "--class_file_name", default=None,
	help="writes names of classes and number of classes into the file\
 		 output directory (default: None)")


args = vars(ap.parse_args())

# Function to create subdirectories for labeling
def create_subdirectories(root_dir):
    """
    Creates a directory for labeling.

    Parameters:
        root_dir (str): The root directory path.

    Returns:
        None.
    """
    label_dir = "label"
    try:
        os.mkdir(os.path.join(root_dir, label_dir))
        print(label_dir + " directory is created under " + root_dir + " !!!")
    except OSError as error:
        print("Directory exists !!")

# Determine the label directory based on the output or input directory
label_dir = args["output_dir"]
if args["output_dir"] == None:
    label_dir = args["input_dir"]

# Uncomment the following line to create subdirectories for labeling
# create_subdirectories(label_dir)

# Object detection using YOLO
OD = ObjectDetection(args["weight_file"], args["model_size"], args["conf_thresh"], args["iou_thresh"], args["objects"])

# Loop over all the images in the input directory
for img in glob.glob(args["input_dir"] + "/*." + args["image_extension"]):
    # Determine the label file name corresponding to the current image
    label_file = img.strip().split('/')[-1].split('.' + args["image_extension"])[0]
    label_file += ".txt"

    # Read the image using OpenCV
    cv_image = cv2.imread(img)

    # Detect objects in the image using the YOLO model
    class_ids, _, bboxes_coords, num_detections, _ = OD.detect_objects(cv_image)

    # Process each detected object and write its label to the label file
    with open(label_dir + label_file, 'w'):
        for i in range(num_detections):
            class_id = str(int(class_ids[i]))
            xmin = bboxes_coords[i][0]  # x-coordinate of the top-left corner
            ymin = bboxes_coords[i][1]  # y-coordinate of the top-left corner
            xmax = bboxes_coords[i][2]  # x-coordinate of the bottom-right corner
            ymax = bboxes_coords[i][3]  # y-coordinate of the bottom-right corner

            width = str(xmax - xmin)
            height = str(ymax - ymin)
            center_x = str((xmin + xmax) / 2.0)
            center_y = str((ymin + ymax) / 2.0)

			# Write the label information to the label file
            with open(label_dir + label_file, 'a') as f:
                f.write(class_id + " " + center_x + " " + center_y + " " + width + " " + height + "\r\n")

# Create a class file if specified
if args["class_file_name"] != None:
    with open(args["class_file_name"], 'w') as f:
        f.write("nc: " + str(args["number_of_classes"]) + "\r\nnames: ")
        for i in range(len(args["class_names"])):
            f.write(args["class_names"][i])
            if i != len(args["class_names"]) - 1:
                f.write(", ")
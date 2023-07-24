#!/usr/bin/env python3
from time import time
from ultralytics import YOLO

class ObjectDetection():
    def __init__(self, yolo_model, input_size, conf_thresh, iou_thresh, classes):
        """
        Initialize the ObjectDetection class.

        Parameters:
            yolo_model (str): The path to the YOLO model.
            input_size (int): The size of the input image for the model (e.g., 416).
            conf_thresh (float): The confidence threshold for object detection.
            iou_thresh (float): The IOU (Intersection over Union) threshold for object detection.
            classes (list): A list of class labels used for object detection.

        Returns:
            None.
        """
        # Load the YOLO model with given parameters
        self.model = YOLO(yolo_model, task='detect')
        self.model_size = input_size
        self.conf_thresh = conf_thresh
        self.iou_thresh = iou_thresh
        self.classes = classes

    def detect_objects(self, img):
        """
        Perform object detection on the input image.

        Parameters:
            img (torch.Tensor): The input image as a Torch Tensor.

        Returns:
            class_ids (numpy.ndarray): An array containing the predicted class IDs for each detected object.
            conf_vals (numpy.ndarray): An array containing the confidence values for each detected object.
            bbox_coords (numpy.ndarray): An array containing the bounding box coordinates for each detected object.
            num_detections (int): The total number of detected objects.
            elapsed_time (float): The time taken for object detection in seconds.
        """
        start_time = time()
        num_detections = 0

        # Perform object detection using the YOLO model
        results = self.model(img,
                             conf=self.conf_thresh,
                             half=True,
                             classes=self.classes,
                             device=0,
                             iou=self.iou_thresh,
                             imgsz=self.model_size)
        boxes = results[0].boxes
        num_detections = len(results[0])
        bbox_coords = boxes.xyxyn.to('cpu').numpy()

        end_time = time()
        elapsed_time = end_time - start_time
        elapsed_time = round(elapsed_time, 3)

        # Return the results of object detection
        return boxes.cls.to('cpu').numpy(), boxes.conf.to('cpu').numpy(), bbox_coords, num_detections, elapsed_time

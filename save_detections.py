#!/usr/bin/env python3
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

    def detect_objects(self):
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

        # Perform object detection using the YOLO model
        results = self.model.predict(
                             conf=self.conf_thresh,
                             half=False,
                             classes=self.classes,
                             device=0,
                             iou=self.iou_thresh,
                             imgsz=self.model_size,
                             source='/home/can/storage/videos/aire/toward_boat_front/_frontpi_oak_rgb_image_raw_compressed/*.jpg',
                             save=True,
                             save_conf= True)
        return results[0].plot()
    

weight_file = '/home/can/storage/weight_files/aire/custom/weights/v5l6.pt'
od = ObjectDetection(weight_file, 1280, 0.5, 0.3, [0,1])
# weight_file = '/home/can/Downloads/yolov5x6.pt'
# od = ObjectDetection(weight_file, 1280, 0.5, 0.3, [8])
od.detect_objects()
from inference import get_model
import supervision as sv
import cv2
import time

class DetectionModel:
    # Class-level constants
    MODEL_ID = "rivals-heads/2"
    API_KEY = "8LckOsnMlNQH2aUz4DZI"

    def __init__(self):
        """
        Initialize the DetectionModel with a pre-trained model.

        Args:
            model_id (str): The model ID to load.
            api_key (str): The API key for accessing the model.
        """
        self.model = self._load_model(self.MODEL_ID, self.API_KEY)

    def _load_model(self, model_id, api_key):
        """
        Load the model and measure the time taken.

        Args:
            model_id (str): The model ID to load.
            api_key (str): The API key for accessing the model.

        Returns:
            Model instance.
        """
        start_time = time.time()
        model = get_model(model_id=model_id, api_key=api_key)
        elapsed_time = time.time() - start_time
        print(f"Model loaded in {elapsed_time:.2f} seconds")
        return model

    def get_detection_coordinates(self, image):
        """
        Run inference on the input image and return the coordinates of the first detection.

        Args:
            image.

        Returns:
            dict: A dictionary containing the coordinates of the first detection.
        """

        # Run inference
        start_time = time.time()
        results = self.model.infer(image, confidence=0.01)[0]
        elapsed_time = time.time() - start_time
        print(f"Inference completed in {elapsed_time:.2f} seconds")

        # Process detections
        detections = sv.Detections.from_inference(results)

        # Extract the first detection
        if len(detections.xyxy) > 0:
            coordinates = sv.Detections(
                xyxy=detections.xyxy[:1],  # Bounding box of the first detection
                confidence=detections.confidence[:1],  # Confidence of the first detection
                class_id=detections.class_id[:1],  # Class ID of the first detection
                data={key: value[:1] for key, value in detections.data.items()}  # Slice data to keep only the first detection
            )
        else:
            coordinates = None

        return coordinates
    
    def get_position(self, image):
        coordinates = self.get_detection_coordinates(image)
        print("target found: ", coordinates)
        if coordinates is None:
            return None, None
        box = coordinates.xyxy[0]
        x_center = int((box[0] + box[2]) / 2)  # Center X
        y_center = int((box[1] + box[3]) / 2)
        return x_center, y_center
    

if __name__ == "__main__":
    # Initialize the DetectionModel
    model = DetectionModel()
    # image = cv2.imread("screenshots/screenshot_12281818-0027.png")
    image = cv2.imread("screenshots/Xnip2024-12-31_17-46-46.jpg")

    # # Load an image file into binary format
    # with open("screenshots/screenshot_12281818-0027.png", "rb") as f:
    #     image_binary = f.read()

    # Get detection coordinates
    detection = model.get_detection_coordinates(image)

    if detection:
        print(f"Detection: {detection}")
        # create supervision annotators
        bounding_box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()

        # Use `detection` for annotating the image
        annotated_image = bounding_box_annotator.annotate(
            scene=image, detections=detection)
        annotated_image = label_annotator.annotate(
            scene=annotated_image, detections=detection)
        
        # Draw circles at the center of bounding boxes
        for box in detection.xyxy:
            x_center = int((box[0] + box[2]) / 2)  # Center X
            y_center = int((box[1] + box[3]) / 2)  # Center Y
            cv2.circle(annotated_image, (x_center, y_center), radius=5, color=(0, 0, 255), thickness=-1)

        # display the image
        sv.plot_image(annotated_image)
    else:
        print("No detection found.")

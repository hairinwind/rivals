from inference import get_model
import supervision as sv
import cv2
import time

def measure_time(func, *args, **kwargs):
    """
    Measure the time taken to execute a function.
    
    Args:
        func: The function to execute.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.
    
    Returns:
        result: The result of the function call.
        elapsed_time: The time taken to execute the function.
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed_time = time.time() - start_time
    print(f"Time to execute {func.__name__}: {elapsed_time:.2f} seconds")
    return result

# define the image url to use for inference
image_file = "screenshots/screenshot_12281818-0027.png"
image = cv2.imread(image_file)

# load a pre-trained yolov8n model
# model = get_model(model_id="rivals-heads/2", api_key="8LckOsnMlNQH2aUz4DZI")
model = measure_time(get_model, model_id="rivals-heads/2", api_key="8LckOsnMlNQH2aUz4DZI")

# run inference on our chosen image, image can be a url, a numpy array, a PIL image, etc.
# results = model.infer(image, confidence=0.01)[0]
results = measure_time(model.infer, image, confidence=0.01)[0]

# load the results into the supervision Detections api
detections = sv.Detections.from_inference(results)
print(detections)
# Keep only the first detection
if len(detections.xyxy) > 0:
    first_detection = sv.Detections(
        xyxy=detections.xyxy[:1],  # Bounding box of the first detection
        confidence=detections.confidence[:1],  # Confidence of the first detection
        class_id=detections.class_id[:1],  # Class ID of the first detection
        data={key: value[:1] for key, value in detections.data.items()}  # Slice data to keep only the first detection
    )
else:
    first_detection = sv.Detections()  # Create an empty Detections object

# create supervision annotators
bounding_box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# Use `first_detection` for annotating the image
annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=first_detection)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=first_detection)

# display the image
sv.plot_image(annotated_image)
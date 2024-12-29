# from roboflow import Roboflow

# rf = Roboflow(api_key="8LckOsnMlNQH2aUz4DZI")
# project = rf.workspace().project("https://detect.roboflow.com/rivals-heads")
# model = project.version(2).model

# # infer on a local image
# # print(model.predict("your_image.jpg", confidence=40, overlap=30).json())

# # visualize your prediction
# model.predict("screenshots/screenshot_12281818-0027.png", confidence=0, overlap=30).save("prediction.jpg")

# # infer on an image hosted elsewhere
# # print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())

# import the inference-sdk
from inference_sdk import InferenceHTTPClient

# initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="8LckOsnMlNQH2aUz4DZI"
)

# infer on a local image
result = CLIENT.infer("screenshots/screenshot_12281818-0027.png", model_id="rivals-heads/2")
print(result)
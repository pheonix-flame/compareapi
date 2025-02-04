import requests
import base64

# Define the endpoint URL
url = "http://127.0.0.1:8000/compare_images/"

# Load and encode reference images and the new image
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Example image paths
reference_image_paths = ["img1.jpg", "img4.jpg"]
new_image_path = "img3.jpg"

# Encode reference images to base64
reference_images_base64 = [encode_image_to_base64(path) for path in reference_image_paths]

# Encode new image to base64
new_image_base64 = encode_image_to_base64(new_image_path)

# Prepare the JSON payload
payload = {
    "reference_images": reference_images_base64,
    "new_image": new_image_base64
}

# Send the request to the FastAPI endpoint
response = requests.post(url, json=payload)

# Print the server response
print("Response status code:", response.status_code)
print("Response body:", response.json())

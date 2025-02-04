from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from PIL import Image
import io
import numpy as np
import base64
from skimage.metrics import structural_similarity as ssim

app = FastAPI()

class ImageComparisonRequest(BaseModel):
    reference_images: List[str]  # Base64-encoded images
    new_image: str  # Base64-encoded new image

def decode_base64_to_image(base64_string: str) -> np.ndarray:
    """Decode Base64 image to numpy array."""
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        image = image.convert("RGB")
        return np.array(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Base64 image data: {str(e)}")

def compare_images(img1: np.ndarray, img2: np.ndarray) -> float:
    """Compare two images and return similarity percentage."""
    if img1.shape != img2.shape:
        raise HTTPException(status_code=400, detail="Images must have the same dimensions.")
    img1_gray = np.mean(img1, axis=2).astype("uint8")
    img2_gray = np.mean(img2, axis=2).astype("uint8")
    similarity, _ = ssim(img1_gray, img2_gray, full=True)
    return similarity * 100

@app.get("/")
def read_root():
    """Return a welcome message with instructions."""
    return {"message": "Welcome! Use the '/compare_images' endpoint for your image comparison API."}

@app.post("/compare_images/")
async def compare_images_api(request: ImageComparisonRequest):
    """Compare multiple reference images with a new image."""
    reference_images = [decode_base64_to_image(img) for img in request.reference_images]
    new_image = decode_base64_to_image(request.new_image)

    best_similarity = 0.0
    for ref_image in reference_images:
        similarity_score = compare_images(ref_image, new_image)
        best_similarity = max(best_similarity, similarity_score)

    status = "good" if best_similarity >= 50 else "bad"
    return {"status": status, "best_similarity_percentage": best_similarity}

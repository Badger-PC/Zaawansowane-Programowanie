import os
import requests
from PIL import Image, ImageDraw, ImageFont

# COCO Class names (index matches the model output)
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
    'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# Animals including 'bird' but excluding 'person'
ANIMAL_CLASSES = [
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'fox'
]

def download_image(url: str, save_path: str) -> str:
    """Downloads an image from a URL and saves it to the specified path."""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return save_path
    except Exception as e:
        print(f"Error downloading image: {e}")
        if os.path.exists(save_path):
            os.remove(save_path)
        raise

def draw_boxes(image_path: str, detections: list, output_path: str):
    """
    Draws bounding boxes and labels on the image.
    detections: list of dicts {'box': [x1, y1, x2, y2], 'label': str, 'score': float}
    """
    try:
        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        # Try to load a font, fallback to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        for det in detections:
            box = det['box']
            label = f"{det['label']} {det['score']:.2f}"
            draw.rectangle(xy=box, outline="red", width=3)
            
            # Draw text with background
            text_bbox = draw.textbbox((box[0], box[1]), label, font=font)
            draw.rectangle(text_bbox, fill="red")
            draw.text((box[0], box[1]), label, fill="white", font=font)

        image.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error drawing boxes: {e}")
        raise

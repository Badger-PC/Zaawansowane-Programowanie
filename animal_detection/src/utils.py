import os
import requests
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from urllib.parse import urljoin 

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book', 'clock', 'vase',
    'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

ANIMAL_CLASSES = [
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 
]


def download_image(url: str, save_path: str) -> str:
    """
    Downloads an image from a URL and saves it to the specified path.
    If the URL points to a web page, it attempts to find the main image.
    """
    try:
        # User agent to avoid some 403s
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        # First request to check content type
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '').lower()
        
        if 'text/html' in content_type:
            # It's a web page, attempt to find an image
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try og:image first
            img_tag = soup.find('meta', property='og:image')
            if img_tag and img_tag.get('content'):
                image_url = img_tag['content']
            else:
                # Try finding an img tag
                # This is a basic heuristic: get the largest image or first relevant one
                # For now, let's just take the first img that looks like a photo (jpg/png)
                images = soup.find_all('img')
                image_url = None
                for img in images:
                    src = img.get('src')
                    if src and any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                         image_url = src
                         break
                
                if not image_url and images:
                    # Fallback to just the first image
                    image_url = images[0].get('src')

            if not image_url:
                raise ValueError("No suitable image found on the page.")
                
            # Handle relative URLs
            image_url = urljoin(url, image_url)
            print(f"Found image on page: {image_url}")
            
            # Recursive call with the new image URL
            return download_image(image_url, save_path)
            
        else:
            # Assume it's an image or binary file, save it
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

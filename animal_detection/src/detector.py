import torch
import torchvision
from torchvision.transforms import functional as F
from PIL import Image
from .utils import COCO_INSTANCE_CATEGORY_NAMES, ANIMAL_CLASSES
import ssl

# Fix SSL issue on Mac
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

class AnimalDetector:
    def __init__(self, threshold=0.5):
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        # Load a pre-trained Faster R-CNN model
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights='DEFAULT')
        self.model.to(self.device)
        self.model.eval()
        self.threshold = threshold

    def detect(self, image_path: str):
        """
        Detects animals in an image.
        Returns:
            count (int): Number of detected animals
            detections (list): List of dicts with box, label, score
        """
        try:
            image = Image.open(image_path).convert("RGB")
            image_tensor = F.to_tensor(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                prediction = self.model(image_tensor)[0]

            detections = []
            count = 0

            for i, score in enumerate(prediction['scores']):
                if score > self.threshold:
                    label_idx = prediction['labels'][i].item()
                    label_name = COCO_INSTANCE_CATEGORY_NAMES[label_idx]
                    
                    if label_name in ANIMAL_CLASSES:
                        count += 1
                        box = prediction['boxes'][i].cpu().numpy().tolist()
                        detections.append({
                            'box': box,
                            'label': label_name,
                            'score': score.item()
                        })
            
            return count, detections
        except Exception as e:
            print(f"Error in detection: {e}")
            raise

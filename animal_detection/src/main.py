from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Query, Path
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import uuid
import os
import json
import shutil
import asyncio
import cv2
from typing import Optional

# Import local modules
from .detector import AnimalDetector
from .utils import download_image, draw_boxes

app = FastAPI(
    title="Animal Detection API",
    description="""
    ## Welcome to the Animal Detection API! 🐾

    This API allows you to detect animals (cats, dogs, birds, etc.) in images using AI.
    
    You can try the following:
    1. **Local Detection**: Detect animals in files you place in the `input_images` folder.
    2. **Webcam Detection**: Capture a photo from your webcam and check for animals.
    3. **Async URL**: Queue an image from the internet for processing.
    4. **Async Upload**: Upload your own image file for processing.
    """,
    version="1.0.0"
)

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
IMAGES_DIR = os.path.join(STORAGE_DIR, "images")
PROCESSED_DIR = os.path.join(STORAGE_DIR, "processed")
RESULTS_DIR = os.path.join(STORAGE_DIR, "results")
INPUT_IMAGES_DIR = os.path.join(BASE_DIR, "input_images")

# Ensure directories exist
for d in [IMAGES_DIR, PROCESSED_DIR, RESULTS_DIR, INPUT_IMAGES_DIR]:
    os.makedirs(d, exist_ok=True)

# Global variables
detector = None
task_queue = asyncio.Queue()

@app.on_event("startup")
async def startup_event():
    global detector
    detector = AnimalDetector()
    asyncio.create_task(worker())

async def worker():
    while True:
        task = await task_queue.get()
        await process_task(task)
        task_queue.task_done()

async def process_task(data):
    task_id = data.get("task_id")
    
    try:
        image_path = data.get("image_path")
        if not image_path:
             # Download if URL
            image_url = data.get("image_url")
            if image_url:
                filename = f"{task_id}.jpg"
                image_path = os.path.join(IMAGES_DIR, filename)
                download_image(image_url, image_path)
            else:
                raise ValueError("No image source")

        # Detect
        loop = asyncio.get_event_loop()
        count, detections = await loop.run_in_executor(None, detector.detect, image_path)
        
        # Draw boxes
        output_filename = f"{task_id}_processed.jpg"
        output_path = os.path.join(PROCESSED_DIR, output_filename)
        draw_boxes(image_path, detections, output_path)

        result = {
            "task_id": task_id,
            "status": "completed",
            "count": count,
            "detections": detections,
            "processed_image_path": output_path
        }
    except Exception as e:
        print(f"Error task {task_id}: {e}")
        result = {
            "task_id": task_id,
            "status": "failed",
            "error": str(e)
        }
    
    # Save result
    with open(os.path.join(RESULTS_DIR, f"{task_id}.json"), 'w') as f:
        json.dump(result, f)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Animal Detection</title>
            <style>
                body { font-family: sans-serif; max-width: 800px; margin: 40px auto; line-height: 1.6; }
                code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
                .btn { display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin-top: 10px;}
                .btn:hover { background: #0056b3; }
            </style>
        </head>
        <body>
            <h1>Animal Detection API</h1>
            <p>Welcome! This service can count animals in your images.</p>
            
            <h2>How to use:</h2>
            <ol>
                <li><strong>Swagger UI:</strong> Go to <a href="/docs">/docs</a> to try out the endpoints interactively.</li>
                <li><strong>Local Files:</strong> Place images in the <code>input_images</code> folder and use <code>/detect-local</code>.</li>
                <li><strong>Webcam:</strong> Use <code>/detect-webcam</code> to snap a photo now.</li>
            </ol>
            
            <a href="/docs" class="btn">Open API Documentation</a>
        </body>
    </html>
    """
@app.get("/get-local", summary="Get Local Files", description="Get a list of files in the `input_images` directory.")
def get_local():
    files = os.listdir(INPUT_IMAGES_DIR)
    return {"files": files}

@app.get("/detect-local", summary="Detect from Local File", description="Process an image file located in the `input_images` directory.")
def detect_local(
    filename: str = Query(..., description="Name of the file in `input_images` folder", example="cat.jpg")
):
    """
    **Instructions:**
    1. Put a file (e.g. `cat.jpg`) inside `animal_detection/input_images/`.
    2. Enter the filename here.
    3. The system will detect animals and save the result in `storage/processed/`.
    """
    path = os.path.join(INPUT_IMAGES_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found in {INPUT_IMAGES_DIR}. Please place the file there correctly.")
    
    try:
        count, detections = detector.detect(path)
        
        # Save processed version
        output_path = os.path.join(PROCESSED_DIR, f"local_{filename}")
        draw_boxes(path, detections, output_path)

        return {
            "file": filename,
            "animal_count": count,
            "message": f"Found {count} animals. Check output image.",
            "detections": detections,
            "processed_image_location": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect-url-async", summary="Detect from URL (Async using Queue)")
async def detect_url_async(
    url: str = Query(..., description="URL of the image to analyze", example="https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_March_2010-1.jpg")
):
    """
    **Instructions:**
    1. Provide a direct link to an image (ending in .jpg or .png).
    2. We will download it and process it in the background.
    3. Use the returned `task_id` to check the status at `/task/{task_id}`.
    """
    task_id = str(uuid.uuid4())
    await task_queue.put({
        "task_id": task_id,
        "image_url": url
    })
    return {"task_id": task_id, "status": "queued", "message": "Task queued. Use GET /task/{task_id} to check results."}

@app.post("/detect-upload-async", summary="Upload Image (Async using Queue)")
async def detect_upload_async(file: UploadFile = File(..., description="Select an image file to upload")):
    """
    **Instructions:**
    1. Click 'Try it out'.
    2. Select an image file from your computer.
    3. Click 'Execute'.
    4. Use the returned `task_id` to check status.
    """
    task_id = str(uuid.uuid4())
    file_path = os.path.join(IMAGES_DIR, f"{task_id}.jpg")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    await task_queue.put({
        "task_id": task_id,
        "image_path": file_path
    })
    return {"task_id": task_id, "status": "queued", "message": "Task queued. Use GET /task/{task_id} to check results."}

@app.get("/task/{task_id}", summary="Check Task Status")
def get_task_status(task_id: str = Path(..., description="The Task ID you received from an async endpoint")):
    result_path = os.path.join(RESULTS_DIR, f"{task_id}.json")
    if os.path.exists(result_path):
        with open(result_path, 'r') as f:
            return json.load(f)
    return {"task_id": task_id, "status": "processing", "message": "Still working... try again in a second."}

@app.post("/detect-webcam", summary="Detect from Webcam")
def detect_webcam():
    """
    **Instructions:**
    1. Triggers the server's webcam to take 1 photo.
    2. Detects animals in that photo.
    3. Returns the count and saves the image.
    """
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise HTTPException(status_code=500, detail="Could not open webcam. Is it connected?")
        
        # Warmup
        for _ in range(5):
            cap.read()

        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise HTTPException(status_code=500, detail="Could not read frame from webcam.")
        
        filename = f"webcam_{uuid.uuid4()}.jpg"
        filepath = os.path.join(IMAGES_DIR, filename)
        cv2.imwrite(filepath, frame)
        
        count, detections = detector.detect(filepath)
        output_path = os.path.join(PROCESSED_DIR, filename)
        draw_boxes(filepath, detections, output_path)
        
        return {
            "source": "webcam",
            "animal_count": count,
            "detections": detections,
            "processed_image_location": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

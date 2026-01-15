from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Query, Path
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import uuid
import os
import json
import shutil
import asyncio
import cv2

# Import local modules
from .detector import AnimalDetector
from .utils import download_image, draw_boxes

app = FastAPI(
    title="Animal Detection API",
    description="""
    ## Welcome to the Animal Detection API!

    This API allows you to detect animals (cats, dogs, birds, bears) in images using AI.
    Animal classes available: 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe'
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
             raise ValueError("No image path provided for task")

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
from enum import Enum

# Dynamic Enum for Swagger UI
def get_image_files():
    try:
        files = sorted([f for f in os.listdir(INPUT_IMAGES_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])
    except Exception:
        files = []
    if not files:
        return {"NO_FILES": "no_files_found"}
    return {f: f for f in files}

# Create the Enum dynamically
# We need to recreate this if files change, but for now it's static on load/reload.
image_files_dict = get_image_files()
ImageEnum = Enum("ImageEnum", image_files_dict)

@app.get("/get-local", summary="Get Local Files", description="Get a list of files in the `input_images` directory.")
def get_local():
    files = os.listdir(INPUT_IMAGES_DIR)
    return {"files": files}

@app.get("/detect-local", summary="Detect from Local File", description="Process an image file located in the `input_images` directory.")
def detect_local(
    filename: ImageEnum = Query(..., description="Select a file from `input_images` folder")
):
    """
    **Instructions:**
    1. Select a file from the dropdown list.
    2. The system will detect animals and save the result in `storage/processed/`.
    """
    # filename will be the Enum member. We need the value (the actual filename)
    # FastAPI usually converts it, but let's be safe.
    actual_filename = filename.value
    
    path = os.path.join(INPUT_IMAGES_DIR, actual_filename)
    if not os.path.exists(path):
        # This might happen if file was deleted after server start
        raise HTTPException(status_code=404, detail=f"File '{actual_filename}' not found in {INPUT_IMAGES_DIR}.")
    
    try:
        count, detections = detector.detect(path)
        
        # Save processed version
        output_path = os.path.join(PROCESSED_DIR, f"local_{actual_filename}")
        draw_boxes(path, detections, output_path)

        return {
            "file": actual_filename,
            "animal_count": count,
            "message": f"Found {count} animals. Check output image.",
            "detections": detections,
            "processed_image_location": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect-url", summary="Detect from URL ")
async def detect_url(
    url: str = Query(..., description="URL of the image to analyze", example="https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_March_2010-1.jpg")
):
    """
    **Instructions:**
    1. Provide a direct link to an image (ending in .jpg or .png).
    2. We will download it and process it in the background.
    3. Use the returned `task_id` to check the status at `/task/{task_id}`.
    """
    task_id = str(uuid.uuid4())
    filename = f"{task_id}.jpg"
    image_path = os.path.join(IMAGES_DIR, filename)

    try:
        # Download image first (running in executor to avoid blocking main loop)
        loop = asyncio.get_event_loop()
        # Create a partial to pass arguments if needed, or just pass directly
        await loop.run_in_executor(None, download_image, url, image_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to download image: {str(e)}")

    await task_queue.put({
        "task_id": task_id,
        "image_path": image_path
    })
    return {"task_id": task_id, "status": "queued", "message": "Task queued. Use GET /task/{task_id} to check results."}

@app.post("/detect-upload", summary="Upload Image")
async def detect_upload(file: UploadFile = File(..., description="Select an image file to upload")):
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

# Dynamic Enum for Task IDs
def get_task_ids():
    try:
        # List json files in RESULTS_DIR
        files = sorted([f for f in os.listdir(RESULTS_DIR) if f.endswith('.json')])
        # Remove extension
        ids = [f.replace('.json', '') for f in files]
    except Exception:
        ids = []
    
    if not ids:
        return {"NO_TASKS": "no_tasks_found"}
    return {i: i for i in ids}

# Create TaskEnum
task_ids_dict = get_task_ids()
TaskEnum = Enum("TaskEnum", task_ids_dict)

@app.get("/task/{task_id}", summary="Check Task Status")
def get_task_status(task_id: TaskEnum = Path(..., description="The Task ID you received from an async endpoint")):
    # Extract value from Enum
    actual_task_id = task_id.value
    
    result_path = os.path.join(RESULTS_DIR, f"{actual_task_id}.json")
    if os.path.exists(result_path):
        with open(result_path, 'r') as f:
            return json.load(f)
    return {"task_id": actual_task_id, "status": "processing", "message": "Still working... try again in a second."}

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

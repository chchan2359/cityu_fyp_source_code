# Author        : CHAN Cheuk Hei
# Student Name  : CHAN Cheuk Hei
# Student ID    : 57270778
# Usage         : Main   - API Hosting (YOLO Model Object Detection) | Port 5010

import cv2
import base64
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize YOLO Models
model_plant_detect = YOLO("./yolo_model/plant_detect_9c_40e.pt", task="detect")
model_plant_diseases_twoknid = YOLO("./yolo_model/plant_disease_1c_60e.pt", task="detect")
model_plant_diseases_v1 = YOLO("./yolo_model/plant_disease_4c_50e.pt", task="detect")
model_plant_diseases_v2 = YOLO("./yolo_model/plant_diseases_v2_6c_50e.pt", task="detect")
model_plant_diseases_v2_large = YOLO("./yolo_model/plant_diseases_v2_6c_55e_L.pt", task="detect")
model_plant_diseases_v3 = YOLO("./yolo_model/plant_diseases_v3_7c_70e_L.pt", task="detect")

class_labels_plant_detect = model_plant_detect.names
class_labels_plant_diseases_twoknid = model_plant_diseases_twoknid.names
class_labels_plant_diseases_v1 = model_plant_diseases_v1.names
class_labels_plant_diseases_v2 = model_plant_diseases_v2.names
class_labels_plant_diseases_v2_large = model_plant_diseases_v2_large.names
class_labels_plant_diseases_v3 = model_plant_diseases_v3.names

CONFIDENCE_THRESHOLD = 0.35

# Bounding box colors (same as original script)
bbox_colors = [
    (164, 120, 87), (68, 148, 228), (93, 97, 209), (178, 182, 133),(88, 159, 106), 
    (96, 202, 231), (159, 124, 168), (169, 162, 241),(98, 118, 150), (172, 176, 184)
]

def detect_objects(image, model_name, threshold=CONFIDENCE_THRESHOLD):
    # Model Selection
    if model_name == "plant_detect":
        model = model_plant_detect
        class_labels = class_labels_plant_detect
    elif model_name == "plant_diseases_twokind":
        model = model_plant_diseases_twoknid
        class_labels = class_labels_plant_diseases_twoknid
    elif model_name == "plant_diseases_v1":
        model = model_plant_diseases_v1
        class_labels = class_labels_plant_diseases_v1
    elif model_name == "plant_diseases_v2":
        model = model_plant_diseases_v2
        class_labels = class_labels_plant_diseases_v2
    elif model_name == "plant_diseases_v2_large":
        model = model_plant_diseases_v2_large
        class_labels = class_labels_plant_diseases_v2_large
    elif model_name == "plant_diseases_v3":
        model = model_plant_diseases_v3
        class_labels = class_labels_plant_diseases_v3
    else:
        raise ValueError(f"Invalid model_type: {model_name}.")
    
    # Object Detection
    results = model(image, verbose=False)
    detections = results[0].boxes
    detected_objects = []
    detected_objects_class_only = []

    for detection in detections:
        x1, y1, x2, y2 = detection.xyxy.cpu().numpy().squeeze().astype(int)
        class_id = int(detection.cls.item())
        confidence = detection.conf.item()

        if confidence < threshold:
            continue

        class_name = class_labels[class_id]
        detected_objects.append({
            "class_name": class_name,
            "confidence": float(confidence),
            "bbox": [int(x1), int(y1), int(x2), int(y2)]
        })
        
        # Detection Boxes
        color = bbox_colors[class_id % 10]
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        # Detection Labels
        label = f"{class_name}: {confidence:.2f}"
        (label_width, label_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        y_label = max(y1, label_height + 10)

        # Rendering
        cv2.rectangle(image, (x1, y_label - label_height - 10), (x1 + label_width, y_label + baseline - 10), color, cv2.FILLED)
        cv2.putText(image, label, (x1, y_label - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    return image, detected_objects

@app.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    
    # File Type Validation
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
        return jsonify({"error": "Invalid file type. Only JPG, JPEG, PNG, and GIF are supported."}), 400

    # OpenCV Image Convertion
    try:
        image_data = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Failed to decode image.")
    except Exception as e:
        return jsonify({"error": f"Error reading image: {str(e)}"}), 400

    # Thresh Setting, Default Value : 0.35
    threshold = float(request.form.get("thresh", CONFIDENCE_THRESHOLD))

    # Model Selection, Default Model : Plant Detection
    model_type = request.form.get("model_type", "plant_diseases_v3")
    

    # Object Detection - YOLO Models
    try:
        _, plant_detect_detected_objects = detect_objects(image, "plant_detect", CONFIDENCE_THRESHOLD) # Plant Detect
        plant_result_image, detected_diseases_objects = detect_objects(image, model_type, threshold) # Plant Diseases
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Result Image Base64 Convertion
    _, buffer = cv2.imencode(".jpg", plant_result_image)
    result_image_base64 = base64.b64encode(buffer).decode("utf-8")
    
    # Return Message
    response = {
        "plant_result_image": f"data:image/jpeg;base64,{result_image_base64}",
        "plant_detect_detections": plant_detect_detected_objects,
        "plant_diseases_detections": detected_diseases_objects,
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)
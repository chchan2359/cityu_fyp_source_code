// Author        : CHAN Cheuk Hei
// Student Name  : CHAN Cheuk Hei
// Student ID    : 57270778
// Usage         : Main - React.js Component [FileUpload.jsx - Object Detection]

import { useState, useEffect } from "react";
import Card from "./Card";

function FileUpload() {
    const [file, setFile] = useState(null);
    const [previewImage, setPreviewImage] = useState(null);
    const [resultImage, setResultImage] = useState(null);
    const [plantDetections, setPlantDetections] = useState([]);
    const [diseasesDetections, setDiseasesDetections] = useState([]);
    const [error, setError] = useState("");
    const [modelType, setModelType] = useState("plant_diseases_v3");

    // Handle file input change
    function handleChange(e) {
        console.log(e.target.files);
        setFile(e.target.files[0]);
        setPreviewImage(URL.createObjectURL(e.target.files[0]));
        setResultImage(null);
        setPlantDetections([]);
        setDiseasesDetections([]);
        setError("");
    }

    // Handle model selection change
    function handleModelChange(e) {
        setModelType(e.target.value);
    }

    // Handle form submission to detect objects
    function handleSubmit() {
        if (!file) {
            setError("Please select an image file.");
            return;
        }
        setResultImage(null)

        const formData = new FormData();
        formData.append("image", file);
        formData.append("thresh", "0.35");
        formData.append("model_type", modelType);

        fetch("http://localhost:5010/detect", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            setResultImage(data.plant_result_image);
            setPlantDetections(data.plant_detect_detections);
            setDiseasesDetections(data.plant_diseases_detections);
            setError("");
        })
        .catch(err => {
            setError(`Error: ${err.message}`);
            setResultImage(null);
            setPlantDetections([]);
            setDiseasesDetections([]);
        });
    }

    // Clean up memory by revoking object URL
    useEffect(() => {
        return () => {
            if (previewImage) {
                URL.revokeObjectURL(previewImage);
            }
        };
    }, [previewImage]);

    return (
        <Card title="Houseplant Type & Problems Detector [YOLO Model Object Detection]">
            <div id="box-container">
                <div>
                    {file && (
                        <div id="display-inline-block" className="imagebox">
                            <img src={previewImage} alt="preview" />
                        </div>
                    )}
                    <div id="display-inline-block">
                        <input type="file" accept="image/*" onChange={handleChange} />
                    </div>
                    <div id="display-inline-block">
                        <select value={modelType} onChange={handleModelChange}>
                            <option value="plant_diseases_v3">Plant Diseases - V3</option>
                            <option value="plant_diseases_twokind">Plant Diseases - Two Kinds</option>
                            <option value="plant_diseases_v1">Plant Diseases - V1</option>
                            <option value="plant_diseases_v2">Plant Diseases - V2</option>
                            <option value="plant_diseases_v2_large">Plant Diseases - V2 Large</option>
                        </select>
                    </div>
                    <div id="display-inline-block">
                        <button onClick={handleSubmit}>Detect Objects</button>
                    </div>
                </div>
                {resultImage && (
                    <div>
                        <div id="display-inline-block" className="imagebox">
                            <img src={resultImage} alt="YOLO Detected" />
                        </div>
                        {(plantDetections.length > 0 || diseasesDetections.length > 0) && (
                            <div>
                                <h3>Plant Detections:</h3>
                                <ul>
                                    {plantDetections.map((det, index) => (
                                        <li key={index}>
                                            {det.class_name}: {det.confidence.toFixed(2)} (BBox: {det.bbox.join(", ")})
                                        </li>
                                    ))}
                                    {plantDetections.length === 0 && <p>No Plant Detection</p>}
                                </ul>
                                <hr />

                                <h3>Diseases Detections:</h3>
                                <ul>
                                    {diseasesDetections.map((det, index) => (
                                        <li key={index}>
                                            {det.class_name}: {det.confidence.toFixed(2)} (BBox: {det.bbox.join(", ")})
                                        </li>
                                    ))}
                                    {diseasesDetections.length === 0 && <p>No Diseases Detection</p>}
                                </ul>
                            </div>
                        )}
                    </div>
                )}
                {error && <p style={{ color: "red" }}>{error}</p>}
            </div>
        </Card>
    );
}

export default FileUpload;
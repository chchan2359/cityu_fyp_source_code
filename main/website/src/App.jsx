// Author        : CHAN Cheuk Hei
// Student Name  : CHAN Cheuk Hei
// Student ID    : 57270778
// Usage         : Main - React.js Component [App.jsx]

import RAG from "./RAG"
import FileUpload from "./FileUpload"
import InfoRAG from "./InfoRAG"
import InfoObjectDection from "./InfoObjectDection";
import Card from "./Card";
import { useState } from "react";

function App() {
    const [infoObjectDetection, setInfoObjectDetection] = useState(false)
    const [infoRAG, setInfoRAG] = useState(false)

    const toggleInfoOD = () => {
        setInfoObjectDetection(!infoObjectDetection);
    }

    const toggleInfoRAG = () => {
        setInfoRAG(!infoRAG);
    }

    return(
        <>
            <FileUpload />
            <RAG />
            <Card title="Tools Information">
                <button onClick={toggleInfoOD}>Houseplant Type & Problems Detector</button>
                <button onClick={toggleInfoRAG}>Housepalnt AI Agent</button>
            </Card>
            {infoObjectDetection &&
            <InfoObjectDection />
            }
            {infoRAG &&
            <InfoRAG />
            }
        </>
    )
}

export default App
// Author        : CHAN Cheuk Hei
// Student Name  : CHAN Cheuk Hei
// Student ID    : 57270778
// Usage         : Main - React.js Component [RAG.jsx - Recommendation System]

import { useState } from "react";
import Card from "./Card";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function RAG() {
    const [question, setQuestion] = useState("");
    const [modifiedQuestion, setModifiedQuestion] = useState(""); // Modified Question
    const [retrievedDocs, setRetrievedDocs] = useState([]); // Retrieved Documents
    const [ollamaReply, setOllamaReply] = useState(""); // LLM Reply
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = () => {
        if (!question.trim()) {
            alert("Please enter a question!");
            return;
        }

        setIsLoading(true);
        setModifiedQuestion("");
        setRetrievedDocs([]);
        setOllamaReply("");

        fetch("http://localhost:5000/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            function readStream() {
                reader.read().then(({ done, value }) => {
                    if (done) {
                        setIsLoading(false);
                        return;
                    }

                    const chunk = decoder.decode(value, { stream: true });
                    const lines = chunk.split("\n");

                    lines.forEach(line => {
                        if (line.startsWith("data: ")) {
                            const jsonData = line.replace("data: ", "");
                            try {
                                const data = JSON.parse(jsonData);
                                if (data.modified_question) {
                                    setModifiedQuestion(data.modified_question);
                                }
                                if (data.retrieved_docs) {
                                    setRetrievedDocs(data.retrieved_docs);
                                }
                                if (data.ollama_answer) {
                                    setOllamaReply(data.ollama_answer);
                                }
                            } catch (e) {
                                console.error("Error parsing JSON:", e);
                            }
                        }
                    });

                    readStream();
                }).catch(error => {
                    console.error("Stream error:", error);
                    setOllamaReply("Error: Could not read stream.");
                    setIsLoading(false);
                });
            }
            readStream();
        })
        .catch(error => {
            console.error("Error:", error);
            setOllamaReply("Error: Could not connect to the server.");
            setIsLoading(false);
        });
    };

    return (
        <div>
            <Card title="Houseplant AI Agent">
                <textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Enter your question here..."
                    disabled={isLoading}
                />
                <div>
                    <button onClick={handleSubmit} disabled={isLoading}>
                        {isLoading ? "Loading..." : "Submit"}
                    </button>
                </div>
            </Card>
            
            {(modifiedQuestion || retrievedDocs.length > 0 || ollamaReply) && (
                <Card title="Query Result">
                    {modifiedQuestion && (
                        <p><strong>Modified Question:</strong> {modifiedQuestion}</p>
                    )}
                    {retrievedDocs.length > 0 && (
                        <>
                            <p><strong>Retrieved Documents:</strong></p>
                            <ul>
                                {retrievedDocs.map((doc, index) => (
                                    <li key={index}>{doc}</li>
                                ))}
                            </ul>
                        </>
                    )}
                    {retrievedDocs.length > 0  && (
                        <>
                            <p><strong>Answer:</strong></p>
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {ollamaReply || "Please wait..."}
                            </ReactMarkdown>
                        </>
                    )}
                </Card>
            )}
        </div>
    );
}

export default RAG;
import "./App.css";

import { useState, useRef } from "react";
import axios from "axios";

function App() {

    const [question, setQuestion] = useState("");

    const [answer, setAnswer] = useState("");

    const [sources, setSources] = useState([]);

    const [loading, setLoading] = useState(false);

    const [uploading, setUploading] = useState(false);

    const [file, setFile] = useState(null);

    const fileInputRef = useRef(null);

    async function askQuestion() {

        if (question.trim() === "") return;

        setLoading(true);

        setAnswer("");
        setSources([]);

        try {

            const response = await axios.post(
                "http://127.0.0.1:8000/query",
                {
                    question: question
                }
            );

            setAnswer(response.data.answer);
            setSources(response.data.sources);

        }
        catch (error) {

            console.log(error);

            setAnswer("Failed to generate answer. Please try again.");

            setSources([]);

        }
        finally {

            setLoading(false);

        }

    }

    async function uploadPdf() {

        if (!file) return;

        setUploading(true);

        try {

            const formData = new FormData();

            formData.append("file", file);

            await axios.post(
                "http://127.0.0.1:8000/upload",
                formData
            );

            alert("PDF Uploaded Successfully");

            setFile(null);

            fileInputRef.current.value = "";

        }
        catch (error) {

            console.log(error);

            alert("Upload failed.");

        }
        finally {

            setUploading(false);

        }

    }

    return (

        <div className="container">

            <h1>Research Assistant</h1>

            <p className="subtitle">
                Upload PDFs.. and ask questions using Retrieval-Augmented Generation..
            </p>

            <div className="search-box">

                <input
                    type="text"
                    value={question}
                    placeholder="Ask anything..."
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            askQuestion();
                        }
                    }}
                />

                <button
                    onClick={askQuestion}
                    disabled={loading}
                >
                    {loading ? "Thinking..." : "Ask"}
                </button>

            </div>

            {
                loading &&
                <div className="loading">
                    Generating answer...
                </div>
            }

            {
                answer &&
                <div className="answer">

                    <h2>Answer</h2>

                    <p>{answer}</p>

                    <div className="sources">

                        <h3>Sources</h3>

                        {
                            sources.map((source, index) =>

                                <div
                                    key={index}
                                    className="source"
                                >
                                    {source.paper_name} | Chunk {source.chunk_id}
                                </div>

                            )
                        }

                    </div>

                </div>
            }

            <div className="upload">

                <h2>Upload PDF</h2>

                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setFile(e.target.files[0])}
                />

                {
                    file &&
                    <p>
                        {file.name}
                    </p>
                }

                <br />
                <br />

                <button
                    onClick={uploadPdf}
                    disabled={uploading}
                >
                    {uploading ? "Uploading..." : "Upload"}
                </button>

            </div>

        </div>

    );

}

export default App;
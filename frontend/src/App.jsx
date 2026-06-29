import "./App.css";

import { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function App() {

    const [question, setQuestion] = useState("");

    const [messages, setMessages] = useState([]);

    const [papers, setPapers] = useState([]);

    const [selectedPapers,setSelectedPapers]=useState([]);

    const [loading, setLoading] = useState(false);

    const [uploading, setUploading] = useState(false);

    const [file, setFile] = useState(null);

    const fileInputRef = useRef(null);

    const messageRefs = useRef([]);

    const bottomRef = useRef(null);

    async function askQuestion() {

        if (loading || question.trim() === "") return;

        setLoading(true);

        const userQuestion = question;

        setQuestion("");

        setMessages((prev) => [

            ...prev,

            {
                role: "user",
                text: userQuestion
            },

            {
                role: "assistant",
                text: "",
                sources: []
            }

        ]);

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/query/stream",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        question: userQuestion,
                        papers: selectedPapers
                    })
                }
            );

            const reader = response.body.getReader();

            const decoder = new TextDecoder();

            let answer = "";

            let buffer = "";

            let sources = [];

            while (true) {

                const { done, value } = await reader.read();

                if (done) break;

                buffer += decoder.decode(value);

                const lines = buffer.split("\n");

                buffer = lines.pop();

                for (const line of lines) {

                    if (line.trim() === "") continue;

                    const event = JSON.parse(line);

                    if (event.type === "token") {

                        answer += event.content;

                    }

                    else if (event.type === "sources") {

                        sources = event.content;

                    }

                    setMessages((prev) => {

                        const updated = [...prev];

                        updated[updated.length - 1] = {

                            ...updated[updated.length - 1],

                            text: answer,

                            sources: sources

                        };

                        return updated;

                    });

                }

            }

            if (buffer.trim() !== "") {

                const event = JSON.parse(buffer);

                if (event.type === "sources") {

                    setMessages((prev) => {

                        const updated = [...prev];

                        updated[updated.length - 1] = {

                            ...updated[updated.length - 1],

                            sources: event.content

                        };

                        return updated;

                    });

                }

            }

        }
        catch (error) {

            console.log(error);

            setMessages((prev) => {

                const updated = [...prev];

                updated[updated.length - 1] = {

                    role: "assistant",

                    text: "Failed to generate answer.",

                    sources: []

                };

                return updated;

            });

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

            loadPapers();

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

    async function loadPapers(){

        try{

            const response = await axios.get(
                "http://127.0.0.1:8000/papers"
            );
            setPapers(response.data);
            setSelectedPapers(response.data);
        }
        catch(error){
            console.log(error);
        }

    }

    useEffect(()=>{

        loadPapers();

    },[]);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth"
        });

    }, [messages]);

    function togglePaper(paper){

        if(selectedPapers.includes(paper)){

            setSelectedPapers(

                selectedPapers.filter(
                    p=>p!==paper
                )

            );

        }

        else{

            setSelectedPapers(

                [...selectedPapers,paper]

            );

        }

    }


    return (

        <div className="app">
            <aside className="sidebar">

                <h2>Research RAG</h2>

                <div className="upload">

                    <h3>Upload PDF</h3>

                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf"
                        onChange={(e)=>setFile(e.target.files[0])}
                    />

                    {
                        file &&
                        <p>{file.name}</p>
                    }

                    <button
                        onClick={uploadPdf}
                        disabled={uploading}
                    >
                        {
                            uploading
                            ? "Uploading..."
                            : "Upload"
                        }
                    </button>

                </div>

                <div className="papers">

                    <h3>Uploaded Papers</h3>

                    {
                        papers.length===0 ?

                        <p>No papers uploaded</p>

                        :

                        papers.map((paper,index)=>

                            <label
                                key={index}
                                className="paper"
                            >

                                <input

                                    type="checkbox"

                                    checked={selectedPapers.includes(paper)}

                                    onChange={()=>togglePaper(paper)}

                                />

                                {paper}

                            </label>

                        )
                    }

                </div>

                <h3>Chat History</h3>

                <div className="history">

                {
                    messages.map((message,index)=>

                        message.role==="user" &&

                        <div

                            key={index}

                            className="history-item"

                            onClick={()=>

                                messageRefs.current[index]?.scrollIntoView({

                                    behavior:"smooth",

                                    block:"start"

                                })

                            }

                        >

                            {message.text.length>30

                                ? message.text.substring(0,30)+"..."

                                : message.text}

                        </div>

                    )
                }

                </div>

            </aside>

            <main className="main">

                <h1>Research Assistant</h1>

                <p className="subtitle">
                    Upload PDFs.. and ask questions using Retrieval-Augmented Generation..
                </p>


                {
                    loading &&
                    <div className="loading">
                        Generating answer...
                    </div>
                }

                <div className="chat">

                    {
                        messages.map((message, index) => (

                            <div
                                ref={(el)=>messageRefs.current[index]=el}
                                key={index}
                                className={
                                    message.role === "user"
                                    ? "user-message"
                                    : "assistant-message"
                                }
                            >

                                <strong>
                                    {message.role === "user"
                                        ? "You"
                                        : "Assistant"}
                                </strong>

                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm]}
                                >
                                    {message.text}
                                </ReactMarkdown>

                                {
                                    message.sources &&
                                    message.sources.length > 0 &&

                                    <div className="sources">

                                        <h4>Sources</h4>

                                        {
                                            message.sources.map((source, i) => (

                                                <div
                                                    key={i}
                                                    className="source"
                                                >
                                                    {source.paper_name} | Chunk {source.chunk_id}
                                                </div>

                                            ))
                                        }

                                    </div>
                                }

                            </div>

                        ))
                    }
                    <div ref={bottomRef}></div>

                </div>

                <div className="search-box">

                    <input
                        type="text"
                        value={question}
                        placeholder="Ask anything..."
                        onChange={(e) => setQuestion(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" && !loading) {
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

            </main>

        </div>

    );

}

export default App;
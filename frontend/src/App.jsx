import React, { useState } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) {
      setResponse("Error: Query cannot be empty.");
      return;
    }

    try {
      const res = await axios.post("http://localhost:5000/chat", {
        message: input,
      });

      setQuery(res.data.query || "Query not available");
      setResponse(res.data.response);
    } catch (error) {
      setResponse("Error connecting to backend.");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Neo4j Cypher Chatbot</h1>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask something..."
        onKeyDown={handleKeyDown}
        style={{ padding: "10px", width: "300px" }}
      />
      <button onClick={sendMessage} style={{ marginLeft: "10px", padding: "10px" }}>
        Send
      </button>

      <div style={{ textAlign: "left", marginTop: "20px", padding: "10px", backgroundColor: "#f5f5f5", borderRadius: "5px" }}>
        <h3>Generated Cypher Query:</h3>
        <pre>{query}</pre>
      </div>

      <div style={{ textAlign: "left", marginTop: "20px", padding: "10px", backgroundColor: "#e8f0fe", borderRadius: "5px" }}>
        <h3>Response:</h3>
        <pre>{typeof response === "object" ? JSON.stringify(response, null, 2) : response}</pre>
      </div>
    </div>
  );
}

export default App;

import React, { useState, useEffect, useRef } from "react";
import { query } from "../api";
import toast from "react-hot-toast";
import MessageBubble from "../components/MessageBubble";

const getFormattedTimestamp = () => {
  const now = new Date();
  return now.toISOString();
};

const Chat = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const timestamp = getFormattedTimestamp();
    setMessages((prev) => [
      ...prev,
      { sender: "user", text: trimmed, timestamp },
    ]);
    setInput("");
    setLoading(true);

    try {
      const response = await query(trimmed);
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: response?.answer || "No response.",
          timestamp: getFormattedTimestamp(),
        },
      ]);
    } catch (err) {
      console.error(err);
      toast.error("Error fetching response");
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Error fetching response",
          timestamp: getFormattedTimestamp(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const chatStyle = {
    marginTop: "16px",
    padding: "16px",
    borderRadius: "8px",
    backgroundColor: "#1e1e1e", // Replace with your actual background color
  };

  const messagesStyle = {
    marginBottom: "16px",
  };

  const inputStyle = {
    display: "flex",
    gap: "8px",
    marginTop: "8px",
  };

  const inputFieldStyle = {
    flex: 1,
    padding: "8px",
    borderRadius: "4px",
  };

  const buttonStyle = {
    padding: "8px 16px",
    backgroundColor: "#3b82f6",
    color: "#ffffff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  };

  const darkModeStyle = {
    backgroundColor: "#000000",
    color: "#ffffff",
    margin: "16px",
    padding: "16px",
    borderRadius: "10px",
  };

  return (
    <div style={darkModeStyle}>
      <h3>How can I assist you today?</h3>
      <div style={chatStyle}>
        <div style={messagesStyle}>
          {messages.map((msg, index) => (
            <MessageBubble
              key={index}
              sender={msg.sender}
              text={msg.text}
              timestamp={msg.timestamp}
            />
          ))}
        </div>
        <div style={inputStyle}>
          <input
            type="text"
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSend();
              }
            }}
            placeholder="Ask a question..."
            style={inputFieldStyle}
          />
          <button onClick={handleSend} style={buttonStyle}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;

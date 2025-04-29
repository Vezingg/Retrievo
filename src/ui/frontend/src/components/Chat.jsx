import React, { useState } from "react";
import { query } from "../api";

const Chat = () => {
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([]);

    const handleSend = async () => {
        if (input.trim()) {
            const userMessage = { sender: "user", text: input, timestamp: new Date().toLocaleTimeString() };
            setMessages((prev) => [...prev, userMessage]);

            try {
                const response = await query(input);
                const botMessage = { sender: "bot", text: response.answer, timestamp: new Date().toLocaleTimeString() };
                setMessages((prev) => [...prev, botMessage]);
            } catch (error) {
                const errorMessage = { sender: "bot", text: "Error fetching response", timestamp: new Date().toLocaleTimeString() };
                setMessages((prev) => [...prev, errorMessage]);
            }

            setInput("");
        }
    };

    return (
        <div className="chat">
            <div className="chat-messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`chat-message ${msg.sender}`}>
                        <span className="chat-timestamp">[{msg.timestamp}]</span> <b>{msg.sender}:</b> {msg.text}
                    </div>
                ))}
            </div>
            <div className="chat-input">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a question..."
                />
                <button onClick={handleSend}>Send</button>
            </div>
        </div>
    );
};

export default Chat;
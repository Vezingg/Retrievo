import React from "react";

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};

const MessageBubble = ({ sender, text, timestamp }) => {
  const isUser = sender === "user";
  const containerStyle = {
    display: "flex",
    justifyContent: isUser ? "flex-end" : "flex-start",
    marginBottom: "8px",
  };

  const bubbleStyle = {
    maxWidth: "300px",
    padding: "12px",
    borderRadius: "16px",
    boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.1)",
    backgroundColor: isUser ? "#3b82f6" : "#e5e7eb",
    color: isUser ? "#ffffff" : "#000000",
  };

  const timestampStyle = {
    fontSize: "12px",
    textAlign: isUser ? "right" : "left",
    color: isUser ? "#d1d5db" : "#6b7280",
  };

  return (
    <div style={containerStyle}>
      <div style={bubbleStyle}>
        <p style={{ marginBottom: "8px" }}>{text}</p>
        <div style={timestampStyle}>{formatTimestamp(timestamp)}</div>
      </div>
    </div>
  );
};

export default MessageBubble;

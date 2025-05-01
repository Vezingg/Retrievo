// components/URLProcessor.jsx
import React, { useState } from "react";
import toast from "react-hot-toast";
import { processURL } from "../api";

const URLProcessor = () => {
  const [url, setURL] = useState("");
  const [loading, setLoading] = useState(false);

  const isValidURL = (str) => {
    try {
      new URL(str);
      return true;
    } catch {
      return false;
    }
  };

  const handleProcessURL = async () => {
    if (!url) return toast.error("Enter a URL");
    if (!isValidURL(url)) return toast.error("Invalid URL format");

    setLoading(true);
    try {
      await processURL(url);
      toast.success("URL processed successfully");
    } catch (err) {
      console.error(err);
      toast.error("Failed to process URL");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>URL Processor</h3>
      <input
        type="text"
        placeholder="Enter URL"
        value={url}
        style={{ margin: "8px auto" }}
        onChange={(e) => setURL(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSend();
          }
        }}
      />
      <button onClick={handleProcessURL} disabled={loading}>
        {loading ? "Processing..." : "Process URL"}
      </button>
    </div>
  );
};

export default URLProcessor;

import React, { useState } from "react";
import { uploadPDF, processURL } from "../api";

const FileUploader = () => {
    const [file, setFile] = useState(null);
    const [url, setURL] = useState("");
    const [message, setMessage] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleURLChange = (e) => {
        setURL(e.target.value);
    };

    const handleUpload = async () => {
        if (file) {
            try {
                const response = await uploadPDF(file);
                setMessage(response.message);
            } catch (error) {
                setMessage("Error uploading file");
            }
        } else {
            setMessage("Please select a file first");
        }
    };

    const handleProcessURL = async () => {
        if (url) {
            try {
                const response = await processURL(url);
                setMessage(response.message);
            } catch (error) {
                setMessage("Error processing URL");
            }
        } else {
            setMessage("Please enter a URL first");
        }
    };

    return (
        <div className="file-uploader">
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload File</button>
            <br />
            <input
                type="text"
                placeholder="Enter URL"
                value={url}
                onChange={handleURLChange}
            />
            <button onClick={handleProcessURL}>Process URL</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default FileUploader;
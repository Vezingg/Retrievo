// modules/FileUploader.jsx
import toast from "react-hot-toast";
import { uploadPDF } from "../api";
import React, { useState } from "react";

const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return toast.error("Please select a file first");

    const allowed = ["application/pdf", "image/jpeg", "image/png"];
    if (!allowed.includes(file.type))
      return toast.error("Unsupported file type");
    if (file.size > 5 * 1024 * 1024)
      return toast.error("File too large (max 5MB)");

    setLoading(true);
    try {
      await uploadPDF(file);
      toast.success("File uploaded successfully");
    } catch (err) {
      console.error(err);
      toast.error("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>File Upload</h3>
      <input
        type="file"
        onChange={handleFileChange}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSend();
          }
        }}
      />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
};

export default FileUploader;

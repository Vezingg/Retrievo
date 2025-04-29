import axios from "axios";

const API_BASE_URL = "http://localhost:8080"; // FastAPI backend URL

export const uploadPDF = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(`${API_BASE_URL}/upload/pdf`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
};

export const processURL = async (url) => {
    const response = await axios.post(`${API_BASE_URL}/process/url`, { url });
    return response.data;
};

export const query = async (queryText) => {
    const response = await axios.post(`${API_BASE_URL}/query`, { query: queryText });
    return response.data;
};
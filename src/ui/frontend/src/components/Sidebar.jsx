import React from "react";
import { FaBars, FaTimes } from "react-icons/fa";
import FileUploader from "../modules/FileUploader";
import URLProcessor from "../modules/URLProcessor";

const Sidebar = ({ isSidebarOpen, toggleSidebar, setIsSidebarOpen }) => {
  return (
    <div
      style={{
        position: "fixed",
        left: 0,
        top: 0,
        bottom: 0,
        width: isSidebarOpen ? "250px" : "50px",
        background: "#1e1e1e",
        color: "#fff",
        transition: "width 0.4s",
        overflow: "hidden",
      }}
    >
      <button
        onClick={toggleSidebar}
        style={{
          background: "#333",
          color: "#fff",
          border: "none",
          width: "100%",
          padding: "10px",
          cursor: "pointer",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        {isSidebarOpen ? <FaTimes size={20} /> : <FaBars size={20} />}
      </button>
      {isSidebarOpen && (
        <div style={{ padding: "10px", width: "100%" }}>
          <FileUploader setIsSidebarOpen={setIsSidebarOpen} />
          <URLProcessor setIsSidebarOpen={setIsSidebarOpen} />
        </div>
      )}
    </div>
  );
};

export default Sidebar;

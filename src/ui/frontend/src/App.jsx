import React, { useState } from "react";
import { Toaster } from "react-hot-toast";
import Sidebar from "./components/Sidebar";
import Chat from "./modules/Chat";
import "./css/App.css"; // Assuming you have a CSS file for styling

const App = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSend = () => {
    setIsSidebarOpen(false); // Close the sidebar when send is triggered
  };

  return (
    <>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 2000,
          style: {
            background: "#333",
            color: "#fff",
          },
        }}
        closeButton
      />
      <div style={{ display: "flex" }}>
        <Sidebar
          isSidebarOpen={isSidebarOpen}
          toggleSidebar={toggleSidebar}
          setIsSidebarOpen={setIsSidebarOpen}
        />
        <div
          style={{
            flex: 1,
            marginLeft: isSidebarOpen ? "250px" : "50px",
            padding: "20px",
          }}
        >
          <h1 style={{ textAlign: "center" }}>Welcome to Retrievo</h1>
          <Chat />
        </div>
      </div>
    </>
  );
};

export default App;

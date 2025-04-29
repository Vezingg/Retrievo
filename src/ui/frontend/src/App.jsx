import React from "react";
import FileUploader from "./components/FileUploader";
import Chat from "./components/Chat";

const App = () => {
    return (
        <div className="app ">
            <h1>Welcome to Retrievo</h1>
            <FileUploader />
            <Chat />
        </div>
    );
};

export default App;

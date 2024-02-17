import { Box, Button, Text } from "@chakra-ui/react";
import axios from "axios";

import { useState } from "react";

function App() {
  const handleUpload = async () => {
    try {
      const response = await axios.post("http://localhost:8000/", {
        number: 100,
      });
      console.log("Number uploaded successfully:", response.data);
    } catch (error) {
      console.error("Error uploading number:", error);
    }
  };

  return (
    <div>
      <h1>Number Uploader</h1>
      <button onClick={handleUpload}>Upload Number</button>
    </div>
  );
}

export default App;

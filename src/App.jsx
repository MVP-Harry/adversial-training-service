import { Box, Button, Text } from "@chakra-ui/react";
import axios from "axios";
import { useState } from "react";

function App() {
  const [file, setFile] = useState();

  function handleChange(event) {
    setFile(event.target.files[0]);
  }

  function handleSubmit(event) {
    event.preventDefault();
    const url = "http://localhost:8000/";
    const formData = new FormData();
    formData.append("file", file);
    formData.append("fileName", file.name);
    const config = {
      headers: {
        "content-type": "multipart/form-data",
      },
    };
    axios.post(url, formData, config).then((response) => {
      console.log(response.data);
    });
  }

  return (
    <>
      <main className="container max-w-2xl flex flex-col gap-8">
        <h1 className="text-2xl font-extrabold mt-8 text-center">
          Enhance Your Model Through Adversial Training
        </h1>

        <input type="file" onChange={handleChange} />
        <Button onSubmit={handleSubmit}>Upload</Button>
        {/* <button type="submit">Upload</button> */}

        <Box></Box>
      </main>
    </>
  );
}

export default App;

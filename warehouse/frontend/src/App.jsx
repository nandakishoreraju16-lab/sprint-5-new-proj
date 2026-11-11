import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [name, setName] = useState("");
  const [destination, setDestination] = useState("");
  const [weight, setWeight] = useState("");
  const [vehicle, setVehicle] = useState("");
  const [batchId, setBatchId] = useState("");
  const [message, setMessage] = useState("");

  // POST /packages   (register a package)
  function addPackage() {
    fetch(API_URL + "/packages?name=" + name + "&destination=" + destination + "&weight=" + weight, {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => setMessage(data.detail ? "Error: " + data.detail : "Registered " + data.name + " as package " + data.id));
  }

  // POST /dispatch-batches   (make a new batch with this package)
  function addNewBatch() {
    fetch(API_URL + "/dispatch-batches?name=" + name + "&destination=" + destination + "&weight=" + weight + "&vehicle=" + vehicle, {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => setMessage(data.detail ? "Error: " + data.detail : "Added " + data.package.name + " to new batch " + data.batch.id));
  }

  // POST /dispatch-batches   (add this package to an old batch)
  function addToBatch() {
    fetch(API_URL + "/dispatch-batches?name=" + name + "&destination=" + destination + "&weight=" + weight + "&batch_id=" + batchId, {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => setMessage(data.detail ? "Error: " + data.detail : "Added " + data.package.name + " to batch " + data.batch.id));
  }

  return (
    <>
      <h1>Warehouse Dispatch</h1>
      <p>Package name: <input value={name} onChange={(e) => setName(e.target.value)} /></p>
      <p>Destination: <input value={destination} onChange={(e) => setDestination(e.target.value)} /></p>
      <p>Weight (kg): <input value={weight} onChange={(e) => setWeight(e.target.value)} /></p>
      <button onClick={addPackage}>Register package</button>

      <p>Vehicle: <input value={vehicle} onChange={(e) => setVehicle(e.target.value)} /></p>
      <button onClick={addNewBatch}>Add to new batch</button>

      <p>Batch id: <input value={batchId} onChange={(e) => setBatchId(e.target.value)} /></p>
      <button onClick={addToBatch}>Add to old batch</button>

      <p>{message}</p>
    </>
  );
}

export default App;

import { useState } from "react";

function AddClub({ onAdd }) {
  const [name, setName] = useState("");
  const [category, setCategory] = useState("technical");
  const [seats, setSeats] = useState("");
  const [deadline, setDeadline] = useState("");

  return (
    <>
      <h1>Add a club</h1>
      Name <input onChange={(e) => setName(e.target.value)} />
      <select onChange={(e) => setCategory(e.target.value)}>
        <option>technical</option>
        <option>cultural</option>
        <option>sports</option>
        <option>social</option>
        <option>literary</option>
      </select>
      Seats <input type="number" onChange={(e) => setSeats(e.target.value)} />
      Deadline <input type="date" onChange={(e) => setDeadline(e.target.value)} />
      <button onClick={() => onAdd(name, category, seats, deadline)}>Add</button>
    </>
  );
}

export default AddClub;

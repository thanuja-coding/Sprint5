import { useState } from "react";

function ClubItem({ club, onApply, onToggle }) {
  const [whyJoin, setWhyJoin] = useState("");

  return (
    <li className="club">
      <h2>{club.name}</h2>
      <p>{club.category}</p>
      <p>Deadline: {club.deadline}</p>
      <p>Seats: {club.seats}</p>

      {club.recruiting ? (
        <>
          <input placeholder="Why do you want to join?" onChange={(e) => setWhyJoin(e.target.value)} />
          <button onClick={() => onApply(club.id, whyJoin)}>Apply</button>
        </>
      ) : (
        <p>Recruitment closed</p>
      )}

      <button onClick={() => onToggle(club.id, club.recruiting ? 0 : 1)}>
        {club.recruiting ? "Close recruitment" : "Open recruitment"}
      </button>
    </li>
  );
}

export default ClubItem;

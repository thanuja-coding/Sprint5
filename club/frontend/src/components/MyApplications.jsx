import { useState } from "react";

function MyApplications({ applications, onShow, onStatus, onWithdraw }) {
  const [rollNo, setRollNo] = useState("");

  return (
    <>
      <h1>My applications</h1>
      <input placeholder="Your roll number" value={rollNo} onChange={(e) => setRollNo(e.target.value)} />
      <button onClick={() => onShow(rollNo)}>Show</button>
      <ul>
        {applications.map((application) => (
          <li key={application.id}>
            Club {application.club_id} · {application.status}
            {application.status === "applied" ? (
            <>
             <button onClick={() => onStatus(application.id, "shortlisted", rollNo)}>Shortlist</button>
             <button onClick={() => onStatus(application.id, "rejected", rollNo)}>Reject</button>
            </>
            ) : null}

            {application.status === "shortlisted" ? (
            <>
             <button onClick={() => onStatus(application.id, "selected", rollNo)}>Select</button>
             <button onClick={() => onStatus(application.id, "rejected", rollNo)}>Reject</button>
            </>
            ) : null}
            {application.status === "applied" ? (
            <button onClick={() => onWithdraw(application.id, rollNo)}>Withdraw</button>
            ) : null}
          </li>
        ))}
      </ul>
    </>
  );
}


export default MyApplications;

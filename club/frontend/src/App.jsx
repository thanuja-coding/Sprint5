import { useState, useEffect } from "react";
import ClubList from "./components/ClubList";
import MyApplications from "./components/MyApplications";
import AddClub from "./components/AddClub";
import Clubitem from "./components/ClubItem";


const API_URL = "http://127.0.0.1:8001";
function App() {
  const [clubs, setClubs] = useState([]);
  const [applications, setApplications] = useState([]);
  const [rollNo, setRollNo] = useState("");

  useEffect(() => {
    fetch(API_URL + "/clubs")
      .then((response) => response.json())
      .then((data) => setClubs(data));
  }, []);

function addClub(name, category, seats, deadline) {
    fetch(`${API_URL}/clubs?name=${name}&category=${category}&seats=${seats}&deadline=${deadline} 00:00:00`, {
    method: "POST"
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          console.log("API error:", data);
          return;
        }

        setClubs([...clubs, data]);
      })
      .catch((error) => console.log("Fetch error:", error));
  }


  function toggleRecruitment(id, recruiting) {
    fetch(`${API_URL}/clubs/${id}/recruitment?recruiting=${recruiting}`, {
    method: "PATCH"
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          console.log("API error:", data);
          return;
        }

        const res = await fetch(`${API_URL}/clubs`);
        const clubsData = await res.json();
        setClubs(clubsData);
      })
      .catch((error) => console.log("Fetch error:", error));
  }
  }

  function apply(id, whyJoin) {
  fetch(`${API_URL}/clubs/${id}/applications?roll_no=${rollNo}&why_join=${whyJoin}`, {
    method: "POST"
  })
    .then(async (response) => {
      const data = await response.json();

      if (!response.ok) {
        console.log("API error:", data);
        return;
      }

      fetch(`${API_URL}/clubs`  )
        .then((response) => response.json())
        .then((data) => setClubs(data));
    })
    .catch((error) => console.log("Fetch error:", error));
}


  function showApplications(roll) {
    fetch(API_URL + "/students/" + roll + "/applications")
      .then((response) => response.json())
      .then((data) => setApplications(data));
  }


  function updateStatus(id, status, roll) {
  fetch(API_URL + "/applications/" + id + "/status?status=" + status, {
    method: "PATCH"
  })
    .then(async (response) => {
      const data = await response.json();

      if (!response.ok) {
        console.log("API error:", data);
        return;
      }

      showApplications(roll);
    })
    .catch((error) => console.log("Fetch error:", error));
}

function withdrawApplication(id, roll) {
    fetch(`${API_URL}/applications/${id}/withdraw?roll_no=${roll}`, {
      method: "PATCH"
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          console.log("API error:", data);
          return;
        }

        setApplications(applications.map((application) => (application.id === data.id ? data : application)));
      })
      .catch((error) => console.log("Fetch error:", error));
  }
  return (
    <>
      Roll number <input onChange={(e) => setRollNo(e.target.value)} />
      <ClubList clubs={clubs} onApply={apply} onToggle={toggleRecruitment} />
      <MyApplications applications={applications} onShow={showApplications} onStatus={updateStatus} onWithdraw={withdrawApplication} />
      <AddClub onAdd={addClub} />
    </>
  );
export default App;

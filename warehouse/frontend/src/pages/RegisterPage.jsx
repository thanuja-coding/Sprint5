import { useState } from "react";

function RegisterPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("staff");

    async function register() {
        const res = await fetch("http://127.0.0.1:8000/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: `{"user_name": "${username}", "password": "${password}", "role": "${role}"}`,
        });
        const data = await res.json();
        if (res.ok) {
            alert(data.message);
        } else {
            alert(data.detail);
        }
    }

    return (
        <div>
            <h1>Register</h1>
            <input placeholder="Username" value={username} onChange={(event) => setUsername(event.target.value)} />
            <input placeholder="Password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
            <select value={role} onChange={(event) => setRole(event.target.value)}>
                <option value="staff">staff</option>
                <option value="admin">admin</option>
            </select>
            <button onClick={() => register()}>Register</button>
        </div>
    );
}

export default RegisterPage;
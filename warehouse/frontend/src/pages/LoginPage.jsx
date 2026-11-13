import { useState } from "react";

function LoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    async function login() {
        const res = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: `{"username": "${username}", "password": "${password}"}`,
        });
        const data = await res.json();
        if (res.ok) {
            alert("Login successful");
        } else {
            alert(data.detail);
        }
    }

    return (
        <div>
            <h1>Login</h1>
            <input placeholder="Username" value={username} onChange={(event) => setUsername(event.target.value)} />
            <input placeholder="Password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
            <button onClick={() => login()}>Login</button>
        </div>
    );
}

export default LoginPage;
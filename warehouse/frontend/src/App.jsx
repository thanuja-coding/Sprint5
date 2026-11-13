import { Routes, Route } from "react-router";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";

function App() {
    return (
        <Routes>
            <Route path="/" element={<div><RegisterPage /><LoginPage /></div>} />
            <Route path="*" element={<h1>404 Page Not Found</h1>} />
        </Routes>
    );
}

export default App;
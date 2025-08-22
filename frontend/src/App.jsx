import { useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem("token"));

  const handleLoginSuccess = () => {
    setLoggedIn(true);
  };

  return loggedIn ? <Dashboard /> : <Login onLoginSuccess={handleLoginSuccess} />;
}

export default App;

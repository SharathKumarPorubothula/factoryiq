import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API_URL = "http://localhost:5002/api";

function Dashboard() {

  const navigate = useNavigate();

  const [user, setUser] = useState(null);

  useEffect(() => {

    const storedUser = localStorage.getItem("user");

    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }

  }, []);

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    navigate("/login");
  };

  return (
    <div style={styles.page}>

      <header style={styles.header}>

        <h2>FactoryIQ</h2>

        <button onClick={logout} style={styles.logout}>
          Logout
        </button>

      </header>

      <main style={styles.main}>

        <h1>Dashboard</h1>

        {user && (
          <div style={styles.card}>

            <h3>Welcome, {user.first_name || user.username}</h3>

            <p>
              <strong>Username:</strong> {user.username}
            </p>

            <p>
              <strong>Email:</strong> {user.email}
            </p>

            <p>
              <strong>Roles:</strong>{" "}
              {user.roles?.join(", ")}
            </p>

          </div>
        )}

        <div style={styles.actions}>

          <button
            onClick={() => navigate("/create-user")}
            style={styles.button}
          >
            Create User
          </button>

        </div>

      </main>

    </div>
  );
}

const styles = {

  page: {
    minHeight: "100vh",
    background: "#f4f6f8",
  },

  header: {
    height: "60px",
    padding: "0 30px",
    background: "white",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
  },

  main: {
    padding: "30px",
  },

  card: {
    background: "white",
    padding: "25px",
    borderRadius: "10px",
    maxWidth: "500px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.08)",
  },

  actions: {
    marginTop: "25px",
  },

  button: {
    padding: "12px 20px",
    background: "#2563eb",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },

  logout: {
    padding: "8px 15px",
    background: "#dc2626",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
};

export default Dashboard;
import { useEffect, useState } from 'react';
import PatientCard from '../components/PatientCard';
import RecommendationList from '../components/RecommendationList';

const REACT_APP_API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const Dashboard = () => {
  const [patient, setPatient] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      setError("No token found. Please login.");
      return;
    }

    const headers = {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    };

    fetch(`${REACT_APP_API_BASE_URL}/patients/1`, { headers })
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch patient data");
        return res.json();
      })
      .then(data => setPatient(data.patient))
      .catch(err => setError(err.message));

    fetch(`${REACT_APP_API_BASE_URL}/recommend/1`, { headers })
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch recommendations");
        return res.json();
      })
      .then(data => setRecommendations(data.recommendations)) 
      .catch(err => setError(err.message));

  }, []);

  if (error) return <p className="text-red-600">{error}</p>;
  if (!patient) return <p>Loading...</p>;

  return (
    <div className="container">
      <PatientCard patient={patient} />
      <RecommendationList recommendations={recommendations} />
    </div>
  );
};

export default Dashboard;

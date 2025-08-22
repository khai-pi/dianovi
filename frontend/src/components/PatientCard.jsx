// src/components/PatientCard.jsx
const PatientCard = ({ patient }) => (
  <div className="patient-info">
    <h2>{patient.name}</h2>
    <p>Age: {patient.age}</p>
    <p>Condition: {patient.diagnosis}</p>
  </div>
);

export default PatientCard;

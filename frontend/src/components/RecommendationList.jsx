// src/components/RecommendationList.jsx
const RecommendationList = ({ recommendations }) => (
  <div className="recommendation-list">
    <h3>Recommendations</h3>
    <ul>
      {recommendations.map((rec, idx) => (
        <li key={idx}>{rec}</li>
      ))}
    </ul>
  </div>
);

export default RecommendationList;

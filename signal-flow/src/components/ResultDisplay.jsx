import React from 'react';

const ResultDisplay = ({ result, transferFunction }) => {
  return (
    <div className="card">
      <h2>Results</h2>
      <p><strong>Transfer Function:</strong> {transferFunction || 'Not calculated yet'}</p>
      <p><strong>Stability Result:</strong> {result || 'No result yet'}</p>
    </div>
  );
};

export default ResultDisplay;

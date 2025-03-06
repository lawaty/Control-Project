import React, { useState } from 'react';

const RouthStabilityChecker = ({ setStabilityResult }) => {
  const [equation, setEquation] = useState('');

  const handleCheckStability = () => {
    const coefficients = equation
      .match(/[-+]?\d*\.?\d+/g)
      .map(Number);

    if (coefficients.length === 0) {
      setStabilityResult('Invalid equation');
      return;
    }

    let signChanges = 0;
    for (let i = 1; i < coefficients.length; i++) {
      if (coefficients[i - 1] * coefficients[i] < 0) signChanges++;
    }

    setStabilityResult(
      signChanges > 0
        ? `Unstable System with ${signChanges} poles on RHS`
        : 'Stable System'
    );
  };

  return (
    <div className="card">
      <h2>Routh Stability Checker</h2>
      <input
        type="text"
        placeholder="Enter characteristic equation..."
        value={equation}
        onChange={(e) => setEquation(e.target.value)}
      />
      <button onClick={handleCheckStability}>Check Stability</button>
    </div>
  );
};

export default RouthStabilityChecker;

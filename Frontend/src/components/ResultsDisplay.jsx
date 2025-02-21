import React from 'react';

const ResultsDisplay = ({ results }) => (
  <div className="mt-8">
    <h3 className="text-xl font-bold mb-4">Analysis Results</h3>
    <div className="space-y-4">
      {results.predictions.map((result, index) => (
        <div key={index} className="card bg-base-100 shadow-xl p-4">
          <h4 className="font-bold">Policy {result.policy_id + 1}</h4>
          <p>Fraud Probability: {(result.fraud_probability * 100).toFixed(2)}%</p>
          {result.analysis && (
            <div className="mt-2">
              <h5 className="font-semibold">Risk Analysis:</h5>
              <p>{result.analysis}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  </div>
);

export default ResultsDisplay;
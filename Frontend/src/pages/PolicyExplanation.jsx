import React, { useState } from 'react';
import Markdown from 'markdown-to-jsx';
import { apiService } from '../../services/api';
import Loader, { ErrorAlert } from '../components/Loader';

const PolicyExplanation = () => {
  const [policyName, setPolicyName] = useState('');
  const [explanation, setExplanation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await apiService.explainPolicy(policyName);
      setExplanation(response.data.explanation);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Policy Explanation</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="form-control">
          <label className="label">
            <span className="label-text">Policy Name</span>
          </label>
          <input
            type="text"
            className="input input-bordered"
            value={policyName}
            onChange={(e) => setPolicyName(e.target.value)}
            placeholder="Enter policy name"
            required
          />
        </div>
        
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Fetching..." : "Get Explanation"}
        </button>
      </form>

      {loading && <Loader />}
      {error && <ErrorAlert message={error} />}

      {explanation && (
        <div className="mt-8 card bg-base-100 shadow-xl p-4">
          <h3 className="text-xl font-bold mb-4">Policy Explanation</h3>
          <div className="prose max-w-none">
            <Markdown>{explanation}</Markdown>
          </div>
        </div>
      )}
    </div>
  );
};

export default PolicyExplanation;

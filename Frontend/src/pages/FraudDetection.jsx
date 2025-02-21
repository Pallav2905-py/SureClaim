import React, { useState } from 'react';
import Loader, { ErrorAlert, PolicyForm, ResultsDisplay } from '../components/Loader';
import { apiService } from '../../services/api';

const FraudDetection = () => {
  const [policies, setPolicies] = useState([{
    policy_amount: '',
    customer_age: '',
    policy_duration: '',
    claims_history: '',
    payment_delay: '',
    customer_rating: '',
    policy_changes: '',
    agent_id: '',
    location_risk: '',
    previous_claims: ''
  }]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiService.detectFraud(policies);
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handlePolicyChange = (index, field, value) => {
    const newPolicies = [...policies];
    newPolicies[index] = { ...newPolicies[index], [field]: value };
    setPolicies(newPolicies);
  };

  const addPolicy = () => {
    setPolicies([...policies, { ...policies[0] }]);
  };

  if (loading) return <Loader />;

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Fraud Detection</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {policies.map((policy, index) => (
          <PolicyForm
            key={index}
            policy={policy}
            index={index}
            onChange={handlePolicyChange}
          />
        ))}
        
        <div className="flex gap-4">
          <button type="button" onClick={addPolicy} className="btn btn-secondary">
            Add Another Policy
          </button>
          <button type="submit" className="btn btn-primary">
            Analyze Policies
          </button>
        </div>
      </form>

      {error && <ErrorAlert message={error} />}
      {results && <ResultsDisplay results={results} />}
    </div>
  );
};

export default FraudDetection;
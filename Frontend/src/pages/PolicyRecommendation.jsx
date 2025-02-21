import React, { useState } from 'react';
import { apiService } from '../../services/api';
import ErrorAlert from '../components/ErrorAlert';
import Loader from '../components/Loader';
import Markdown from 'markdown-to-jsx';

const PolicyRecommendation = () => {
  const [userData, setUserData] = useState({
    age: '',
    gender: '',
    location: '',
    occupation: '',
    annual_income: '',
    previous_policy: '',
    family_size: '',
    medical_history: '',
    vehicle_details: '',
    property_details: '',
    risk_appetite: '',
    coverage_needs: ''
  });

  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await apiService.recommendPolicy(userData);
      setRecommendations(response.data.recommendations);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Policy Recommendation</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="card bg-base-100 shadow-xl p-4">
          <div className="grid grid-cols-2 gap-4">
            {Object.entries(userData).map(([field, value]) => (
              <div key={field} className="form-control">
                <label className="label">
                  <span className="label-text">
                    {field.replace(/_/g, ' ').toUpperCase()}
                  </span>
                </label>
                <input
                  type={
                    ['age', 'annual_income', 'family_size'].includes(field)
                      ? 'number'
                      : 'text'
                  }
                  className="input input-bordered"
                  value={value}
                  onChange={(e) =>
                    setUserData((prev) => ({ ...prev, [field]: e.target.value }))
                  }
                  placeholder={`Enter ${field.replace(/_/g, ' ')}`}
                  required
                />
              </div>
            ))}
          </div>
        </div>
        
        <button type="submit" className="btn btn-primary">
          Get Recommendations
        </button>
      </form>

      {error && <ErrorAlert message={error} />}

      {recommendations && (
        <div className="mt-8 card bg-base-100 shadow-xl p-4">
          <h3 className="text-xl font-bold mb-4">Policy Recommendations</h3>
          <div className="prose max-w-none">
           
              <Markdown>{recommendations}</Markdown>
            
          </div>
        </div>
      )}
    </div>
  );
};

export default PolicyRecommendation;

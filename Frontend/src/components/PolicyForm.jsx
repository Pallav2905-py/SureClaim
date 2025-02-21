import React from 'react';

const PolicyForm = ({ policy, index, onChange }) => (
  <div className="card bg-base-100 shadow-xl p-4">
    <h3 className="font-bold mb-2">Policy {index + 1}</h3>
    <div className="grid grid-cols-2 gap-4">
      {Object.entries(policy).map(([field, value]) => (
        <div key={field} className="form-control">
          <label className="label">
            <span className="label-text">{field.replace(/_/g, ' ').toUpperCase()}</span>
          </label>
          <input
            type="number"
            className="input input-bordered"
            value={value}
            onChange={(e) => onChange(index, field, e.target.value)}
          />
        </div>
      ))}
    </div>
  </div>
);

export default PolicyForm;
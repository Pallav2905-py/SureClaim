import React from 'react';

const ErrorAlert = ({ message }) => (
  <div className="alert alert-error mt-4">
    <span>{message}</span>
  </div>
);

export default ErrorAlert;
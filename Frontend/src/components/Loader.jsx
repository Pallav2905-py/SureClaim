export { default as Loader } from './Loader';
export { default as ErrorAlert } from './ErrorAlert';
export { default as PolicyForm } from './PolicyForm';
export { default as ResultsDisplay } from './ResultsDisplay';

// src/components/Loader.jsx
import React from 'react';

const Loader = () => (
  <div className="flex justify-center items-center min-h-[60vh]">
    <span className="loading loading-spinner loading-lg"></span>
  </div>
);

export default Loader;
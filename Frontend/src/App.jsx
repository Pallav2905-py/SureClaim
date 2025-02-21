import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Loader from './components/Loader';

const Home = React.lazy(() => import('./pages/Home'));
const FraudDetection = React.lazy(() => import('./pages/FraudDetection'));
const PolicyExplanation = React.lazy(() => import('./pages/PolicyExplanation'));
const PolicyRecommendation = React.lazy(() => import('./pages/PolicyRecommendation'));

const App = () => {
  return (
    <Router>
      <div className="min-h-screen bg-base-200">
        <nav className="navbar bg-base-100 shadow-lg">
          <div className="flex-1">
            <Link to="/" className="btn btn-ghost normal-case text-xl">Insurance Portal</Link>
          </div>
          <div className="flex-none">
            <ul className="menu menu-horizontal px-1">
              <li><Link to="/fraud-detection">Fraud Detection</Link></li>
              <li><Link to="/policy-explanation">Policy Explanation</Link></li>
              <li><Link to="/policy-recommendation">Policy Recommendation</Link></li>
            </ul>
          </div>
        </nav>
        
        <div className="container mx-auto p-4">
          <Suspense fallback={<Loader />}>
            <Routes>
              <Route path="/fraud-detection" element={<FraudDetection />} />
              <Route path="/policy-explanation" element={<PolicyExplanation />} />
              <Route path="/policy-recommendation" element={<PolicyRecommendation />} />
              <Route path="/" element={<Home />} />
            </Routes>
          </Suspense>
        </div>
      </div>
    </Router>
  );
};

export default App;
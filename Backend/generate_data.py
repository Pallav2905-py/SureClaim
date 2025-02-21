import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    
    data = {
        'policy_amount': np.random.uniform(1000, 100000, n_samples),
        'customer_age': np.random.normal(40, 15, n_samples),
        'policy_duration': np.random.choice([12, 24, 36, 48, 60], n_samples),
        'claims_history': np.random.poisson(2, n_samples),
        'payment_delay': np.random.exponential(2, n_samples),
        'customer_rating': np.random.normal(7, 2, n_samples),
        'policy_changes': np.random.poisson(1, n_samples),
        'agent_id': np.random.randint(1, 51, n_samples),
        'location_risk': np.random.uniform(0, 1, n_samples),
        'previous_claims': np.random.poisson(1.5, n_samples)
    }
    
    # Generate fraud labels (about 10% fraud rate)
    fraud_prob = np.zeros(n_samples)
    fraud_prob += 0.3 * (data['policy_amount'] > 80000)
    fraud_prob += 0.2 * (data['payment_delay'] > 5)
    fraud_prob += 0.2 * (data['claims_history'] > 4)
    fraud_prob += 0.2 * (data['policy_changes'] > 2)
    fraud_prob += 0.1 * (data['customer_rating'] < 4)
    
    data['fraud'] = (fraud_prob > 0.5).astype(int)
    
    df = pd.DataFrame(data)
    
    # Normalize features
    scaler = StandardScaler()
    features = list(data.keys())[:-1]  # Exclude fraud label
    df[features] = scaler.fit_transform(df[features])
    
    return df

if __name__ == "__main__":
    df = generate_synthetic_data()
    df.to_csv('policy_data.csv', index=False)
    print("Generated synthetic policy data and saved to policy_data.csv")

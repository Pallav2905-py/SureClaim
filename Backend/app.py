# app.py
from flask import Flask, request, jsonify
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import networkx as nx
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import json
from groq import Groq
import re
from flask_cors import CORS
from flask_cors import cross_origin


load_dotenv()

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
client = Groq(api_key="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")


# GNN Model Definition
class GNNPolicyFraudDetector(torch.nn.Module):
    def __init__(self, num_features):
        super(GNNPolicyFraudDetector, self).__init__()
        self.conv1 = GCNConv(num_features, 64)
        self.conv2 = GCNConv(64, 32)
        self.conv3 = GCNConv(32, 2)

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.5, training=self.training)
        x = F.relu(self.conv2(x, edge_index))
        x = self.conv3(x, edge_index)
        return F.log_softmax(x, dim=1)


def analyze_policy_with_llm(policy_data):
    """
    Analyze policy using pattern matching when LLM is unavailable
    """
    risk_factors = []

    # Define risk thresholds
    if policy_data.get("policy_amount", 0) > 80000:
        risk_factors.append("High policy amount")
    if policy_data.get("payment_delay", 0) > 5:
        risk_factors.append("Significant payment delays")
    if policy_data.get("claims_history", 0) > 4:
        risk_factors.append("High number of previous claims")
    if policy_data.get("policy_changes", 0) > 2:
        risk_factors.append("Frequent policy changes")
    if policy_data.get("customer_rating", 10) < 4:
        risk_factors.append("Low customer rating")

    if risk_factors:
        analysis = "Risk factors identified:\n- " + "\n- ".join(risk_factors)
    else:
        analysis = "No significant risk factors identified."

    return analysis


# Load pre-trained model
try:
    model = GNNPolicyFraudDetector(num_features=10)
    model.load_state_dict(torch.load("model.pth"))
    model.eval()
except Exception as e:
    print(f"Error loading model: {e}")
    model = None


@app.route("/detect_fraud", methods=["POST"])
@cross_origin()
def detect_fraud():
    try:
        data = request.get_json()
        policies = data.get("policies", [])

        if not policies:
            return jsonify({"error": "No policy data provided"}), 400

        if model is None:
            return jsonify({"error": "Model not loaded properly"}), 500

        # Convert policies to tensor
        features = [
            "policy_amount",
            "customer_age",
            "policy_duration",
            "claims_history",
            "payment_delay",
            "customer_rating",
            "policy_changes",
            "agent_id",
            "location_risk",
            "previous_claims",
        ]

        x = torch.tensor(
            [[float(policy.get(f, 0)) for f in features] for policy in policies],
            dtype=torch.float,
        )

        # Create simple fully connected graph for demonstration
        edges = []
        for i in range(len(policies)):
            for j in range(i + 1, len(policies)):
                edges.append([i, j])
                edges.append([j, i])

        if not edges:  # Handle single policy case
            edges = [[0, 0]]  # Self-loop

        edge_index = torch.tensor(edges, dtype=torch.long).t()

        # Get predictions
        with torch.no_grad():
            output = model(x, edge_index)
            predictions = output.exp()

        # Analyze policies
        results = []
        for idx, pred in enumerate(predictions):
            fraud_prob = float(pred[1])
            result = {
                "policy_id": idx,
                "fraud_probability": fraud_prob,
            }

            if fraud_prob > 0.7:  # High risk threshold
                result["analysis"] = analyze_policy_with_llm(policies[idx])

            results.append(result)

        return jsonify(
            {
                "status": "success",
                "predictions": results,
                "total_policies_analyzed": len(policies),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
@cross_origin()
def health_check():
    return jsonify({"status": "healthy", "model_loaded": model is not None})


@app.route("/explain_policy", methods=["GET"])
@cross_origin()
def explain_policy():
    try:
        policy_name = request.args.get("policy_name")
        print("policyname",policy_name)
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {
                    "role": "user",
                    "content": f'Refined Prompt: "Provide a comprehensive and up-to-date list of key aspects, features, and details about ${policy_name}\n in pointer format, covering its definition, objectives, benefits, components, and any other relevant information."\n\nTemplate:\n\nI. Introduction to [Scheme Name]\n\nDefinition:\nObjective:\nBackground:\nII. Key Features of [Scheme Name]\n\n[Feature 1]:\n[Feature 2]:\n[Feature 3]:\n...\nIII. Benefits of [Scheme Name]\n\n[Benefit 1]:\n[Benefit 2]:\n[Benefit 3]:\n...\nIV. Components of [Scheme Name]\n\n[Component 1]:\n[Component 2]:\n[Component 3]:\n...\nV. Eligibility and Requirements\n\nEligibility criteria:\nRequired documents:\nApplication process:\nVI. Implementation and Management\n\nImplementation timeline:\nManagement structure:\nFunding and resources:\nVII. Impact and Outcomes\n\nExpected outcomes:\nSuccess stories:\nChallenges and limitations:\nVIII. Latest Developments and Updates\n\nRecent changes:\nUpcoming milestones:\nFuture plans:\nIX. Conclusion\n\nSummary of key points:\nFinal thoughts:\nX. Additional Resources\n\nRelevant links:\nContact information:\nFurther reading:\nNote: Replace [Scheme Name] with the actual name of the scheme you want to list, and fill in the pointers with the latest and most accurate information available.\n\nExample: If you want to list all the things about the "National Education Policy", the template would become:\n\nI. Introduction to National Education Policy\n\nDefinition: A comprehensive framework for education in a country...\nObjective: To improve the quality of education...\nBackground: The policy was introduced in [Year]...\nAnd so on...',
                }
            ],
            temperature=0.6,
            # max_completion_tokens=4096,
            top_p=0.95,
            stream=True,
            stop=None,
        )

        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""

        cleaned_text = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)

        print(cleaned_text)
        return jsonify({"status": "success", "explanation": cleaned_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/recommend_policy", methods=["POST"])
@cross_origin()
def recommend_policy():
    try:
        user_data = request.get_json()


        # Construct a detailed prompt for the LLM
        prompt = f"""
        As an insurance policy recommendation expert, analyze this user's profile and provide detailed, personalized insurance policy and 3 other policy recommendations.

        User Profile:
        - Age: {user_data.get('age')}
        - Gender: {user_data.get('gender')}
        - Location: {user_data.get('location')}
        - Occupation: {user_data.get('occupation')}
        - Annual Income: {user_data.get('annual_income')}
        - Previous Policy: {user_data.get('previous_policy')}
        - Family Size: {user_data.get('family_size')}
        - Medical History: {user_data.get('medical_history', [])}
        - Vehicle Details: {user_data.get('vehicle_details', {})}
        - Property Details: {user_data.get('property_details', {})}
        - Risk Appetite: {user_data.get('risk_appetite')}
        - Current Coverage Needs: {user_data.get('coverage_needs', [])}

        Please provide insurance policy recommendations in the following format:

        1. Primary Policy Recommendation
        - Policy Type:
        - Coverage Amount:
        - Key Benefits:
        - Premium Range:
        - Why This Policy:
        - Special Features:

        2. Additional Coverage Recommendations
        - List of recommended add-ons
        - Priority order
        - Justification for each

        3. Cost Optimization Suggestions
        - Premium reduction strategies
        - Bundling opportunities
        - Long-term savings options

        4. Risk Assessment
        - Key risk factors
        - Mitigation strategies
        - Coverage considerations

        Base your recommendations on the user's specific profile, local regulations, and market conditions.
        Consider age-specific needs, location-based risks, occupation hazards, and family circumstances.
        Provide specific premium ranges and coverage amounts in numerical format.
        """

        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=False,
        )

        recommendations = completion.choices[0].message.content
        recommendations = re.sub(
            r"<think>.*?</think>", "", recommendations, flags=re.DOTALL
        )

        print(recommendations)
        return jsonify({"status": "success", "recommendations": recommendations})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

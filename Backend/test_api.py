# import requests
# import json

# # Test data
# test_data = {
    # "policies": [
    #     {
    #         "policy_amount": 85000,
    #         "customer_age": 35,
    #         "policy_duration": 24,
    #         "claims_history": 5,
    #         "payment_delay": 6,
    #         "customer_rating": 3,
    #         "policy_changes": 3,
    #         "agent_id": 25,
    #         "location_risk": 0.8,
    #         "previous_claims": 4
    #     },
    #     {
    #         "policy_amount": 15000,
    #         "customer_age": 45,
    #         "policy_duration": 12,
    #         "claims_history": 1,
    #         "payment_delay": 0,
    #         "customer_rating": 8,
    #         "policy_changes": 0,
    #         "agent_id": 10,
    #         "location_risk": 0.2,
    #         "previous_claims": 0
    #     }
    # ]
# }

# # Send request to API
# response = requests.post('http://localhost:5000/detect_fraud', 
#                         json=test_data)

# # Print results
# print(json.dumps(response.json(), indent=2))


from groq import Groq

client = Groq(api_key="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")
completion = client.chat.completions.create(
    model="deepseek-r1-distill-llama-70b",
    messages=[
        {
            "role": "user",
            "content": "Refined Prompt: \"Provide a comprehensive and up-to-date list of key aspects, features, and details aboutPradhan Mantri Jan Arogya Yojana (PM-JAY)\n in pointer format, covering its definition, objectives, benefits, components, and any other relevant information.\"\n\nTemplate:\n\nI. Introduction to [Scheme Name]\n\nDefinition:\nObjective:\nBackground:\nII. Key Features of [Scheme Name]\n\n[Feature 1]:\n[Feature 2]:\n[Feature 3]:\n...\nIII. Benefits of [Scheme Name]\n\n[Benefit 1]:\n[Benefit 2]:\n[Benefit 3]:\n...\nIV. Components of [Scheme Name]\n\n[Component 1]:\n[Component 2]:\n[Component 3]:\n...\nV. Eligibility and Requirements\n\nEligibility criteria:\nRequired documents:\nApplication process:\nVI. Implementation and Management\n\nImplementation timeline:\nManagement structure:\nFunding and resources:\nVII. Impact and Outcomes\n\nExpected outcomes:\nSuccess stories:\nChallenges and limitations:\nVIII. Latest Developments and Updates\n\nRecent changes:\nUpcoming milestones:\nFuture plans:\nIX. Conclusion\n\nSummary of key points:\nFinal thoughts:\nX. Additional Resources\n\nRelevant links:\nContact information:\nFurther reading:\nNote: Replace [Scheme Name] with the actual name of the scheme you want to list, and fill in the pointers with the latest and most accurate information available.\n\nExample: If you want to list all the things about the \"National Education Policy\", the template would become:\n\nI. Introduction to National Education Policy\n\nDefinition: A comprehensive framework for education in a country...\nObjective: To improve the quality of education...\nBackground: The policy was introduced in [Year]...\nAnd so on..."
        }
    ],
    temperature=0.6,
    # max_completion_tokens=4096,
    top_p=0.95,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")

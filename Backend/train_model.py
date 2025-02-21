import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import pandas as pd
import numpy as np
import networkx as nx
from sklearn.model_selection import train_test_split

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

def create_policy_graph(df):
    G = nx.Graph()
    
    # Add nodes
    for idx, row in df.iterrows():
        G.add_node(idx, features=row.drop('fraud').values)
    
    # Add edges based on feature similarity
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            similarity = np.sum(np.abs(df.iloc[i].drop('fraud').values - 
                                     df.iloc[j].drop('fraud').values) < 0.5)
            if similarity > 5:  # Connect if more than 5 features are similar
                G.add_edge(i, j)
    
    return G

def train_gnn(df):
    # Create graph
    G = create_policy_graph(df)
    
    # Prepare PyTorch Geometric data
    edge_index = torch.tensor(list(G.edges())).t().contiguous()
    x = torch.tensor(df.drop('fraud', axis=1).values, dtype=torch.float)
    y = torch.tensor(df['fraud'].values, dtype=torch.long)
    
    # Initialize model
    model = GNNPolicyFraudDetector(num_features=df.shape[1]-1)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    # Training loop
    model.train()
    for epoch in range(200):
        optimizer.zero_grad()
        out = model(x, edge_index)
        loss = F.nll_loss(out, y)
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 20 == 0:
            pred = out.argmax(dim=1)
            correct = (pred == y).sum()
            acc = int(correct) / len(y)
            print(f'Epoch {epoch+1}: Loss = {loss.item():.4f}, Accuracy = {acc:.4f}')
    
    return model

if __name__ == "__main__":
    # Load data
    df = pd.read_csv('policy_data.csv')
    
    # Train model
    model = train_gnn(df)
    
    # Save model
    torch.save(model.state_dict(), 'model.pth')
    print("Model trained and saved as model.pth")

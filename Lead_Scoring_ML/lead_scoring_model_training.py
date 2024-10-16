import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import torch
from transformers import BertTokenizer, BertModel
from tqdm import tqdm
import joblib

# Check for GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load the data
df = pd.read_csv('./company_data_with_descriptions.csv')

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased').to(device)

# Function to get BERT embeddings
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()

# Apply BERT embeddings to company descriptions
print("Generating BERT embeddings...")
embeddings = []
for text in tqdm(df['company_description']):
    embeddings.append(get_bert_embedding(text))

# Convert embedding to separate columns
embedding_df = pd.DataFrame(embeddings, columns=[f'embed_{i}' for i in range(768)])
df = pd.concat([df, embedding_df], axis=1)

# Prepare features and target
features = ['number_of_employees', 'revenue_growth_percentage', 'revenue_amount_aed', 'founded_year', 'industry'] + [f'embed_{i}' for i in range(768)]
X = df[features]
y = df['lead_converted']

# Encode categorical variables
le = LabelEncoder()
X['industry'] = le.fit_transform(X['industry'])
for i in range(len(y)):
    if y[i]==True:
        y[i] = 1
    else:
        y[i] = 0
y = y.astype(int)
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the XGBoost model
print("Training XGBoost model...")
model = XGBClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['lead_not_converted', 'lead_converted']))

# Feature importance
feature_importance = model.feature_importances_
feature_names = X.columns
sorted_idx = np.argsort(feature_importance)
print("\nTop 10 Important Features:")
for idx in sorted_idx[-10:]:
    print(f"{feature_names[idx]}: {feature_importance[idx]:.4f}")

# Save the model
joblib.dump(model, 'lead_generation_model.joblib')
print("Model saved as 'lead_generation_model.joblib'")
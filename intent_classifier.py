import pandas as pd

df = pd.read_csv("intent_dataset.csv")

from sentence_transformers import SentenceTransformer

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode all text
X = model.encode(df['user_input'].tolist())
y = df['intent'].tolist()


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
# print(classification_report(y_test, y_pred))


def predict_intent(user_input):
    vector = model.encode([user_input])
    prediction = clf.predict(vector)[0]
    return prediction

# def predict_intent(user_input, threshold=0.6):
#     vector = model.encode([user_input])
#     probabilities = clf.predict_proba(vector)[0]
#     max_prob = max(probabilities)
#     predicted_intent = clf.classes_[probabilities.argmax()]
    
#     if max_prob >= threshold:
#         return predicted_intent
#     else:
#         return "unknown_intent"


import pickle

# Save the classifier
with open('intent_classifier.pkl', 'wb') as f:
    pickle.dump(clf, f)

# Save the SentenceTransformer model separately (recommended way)
model.save("intent_sentence_bert_model")



import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

data = {
"text":[
"verify your bank account now",
"urgent click this link to login",
"free gift card claim now",
"meeting tomorrow at 5",
"let's have lunch",
"project discussion"
],
"label":[1,1,1,0,0,0]
}

df = pd.DataFrame(data)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])
y = df["label"]

model = LogisticRegression()
model.fit(X,y)

pickle.dump(model,open("model.pkl","wb"))
pickle.dump(vectorizer,open("vectorizer.pkl","wb"))

print("model ready")

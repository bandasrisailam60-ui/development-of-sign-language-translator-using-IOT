import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


# load data
df = pd.read_csv('dataset.csv')
X = df[['f1','f2','f3','f4','f5']].values.astype('float32')
labels = df['label'].values


le = LabelEncoder()
y = le.fit_transform(labels)
num_classes = len(le.classes_)


# split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)


# simple MLP
model = keras.Sequential([
layers.Input(shape=(5,)),
layers.Dense(64, activation='relu'),
layers.Dropout(0.2),
layers.Dense(64, activation='relu'),
layers.Dense(num_classes, activation='softmax')
])


model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


model.fit(X_train, y_train, validation_data=(X_val,y_val), epochs=80, batch_size=32)


model.save('sign_model.h5')


# save label encoder mapping
import pickle
with open('label_encoder.pkl','wb') as f:
pickle.dump(le, f)


print('Saved model and label encoder. Classes:', le.classes_)
import pandas as pd
import ast  # To parse the string representation of lists
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.morphology.database import MorphologyDB
from camel_tools.utils.dediac import dediac_ar
from sklearn.feature_extraction.text import TfidfVectorizer

# Load and clean your CSV file
df = pd.read_csv('stemmed_manners.csv')

# Initialize Morphology Analyzer for Lemmatization
db = MorphologyDB.builtin_db()  # Load built-in database for morphology analysis
analyzer = Analyzer(db)

def stem_arabic_tokens(tokens):
    """
    Function to stem a list of Arabic tokens using Camel Tools.
    """
    stemmed_tokens = []
    for token in tokens:
        analysis = analyzer.analyze(token)
        if analysis:  # Check if any analysis exists
            stemmed_token = analysis[0]['stem']  # Use the first stem from the analysis
            stemmed_tokens.append(stemmed_token)
        else:
            stemmed_tokens.append(token)  # If no stem found, keep the original token
    return stemmed_tokens

def process_stemming(row):
    """
    Function to process a string representation of tokenized words,
    parse it into a list, and stem the tokens.
    """
    try:
        # Convert the string representation of the list into an actual list
        tokens = ast.literal_eval(row)
        if isinstance(tokens, list):
            # Apply stemming
            return stem_arabic_tokens(tokens)
        else:
            return []  # Return an empty list if the input is not a valid list
    except (ValueError, SyntaxError):
        return []  # Return an empty list if parsing fails




df['Stemmed_tokens2'] = df['Tokenized_Citation'].apply(process_stemming)
# Convert lists of stemmed tokens into strings
df['Stemmed_tokenss'] = df['Stemmed_tokens2'].apply(lambda x: ' '.join(x))


# Save the updated DataFrame to a new CSV file
#df.to_csv('stemmed2_manners.csv', index=False, encoding='utf-8')


# Vectorization using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Stemmed_tokenss'])

# Convert the matrix to a DataFrame for easy manipulation
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
tfidf_df.index = df.index  # Ensure indices match the original DataFrame

# Concatenate TF-IDF results with the original DataFrame
df_with_tfidf = pd.concat([df, tfidf_df], axis=1)
df_with_tfidf.drop(columns=['Cleaned_Citation', 'Stemmed_tokens', 'Tokenized_Citation','Stemmed_tokens2'], inplace=True)  # Drop unnecessary columns

# Save the final DataFrame with TF-IDF results to a new CSV file
#df_with_tfidf.to_csv('tfidf_stemmed_manners.csv', index=False, encoding='utf-8')

# Display the DataFrame with TF-IDF results
#print(df_with_tfidf.head())

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# Load and clean your CSV file
df = pd.read_csv('tfidf_stemmed_manners.csv')

# X = données vectorisées
X = tfidf_matrix

# y = étiquettes
y = df['Manner']

####
from imblearn.over_sampling import RandomOverSampler

ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(X, y)


# Entraînez ensuite votre modèle avec ces données rééchantillonnées

# Vous pouvez maintenant entraîner votre modèle sur X_resampled et y_resampled

# Logique de régression
""" 
# Diviser en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42)

# Entraîner le modèle de régression logistique multinomiale
from sklearn.linear_model import LogisticRegression

model = LogisticRegression( max_iter=1000)

model.fit(X_train, y_train)

# Prédire et évaluer
y_pred = model.predict(X_test)

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred)) 
 """
# SVM
""" 
# Import necessary libraries
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Assuming you already have your data in X (features) and y (labels)
# Example: X = your_features_data, y = your_labels_data

# Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Initialize the Support Vector Classifier (SVC)
# You can adjust kernel, C, and gamma as per your needs
svm = SVC(kernel='rbf', C=1.0, gamma='scale')  # For non-linear boundary

# Train the model on training data
svm.fit(X_train, y_train)

# Make predictions on the test data
y_pred = svm.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Detailed classification report (Precision, Recall, F1-Score)
print(classification_report(y_test, y_pred))
 """

### Naive Bayes
""" 
# Import necessary libraries
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score

# Splitting the dataset into training and testing sets (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Initialize the Multinomial Naive Bayes classifier
nb_model = MultinomialNB()

# Train the model on the training data
nb_model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = nb_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Detailed classification report (Precision, Recall, F1-Score)
print(classification_report(y_test, y_pred))

 """
### Random Forest
""" 
# Import necessary libraries
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score

# Step 2: Splitting the dataset into training and testing sets (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Step 3: Initialize the Random Forest classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)  # You can adjust n_estimators for more trees

# Step 4: Train the Random Forest model on the training data
rf_model.fit(X_train, y_train)

# Step 5: Make predictions on the test data
y_pred = rf_model.predict(X_test)

# Step 6: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Detailed classification report (Precision, Recall, F1-Score)
print(classification_report(y_test, y_pred)) 
 """
""" 
### Gradient Boosting
# Import necessary libraries
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score


# Step 2: Splitting the dataset into training and testing sets (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Step 3: Initialize the Gradient Boosting classifier
gb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)

# Step 4: Train the Gradient Boosting model on the training data
gb_model.fit(X_train, y_train)

# Step 5: Make predictions on the test data
y_pred = gb_model.predict(X_test)

# Step 6: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Detailed classification report (Precision, Recall, F1-Score)
print(classification_report(y_test, y_pred)) 
 """

""" 
### Deep Learning FNN

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score



# Step 3: Encode the labels
from sklearn.preprocessing import LabelEncoder

# Step 1: Initialize the LabelEncoder
label_encoder = LabelEncoder()

# Step 2: Convert string labels into numeric labels
y_train_encoded = label_encoder.fit_transform(y)

# Step 4: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_train_encoded, test_size=0.2, random_state=42)

# Step 5: Build the Feedforward Neural Network Model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(512, activation='relu', input_dim=X_train.shape[1]),  # Input layer
    tf.keras.layers.Dropout(0.5),  # Dropout layer for regularization
    tf.keras.layers.Dense(256, activation='relu'),  # Hidden layer
    tf.keras.layers.Dropout(0.5),  # Dropout layer for regularization
    tf.keras.layers.Dense(len(np.unique(y)), activation='softmax')  # Output layer (softmax for multiclass classification)
])

# Step 6: Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',  # Use sparse categorical crossentropy for multiclass
              metrics=['accuracy'])

# Step 7: Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Step 8: Evaluate the model
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)  # Convert predicted probabilities to class labels

# Step 9: Print evaluation metrics
accuracy = accuracy_score(y_test, y_pred_classes)
print(f'Accuracy: {accuracy:.2f}')
print(classification_report(y_test, y_pred_classes, target_names=label_encoder.classes_))
 """
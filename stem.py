import pandas as pd
import ast  # To parse the string representation of lists
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.morphology.database import MorphologyDB
from camel_tools.utils.dediac import dediac_ar
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import RFE
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, accuracy_score, confusion_matrix, mean_absolute_error, mean_squared_error
from imblearn.over_sampling import RandomOverSampler

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

# Apply stemming
df['Stemmed_tokens2'] = df['Tokenized_Citation'].apply(process_stemming)
df['Stemmed_tokenss'] = df['Stemmed_tokens2'].apply(lambda x: ' '.join(x))  # Join tokens as strings

# Vectorization using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Stemmed_tokenss'])

# Convert the matrix to a DataFrame for easy manipulation
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
tfidf_df.index = df.index  # Ensure indices match the original DataFrame

# Concatenate TF-IDF results with the original DataFrame
df_with_tfidf = pd.concat([df, tfidf_df], axis=1)
df_with_tfidf.drop(columns=['Cleaned_Citation', 'Stemmed_tokens', 'Tokenized_Citation', 'Stemmed_tokens2'], inplace=True)
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, log_loss
from imblearn.over_sampling import SMOTE
from scipy.sparse import csr_matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.metrics import roc_curve, roc_auc_score
import numpy as np

# Assume df_with_tfidf and tfidf_matrix are predefined
X = tfidf_matrix  # Sparse matrix
y = df_with_tfidf['Manner']  # Target labels

# Step 1: Handle rare classes
label_counts = y.value_counts()

# Get labels with counts of 0 or 1 (these are rare classes)
rare_labels = label_counts[label_counts <= 1].index.tolist()

# Remove rare classes with only 1 sample
y_filtered = y[~y.isin(rare_labels)]

# Recreate X using the filtered y (corresponding to the filtered labels)
if not isinstance(X, csr_matrix):
    X = csr_matrix(X)

X_filtered = X[y_filtered.index.values]

# Step 2: Calculate the mean number of samples per class
class_counts = y_filtered.value_counts()
mean_samples = int(np.mean(class_counts))

# Step 3: Define the sampling strategy for classes with fewer samples than the mean
sampling_strategy = {label: mean_samples for label, count in class_counts.items() if count < mean_samples}

# Step 4: Apply SMOTE with the custom sampling strategy
smote = SMOTE(random_state=42, sampling_strategy=sampling_strategy, k_neighbors=1)
X_resampled, y_resampled = smote.fit_resample(X_filtered, y_filtered)

# Step 5: Initialize the Random Forest classifier
rf_model = RandomForestClassifier(
    n_estimators=100, 
    random_state=42, 
)
# Step 6: Implement Stratified Cross-Validation
cv = StratifiedKFold(n_splits=7, shuffle=True, random_state=42)

# List to store models and their accuracies
accuracies = []
models = []

# Iterate through each fold
# Step 6: Implement Stratified Cross-Validation
cv = StratifiedKFold(n_splits=7, shuffle=True, random_state=42)

# List to store models, accuracies, and data splits
accuracies = []
models = []
last_train_data = None
last_test_data = None

# Iterate through each fold
for fold, (train_index, test_index) in enumerate(cv.split(X_resampled, y_resampled)):
    X_train, X_test = X_resampled[train_index], X_resampled[test_index]
    y_train, y_test = y_resampled[train_index], y_resampled[test_index]
    
    # Step 7: Train the Random Forest model on the training data
    rf_model.fit(X_train, y_train)

    # Step 8: Make predictions on the test data
    y_pred = rf_model.predict(X_test)
    y_prob = rf_model.predict_proba(X_test)  # Get predicted probabilities

    # Step 9: Calculate Log Loss
    log_loss_value = log_loss(y_test, y_prob)
    print(f"Log Loss: {log_loss_value:.4f}")

    # Evaluate the model with accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')
    
    # Store model and accuracy
    accuracies.append(accuracy)
    models.append(rf_model)

    # Save the last fold's train and test data
    if fold == cv.get_n_splits() - 1:  # Check if this is the last fold
        last_train_data = (X_train, y_train)
        last_test_data = (X_test, y_test)

# Print extracted data from the last fold
if last_train_data and last_test_data:
    print("Last Train Data (X_train and y_train):")
    print(last_train_data[0].shape, last_train_data[1].shape)  # X_train, y_train shapes
    print("Last Test Data (X_test and y_test):")
    print(last_test_data[0].shape, last_test_data[1].shape)  # X_test, y_test shapes

# After the loop, find and return the model(s) with accuracy 0.68
matching_models = [model for model, accuracy in zip(models, accuracies) if round(accuracy, 2) == 0.68]

# Get the last model with accuracy 0.68
if matching_models:
    last_model_0_68 = matching_models[-1]  # Retrieve the last model with accuracy 0.68
    print("Last model with accuracy 0.68 found.")
else:
    last_model_0_68 = None
    print("No model with accuracy 0.68 found.")
# Last train data shapes
X_train_last = last_train_data[0]  # Shape: (6744, 1976)
y_train_last = last_train_data[1]  # Shape: (6744,)

# Last test data shapes
X_test_last = last_test_data[0]  # Shape: (1123, 1976)
y_test_last = last_test_data[1]  # Shape: (1123,)

# Now X_train_last, y_train_last are your training sets,
# and X_test_last, y_test_last are your test sets
print(f"Training Data Shape: X_train: {X_train_last.shape}, y_train: {y_train_last.shape}")
print(f"Test Data Shape: X_test: {X_test_last.shape}, y_test: {y_test_last.shape}")
print("********************************************************")
rf_model.fit(X_train_last, y_train_last)
# Step 8: Make predictions on the test data
y_pred = rf_model.predict(X_test_last)
y_prob = rf_model.predict_proba(X_test_last)  # Get predicted probabilities

# Step 9: Calculate Log Loss
log_loss_value = log_loss(y_test_last, y_prob)
print(f"Log Loss: {log_loss_value:.4f}")
accuracy = accuracy_score(y_test_last, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# The last model with accuracy 0.68 is now stored in last_model_0_68

# Grid search to tune hyperparameters
""" param_grid = {
    'n_estimators': [100, 150, 200],
    'max_depth': [10, 15, None],
    'min_samples_split': [ 10, 20, 25]
}

grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

# Fit grid search with cross-validation
grid_search.fit(X_train, y_train)

# Get the best model after grid search
best_rf_model = grid_search.best_estimator_

# Step 4: Perform cross-validation on the best model
cross_val_scores = cross_val_score(best_rf_model, X_resampled, y_resampled, cv=5, scoring='accuracy', n_jobs=-1)

# Print cross-validation results
print(f'Cross-validation accuracy scores: {cross_val_scores}')
print(f'Mean cross-validation accuracy: {cross_val_scores.mean():.2f}')

# Step 5: Make predictions on the test data using the best model
y_pred = best_rf_model.predict(X_test)

# Step 6: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy on test data: {accuracy:.2f}')
print(classification_report(y_test, y_pred))

# Print the best hyperparameters found by GridSearchCV
print("Best parameters found by GridSearchCV: ", grid_search.best_params_) 

 """



#### KNN
""" from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Use the updated DataFrame for `X` and `y`
X = tfidf_df.values  # Convert TF-IDF matrix to dense numpy array
y = df['Manner']  # This is the original string labels

# Initialize the label encoder
label_encoder = LabelEncoder()

# Encode the string labels into integer labels
y_encoded = label_encoder.fit_transform(y)


# Split the balanced data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Initialize the KNN classifier
knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')

# Train the KNN model
knn.fit(X_train, y_train)

# Make predictions
y_pred = knn.predict(X_test)

# Decode the predicted and true labels back to the original string labels
y_test_decoded = label_encoder.inverse_transform(y_test)
y_pred_decoded = label_encoder.inverse_transform(y_pred)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test_decoded, y_pred_decoded))
print("\nConfusion Matrix:\n", confusion_matrix(y_test_decoded, y_pred_decoded))
print("\nClassification Report:\n", classification_report(y_test_decoded, y_pred_decoded))
 """



# Logique de régression
""" 

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
 
""" # Import necessary libraries
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Assuming you already have your data in X (features) and y (labels)
# Example: X = your_features_data, y = your_labels_data

# Split the dataset into training and testing sets (80% train, 20% test)


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


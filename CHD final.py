# -*- coding: utf-8 -*-
"""CHDfinal.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18w0asHOML4s-lJjoWWsy5k2wghxcLty0
"""

# Install imbalanced-learn library
!pip install imblearn

# Import libraries for data manipulation and analysis
import pandas as pd
import numpy as np

# Import libraries for data visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Import libraries for data preprocessing and feature selection
from sklearn.preprocessing import StandardScaler

# Import libraries for machine learning models
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Import libraries for model evaluation
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# Import libraries for handling imbalanced datasets
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from collections import Counter

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score

# Load dataset
df = pd.read_csv("framingham.csv")
df = df.drop(['education'], axis=1)
df = df.drop(['currentSmoker'], axis=1)

# Remove any rows with missing values
df.dropna(axis=0, inplace = True)

# Rename male column to sex
df.rename(columns={"male": "sex"}, inplace=True)

# Display first 5 rows
df.head()

# Seperate features and target variable
X = df.iloc[:, 0:14]
y = df.iloc[:, -1]

# Balance the dataset using SMOTE and RandomUnderSampler
before = dict(Counter(y))

over_sampling = SMOTE(sampling_strategy = 0.7)
under_sampling = RandomUnderSampler(sampling_strategy = 0.7)
steps = [("o",over_sampling),("u",under_sampling)]
pipeline = Pipeline(steps=steps)

X_smote, y_smote = pipeline.fit_resample(X, y)

after = dict(Counter(y_smote))

print(before,after)

# Graph the data before vs after balancing
labels = ["Negative Cases","Positive Cases"]
plt.figure(figsize=(16, 6))
plt.subplot(1, 2, 1)
sns.barplot(x=labels, y=list(before.values()), palette = "mako")
plt.title("Numbers Before Balancing")
plt.subplot(1,2, 2)
sns.barplot(x=labels, y=list(after.values()), palette = "mako")
plt.title("Numbers After Balancing")
plt.show()

# Print neg:pos ratio before vs after
print(f"Ratio before: {round(before[0]/before[1], 2)}")
print(f"Ratio after: {round(after[0]/after[1], 2)}")

# Age distribution graph
plt.figure(figsize=(8, 6))
plt.grid()
plt.plot()
sns.boxplot(x=df['TenYearCHD'], y=df["age"], palette= "mako")
plt.title("Age Distribution by 10 year CHD risk")

# Concatenate features and target variable after balancing
data2 = pd.concat([pd.DataFrame(X_smote), pd.DataFrame(y_smote)], axis =1)
data2 = pd.concat([pd.DataFrame(X_smote), pd.DataFrame(y_smote)], axis =1)
# Drop duplicate 'TenYearCHD' columns
data2 = data2.loc[:,~data2.columns.duplicated()]
# Rename the remaining column to 'TenYearCHD'
data2.rename(columns={'TenYearCHD.1': 'TenYearCHD'}, inplace=True)
data2.col = ['sex','age','cigsPerDay','BPMeds','prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose', 'TenYearCHD']
data2.head()

# Seperate features and target variable
newX = data2.iloc[:, 0:13]
newy = data2.iloc[:, -1]
newy.head()

newX.head()

# Split data into train and test data
Xtrain, Xtest, ytrain, ytest = train_test_split(newX, newy, test_size=0.2, random_state=42)

# Initialize the Standard Scaler
scaler = StandardScaler()

# Scale train and test data
Xtrain_scaled = scaler.fit_transform(Xtrain)
Xtrain = pd.DataFrame(Xtrain_scaled)

Xtest_scaled = scaler.transform(Xtest)
Xtest = pd.DataFrame(Xtest_scaled)

# Define parameters for Logistic Regression model
parameters = {'penalty':['l2'],
              'C':[0.01,0.1,1,10,100],
              'class_weight':['balanced',None]}

# Use GridSearchCV to find the best parameters for Logistic Regression
logisticClassifier = GridSearchCV(LogisticRegression(solver='liblinear'),param_grid=parameters,cv=10)

# Train the Logistic Regression model
logisticClassifier.fit(Xtrain,ytrain)
# Get the best parameters for Logistic Regression
logisticClassifier.best_params_

# Make predictions using Logistic Regression
predictLog = logisticClassifier.predict(Xtest)

# Calculate the accuracy of the Logistic Regression model
accuracyLog= accuracy_score(ytest,predictLog)
print(f"Logistic regression accuracy: {round(accuracyLog*100,2)}%")

# Create a confusion matrix for Logistic Regression
cm = confusion_matrix(ytest, predictLog)
confusionMatrix = pd.DataFrame(data=cm, columns = ['Predicted, Negative', 'Predicted, Positive'], index=['Actual, Negative', 'Actual, Positive'])
plt.figure(figsize = (8,6))
sns.heatmap(confusionMatrix, annot=True, fmt='d', cmap="mako")
plt.title("Logistic Regression Confusion Matrix")
plt.show()

# Print the classification report for Logistic Regression
print(classification_report(ytest, predictLog))

# Calculate the F1 score for Logistic Regression
f1Log = f1_score(ytest, predictLog)
print(f"Logistic Regression F1 Score: {round(f1Log*100,2)}%")

# Define parameters for KNN model
parameters = {'n_neighbors' : np.arange(1, 10)}
# Use GridSearchCV to find the best parameters for KNN
gridSearch = GridSearchCV(estimator = KNeighborsClassifier(), param_grid = parameters, scoring = 'accuracy', cv = 10, n_jobs = -1)
classificationKNN = GridSearchCV(KNeighborsClassifier(),parameters,cv=3, n_jobs=-1)

# Train the KNN model
classificationKNN.fit(Xtrain,ytrain)
# Get the best parameters for KNN
classificationKNN.best_params_

# Make predictions using KNN
predictKNN = classificationKNN.predict(Xtest)

# Calculate the accuracy of the KNN model
accuracyKNN = accuracy_score(ytest,predictKNN)
print(f"K-Nearest neighbour accuracy: {round(accuracyKNN*100,2)}%")

# Create a confusion matrix for KNN
cm = confusion_matrix(ytest, predictKNN)
confusionMatrix = pd.DataFrame(data=cm, columns = ['Predicted, Negative', 'Predicted, Positive'], index=['Actual, Negative', 'Actual, Positive'])
plt.figure(figsize = (8,6))
sns.heatmap(confusionMatrix, annot=True, fmt='d', cmap="mako")
plt.title("K-Nearest Neighbours Confusion Matrix")
plt.show()

# Print the classification report for KNN
print(classification_report(ytest, predictKNN))

# Calculate the F1 score for KNN
f1KNN = f1_score(ytest, predictKNN)
print(f"Logistic Regression F1 Score: {round(f1KNN*100,2)}%")

# Initialize the Decision Tree Classifier
dtree = DecisionTreeClassifier(random_state=42)

# Define parameters for Decision Tree model
parameters = {'max_features': ['auto', 'sqrt', 'log2'],'min_samples_split': [2,3,4,5,6,7,8,9,10,11,12,13,14,15],'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10,11]}
# Use GridSearchCV to find the best parameters for Decision Tree
treeClassifier = GridSearchCV(dtree, param_grid = parameters, n_jobs = -1)

# Train the Decision Tree model
treeClassifier.fit(Xtrain,ytrain)
# Get the best parameters for Decision Tree
treeClassifier.best_params_

# Make predictions using Decision Tree
predictTree = treeClassifier.predict(Xtest)

# Calculate the accuracy of the Decision Tree model
accuracyTree = accuracy_score(ytest,predictTree)
print(f"Decision Tree accuracy: {round(accuracyTree*100,2)}%")

# Create a confusion matrix for Decision Tree
cm = confusion_matrix(ytest, predictTree)
confusionMatrix = pd.DataFrame(data=cm, columns = ['Predicted, Negative', 'Predicted, Positive'], index=['Actual, Negative', 'Actual, Positive'])
plt.figure(figsize = (8,6))
sns.heatmap(confusionMatrix, annot=True, fmt='d', cmap="mako")
plt.title("Decision Tree Confusion Matrix")
plt.show()

# Print the classification report for Decision Tree
print(classification_report(ytest, predictTree))

# Calculate the F1 score for Decision Tree
f1Tree = f1_score(ytest, predictTree)
print(f"Decicion Tree F1 Score: {round(f1Tree*100,2)}%")

# Define parameters for SVM model
C_values = [0.001, 0.01, 0.1, 1, 10]
gamma_values = [0.001, 0.01, 0.1, 1]
parameters = {'C': C_values, 'gamma' : gamma_values}
classifierSVM = GridSearchCV(SVC(kernel='rbf'), param_grid = parameters, n_jobs = -1)

# Use GridSearchCV to find the best parameters for SVM
classifierSVM.fit(Xtrain,ytrain)
# Get the best parameters for SVM
classifierSVM.best_params_

# Make predictions using SVM
predictSVM = classifierSVM.predict(Xtest)

# Calculate the accuracy of the SVM model
accuracySVM = accuracy_score(ytest,predictSVM)
print(f"Support vector machine accuracy: {round(accuracySVM*100,2)}%")

# Create a confusion matrix for SVM
cm = confusion_matrix(ytest, predictSVM)
confusionMatrix = pd.DataFrame(data=cm, columns = ['Predicted, Negative', 'Predicted, Positive'], index=['Actual, Negative', 'Actual, Positive'])
plt.figure(figsize = (8,6))
sns.heatmap(confusionMatrix, annot=True, fmt='d', cmap="mako")
plt.title("Support Vector Machine Confusion Matrix")
plt.show()

# Print the classification report for SVM
print(classification_report(ytest, predictSVM))

# Calculate the F1 score for SVM
f1SVM = f1_score(ytest, predictSVM)
print(f"Support vector machine F1 Score: {round(f1SVM*100,2)}%")

# Define parameters for Random Forest model
parameters = {'n_estimators': [50, 100, 150,], 'max_depth': [None, 12, 24, 36], 'min_samples_split': [2, 5, 8], 'min_samples_leaf': [2, 5, 8], 'max_features': ['auto', 'sqrt',]}
# Initialize the Random Forest Classifier
classifierRF = RandomForestClassifier(random_state = 42)
# Use GridSearchCV to find the best parameters for Random Forest
gridSearch = GridSearchCV(classifierRF, param_grid = parameters, cv = 5, n_jobs = -1)
# Train the Random Forest model
gridSearch.fit(Xtrain, ytrain)

# Get the best parameters for Random Forest
bestParameters = gridSearch.best_params_
# Make predictions using Random Forest
predictRF = gridSearch.predict(Xtest)

# Calculate the accuracy of the Random Forest model
accuracyRF = accuracy_score(ytest,predictRF)
print(f"Random Forest accuracy: {round(accuracyRF*100,2)}%")

# Create a confusion matrix for Random Forest
cm = confusion_matrix(ytest, predictRF)
confusionMatrix = pd.DataFrame(data=cm, columns = ['Predicted, Negative', 'Predicted, Positive'], index=['Actual, Negative', 'Actual, Positive'])
plt.figure(figsize = (8,6))
sns.heatmap(confusionMatrix, annot=True, fmt='d', cmap="mako")
plt.title("Random Forest Confusion Matrix")
plt.show()

# Print the classification report for Random Forest
print(classification_report(ytest, predictRF))

# Calculate the F1 score for Random Forest
f1RF = f1_score(ytest, predictRF)
print(f"Random Forest F1 Score: {round(f1RF*100,2)}%")

# Create a DataFrame to store the results
Results = pd.DataFrame({
    "Logistic regression":{'Accuracy':accuracyLog, 'F1 score':f1Log},
    "K-nearest neighbours":{'Accuracy':accuracyKNN, 'F1 score':f1KNN},
    "Decision trees":{'Accuracy':accuracyTree, 'F1 score':f1Tree},
    "Support vector machine":{'Accuracy':accuracySVM, 'F1 score':f1SVM},
    "Random Forest Classifier":{'Accuracy':accuracyRF, 'F1 score':f1RF},
}).T.reset_index()

Results.columns = ['Models', 'Accuracy', 'F1 score']

# Create a figure for the results
results_figure = plt.gcf()
results_figure.set_size_inches(26, 10)
titles = ['Accuracy', 'F1 score']
# Iterate over the metrics
for i, metric in enumerate(['Accuracy', 'F1 score']):
    # Create a subplot for each metric
    plt.subplot(1, 2, i+1)
    ax = sns.barplot(x='Models', y=metric, data=Results, palette="mako")
    plt.title(titles[i])
    # Annotate the bars with the values
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.3f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')


plt.show()

# Select features for importance analysis
X_selected = newX

# Check correlation with the target variable
correlation = X_selected.corrwith(newy)
print("\nCorrelation with target variable:")
print(correlation.sort_values(ascending=False))

# Train the Random Forest model with selected features
from sklearn.ensemble import RandomForestClassifier
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_selected, newy)

# Calculate feature importance
feature_importance = pd.DataFrame({
    'Feature': X_selected.columns,
    'Importance': rf_model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance)

# Visualize feature importance
plt.figure(figsize=(12, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance, palette="mako")
plt.title('Random Forest Feature Importance for CHD Prediction')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.tight_layout()
plt.show()
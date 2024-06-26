
# Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import xgboost as Xgb

# Load data
tf = pd.read_csv('Overview.csv')
cv = pd.read_csv('CurrentVoltage.csv')

# Preprocess data
tf['DeviceTimeStamp'] = pd.to_datetime(tf['DeviceTimeStamp'], format='%Y-%m-%d %H:%M:%S')
cv['DeviceTimeStamp'] = pd.to_datetime(cv['DeviceTimeStamp'], format='%Y-%m-%d %H:%M:%S')

transformer = pd.merge(tf, cv, on='DeviceTimeStamp')

# Data visualization (you can keep or remove these based on your preference)

# Define X and y
X = transformer.drop(['DeviceTimeStamp','MOG_A'],axis=1)
y = transformer['MOG_A']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=21)

# Normalize the data
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model training and evaluation
models = {
    'Logistic Regression': LogisticRegression(),
    'Support Vector Machines': SVC(),
    'KNN': KNeighborsClassifier(n_neighbors=3),
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(n_estimators=100),
    'Extra Trees': ExtraTreesClassifier(n_estimators=100),
    'AdaBoost': AdaBoostClassifier(),
    'XGBoost': Xgb.XGBClassifier()
}

results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    train_accuracy = round(model.score(X_train, y_train) * 100, 2)
    test_accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)
    results.append({'Model': name, 'Training Accuracy': train_accuracy, 'Model Accuracy Score': test_accuracy})

# Model comparison
results_df = pd.DataFrame(results)

# Fine-tuning with GridSearchCV (example for SVM)
svm_parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
svm_model = SVC()
svm_grid_search = GridSearchCV(svm_model, svm_parameters)
svm_grid_search.fit(X_train, y_train)
svm_best_params = svm_grid_search.best_params_

# Evaluating the tuned model
y_pred = svm_grid_search.best_estimator_.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')
recall = recall_score(y_test, y_pred, average='macro')
f1 = f1_score(y_test, y_pred, average='macro')

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

# You can add more fine-tuning for other models if needed

# Visualize results
results_df_sorted = results_df.sort_values(by='Model Accuracy Score', ascending=False)
sns.barplot(y='Model', x='Model Accuracy Score', data=results_df_sorted)
plt.title('COMPARE THE MODEL')
plt.xlabel('Model Accuracy Score')
plt.ylabel('Model')
plt.show()




# Load Voltage Data
voltage = pd.read_csv('CurrentVoltage.csv')

# Preprocess data if necessary

# Define Outcome Variable
threshold_voltage = 240  # Define the threshold voltage
voltage['Alert'] = (voltage['Voltage'] > threshold_voltage).astype(int)

# Split data into training and testing sets
X_voltage = voltage.drop(['DeviceTimeStamp', 'Voltage', 'Alert'], axis=1)
y_voltage = voltage['Alert']
X_train_voltage, X_test_voltage, y_train_voltage, y_test_voltage = train_test_split(X_voltage, y_voltage, test_size=0.20, random_state=21)

# Normalize the data if required
# scaler_voltage = MinMaxScaler()
# X_train_voltage = scaler_voltage.fit_transform(X_train_voltage)
# X_test_voltage = scaler_voltage.transform(X_test_voltage)

# Model training and evaluation
results_voltage = []

for name, model in models.items():
    model.fit(X_train_voltage, y_train_voltage)
    y_pred_voltage = model.predict(X_test_voltage)
    train_accuracy_voltage = round(model.score(X_train_voltage, y_train_voltage) * 100, 2)
    test_accuracy_voltage = round(accuracy_score(y_test_voltage, y_pred_voltage) * 100, 2)
    results_voltage.append({'Model': name, 'Training Accuracy': train_accuracy_voltage, 'Model Accuracy Score': test_accuracy_voltage})

# Model comparison
results_df_voltage = pd.DataFrame(results_voltage)

# Fine-tuning with GridSearchCV (example for SVM)
svm_parameters_voltage = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
svm_model_voltage = SVC()
svm_grid_search_voltage = GridSearchCV(svm_model_voltage, svm_parameters_voltage)
svm_grid_search_voltage.fit(X_train_voltage, y_train_voltage)
svm_best_params_voltage = svm_grid_search_voltage.best_params_

# Evaluating the tuned model
y_pred_voltage = svm_grid_search_voltage.best_estimator_.predict(X_test_voltage)
accuracy_voltage = accuracy_score(y_test_voltage, y_pred_voltage)

# Check if the predicted voltage exceeds the normal range and display an alert message
if y_pred_voltage == 1:
    print("Alert: Voltage exceeds the normal range!")



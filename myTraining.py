import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle
import os

def data_split(data, ratio):
    np.random.seed(42)
    shuffled = np.random.permutation(len(data))
    test_set_size = int(len(data) * ratio)
    test_indices = shuffled[:test_set_size]
    train_indices = shuffled[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

if __name__ == "__main__":
    try:
        # Read the data
        if not os.path.exists('data.csv'):
            raise FileNotFoundError("data.csv file not found")
            
        df = pd.read_csv('data.csv')
        
        # Verify required columns exist
        required_columns = ['fever', 'bodyPain', 'age', 'runnyNose', 'diffBreath', 'infectionProb']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        # Split the data
        train, test = data_split(df, 0.2)
        
        # Prepare features
        feature_columns = ['fever', 'bodyPain', 'age', 'runnyNose', 'diffBreath']
        X_train = train[feature_columns].to_numpy()
        X_test = test[feature_columns].to_numpy()
        
        # Prepare target
        Y_train = train['infectionProb'].to_numpy()
        Y_test = test['infectionProb'].to_numpy()
        
        # Train the model
        clf = LogisticRegression(random_state=42)
        clf.fit(X_train, Y_train)
        
        # Evaluate the model
        train_score = clf.score(X_train, Y_train)
        test_score = clf.score(X_test, Y_test)
        print(f"Training accuracy: {train_score:.2f}")
        print(f"Testing accuracy: {test_score:.2f}")
        
        # Save the model
        with open('model.pkl', 'wb') as file:
            pickle.dump(clf, file)
        print("Model saved successfully as model.pkl")
        
    except Exception as e:
        print(f"Error during model training: {str(e)}")
        raise





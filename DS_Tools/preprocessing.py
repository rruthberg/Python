#Data preprocessing template
import numpy as np
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler

def data_preprocess(filepath):
    try:
        print(">>>Initiating preprocessing.")
        #Read data
        dataset = pd.read_csv(filepath, y_col, impute_cols,mval="NaN",istrat="mean", cat_cols=[0,1], cat_y=False, tsize=0.2, rstate=0, fscaling=False)
        y = dataset.iloc[:, y_col]
        x_dataset = dataset.drop([y_col])
        X = x_dataset.values
        print(">>>Data read successfully.")

        #Solve for missing data
        if impute_cols:
            imputer = Imputer(missing_values=mval, strategy=istrat, axis=0)
            imputer = imputer.fit(X[:, impute_cols[0]:impute_cols[1]])
            X[:, impute_cols[0]:impute_cols[1]] = imputer.transform(X[:, impute_cols[0]:impute_cols[1]])
            print(">>>Initiating preprocessing.")

        #Encode categorical data
        if cat_cols:
            labelenc_X = LabelEncoder()
            X[:, cat_cols[0]:cat_cols[1]] = labelenc_X.fit_transform(X[:, cat_cols[0]:cat_cols[1]])
            onehotenc = OneHotEncoder(categorical_features = [cat_cols[0]:cat_cols[1]])
            X = onehotenc.fit_transform(X).toarray()
            print(">>>Encoding independent variables.")
            if cat_y:
                labelenc_y = LabelEncoder()
                y = labelenc_y.fit_transform(y)
                print(">>>Encoding dependent variable.")

        #Split data into train and test sets
        print(">>>Splitting data into train and test set.")
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=tsize, random_state=rstate)

        #Feature scaling 
        if fscaling:
            sc_X = StandardScaler()
            X_train = sc_X.fit_transform(X_train)
            X_test = sc_X.transform(X_test)
            print(">>>Scaling features.")

        return X_train, X_test, y_train, y_test
    except:
        print("Something went wrong.")

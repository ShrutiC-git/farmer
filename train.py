import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn import preprocessing
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split
import json
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer

df = pd.read_csv("data_processed.csv")

#### Get features ready to model!
y = df.pop("cons_general").to_numpy()
y[y< 5] = 0
y[y>= 5] = 1

X = df.to_numpy()
X = preprocessing.scale(X) # Is standard
# Impute NaNs

imp = SimpleImputer(missing_values=np.nan, strategy='mean')
imp.fit(X)
X = imp.transform(X)


# Linear model
clf = QuadraticDiscriminantAnalysis()
yhat = cross_val_predict(clf, X, y, cv=6)

acc = np.mean(yhat==y)
tn, fp, fn, tp = confusion_matrix(y, yhat).ravel()
specificity = tn / (tn+fp)
sensitivity = tp / (tp + fn)

#Print to console
print('Metrics: ', acc," ", specificity," ", sensitivity)

# Now print to file
with open("metrics.json", 'w') as outfile:
        json.dump({ "accuracy": acc, "specificity": specificity, "sensitivity":sensitivity}, outfile)

# Let's visualize within several slices of the dataset
score = yhat == y
score_int = [int(s) for s in score]
df['pred_accuracy'] = score_int
print('X: ',df['region'],'score_int: ',score_int, 'y: ', y)

# Bar plot by region

sns.set_color_codes("dark")
ax = sns.barplot(x="region", y="pred_accuracy", data=df, palette = "Greens_d")
ax.set(xlabel="Region", ylabel = "Model accuracy")
plt.savefig("by_region.png",dpi=80)

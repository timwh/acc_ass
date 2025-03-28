"""
conf_matrix.py - Script to create and print a confusion matrix with accuracies and Kappa
Author: Tim Whiteside
Requires: geopandas,matplotlib, numpy, scikit-learn

"""

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, cohen_kappa_score, ConfusionMatrixDisplay

# Read classified shapefile with reference data
class_gdf = gpd.read_file("your/path/points_with_class.shp")
points_gdf = class_gdf[['ref_num','Class_name']]

# Drop points with no dat in either field
points_gdf = points_gdf.dropna(subset=["ref_num"])
points_gdf = points_gdf.dropna(subset=["Class_name"])

# Assign a number to each class (match reference numbers)
class_mapping = {
    "Class1":1,
    "Class2":2,
    "Class3":3,
    "Class4":4
}
points_gdf["class_num"] = points_gdf["Class_name"].map(class_mapping)
points_gdf["ref_num"] = points_gdf["ref_num"].astype(int) # sets as integer in case its not

# Check reference versus class
points_gdf.describe()

# Reference and classified data
ref = points_gdf["ref_num"] # Observed reference class
classified = points_gdf["class_num"] # Class from analysis

# Create confusion matrix
clabels = [1,2,3,4] #Class numbers
cm = confusion_matrix(ref,classified, labels=clabels)
# Compute overall accuracy
accuracy = accuracy_score(ref,classified)
# Compute Cohen's kappa
kappa = cohen_kappa_score(ref,classified)

# Compute User's and Producer's Accuracy for each class
user_accuracy = np.diag(cm) / cm.sum(axis=0, where=(cm.sum(axis=0) != 0))  # Precision/FP/errors of commission/Type 1 error
producer_accuracy = np.diag(cm) / cm.sum(axis=1, where=(cm.sum(axis=1) != 0))  # Recall/FN/errors of omission/Type 2 error

# Compute row (actual total) and column (predicted total) sums
row_totals = np.sum(cm, axis=1)
col_totals = np.sum(cm, axis=0)

# Create class labels dynamically
num_classes = cm.shape[0]
labels = [f"Class {i+1}" for i in range(num_classes)]

# Format matrix with accuracy values
cm_with_acc = cm.astype(str)
for i in range(num_classes):
    cm_with_acc[i, -1] = f"{producer_accuracy[i]:.2f}"  # Producer's Accuracy
    cm_with_acc[-1, i] = f"{user_accuracy[i]:.2f}"  # User's Accuracy

# Add row and column labels for "Producer’s Accuracy" and "User’s Accuracy"
cm_with_acc = np.vstack([cm_with_acc, np.round(user_accuracy, 2)])
cm_with_acc = np.column_stack([cm_with_acc, np.append(producer_accuracy, np.nan)])

# Calculate overall accuracy
total = np.sum(cm) # total number of samples
diag = np.diag(cm) # true positives along the diagonal
sum_diag = np.sum(diag) # some of true positives
OA = sum_diag/total*100 # Overall accuracy as a %
print(f"Overall accuracy is {OA:.2f}%")

# Display Confusion Matrix with Accuracies
fig, ax = plt.subplots(figsize=(6,5))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot(ax=ax, cmap="Blues", values_format='d')

# Move X-axis labels to the top
ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()

# Add User's and Producer's Accuracy to the plot
for i in range(num_classes):
    ax.text(num_classes, i, f"{row_totals[i]}", va='center', ha='center', fontsize=10, color="black")  # Row Totals
    ax.text(num_classes + 1, i, f"{producer_accuracy[i]*100:.1f}%", va='center', ha='right', fontsize=10, color="darkblue")
    ax.text(i, num_classes, f"{col_totals[i]}", ha='center', va='center', fontsize=10, color="black")  # Column Totals
    ax.text(i, num_classes + 1, f"{user_accuracy[i]*100:.1f}%\n", va='bottom', ha='center', fontsize=10, color="darkblue")
# Add the overall total of samples in the bottom-right cell
ax.text(num_classes, num_classes, f"{np.sum(row_totals)}", ha='center', va='center', fontsize=10, color="black")

# Title and labels
ax.set_title(f"Confusion Matrix for {billabong} billabong {platform} classification\nOverall Accuracy: {accuracy*100:.1f}%\nKappa: {kappa:.2f}\n", fontsize=14)

ax.set_xlabel("Classified", fontsize=12)
ax.set_ylabel("Reference", fontsize=12)

# Adjust x-axis to fit User's Accuracy
ax.set_xticks(np.arange(num_classes + 2))
ax.set_yticks(np.arange(num_classes + 2))
labels_with_acc = labels + ["Sum","Producer Acc."]
ax.set_xticklabels(labels_with_acc, rotation=45, ha="center",fontsize=9)
labels_with_acc = labels + ["Sum","User Acc."]
ax.set_yticklabels(labels_with_acc, rotation=45,va="center",fontsize=9)

plt.show()

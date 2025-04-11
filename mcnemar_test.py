"""
mcnemars_test.py - Comparing the difference between two classifications
of the same area based on a sin=gle set of reference data.
Author: Tim Whiteside
Requires: geopandas, pandas, numpy, statsmodels
"""
import geopandas as gpd
import numpy as np
from statsmodels.stats.contingency_tables import mcnemar

# Reference data set
ref_pts = gpd.read_file("your/reference.shp")
# Select required columns
ref_pts_select = ref_pts[["ref_num","geometry"]]

# First classified data set
class1 = "your/first/classified/dataset.shp"
class1_polys = gpd.read_file(class1)

# Second classified data set
class2 = "your/second/classified/dataset.shp"
class2_polys = gpd.read_file(class2)

# Link classified datasets to reference
# Classified 1
# Select Class_name columns from classification shapefile
columns_selected = class1_polys[['Class_name', 'geometry']]
# Perform spatial join: assigns polygon class to points
points_with_class = gpd.sjoin(ref_pts_select, columns_selected, how="left", predicate="within")
#points_with_class = gpd.sjoin(ref_pts, class_polys, how="left", predicate="intersects")

# Assign a number to each class, change Class1 etc. to your class names.
class_mapping = {
    "Class1":1,
    "Class2":2,
    "Class3":3,
    "Class4":4
}
points_with_class["class1_num"] = points_with_class["Class_name"].map(class_mapping)
points_with_class["ref_num"] = points_with_class["ref_num"].astype(int) #sets as integer in case its not

# Select only relevent columns with reference and Classified 1
ref_pts_w_d = points_with_class[["ref_num","class1_num","geometry"]]

# Classified 2
# Select Class_name columns from classification shapefile
columns_selected2 = class2_polys[['Class_name', 'geometry']]

# Perform spatial join: assigns polygon class to points
points_with_class2 = gpd.sjoin(ref_pts_w_d, columns_selected2, how="left", predicate="within")
points_with_class2["class2_num"] = points_with_class2["Class_name"].map(class_mapping)

# Select only relevent columns with reference, Classified 1 and Classified 2
ref_pts_w_class = points_with_class2[["ref_num","class1_num","class2_num","geometry"]]

# Data check
ref_pts_w_class.describe()

# Build contingency table
# [ [both correct, A correct B wrong],
#   [A wrong B correct, both wrong] ]
y_true = ref_pts_w_class["ref_num"]
y_pred1 = ref_pts_w_class["class1_num"]
y_pred2 = ref_pts_w_class["class2_num"]

table = [[0, 0], [0, 0]]
for yt, yp1, yp2 in zip(y_true, y_pred1, y_pred2):
    correct1 = (yt == yp1)
    correct2 = (yt == yp2)

    if correct1 and correct2:
        table[0][0] += 1
    elif correct1 and not correct2:
        table[0][1] += 1
    elif not correct1 and correct2:
        table[1][0] += 1
    else:
        table[1][1] += 1

# Run McNemar's test
result = mcnemar(table, exact=True)  # Use exact or chi2

# Output result
print("Contingency Table:")
print(np.array(table))
print(f"statistic: {result.statistic:.4f}, p-value: {result.pvalue:.4f}")

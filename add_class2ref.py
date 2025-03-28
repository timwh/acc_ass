"""
add_class2ref.py - Script to join classes from classified ploygons to reference points
Author: Tim Whiteside
Requires: geopandas
"""

import geopandas as gpd
import os

# Load classification shapefile (must incl. field "Class_name")
class_shp = "your/path/classified_polygons.shp"
class_polys = gpd.read_file(class_shp)

# Load reference points
ref_pts = gpd.read_file("your/path/stratified_random_points.shp")

# Ensure matching CRSs
if ref_pts.crs != class_polys.crs:
    ref_pts = ref_pts.to_crs(class_polys.crs)

# Select Class_name columns from classification shapefile
columns_selected = class_polys[['Class_name', 'geometry']]

# Check class list
list = columns_selected['Class_name'].unique()
print(f"Classes present in Class_name: {list}")

# Perform spatial join: assigns polygon class to points
points_with_class = gpd.sjoin(ref_pts, columns_selected, how="left", predicate="within")

# Save the output to shapefile
points_with_class.to_file("your/path/ref_pts_with_class.shp")


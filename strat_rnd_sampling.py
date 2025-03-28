"""
strat_rnd_sampling.py - Script to generate stratified random sampling points based on class area
Author: Tim Whiteside
Requires: geopandas, pandas, matplotlib, seaborn, numpy, shapely, random
"""

### Packages
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from shapely.geometry import Point
import random
import os

# Shapefile path - Shape file require filed 'Class_name'
shpfile = "your/path/shapefile.shp"

# Parse the name for output filename
fname, ext = os.path.splitext(shpfile)

# Read in the classified shapefile
gdf = gpd.read_file(shpfile)

# Check classes in file
print(gdf['Class_name'].unique())

# Set total number of samples
tot_samples = 255

# Calculate area of polygons in gdf
gdf['area'] = gdf.geometry.area

# Calculate area for each class - when area per polygon already available as a column
class_area = gdf.groupby('Class_name')[area'].sum().reset_index()
# Get number of samples per class based on area
class_area["samples"] = (class_area['area'] / class_area['area'].sum() * tot_samples).round().astype(int)
print(class_area)

# Create empty set to store sample points
sample_points = []

# Generate random points for each class
for _, row in class_area.iterrows():
    land_type = row["Class_name"]
    num_points = row["samples"]
    
    # Filter polygons of this class
    class_polygons = gdf[gdf["Class_name"] == land_type]
    
    # Distribute points among polygons
    for _, poly_row in class_polygons.iterrows():
        poly_area = poly_row["area"]
        proportion = poly_area / class_polygons["area"].sum()
        points_needed = int(proportion * num_points)
        
        # Generate random points within the polygon
        points = generate_random_points(poly_row.geometry, points_needed)
        
        # Store points with class label
        sample_points.extend([(point, land_type) for point in points])

# Convert to GeoDataFrame
sample_gdf = gpd.GeoDataFrame(sample_points, columns=["geometry", "Class_name"], crs=gdf.crs)
# Add an empty colum for reference data
sample_gdf["ref_num"] = None

# Save sampled points to a new shapefile
# Save to a new shapefile
out_points = f"{fname}_strat_rnd_pts{ext}"
sample_gdf.to_file(out_points)

print("Stratified random sampling complete!")


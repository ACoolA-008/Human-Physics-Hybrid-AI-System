import numpy as np
import json

points = np.load('mrms_point_cloud.npy')  # shape: (N, 4)
max_points = 5000
if points.shape[0] > max_points:
    idx = np.random.choice(points.shape[0], max_points, replace=False)
    points = points[idx]

point_list = [{"x": float(x), "y": float(y), "z": float(z), "reflectivity": float(r)} for x, y, z, r in points]
with open("mrms_point_cloud.json", "w") as f:
    json.dump(point_list, f)
print(f"Exported {len(point_list)} points to mrms_point_cloud.json") 
#!/usr/bin/env python3
"""
Script to view NowcastNet results
"""

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from pathlib import Path

def view_results(result_dir="results/us/test_result/0", num_frames=5):
    """
    View predicted vs ground truth frames side by side
    
    Args:
        result_dir: Path to the results directory
        num_frames: Number of frames to display
    """
    
    # Get all predicted and ground truth files
    pred_files = sorted([f for f in os.listdir(result_dir) if f.startswith('pd')])
    gt_files = sorted([f for f in os.listdir(result_dir) if f.startswith('gt')])
    
    # Take the last few frames for comparison
    pred_files = pred_files[-num_frames:]
    gt_files = gt_files[-num_frames:]
    
    # Create subplots
    fig, axes = plt.subplots(2, num_frames, figsize=(3*num_frames, 6))
    fig.suptitle('NowcastNet Results: Predicted vs Ground Truth', fontsize=16)
    
    for i, (pred_file, gt_file) in enumerate(zip(pred_files, gt_files)):
        # Load images
        pred_img = mpimg.imread(os.path.join(result_dir, pred_file))
        gt_img = mpimg.imread(os.path.join(result_dir, gt_file))
        
        # Display predicted frame
        axes[0, i].imshow(pred_img, cmap='viridis')
        axes[0, i].set_title(f'Predicted {pred_file[2:-4]}')
        axes[0, i].axis('off')
        
        # Display ground truth frame
        axes[1, i].imshow(gt_img, cmap='viridis')
        axes[1, i].set_title(f'Ground Truth {gt_file[2:-4]}')
        axes[1, i].axis('off')
    
    plt.tight_layout()
    plt.show()

def list_available_results():
    """List all available result directories"""
    results_dir = Path("results")
    
    if not results_dir.exists():
        print("No results directory found!")
        return
    
    print("Available result directories:")
    for item in results_dir.iterdir():
        if item.is_dir():
            print(f"  - {item}")
            # Check for test_result subdirectories
            test_results = item / "test_result"
            if test_results.exists():
                for test_dir in test_results.iterdir():
                    if test_dir.is_dir():
                        print(f"    └── {test_dir.name}")

if __name__ == "__main__":
    print("NowcastNet Results Viewer")
    print("=" * 30)
    
    list_available_results()
    print("\nTo view results, run:")
    print("python view_results.py")
    print("\nOr modify the script to view specific directories.") 
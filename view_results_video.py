#!/usr/bin/env python3
"""
Script to view NowcastNet results as an animated video
"""

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
import numpy as np
from pathlib import Path
import cv2

def create_video_viewer(result_dir="results/us/test_result/0", fps=2):
    """
    Create an interactive video viewer for NowcastNet results
    
    Args:
        result_dir: Path to the results directory
        fps: Frames per second for playback
    """
    
    # Get all predicted and ground truth files
    pred_files = sorted([f for f in os.listdir(result_dir) if f.startswith('pd')])
    gt_files = sorted([f for f in os.listdir(result_dir) if f.startswith('gt')])
    
    if not pred_files or not gt_files:
        print(f"No result files found in {result_dir}")
        return
    
    # Load all images
    print("Loading images...")
    pred_images = []
    gt_images = []
    
    for pred_file, gt_file in zip(pred_files, gt_files):
        pred_img = mpimg.imread(os.path.join(result_dir, pred_file))
        gt_img = mpimg.imread(os.path.join(result_dir, gt_file))
        pred_images.append(pred_img)
        gt_images.append(gt_img)
    
    # Create the figure and subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle('NowcastNet Results: Predicted vs Ground Truth Animation', fontsize=16)
    
    # Initialize plots
    pred_plot = ax1.imshow(pred_images[0], cmap='viridis')
    gt_plot = ax2.imshow(gt_images[0], cmap='viridis')
    
    ax1.set_title(f'Predicted Frame 0')
    ax2.set_title(f'Ground Truth Frame 0')
    ax1.axis('off')
    ax2.axis('off')
    
    # Add colorbars
    plt.colorbar(pred_plot, ax=ax1, fraction=0.046, pad=0.04)
    plt.colorbar(gt_plot, ax=ax2, fraction=0.046, pad=0.04)
    
    # Animation variables
    current_frame = 0
    is_playing = False
    total_frames = len(pred_images)
    
    def update_frame(frame_num):
        """Update the displayed frames"""
        nonlocal current_frame
        current_frame = frame_num
        
        pred_plot.set_array(pred_images[frame_num])
        gt_plot.set_array(gt_images[frame_num])
        
        ax1.set_title(f'Predicted Frame {frame_num}')
        ax2.set_title(f'Ground Truth Frame {frame_num}')
        
        return pred_plot, gt_plot
    
    def animate():
        """Animation function"""
        nonlocal current_frame, is_playing
        
        if is_playing:
            current_frame = (current_frame + 1) % total_frames
            update_frame(current_frame)
            slider.set_val(current_frame)
            plt.pause(1/fps)
            if is_playing:
                plt.gcf().canvas.draw()
                animate()
    
    def on_slider_change(val):
        """Handle slider changes"""
        nonlocal current_frame
        current_frame = int(val)
        update_frame(current_frame)
        plt.draw()
    
    def toggle_play(event):
        """Toggle play/pause"""
        nonlocal is_playing
        is_playing = not is_playing
        if is_playing:
            play_button.label.set_text('Pause')
            animate()
        else:
            play_button.label.set_text('Play')
        plt.draw()
    
    def reset_animation(event):
        """Reset to first frame"""
        nonlocal current_frame, is_playing
        is_playing = False
        current_frame = 0
        play_button.label.set_text('Play')
        slider.set_val(0)
        update_frame(0)
        plt.draw()
    
    # Add slider for frame control
    ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
    slider = Slider(ax_slider, 'Frame', 0, total_frames-1, valinit=0, valstep=1)
    slider.on_changed(on_slider_change)
    
    # Add control buttons
    ax_play = plt.axes([0.1, 0.02, 0.08, 0.03])
    play_button = Button(ax_play, 'Play')
    play_button.on_clicked(toggle_play)
    
    ax_reset = plt.axes([0.85, 0.02, 0.08, 0.03])
    reset_button = Button(ax_reset, 'Reset')
    reset_button.on_clicked(reset_animation)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    plt.show()

def create_side_by_side_video(result_dir="results/us/test_result/0", output_file="nowcastnet_results.mp4", fps=2):
    """
    Create a video file showing predicted vs ground truth side by side
    
    Args:
        result_dir: Path to the results directory
        output_file: Output video filename
        fps: Frames per second
    """
    
    # Get all predicted and ground truth files
    pred_files = sorted([f for f in os.listdir(result_dir) if f.startswith('pd')])
    gt_files = sorted([f for f in os.listdir(result_dir) if f.startswith('gt')])
    
    if not pred_files or not gt_files:
        print(f"No result files found in {result_dir}")
        return
    
    # Load first image to get dimensions
    first_pred = cv2.imread(os.path.join(result_dir, pred_files[0]))
    first_gt = cv2.imread(os.path.join(result_dir, gt_files[0]))
    
    # Create side-by-side frame
    combined_width = first_pred.shape[1] * 2
    combined_height = first_pred.shape[0]
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (combined_width, combined_height))
    
    print(f"Creating video: {output_file}")
    
    for i, (pred_file, gt_file) in enumerate(zip(pred_files, gt_files)):
        # Load images
        pred_img = cv2.imread(os.path.join(result_dir, pred_file))
        gt_img = cv2.imread(os.path.join(result_dir, gt_file))
        
        # Create side-by-side frame
        combined_frame = np.hstack([pred_img, gt_img])
        
        # Add text labels
        cv2.putText(combined_frame, f'Predicted Frame {i}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(combined_frame, f'Ground Truth Frame {i}', (pred_img.shape[1] + 10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        out.write(combined_frame)
        print(f"Processed frame {i+1}/{len(pred_files)}")
    
    out.release()
    print(f"Video saved as: {output_file}")

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
    print("NowcastNet Video Results Viewer")
    print("=" * 35)
    
    list_available_results()
    print("\nOptions:")
    print("1. Interactive viewer: create_video_viewer()")
    print("2. Create video file: create_side_by_side_video()")
    print("\nExample usage:")
    print("create_video_viewer('results/us/test_result/0', fps=3)")
    print("create_side_by_side_video('results/us/test_result/0', 'results.mp4', fps=3)") 
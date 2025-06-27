# Human-Physics Hybrid AI System for Precipitation Nowcasting

## Overview
This project is a Human-Physics Hybrid AI System for precipitation nowcasting, featuring a modern 3D annotation tool and seamless ML integration. The system enables human-in-the-loop annotation, validation, and correction of AI predictions, bridging the gap between data-driven and physics-based approaches.

## Features
- **3D Point Cloud Visualization**: Interactive, high-performance viewer for MRMS precipitation data.
- **Direct 3D Annotation**: Click and drag to draw bounding boxes, label features, and manage annotations.
- **Flexible UI**: Resizable, modern tool panel and always-visible map for spatial context.
- **Annotation Management**: Add, edit, delete, search, import/export, and bulk operations.
- **Human-in-the-loop ML**: Annotations feed directly into the AI pipeline for training and validation.
- **Server-Side Saving**: Annotations are saved to a dedicated directory for reproducibility.
- **Easy Setup**: Minimal dependencies, simple Python server, and clear instructions.

## Demo
![Annotation Tool New UI](media/annotation_tool_new.png)

## Quick Start
1. **Clone this repo & install requirements**
   ```bash
   pip install -r code/requirements.txt
   ```
2. **Export point cloud data (if needed)**
   ```bash
   python3 export_point_cloud_json.py
   ```
3. **Start the annotation server**
   ```bash
   python3 annotation_server.py
   ```
4. **Open the tool in your browser**
   [http://localhost:8000/viewer.html](http://localhost:8000/viewer.html)
5. **Annotate**
   - Click and drag in the 3D view to draw bounding boxes.
   - Use the right panel to manage, search, and export annotations.
   - Adjust point size and opacity in real time.
6. **Save/Export**
   - Click "Export JSON" to save annotations to the `annotations/` directory.

## How It Works
- The annotation tool allows meteorologists and researchers to mark features in 3D radar data.
- Annotations are saved as JSON and can be converted to masks for ML training.
- The ML pipeline (NowcastNet) uses these masks for supervised learning and evaluation.
- Results can be visualized and compared with human annotations for iterative improvement.

## Example Results
![Comparison Example](media/comparison.png)

## Technical Report
For a deeper dive into the design and workflow, see [docs/technical_report.md](docs/technical_report.md)

## Large Files
Due to GitHub's 100MB limit, download these files separately:
- **Model Checkpoint**: Place in `data/checkpoints/mrms_model.ckpt`
- **Point Cloud Data**: Place in `mrms_point_cloud.npy`

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

If you have questions, ideas, or want to collaborate, don't hesitate to reach out. I hope this project inspires you to blend human insight with AI in your own work!

---
MIT License 

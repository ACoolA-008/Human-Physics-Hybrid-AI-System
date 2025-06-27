# Human-Physics Hybrid AI System for Precipitation Nowcasting

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview
A next-generation, human-in-the-loop AI system for precipitation nowcasting. This project combines a modern 3D annotation tool, seamless ML integration, and a feedback-driven workflow to bridge the gap between human expertise and neural network predictions.

---

## Features
- **3D Point Cloud Visualization**: Explore and annotate radar data in a true 3D environment.
- **Direct 3D Annotation**: Click and drag to draw bounding boxes, label features, and manage annotations.
- **Flexible, Modern UI**: Resizable tool panel, always-visible map, and responsive layout.
- **Annotation Management**: Add, edit, delete, search, import/export, and bulk operations.
- **Human-in-the-loop ML**: Annotations feed directly into the AI pipeline for training and validation.
- **Server-Side Saving**: Annotations are saved to a dedicated directory for reproducibility.
- **Easy Setup**: Minimal dependencies, simple Python server, and clear instructions.

---

## System Architecture

```mermaid
flowchart TD
    A[Data Input] --> B[NowcastNet Inference]
    B --> C[Confidence Check]
    C -- ">= threshold" --> D[Auto-Labeled Data]
    C -- "< threshold" --> E[Human Review Module]
    D --> F[Auto-Labeled Predictions DB]
    E --> G[Human-Labeled Predictions DB]
    F --> H[Retraining Pipeline]
    G --> H
    H -- "Retrain Model" --> B

    %% Human-in-the-loop annotation branch
    E -.-> I[3D Annotation Tool]
    I -- "Export JSON" --> J[Annotation JSON]
    J -- "Convert to Mask" --> K[Mask Generation Script]
    K -- "Mask PNG" --> B

    L[Raw Radar Data (PNG)] -.-> B
```

---

## Demo
![Annotation Tool New UI](media/annotation_tool_new.png)

*Want to add a GIF? Use a screen recorder and [ezgif.com](https://ezgif.com/video-to-gif) to create a GIF, then place it in `media/` and reference it here!*

---

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

---

## Example Usage
- **Convert annotations to masks:**
  ```bash
  python3 convert_annotations_to_masks.py --json annotations/your_annotations.json --output_dir data/dataset/mrms/annotation_masks
  ```
- **Run the ML pipeline:**
  ```bash
  cd code
  python3 run.py --worker 1 --device cpu:0 --cpu_worker 1 --dataset_name radar --dataset_path ../data/dataset/mrms/figure --pretrained_model ../data/checkpoints/mrms_model.ckpt --gen_frm_dir ../results/us/ --num_save_samples 10 --model_name NowcastNet --annotation_mask_path ../data/dataset/mrms/annotation_masks
  ```
- **Visualize results:**
  Check the results folder for side-by-side comparisons of ground truth, predictions, and your annotation masks.

---

## How It Works
- The annotation tool allows meteorologists and researchers to mark features in 3D radar data.
- Annotations are saved as JSON and can be converted to masks for ML training.
- The ML pipeline (NowcastNet) uses these masks for supervised learning and evaluation.
- Results can be visualized and compared with human annotations for iterative improvement.

---

## Example Results
![Comparison Example](media/comparison.png)

---

## Technical Report
A brief technical report explaining the design, workflow, and key decisions is available at:
- [docs/technical_report.md](docs/technical_report.md)

---

## Large Files
Due to GitHub's 100MB limit, download these files separately:
- **Model Checkpoint**: Place in `data/checkpoints/mrms_model.ckpt`
- **Point Cloud Data**: Place in `mrms_point_cloud.npy`

---

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact
For questions, suggestions, or collaboration, open an issue or contact [Your Name/Team] at [your.email@domain.com].

---

If you have questions, ideas, or want to collaborate, don't hesitate to reach out. I hope this project inspires you to blend human insight with AI in your own work!

---

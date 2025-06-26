# Technical Report: Human-Physics Hybrid AI System

## Introduction & Motivation

In my journey to push the boundaries of nowcasting, I realized that pure data-driven AI often misses the nuanced insights that human experts bring to the table. This project is my answer: a hybrid system that fuses human annotation with physics-inspired neural networks, aiming for skillful, interpretable, and adaptive precipitation nowcasting.

## System Design

The architecture is modular and feedback-driven. At its core, the system consists of:
- An interactive 3D annotation tool for human input
- Automated mask generation from annotations
- A flexible data loader that feeds both radar data and annotation masks to the NowcastNet model
- An evaluator that visualizes and compares predictions, ground truth, and human annotations
- A feedback loop that empowers rapid iteration and improvement

![Architecture Diagram](architecture.png)

## Annotation Tool

The browser-based 3D annotation tool is designed for ease of use and expressiveness. Users can:
- Inspect radar point clouds in 3D
- Draw bounding boxes and add descriptions
- Export annotations as JSON for downstream processing

*Demo GIF: (to be added)*

## ML Integration Workflow

Annotations are converted to binary mask images using a simple script. These masks are then optionally loaded alongside radar data by the data loader. The NowcastNet model can thus be trained or evaluated with direct human supervision, enabling:
- Supervised learning with human-labeled regions
- Quantitative and qualitative comparison of predictions and annotations
- A feedback loop where model results inform further annotation

## Results & Insights

The system produces side-by-side visualizations of ground truth, model predictions, and annotation masks. This makes it easy to spot where the model excels or needs improvement, and to iteratively refine both the model and the annotations.

*Example comparison: (to be added)*

Through this workflow, I've found that even a small amount of targeted human annotation can significantly improve model interpretability and performance in challenging cases.

## Conclusion

This project is a step toward more collaborative, transparent, and effective AI for scientific applications. By making human expertise a first-class citizen in the ML pipeline, we can build systems that are not only more accurate, but also more trustworthy and adaptable.

If you have questions, ideas, or want to collaborate, I'd love to hear from you! 
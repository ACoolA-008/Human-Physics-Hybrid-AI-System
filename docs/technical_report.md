# Technical Report: Human-Physics Hybrid AI System for Precipitation Nowcasting

## 1. Motivation & Goals

Accurate precipitation nowcasting is critical for weather safety, hydrology, and climate research. Traditional AI models excel at pattern recognition but often lack physical interpretability, while physics-based models can be limited by data and complexity. This project aims to bridge the gap by:
- Enabling **human-in-the-loop annotation** and correction of AI predictions
- Providing a **modern, intuitive 3D annotation tool** for meteorological data
- Seamlessly integrating human knowledge into the ML pipeline

## 2. System Design

### 2.1. UI/Frontend
- **3D Point Cloud Viewer**: Renders MRMS radar data in a browser using Three.js
- **Annotation Tool**: Click-and-drag bounding box creation, labeling, and management
- **Flexible Layout**: Resizable tool panel, always-visible map, and responsive design
- **Annotation Management**: Add, edit, delete, search, import/export, and bulk operations

### 2.2. Backend & Data Flow
- **Python HTTP Server**: Handles annotation saving and static file serving
- **Annotation Format**: JSON with bounding box coordinates and labels
- **Mask Generation**: Python script converts annotation JSON to mask images for ML

### 2.3. ML Integration
- **NowcastNet**: Deep learning model for precipitation nowcasting
- **Data Loader**: Feeds both radar frames and annotation masks to the model
- **Evaluator**: Visualizes and compares predictions, ground truth, and annotations

## 3. Human-in-the-Loop Workflow
1. **Visualize**: Load and explore 3D radar data
2. **Annotate**: Mark regions of interest (e.g., storm fronts, river beds) with bounding boxes
3. **Export**: Save annotations as JSON for reproducibility
4. **Convert**: Generate mask images for ML training/validation
5. **Train/Evaluate**: Use masks in NowcastNet pipeline
6. **Compare & Refine**: Visualize results, compare with human annotations, and iterate

## 4. Key Design Decisions
- **Direct 3D Annotation**: Click-and-drag for intuitive bounding box creation
- **Flexible, Modern UI**: Resizable panels and always-visible map for spatial context
- **Server-Side Saving**: Ensures annotation reproducibility and easy integration
- **Modular Data Flow**: Clear separation between annotation, mask generation, and ML pipeline
- **Open Standards**: Uses JSON and PNG for interoperability

## 5. Lessons Learned & Future Work
- **User Experience**: Iterative UI improvements (resizing, panel layout, direct drawing) greatly enhance usability
- **Integration**: Seamless data flow from annotation to ML is key for rapid experimentation
- **Scalability**: Future work could include collaborative annotation, more annotation types (polygons, temporal), and real-time feedback from the ML model
- **Extensibility**: The system can be adapted for other geospatial or scientific annotation tasks

## 6. Conclusion
This project demonstrates a practical, creative approach to combining human expertise and AI for weather nowcasting. The open-source, modular design enables rapid iteration and collaboration, paving the way for more interpretable and effective AI systems in meteorology and beyond.

If you have questions, ideas, or want to collaborate, I'd love to hear from you! 
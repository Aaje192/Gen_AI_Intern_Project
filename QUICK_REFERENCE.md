# Cam Ring Analysis - Quick Reference Card

## Installation
```bash
pip install -r requirements.txt
```

## Three Ways to Run

### 1️⃣ Quickest (Automated with test data)
```bash
python quick_start.py
```

### 2️⃣ Interactive (Step-by-step with explanations)
```bash
jupyter notebook analysis_notebook.ipynb
```

### 3️⃣ Direct (Custom Python code)
```python
from src.cam_ring_analyzer import CamRingAnalyzer

analyzer = CamRingAnalyzer('data/your_image.png')
analyzer.canny_edge_detection()
analyzer.find_center()
analyzer.compute_radial_distances()
analyzer.save_results('output')
```

---

## File Locations

| File | Purpose |
|------|---------|
| `data/` | Put your cam ring images here |
| `output/` | Results saved here |
| `src/cam_ring_analyzer.py` | Main analysis engine |
| `analysis_notebook.ipynb` | Tutorial notebook |
| `GUIDE.md` | Complete technical guide |

---

## Quick Parameter Tuning

### Edge Detection (Too sharp? Too noisy?)
```python
# For noisy images:
analyzer.canny_edge_detection(low_threshold=75, high_threshold=200)

# For faint edges:
analyzer.canny_edge_detection(low_threshold=30, high_threshold=100)

# Default (usually works):
analyzer.canny_edge_detection(low_threshold=50, high_threshold=150)
```

### Measurement Resolution
```python
# Every degree (360 measurements):
analyzer = CamRingAnalyzer(image_path, angle_resolution=1)

# Every 2 degrees (180 measurements):
analyzer = CamRingAnalyzer(image_path, angle_resolution=2)

# Every 5 degrees (72 measurements):
analyzer = CamRingAnalyzer(image_path, angle_resolution=5)
```

---

## Key Outputs Explained

### CSV Files
- **radial_distances.csv** - All measurements (angle, inner_radius, outer_radius, distance)
- **analysis_summary.csv** - Summary statistics

### Images
- **detected_edges.png** - Shows what was detected
- **distance_analysis.png** - 4 analysis plots
- **comprehensive_analysis.png** - 6-panel overview

---

## Troubleshooting Checklist

| Problem | Solution |
|---------|----------|
| No edges detected | Lower thresholds (try 30, 100) |
| Too much noise | Increase blur kernel (try 7 or 9) |
| Wrong center | Check image quality, verify edges are detected |
| Bad measurements | Increase blur or enable equalization |
| Memory issues | Use smaller images (< 1600x1600 px) |

---

## Output Interpretation

### Good Results (Healthy Cam Ring)
- ✓ Distance curve is smooth
- ✓ Coefficient of variation < 5%
- ✓ Clean edge detection
- ✓ Consistent measurements

### Issues (May Indicate Problems)
- ⚠ Jagged/noisy curve → Rough surface or noise
- ⚠ CV > 15% → Manufacturing defects
- ⚠ Sudden drops → Potential damage
- ⚠ Offset center → Ring may be eccentric

---

## Code Snippets

### Batch Process Multiple Images
```python
from pathlib import Path
from src.cam_ring_analyzer import CamRingAnalyzer

for image in Path('data').glob('*.png'):
    analyzer = CamRingAnalyzer(str(image))
    analyzer.canny_edge_detection()
    analyzer.find_center()
    analyzer.compute_radial_distances()
    analyzer.save_results(f'output/{image.stem}')
```

### Get Just the Summary
```python
analyzer = CamRingAnalyzer('data/image.png')
analyzer.canny_edge_detection()
analyzer.find_center()
analyzer.compute_radial_distances()

summary = analyzer.get_summary()
print(f"Mean distance: {summary['mean_distance']:.2f} pixels")
print(f"Variation: {summary['std_distance']:.2f} pixels")
```

### Extract Raw Data
```python
analyzer = CamRingAnalyzer('data/image.png')
analyzer.canny_edge_detection()
analyzer.find_center()

# Get polar coordinates
angles, radii = analyzer.convert_to_polar_coordinates()

# Get measurements
df = analyzer.compute_radial_distances()
print(df.describe())  # Statistics
```

---

## Key Definitions

| Term | Meaning |
|------|---------|
| **Inner Edge** | The closest part of the ring to center |
| **Outer Edge** | The farthest part of the ring from center |
| **Radial Distance** | Thickness at a given angle (outer - inner) |
| **Angular Resolution** | How many measurement points (360° / resolution) |
| **Coefficient of Variation** | (Std Dev / Mean) × 100% - measure of uniformity |

---

## Performance Expectations

| Image Size | Time | Memory |
|------------|------|--------|
| 400×400 | <0.5s | 20 MB |
| 800×800 | 1-2s | 50 MB |
| 1600×1600 | 3-5s | 150 MB |

---

## File Structure After Analysis

```
output/
├── radial_distances.csv         ← All measurements
├── analysis_summary.csv         ← Statistics
├── detected_edges.png           ← Edge detection
├── distance_analysis.png        ← 4-panel plot
├── edge_overlay.png             ← Overlay view
├── comprehensive_analysis.png   ← 6-panel summary
└── summary_table.png            ← Statistics table
```

---

## Tips & Tricks

1. **Better edge detection?** Use histogram equalization
2. **Noisy results?** Increase blur kernel size
3. **Want more detail?** Use angle_resolution=0.5
4. **Need speed?** Use angle_resolution=5
5. **Comparing images?** Use same parameters
6. **Batch processing?** Use the loop example above
7. **Custom visualization?** Load CSV and plot with matplotlib

---

## One-Liner Quick Test

```bash
python -c "from src.image_generator import generate_test_images; generate_test_images('data'); from src.cam_ring_analyzer import CamRingAnalyzer; a = CamRingAnalyzer('data/cam_ring_circular.png'); a.canny_edge_detection(); a.find_center(); a.compute_radial_distances(); a.save_results('output'); print('✓ Analysis complete!')"
```

---

## Common Questions

**Q: Can it handle elliptical rings?**  
A: Yes, but results show the variation from round.

**Q: Does order of operations matter?**  
A: Yes - must be: detect edges → find center → get distances

**Q: Can I change the resolution?**  
A: Yes, use `angle_resolution` parameter.

**Q: What's the best image format?**  
A: PNG, JPG, BMP all work. PNG recommended.

**Q: How accurate is it?**  
A: ±1-2 pixels depending on image quality.

---

## Emergency Help

1. Run the test suite: `python test_project.py`
2. Check GUIDE.md for detailed info
3. Review the notebook: `jupyter notebook analysis_notebook.ipynb`
4. Look at quick_start.py for working example

---

**Ready to analyze cam rings? Start with:**
```bash
python quick_start.py
```

Check the `output/` folder for results! 📊

---

*For detailed documentation, see GUIDE.md*

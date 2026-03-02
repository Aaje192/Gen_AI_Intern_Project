"""
Quick Start Guide - Cam Ring Analysis Example

This script provides a simple example of how to use the CamRingAnalyzer
to process a cam ring image and generate all outputs.
"""

import sys
from pathlib import Path

# Add src folder to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from cam_ring_analyzer import CamRingAnalyzer
from image_generator import generate_test_images


def main():
    """Run a quick example of cam ring analysis."""
    
    print("="*70)
    print("CAM RING EDGE DETECTION AND DIMENSIONAL ANALYSIS - QUICK START")
    print("="*70)
    
    # Step 1: Generate or load test images
    print("\n[Step 1] Preparing test images...")
    data_dir = Path('data')
    
    # Generate synthetic test images if not present
    image_files = list(data_dir.glob('*.png'))
    if not image_files:
        print("Generating synthetic test images...")
        generate_test_images(str(data_dir))
    else:
        print(f"Found {len(image_files)} existing image(s)")
    
    # Step 2: Process each image
    print("\n[Step 2] Processing cam ring images...")
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    for image_file in data_dir.glob('*.png'):
        print(f"\n  Processing: {image_file.name}")
        
        try:
            # Create analyzer instance
            analyzer = CamRingAnalyzer(str(image_file), angle_resolution=1)
            
            # Perform edge detection
            print("    - Detecting edges...")
            analyzer.canny_edge_detection(low_threshold=50, high_threshold=150)
            
            # Find center
            print("    - Finding center...")
            center = analyzer.find_center()
            print(f"      Center: {center}")
            
            # Compute radial distances
            print("    - Computing radial distances...")
            results = analyzer.compute_radial_distances()
            print(f"      Analyzed {len(results)} angular positions")
            
            # Save results
            print("    - Saving results...")
            image_output_dir = output_dir / image_file.stem
            analyzer.save_results(str(image_output_dir))
            
            # Print summary
            summary = analyzer.get_summary()
            print("\n      Summary Statistics:")
            print(f"        - Mean distance: {summary['mean_distance']:.2f} px")
            print(f"        - Min distance:  {summary['min_distance']:.2f} px")
            print(f"        - Max distance:  {summary['max_distance']:.2f} px")
            print(f"        - Std deviation: {summary['std_distance']:.2f} px")
            
        except Exception as e:
            print(f"    ERROR: {e}")
            continue
    
    print("\n" + "="*70)
    print("Analysis complete! Check the 'output' folder for results.")
    print("="*70)


if __name__ == "__main__":
    main()

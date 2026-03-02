"""
Main script for Cam Ring Edge Detection and Dimensional Analysis

This script demonstrates the usage of the CamRingAnalyzer class
to process cam ring images and generate results.
"""

import sys
from pathlib import Path
import cv2
import numpy as np
from cam_ring_analyzer import CamRingAnalyzer


def analyze_single_image(image_path, output_dir="output", angle_resolution=1):
    """
    Analyze a single cam ring image.

    Args:
        image_path: Path to the cam ring image
        output_dir: Directory to save results
        angle_resolution: Angular resolution in degrees

    Returns:
        CamRingAnalyzer instance with results
    """
    print(f"Processing image: {image_path}")

    # Create analyzer
    analyzer = CamRingAnalyzer(image_path, angle_resolution=angle_resolution)

    # Perform edge detection
    print("Performing edge detection...")
    analyzer.canny_edge_detection(low_threshold=50, high_threshold=150)

    # Find center
    print("Finding cam ring center...")
    center = analyzer.find_center()
    print(f"Center found at: {center}")

    # Compute radial distances
    print("Computing radial distances...")
    radii_data = analyzer.compute_radial_distances()
    print(f"Analyzed {len(radii_data)} angular positions")

    # Save results
    print(f"Saving results to {output_dir}...")
    analyzer.save_results(output_dir)

    # Print summary
    summary = analyzer.get_summary()
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Image: {summary['image_path']}")
    print(f"Center: {summary['center']}")
    print(f"Angles analyzed: {summary['num_angles_analyzed']}")
    print(f"\nDistance Statistics (in pixels):")
    print(f"  Mean:   {summary['mean_distance']:.2f}")
    print(f"  Min:    {summary['min_distance']:.2f}")
    print(f"  Max:    {summary['max_distance']:.2f}")
    print(f"  Std:    {summary['std_distance']:.2f}")
    print(f"\nRadius Statistics (in pixels):")
    print(f"  Mean Inner Radius: {summary['mean_inner_radius']:.2f}")
    print(f"  Mean Outer Radius: {summary['mean_outer_radius']:.2f}")
    print("=" * 60)

    return analyzer


def main():
    """Main execution function."""
    # Example usage - you can modify this to process actual cam ring images
    current_dir = Path(__file__).parent.parent

    # Check if there are sample images in the data folder
    data_dir = current_dir / "data"
    output_dir = current_dir / "output"

    # Find all image files
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    images = [f for f in data_dir.iterdir() if f.suffix.lower() in image_extensions]

    if not images:
        print(f"No image files found in {data_dir}")
        print("Please place your cam ring images in the 'data' folder")
        print("\nSupported formats: JPG, JPEG, PNG, BMP, TIFF")
        return

    # Process each image
    for image_file in images:
        print(f"\n{'='*60}")
        analyzer = analyze_single_image(str(image_file), output_dir)
        print()


if __name__ == "__main__":
    main()

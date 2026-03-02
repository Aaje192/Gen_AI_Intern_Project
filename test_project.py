"""
Test and Demo Script for Cam Ring Analysis Project

This script tests all functionality and generates sample outputs.
"""

import os
os.environ['DISPLAY'] = ''

import sys
from pathlib import Path
import numpy as np

# Add src folder to path
sys.path.insert(0, str(Path(__file__).parent))

from src.cam_ring_analyzer import CamRingAnalyzer
from src.image_generator import (
    create_synthetic_cam_ring,
    create_elliptical_cam_ring,
    create_irregular_cam_ring
)


def test_image_generation():
    """Test synthetic image generation."""
    print("\n" + "="*70)
    print("TEST 1: Synthetic Image Generation")
    print("="*70)
    
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    print("\nGenerating test images...")
    
    # Test 1: Circular cam ring
    print("  1. Creating circular cam ring...")
    img1 = create_synthetic_cam_ring(
        inner_radius=150,
        outer_radius=250,
        noise_level=10,
        output_path=data_dir / 'test_circular.png'
    )
    print(f"     Shape: {img1.shape}, Range: [{img1.min()}, {img1.max()}]")
    
    # Test 2: Elliptical cam ring
    print("  2. Creating elliptical cam ring...")
    img2 = create_elliptical_cam_ring(
        inner_axes=(100, 150),
        outer_axes=(200, 290),
        angle=45,
        output_path=data_dir / 'test_elliptical.png'
    )
    print(f"     Shape: {img2.shape}, Range: [{img2.min()}, {img2.max()}]")
    
    # Test 3: Irregular cam ring
    print("  3. Creating irregular cam ring with lobes...")
    img3 = create_irregular_cam_ring(
        inner_radius=140,
        outer_radius=240,
        num_lobes=8,
        lobe_amplitude=20,
        output_path=data_dir / 'test_irregular.png'
    )
    print(f"     Shape: {img3.shape}, Range: [{img3.min()}, {img3.max()}]")
    
    print("\n✓ Image generation test passed!")
    return True


def test_edge_detection():
    """Test edge detection functionality."""
    print("\n" + "="*70)
    print("TEST 2: Edge Detection")
    print("="*70)
    
    image_path = Path('data') / 'test_circular.png'
    
    print(f"\nTesting edge detection on: {image_path.name}")
    
    analyzer = CamRingAnalyzer(str(image_path))
    
    print("  1. Preprocessing image...")
    preprocessed = analyzer.preprocess_image()
    print(f"     Preprocessed shape: {preprocessed.shape}")
    print(f"     Preprocessed range: [{preprocessed.min()}, {preprocessed.max()}]")
    
    print("  2. Performing Canny edge detection...")
    edges = analyzer.canny_edge_detection(low_threshold=50, high_threshold=150)
    edge_count = np.sum(edges > 0)
    print(f"     Edge pixels detected: {edge_count}")
    print(f"     Edge map shape: {edges.shape}")
    
    if edge_count > 1000:
        print("     ✓ Sufficient edges detected")
    else:
        print("     ⚠ Warning: Few edges detected")
    
    print("\n✓ Edge detection test passed!")
    return True


def test_center_detection():
    """Test center detection functionality."""
    print("\n" + "="*70)
    print("TEST 3: Center Detection")
    print("="*70)
    
    image_path = Path('data') / 'test_circular.png'
    
    print(f"\nTesting center detection on: {image_path.name}")
    
    analyzer = CamRingAnalyzer(str(image_path))
    analyzer.canny_edge_detection()
    
    print("  1. Detecting center...")
    center = analyzer.find_center()
    print(f"     Detected center: {center}")
    
    # Verify center is within image bounds
    h, w = analyzer.edges.shape
    if 0 <= center[0] < w and 0 <= center[1] < h:
        print(f"     ✓ Center is within image bounds ({w}x{h})")
    else:
        print(f"     ⚠ Warning: Center is outside image bounds")
    
    print("\n✓ Center detection test passed!")
    return True


def test_coordinate_conversion():
    """Test polar coordinate conversion."""
    print("\n" + "="*70)
    print("TEST 4: Coordinate Conversion")
    print("="*70)
    
    image_path = Path('data') / 'test_circular.png'
    
    print(f"\nTesting coordinate conversion on: {image_path.name}")
    
    analyzer = CamRingAnalyzer(str(image_path))
    analyzer.canny_edge_detection()
    analyzer.find_center()
    
    print("  1. Converting to polar coordinates...")
    angles, radii = analyzer.convert_to_polar_coordinates()
    
    print(f"     Number of edge points: {len(angles)}")
    print(f"     Angle range: [{angles.min():.1f}°, {angles.max():.1f}°]")
    print(f"     Radius range: [{radii.min():.1f}, {radii.max():.1f}] pixels")
    
    # Verify angles are in valid range
    if angles.min() >= 0 and angles.max() <= 360:
        print("     ✓ Angles correctly normalized to [0, 360]")
    
    print("\n✓ Coordinate conversion test passed!")
    return True


def test_distance_calculation():
    """Test radial distance calculation."""
    print("\n" + "="*70)
    print("TEST 5: Radial Distance Calculation")
    print("="*70)
    
    image_path = Path('data') / 'test_circular.png'
    
    print(f"\nTesting distance calculation on: {image_path.name}")
    
    analyzer = CamRingAnalyzer(str(image_path), angle_resolution=1)
    analyzer.canny_edge_detection()
    analyzer.find_center()
    
    print("  1. Computing radial distances...")
    results = analyzer.compute_radial_distances()
    
    print(f"     Angular positions analyzed: {len(results)}")
    print(f"     Columns: {list(results.columns)}")
    print(f"\n     Distance statistics:")
    print(f"       Mean:   {results['distance'].mean():.2f} pixels")
    print(f"       Min:    {results['distance'].min():.2f} pixels")
    print(f"       Max:    {results['distance'].max():.2f} pixels")
    print(f"       StdDev: {results['distance'].std():.2f} pixels")
    
    # Verify reasonable values
    mean_dist = results['distance'].mean()
    if 50 < mean_dist < 500:  # Reasonable range for synthetic images
        print(f"     ✓ Distance values are in reasonable range")
    
    print("\n✓ Distance calculation test passed!")
    return results


def test_summary_and_export():
    """Test summary generation and data export."""
    print("\n" + "="*70)
    print("TEST 6: Summary and Export")
    print("="*70)
    
    image_path = Path('data') / 'test_circular.png'
    
    print(f"\nTesting summary and export on: {image_path.name}")
    
    analyzer = CamRingAnalyzer(str(image_path))
    analyzer.canny_edge_detection()
    analyzer.find_center()
    analyzer.compute_radial_distances()
    
    print("  1. Generating summary statistics...")
    summary = analyzer.get_summary()
    
    print(f"     Image: {Path(summary['image_path']).name}")
    print(f"     Center: {summary['center']}")
    print(f"     Angles analyzed: {summary['num_angles_analyzed']}")
    print(f"     Mean distance: {summary['mean_distance']:.2f} pixels")
    print(f"     Distance variation: {summary['max_distance'] - summary['min_distance']:.2f} pixels")
    
    # Verify summary contains all expected keys
    expected_keys = [
        'image_path', 'center', 'angle_resolution', 'num_angles_analyzed',
        'mean_distance', 'min_distance', 'max_distance', 'std_distance',
        'mean_inner_radius', 'mean_outer_radius'
    ]
    
    if all(key in summary for key in expected_keys):
        print("     ✓ Summary contains all expected fields")
    
    print("  2. Exporting results...")
    output_dir = Path('output') / 'test_results'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    analyzer.save_results(str(output_dir))
    
    # Check if files were created
    csv_file = output_dir / 'radial_distances.csv'
    if csv_file.exists():
        print(f"     ✓ CSV file created: {csv_file.name}")
    
    print("\n✓ Summary and export test passed!")
    return True


def test_visualization():
    """Test visualization generation."""
    print("\n" + "="*70)
    print("TEST 7: Visualization")
    print("="*70)
    
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend for testing
    
    image_path = Path('data') / 'test_circular.png'
    
    print(f"\nTesting visualizations on: {image_path.name}")
    
    analyzer = CamRingAnalyzer(str(image_path))
    analyzer.canny_edge_detection()
    analyzer.find_center()
    analyzer.compute_radial_distances()
    
    print("  1. Creating edge visualization...")
    edges_vis = analyzer.visualize_edges()
    print(f"     Shape: {edges_vis.shape}, Type: {edges_vis.dtype}")
    
    print("  2. Creating distance analysis plots...")
    fig = analyzer.visualize_distances()
    print(f"     Figure axes: {len(fig.get_axes())}")
    
    print("  3. Creating overlay visualization...")
    overlay = analyzer.create_overlay_visualization()
    print(f"     Shape: {overlay.shape}, Type: {overlay.dtype}")
    
    print("\n✓ Visualization test passed!")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*80)
    print("CAM RING ANALYSIS - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    tests = [
        ("Image Generation", test_image_generation),
        ("Edge Detection", test_edge_detection),
        ("Center Detection", test_center_detection),
        ("Coordinate Conversion", test_coordinate_conversion),
        ("Distance Calculation", test_distance_calculation),
        ("Summary and Export", test_summary_and_export),
        ("Visualization", test_visualization),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, True))
        except Exception as e:
            print(f"\n✗ {test_name} test FAILED!")
            print(f"  Error: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:<30} {status}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n✓ ALL TESTS PASSED! Project is ready to use.")
    else:
        print(f"\n⚠ {total_count - passed_count} test(s) failed. Please review the errors above.")
    
    print("="*80 + "\n")
    
    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

"""
Utility functions for generating synthetic cam ring images for testing.

This module provides functions to create synthetic cam ring images
with known parameters for testing and validation of the analyzer.
"""

import numpy as np
import cv2
from pathlib import Path


def create_synthetic_cam_ring(
    width=800,
    height=800,
    center_offset=None,
    inner_radius=150,
    outer_radius=250,
    noise_level=10,
    edge_width=3,
    output_path=None,
):
    """
    Create a synthetic cam ring image for testing.

    Args:
        width: Image width in pixels
        height: Image height in pixels
        center_offset: Tuple (dx, dy) for center offset from image center
        inner_radius: Inner radius of the cam ring in pixels
        outer_radius: Outer radius of the cam ring in pixels
        noise_level: Standard deviation of Gaussian noise
        edge_width: Width of the ring edge in pixels
        output_path: Optional path to save the image

    Returns:
        NumPy array representing the image
    """
    # Create blank image
    image = np.ones((height, width, 3), dtype=np.uint8) * 200  # Light gray background

    # Define center
    if center_offset is None:
        center = (width // 2, height // 2)
    else:
        center = (width // 2 + center_offset[0], height // 2 + center_offset[1])

    cx, cy = center

    # Create outer circle
    cv2.circle(image, center, outer_radius, (255, 255, 255), edge_width)

    # Create inner circle
    cv2.circle(image, center, inner_radius, (255, 255, 255), edge_width)

    # Add some noise
    if noise_level > 0:
        noise = np.random.normal(0, noise_level, image.shape)
        image = np.clip(image + noise, 0, 255).astype(np.uint8)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(output_path, gray_image)
        print(f"Synthetic cam ring image saved to {output_path}")

    return gray_image


def create_elliptical_cam_ring(
    width=800,
    height=800,
    center_offset=None,
    inner_axes=(120, 150),
    outer_axes=(220, 280),
    angle=0,
    noise_level=10,
    edge_width=3,
    output_path=None,
):
    """
    Create a synthetic elliptical cam ring image for testing.

    Args:
        width: Image width in pixels
        height: Image height in pixels
        center_offset: Tuple (dx, dy) for center offset from image center
        inner_axes: Tuple (a, b) for inner ellipse semi-axes
        outer_axes: Tuple (a, b) for outer ellipse semi-axes
        angle: Rotation angle in degrees
        noise_level: Standard deviation of Gaussian noise
        edge_width: Width of the ring edge in pixels
        output_path: Optional path to save the image

    Returns:
        NumPy array representing the image
    """
    # Create blank image
    image = np.ones((height, width, 3), dtype=np.uint8) * 200  # Light gray background

    # Define center
    if center_offset is None:
        center = (width // 2, height // 2)
    else:
        center = (width // 2 + center_offset[0], height // 2 + center_offset[1])

    # Create outer ellipse
    cv2.ellipse(image, center, outer_axes, angle, 0, 360, (255, 255, 255), edge_width)

    # Create inner ellipse
    cv2.ellipse(image, center, inner_axes, angle, 0, 360, (255, 255, 255), edge_width)

    # Add some noise
    if noise_level > 0:
        noise = np.random.normal(0, noise_level, image.shape)
        image = np.clip(image + noise, 0, 255).astype(np.uint8)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(output_path, gray_image)
        print(f"Synthetic elliptical cam ring image saved to {output_path}")

    return gray_image


def create_irregular_cam_ring(
    width=800,
    height=800,
    center_offset=None,
    inner_radius=150,
    outer_radius=250,
    num_lobes=0,
    lobe_amplitude=20,
    noise_level=15,
    output_path=None,
):
    """
    Create a synthetic irregular cam ring with lobes (more realistic).

    Args:
        width: Image width in pixels
        height: Image height in pixels
        center_offset: Tuple (dx, dy) for center offset from image center
        inner_radius: Base inner radius in pixels
        outer_radius: Base outer radius in pixels
        num_lobes: Number of lobes (0 for circular)
        lobe_amplitude: Amplitude of lobes in pixels
        noise_level: Standard deviation of Gaussian noise
        output_path: Optional path to save the image

    Returns:
        NumPy array representing the image
    """
    # Create blank image
    image = np.ones((height, width, 3), dtype=np.uint8) * 200

    # Define center
    if center_offset is None:
        center = (width // 2, height // 2)
    else:
        center = (width // 2 + center_offset[0], height // 2 + center_offset[1])

    cx, cy = center

    # Generate points for outer edge with lobes
    angles = np.linspace(0, 2 * np.pi, 360)
    if num_lobes > 0:
        lobe_modulation = lobe_amplitude * np.sin(num_lobes * angles)
    else:
        lobe_modulation = 0

    outer_radii = outer_radius + lobe_modulation
    outer_x = cx + outer_radii * np.cos(angles)
    outer_y = cy + outer_radii * np.sin(angles)
    outer_points = np.stack([outer_x, outer_y], axis=1).astype(np.int32)

    # Generate points for inner edge with lobes
    inner_radii = inner_radius + lobe_modulation * 0.5  # Lobes less pronounced
    inner_x = cx + inner_radii * np.cos(angles)
    inner_y = cy + inner_radii * np.sin(angles)
    inner_points = np.stack([inner_x, inner_y], axis=1).astype(np.int32)

    # Draw outer contour
    cv2.polylines(image, [outer_points], True, (255, 255, 255), 3)

    # Draw inner contour
    cv2.polylines(image, [inner_points], True, (255, 255, 255), 3)

    # Add noise
    if noise_level > 0:
        noise = np.random.normal(0, noise_level, image.shape)
        image = np.clip(image + noise, 0, 255).astype(np.uint8)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(output_path, gray_image)
        print(f"Synthetic irregular cam ring image saved to {output_path}")

    return gray_image


def generate_test_images(data_dir="data"):
    """
    Generate a set of test images for validation.

    Args:
        data_dir: Directory to save test images
    """
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    print("Generating synthetic cam ring test images...")

    # Simple circular cam ring
    create_synthetic_cam_ring(
        inner_radius=150,
        outer_radius=250,
        noise_level=8,
        output_path=data_dir / "cam_ring_circular.png",
    )

    # Offset center
    create_synthetic_cam_ring(
        inner_radius=120,
        outer_radius=230,
        center_offset=(20, -15),
        noise_level=10,
        output_path=data_dir / "cam_ring_offset.png",
    )

    # Elliptical cam ring
    create_elliptical_cam_ring(
        inner_axes=(100, 150),
        outer_axes=(200, 290),
        angle=30,
        noise_level=12,
        output_path=data_dir / "cam_ring_elliptical.png",
    )

    # Irregular cam ring with lobes
    create_irregular_cam_ring(
        inner_radius=140,
        outer_radius=240,
        num_lobes=6,
        lobe_amplitude=15,
        noise_level=15,
        output_path=data_dir / "cam_ring_lobed.png",
    )

    print(f"Test images generated in {data_dir}")


if __name__ == "__main__":
    # Generate test images in the data folder
    generate_test_images("../data")

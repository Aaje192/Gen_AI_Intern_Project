"""
Cam Ring Edge Detection and Dimensional Analysis

This module performs edge detection on cam ring images and computes
the radial distance between inner and outer edges at multiple angular intervals.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from pathlib import Path
import pandas as pd


class CamRingAnalyzer:
    """Analyzes cam rings to detect edges and compute dimensional information."""

    def __init__(self, image_path, angle_resolution=1):
        """
        Initialize the CamRingAnalyzer.

        Args:
            image_path: Path to the cam ring image
            angle_resolution: Angular resolution in degrees (default: 1 degree)
        """
        self.image_path = image_path
        self.angle_resolution = angle_resolution
        self.original_image = cv2.imread(image_path)
        self.grayscale = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.edges = None
        self.center = None
        self.inner_radius = None
        self.outer_radius = None
        self.radii_data = None

    def preprocess_image(self, blur_kernel=5, equalize=True, threshold_value=100):
        """
        Preprocess the image for edge detection.

        Args:
            blur_kernel: Kernel size for Gaussian blur (odd number)
            equalize: Whether to apply histogram equalization
            threshold_value: Binary threshold value

        Returns:
            Preprocessed grayscale image
        """
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(self.grayscale, (blur_kernel, blur_kernel), 1.5)

        # Apply histogram equalization to enhance contrast
        if equalize:
            blurred = cv2.equalizeHist(blurred)

        return blurred

    def canny_edge_detection(self, low_threshold=50, high_threshold=150):
        """
        Perform Canny edge detection on the cam ring image.

        Args:
            low_threshold: Lower threshold for Canny edge detection
            high_threshold: Upper threshold for Canny edge detection

        Returns:
            Binary image with detected edges
        """
        preprocessed = self.preprocess_image()
        self.edges = cv2.Canny(preprocessed, low_threshold, high_threshold)
        return self.edges

    def find_center(self):
        """
        Find the center of the cam ring using contour analysis.

        Returns:
            Tuple of (center_x, center_y)
        """
        # Find contours in the edge image
        contours, _ = cv2.findContours(
            self.edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            raise ValueError("No contours found. Check edge detection parameters.")

        # Find the largest contour (cam ring)
        largest_contour = max(contours, key=cv2.contourArea)

        # Calculate the moments to find center
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            # Fallback: use image center
            h, w = self.edges.shape
            cx, cy = w // 2, h // 2

        # Alternative: use circle fitting
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)
        self.center = (int(x), int(y))
        return self.center

    def extract_edge_coordinates(self):
        """
        Extract coordinates of all edge pixels.

        Returns:
            Array of (y, x) coordinates where edges are detected
        """
        edge_coords = np.argwhere(self.edges > 0)
        return edge_coords

    def convert_to_polar_coordinates(self):
        """
        Convert edge coordinates to polar coordinates (radius, angle).

        Returns:
            Dictionary with angle as key and list of radii as values
        """
        if self.center is None:
            self.find_center()

        edge_coords = self.extract_edge_coordinates()
        cx, cy = self.center

        # Calculate polar coordinates for all edge points
        # Note: OpenCV uses (x, y) but argwhere returns (y, x)
        dy = edge_coords[:, 0] - cy
        dx = edge_coords[:, 1] - cx

        angles = np.arctan2(dy, dx) * 180 / np.pi  # Convert to degrees
        radii = np.sqrt(dx**2 + dy**2)

        # Normalize angles to 0-360 range
        angles = (angles + 360) % 360

        return angles, radii

    def compute_radial_distances(self):
        """
        Compute distances between inner and outer edges at regular angular intervals.

        Returns:
            DataFrame with columns: angle, inner_radius, outer_radius, distance
        """
        angles, radii = self.convert_to_polar_coordinates()

        # Create angular bins
        angle_bins = np.arange(0, 360, self.angle_resolution)
        data = []

        for angle_center in angle_bins:
            angle_range = self.angle_resolution / 2
            # Find all radii within this angular bin
            in_range = (angles >= angle_center - angle_range) & (
                angles < angle_center + angle_range
            )

            if np.any(in_range):
                radii_in_range = radii[in_range]
                # Inner radius is minimum, outer radius is maximum
                inner_r = np.min(radii_in_range)
                outer_r = np.max(radii_in_range)
                distance = outer_r - inner_r

                data.append(
                    {
                        "angle": angle_center,
                        "inner_radius": inner_r,
                        "outer_radius": outer_r,
                        "distance": distance,
                    }
                )

        self.radii_data = pd.DataFrame(data)
        return self.radii_data

    def visualize_edges(self, output_path=None):
        """
        Create a visualization of detected edges with center marked.

        Args:
            output_path: Path to save the visualization (optional)

        Returns:
            Processed image with edges and center marked
        """
        if self.edges is None:
            self.canny_edge_detection()
        if self.center is None:
            self.find_center()

        # Create a color image for visualization
        vis_image = cv2.cvtColor(self.edges, cv2.COLOR_GRAY2BGR)

        # Mark detected edges in green
        vis_image[self.edges > 0] = (0, 255, 0)

        # Mark center in red
        cx, cy = self.center
        cv2.circle(vis_image, (cx, cy), 5, (0, 0, 255), -1)
        cv2.circle(vis_image, (cx, cy), 1, (0, 0, 255), -1)

        if output_path:
            cv2.imwrite(output_path, vis_image)

        return vis_image

    def visualize_distances(self, output_path=None):
        """
        Create a visualization showing radial distances at each angle.

        Args:
            output_path: Path to save the visualization (optional)

        Returns:
            Matplotlib figure
        """
        if self.radii_data is None:
            self.compute_radial_distances()

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Plot 1: Distance vs Angle
        axes[0].plot(
            self.radii_data["angle"], self.radii_data["distance"], "b-", linewidth=2
        )
        axes[0].set_xlabel("Angle (degrees)", fontsize=12)
        axes[0].set_ylabel("Radial Distance (pixels)", fontsize=12)
        axes[0].set_title("Distance Between Inner and Outer Edges vs Angle", fontsize=12)
        axes[0].grid(True, alpha=0.3)
        axes[0].set_xlim(0, 360)

        # Plot 2: Polar representation with distance
        angles_rad = np.deg2rad(self.radii_data["angle"])
        distances = self.radii_data["distance"]

        axes[1] = plt.subplot(1, 2, 2, projection="polar")
        axes[1].plot(angles_rad, distances, "b-", linewidth=2)
        axes[1].fill(angles_rad, distances, alpha=0.25)
        axes[1].set_title("Radial Distance Distribution", fontsize=12)
        axes[1].grid(True)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150)

        return fig

    def create_overlay_visualization(self, inner_color=(255, 0, 0), outer_color=(0, 255, 0), output_path=None):
        """
        Create an overlay visualization showing inner and outer edges.

        Args:
            inner_color: BGR color for inner edge
            outer_color: BGR color for outer edge
            output_path: Path to save the visualization (optional)

        Returns:
            Overlay image
        """
        if self.radii_data is None:
            self.compute_radial_distances()
        if self.center is None:
            self.find_center()

        # Create a blank image for overlay
        overlay = self.original_image.copy()
        cx, cy = self.center

        # Get edge coordinates
        angles, radii = self.convert_to_polar_coordinates()

        # Draw circles at inner and outer radii for each angle
        num_points = 360

        for i in range(num_points):
            angle_start = i
            angle_end = (i + 1) % num_points

            # Find radii for these angles
            mask_start = np.abs(angles - angle_start) < 0.5
            mask_end = np.abs(angles - angle_end) < 0.5

            if np.any(mask_start):
                inner_r_start = np.min(radii[mask_start])
                outer_r_start = np.max(radii[mask_start])

                angle_rad = np.deg2rad(angle_start)
                # Draw inner edge
                x_inner = int(cx + inner_r_start * np.cos(angle_rad))
                y_inner = int(cy + inner_r_start * np.sin(angle_rad))
                cv2.circle(overlay, (x_inner, y_inner), 2, inner_color, -1)

                # Draw outer edge
                x_outer = int(cx + outer_r_start * np.cos(angle_rad))
                y_outer = int(cy + outer_r_start * np.sin(angle_rad))
                cv2.circle(overlay, (x_outer, y_outer), 2, outer_color, -1)

        # Mark center
        cv2.circle(overlay, (cx, cy), 5, (0, 0, 255), -1)

        if output_path:
            cv2.imwrite(output_path, overlay)

        return overlay

    def save_results(self, output_dir):
        """
        Save all results (data, visualizations) to the specified directory.

        Args:
            output_dir: Directory to save results
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save CSV data
        if self.radii_data is not None:
            csv_path = output_dir / "radial_distances.csv"
            self.radii_data.to_csv(csv_path, index=False)
            print(f"Saved radial data to {csv_path}")

        # Save edge detection visualization
        edges_path = output_dir / "detected_edges.png"
        cv2.imwrite(edges_path, self.visualize_edges())
        print(f"Saved edge visualization to {edges_path}")

        # Save distance plot
        plot_path = output_dir / "distance_analysis.png"
        fig = self.visualize_distances()
        fig.savefig(plot_path, dpi=150)
        plt.close(fig)
        print(f"Saved distance plot to {plot_path}")

        # Save overlay visualization
        overlay_path = output_dir / "edge_overlay.png"
        cv2.imwrite(overlay_path, self.create_overlay_visualization())
        print(f"Saved overlay visualization to {overlay_path}")

    def get_summary(self):
        """
        Get a summary of the analysis results.

        Returns:
            Dictionary with summary statistics
        """
        if self.radii_data is None:
            self.compute_radial_distances()

        summary = {
            "image_path": str(self.image_path),
            "center": self.center,
            "angle_resolution": self.angle_resolution,
            "num_angles_analyzed": len(self.radii_data),
            "mean_distance": self.radii_data["distance"].mean(),
            "min_distance": self.radii_data["distance"].min(),
            "max_distance": self.radii_data["distance"].max(),
            "std_distance": self.radii_data["distance"].std(),
            "mean_inner_radius": self.radii_data["inner_radius"].mean(),
            "mean_outer_radius": self.radii_data["outer_radius"].mean(),
        }
        return summary

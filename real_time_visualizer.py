import matplotlib.pyplot as plt
import numpy as np
from collections import deque


class RealTimeVisualizer:
    """
    Real-time visualization of data stream and detected anomalies.

    Provides a live-updating plot showing:
    1. The continuous data stream
    2. Detected anomalies as red dots
    3. Moving window of recent values
    4. Automatic axis scaling

    Uses Matplotlib's interactive mode for real-time updates.

    Attributes:
        max_points (int): Maximum number of points to display
        timestamps (collections.deque): Rolling window of time values
        values (collections.deque): Rolling window of data values
        anomalies_x (collections.deque): Timestamps of detected anomalies
        anomalies_y (collections.deque): Values of detected anomalies
        fig (matplotlib.figure.Figure): The main figure object
        ax (matplotlib.axes.Axes): The plot axes object
        line (matplotlib.lines.Line2D): The main data line
        anomaly_scatter (matplotlib.collections.PathCollection): The anomaly points
        MIN_Y_RANGE (float): Minimum range for y-axis to prevent singular transformation
    """

    # Class constant for minimum y-axis range
    MIN_Y_RANGE = 1.0

    def __init__(self, max_points=200):
        """
        Initialize the visualizer with specified parameters.

        Args:
            max_points (int): Maximum number of points to display in the window
        """
        self.max_points = max_points
        # Initialize deques for efficient fixed-size data storage
        self.timestamps = deque(maxlen=max_points)
        self.values = deque(maxlen=max_points)
        self.anomalies_x = deque(maxlen=max_points)
        self.anomalies_y = deque(maxlen=max_points)

        # Set up the plot in interactive mode
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        (self.line,) = self.ax.plot([], [], "b-", label="Data Stream")
        self.anomaly_scatter = self.ax.scatter(
            [], [], color="red", marker="o", s=100, label="Anomalies"
        )

        # Configure plot appearance
        self.ax.set_title("Real-time Anomaly Detection")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
        self.ax.legend()
        self.ax.grid(True, linestyle="--", alpha=0.7)

    def _calculate_y_limits(self, y_min, y_max):
        """
        Calculate appropriate y-axis limits to prevent singular transformations.

        Args:
            y_min (float): Minimum value in current window
            y_max (float): Maximum value in current window

        Returns:
            tuple: (y_min_limit, y_max_limit) The adjusted y-axis limits
        """
        y_range = y_max - y_min

        # If range is zero or very small, create artificial range
        if y_range < self.MIN_Y_RANGE:
            center = (y_max + y_min) / 2
            y_min = center - self.MIN_Y_RANGE / 2
            y_max = center + self.MIN_Y_RANGE / 2
            y_range = self.MIN_Y_RANGE

        # Add padding (10% of range on each side)
        padding = 0.1 * y_range
        return y_min - padding, y_max + padding

    def update(self, timestamp, value, is_anomaly):
        """
        Update the visualization with new data.

        Handles both regular data points and anomalies, updating the plot
        and adjusting axes as needed for optimal visualization.

        Args:
            timestamp (float): Current timestamp
            value (float): Current value
            is_anomaly (bool): Whether the current value is anomalous
        """
        # Update main data collections
        self.timestamps.append(timestamp)
        self.values.append(value)

        # Store anomalies separately for scatter plot
        if is_anomaly:
            self.anomalies_x.append(timestamp)
            self.anomalies_y.append(value)

        # Update plot data
        self.line.set_data(list(self.timestamps), list(self.values))
        self.anomaly_scatter.set_offsets(
            np.c_[list(self.anomalies_x), list(self.anomalies_y)]
        )

        # Calculate and set y-axis limits with proper range handling
        if len(self.values) > 0:  # Check if we have any values
            y_min, y_max = min(self.values), max(self.values)
            y_min_limit, y_max_limit = self._calculate_y_limits(y_min, y_max)
            self.ax.set_ylim(y_min_limit, y_max_limit)

        # Update x-axis limits to show recent window
        x_min = max(0, timestamp - self.max_points)
        self.ax.set_xlim(x_min, timestamp + 5)

        # Redraw the plot
        try:
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
        except Exception:
            # Handle case where window is closed
            return False
        return True

    def cleanup(self):
        """Clean up matplotlib resources"""
        plt.close(self.fig)
        plt.close("all")

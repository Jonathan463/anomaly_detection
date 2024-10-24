import numpy as np
from collections import deque


class AnomalyDetector:
    """
    Real-time anomaly detection system using moving statistics.

    This class implements a streaming anomaly detection algorithm based on z-scores,
    which measures how many standard deviations away a data point is from the mean.
    It maintains a rolling window of recent values to adapt to changing data patterns.

    The detection is performed by:
    1. Maintaining a rolling window of recent values
    2. Computing mean and standard deviation of the window
    3. Converting new values to z-scores
    4. Flagging values beyond the threshold as anomalies

    Attributes:
        window_size (int): Number of recent values to consider for statistics
        threshold (float): Z-score threshold for anomaly detection
        values (collections.deque): Rolling window of recent values
        is_initialized (bool): Whether enough data has been collected
        mean (float): Rolling mean of the window
        std (float): Rolling standard deviation of the window
    """

    def __init__(self, window_size=100, threshold=3):
        """
        Initialize the anomaly detector with specified parameters.

        Args:
            window_size (int): Size of the rolling window for statistics
            threshold (float): Number of standard deviations for anomaly detection
        """
        self.window_size = window_size
        self.threshold = threshold
        # Use deque for efficient fixed-size window operations
        self.values = deque(maxlen=window_size)
        self.is_initialized = False

    def update_statistics(self):
        """
        Calculate moving statistics (mean and standard deviation) from the current window.

        This method is called after each new value to maintain current statistics.
        NumPy is used for efficient array operations.
        """
        self.mean = np.mean(self.values)
        self.std = np.std(self.values)

    def is_anomaly(self, value):
        """
        Detect if a value is anomalous using z-score method.

        A value is considered anomalous if its z-score (number of standard deviations
        from the mean) exceeds the threshold in either direction.

        Args:
            value (float): The value to check for anomalous behavior

        Returns:
            bool: True if the value is anomalous, False otherwise

        Notes:
            - Initial values are never considered anomalous until enough data is collected
            - A small epsilon (1e-10) is added to std to prevent division by zero
        """
        # Wait for sufficient data before detecting anomalies
        if len(self.values) < self.window_size // 2:
            self.values.append(value)
            return False

        # Initialize statistics if this is the first time we have enough data
        if not self.is_initialized:
            self.update_statistics()
            self.is_initialized = True

        # Calculate z-score (how many standard deviations from mean)
        z_score = (value - self.mean) / (
            self.std + 1e-10
        )  # Add epsilon to prevent division by zero

        # Update rolling window and statistics
        self.values.append(value)
        self.update_statistics()

        # Return True if absolute z-score exceeds threshold
        return abs(z_score) > self.threshold

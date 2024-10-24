import numpy as np


class DataStreamSimulator:
    """
    Simulates a realistic data stream with patterns and anomalies.

    Generates synthetic time series data with the following components:
    1. Seasonal pattern (sine wave)
    2. Linear trend
    3. Random noise
    4. Occasional anomalies

    The resulting stream mimics real-world patterns while providing
    ground truth for anomaly detection testing.

    Attributes:
        seasonal_period (int): Number of points in one seasonal cycle
        trend_factor (float): Slope of the linear trend
        noise_level (float): Standard deviation of the random noise
        counter (int): Number of points generated so far
    """

    def __init__(self, seasonal_period=24, trend_factor=0.1, noise_level=0.5):
        """
        Initialize the data stream simulator with specified parameters.

        Args:
            seasonal_period (int): Period of seasonal pattern (points per cycle)
            trend_factor (float): Strength of upward/downward trend
            noise_level (float): Amount of random noise to add
        """
        self.seasonal_period = seasonal_period
        self.trend_factor = trend_factor
        self.noise_level = noise_level
        self.counter = 0

    def get_next_value(self):
        """
        Generate the next value in the stream.

        Combines multiple components to create a realistic data point:
        1. Seasonal component: sin(2π * counter / period)
        2. Trend component: trend_factor * counter
        3. Noise component: Normal(0, noise_level)
        4. Potential anomaly: Random spike with 1% probability

        Returns:
            float: The next value in the sequence
        """
        # Generate seasonal pattern using sine wave
        seasonal = np.sin(2 * np.pi * self.counter / self.seasonal_period)

        # Add linear trend
        trend = self.trend_factor * self.counter

        # Add random noise from normal distribution
        noise = np.random.normal(0, self.noise_level)

        # Randomly inject anomalies (1% probability)
        if np.random.random() < 0.01:
            # Equal probability of positive or negative anomalies
            direction = np.random.choice([-1, 1])
            magnitude = np.random.uniform(5, 10)
            if direction == -1:
                magnitude *= 1.5  # Make negative anomalies more pronounced
            anomaly = direction * magnitude
        else:
            anomaly = 0

        self.counter += 1
        return seasonal + trend + noise + anomaly

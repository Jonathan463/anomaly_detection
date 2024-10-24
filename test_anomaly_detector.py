import unittest
from anomaly_detector import AnomalyDetector


class TestAnomalyDetector(unittest.TestCase):
    def test_normal_values(self):
        detector = AnomalyDetector(window_size=5, threshold=2.5)
        values = [1, 1, 1, 1, 1]  # Normal values, no anomaly
        for value in values:
            self.assertFalse(detector.is_anomaly(value))

    def test_anomaly(self):
        detector = AnomalyDetector(window_size=5, threshold=2.5)
        values = [1, 1, 1, 1, 1]  # Normal values to stabilize statistics
        for value in values:
            detector.is_anomaly(value)  # Populate the detector with normal values

        anomaly_value = 10  # Anomaly on the next value
        is_anomaly = detector.is_anomaly(anomaly_value)
        self.assertTrue(is_anomaly)  # The anomaly should be detected

    def test_dynamic_detection(self):
        detector = AnomalyDetector(window_size=10, threshold=2.5)
        # Insert normal values
        normal_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        for value in normal_values:
            detector.is_anomaly(value)

        # Now we introduce an anomaly
        anomaly_value = 10
        is_anomaly = detector.is_anomaly(anomaly_value)
        self.assertTrue(is_anomaly)  # The anomaly should be detected

        # Check that the next normal value doesn't trigger an anomaly
        self.assertFalse(detector.is_anomaly(1))


if __name__ == "__main__":
    unittest.main()

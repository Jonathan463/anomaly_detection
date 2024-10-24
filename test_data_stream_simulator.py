import unittest
from data_stream_simulator import DataStreamSimulator


class TestDataStreamSimulator(unittest.TestCase):
    def test_data_stream(self):
        simulator = DataStreamSimulator(
            seasonal_period=24, trend_factor=0.1, noise_level=0.5
        )
        values = [simulator.get_next_value() for _ in range(100)]
        self.assertEqual(len(values), 100)
        # Test that the stream contains values (not empty)
        self.assertTrue(all(isinstance(value, float) for value in values))

    def test_anomaly_in_stream(self):
        simulator = DataStreamSimulator(
            seasonal_period=10, trend_factor=0.0, noise_level=0.5
        )
        anomalies_count = 0
        for _ in range(100):
            value = simulator.get_next_value()
            if abs(value - 10) < 2:  # Check if the value is within the anomaly range
                anomalies_count += 1
        self.assertGreater(anomalies_count, 0)  # Expect at least one anomaly


if __name__ == "__main__":
    unittest.main()

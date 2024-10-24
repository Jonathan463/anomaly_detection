import logging
import time
from anomaly_detector import AnomalyDetector
from data_stream_simulator import DataStreamSimulator
from real_time_visualizer import RealTimeVisualizer
import matplotlib.pyplot as plt
import signal


# Set up logging
logging.basicConfig(filename="anomalies.log", level=logging.INFO)


class AnomalyDetectionSystem:
    """
    Coordinates the anomaly detection components and handles shutdown.
    """

    def __init__(self):
        self.running = True
        self.detector = AnomalyDetector(window_size=50, threshold=2.5)
        self.simulator = DataStreamSimulator(noise_level=0.3)
        self.visualizer = RealTimeVisualizer()

        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\nReceived signal to stop. Shutting down gracefully...")
        self.running = False

    def run(self):
        """Main loop with proper resource cleanup"""
        try:
            while self.running:
                value = self.simulator.get_next_value()
                is_anomaly = self.detector.is_anomaly(value)

                # Check if visualization was successful
                if not self.visualizer.update(
                    self.simulator.counter, value, is_anomaly
                ):
                    self.running = False
                    break

                time.sleep(0.05)

        except Exception as e:
            print(f"\nError occurred: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        print("\nCleaning up resources...")
        self.visualizer.cleanup()
        plt.ioff()  # Turn off interactive mode
        print("Shutdown complete.")


def main():
    """
    Main function with improved error handling and resource cleanup.
    """
    system = AnomalyDetectionSystem()
    system.run()


if __name__ == "__main__":
    main()

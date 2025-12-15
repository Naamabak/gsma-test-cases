I'll convert this test case into an executable pytest script. The script will test if an IoT device application maintains always-on connectivity when transmitting data frequently, even under various adverse conditions.

```python
import pytest
import time
import random
import logging
from unittest.mock import patch, MagicMock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mock classes to simulate the IoT device and network environment
class MockRadioConnection:
    def __init__(self):
        self.connected = False
        self.connection_count = 0
        self.disconnection_count = 0
        self.connection_history = []
        
    def connect(self):
        if not self.connected:
            self.connected = True
            self.connection_count += 1
            timestamp = time.time()
            self.connection_history.append({"event": "connect", "timestamp": timestamp})
            logger.info(f"Radio connection established at {timestamp}")
            return True
        return False
    
    def disconnect(self):
        if self.connected:
            self.connected = False
            self.disconnection_count += 1
            timestamp = time.time()
            self.connection_history.append({"event": "disconnect", "timestamp": timestamp})
            logger.info(f"Radio connection torn down at {timestamp}")
            return True
        return False
    
    def is_connected(self):
        return self.connected
    
    def get_connection_events(self):
        return self.connection_history
    
    def get_connection_stats(self):
        return {
            "connection_count": self.connection_count,
            "disconnection_count": self.disconnection_count,
            "currently_connected": self.connected
        }


class MockIoTDevice:
    def __init__(self, transmission_interval=30):
        self.radio = MockRadioConnection()
        self.transmission_interval = transmission_interval  # seconds
        self.running = False
        self.data_sent_count = 0
        self.transmission_history = []
    
    def start(self):
        if not self.running:
            self.running = True
            self.radio.connect()
            logger.info(f"IoT device started with transmission interval: {self.transmission_interval}s")
    
    def stop(self):
        if self.running:
            self.running = False
            # We're testing if the device keeps connection open, so we won't automatically disconnect
            logger.info("IoT device stopped")
    
    def send_data(self, payload_size="normal"):
        if self.running:
            if not self.radio.is_connected():
                self.radio.connect()
                
            timestamp = time.time()
            self.data_sent_count += 1
            self.transmission_history.append({"timestamp": timestamp, "payload_size": payload_size})
            logger.info(f"Data sent at {timestamp} with {payload_size} payload size")
            return True
        return False
    
    def simulate_device_crash(self):
        logger.info("Simulating device crash...")
        self.running = False
        time.sleep(1)  # Simulate brief downtime
        self.start()
        logger.info("Device restarted after crash")
    
    def simulate_app_crash_and_restart(self):
        logger.info("Simulating application crash...")
        self.running = False
        time.sleep(2)  # Simulate downtime
        self.start()
        logger.info("Application restarted after crash")


class MockNetworkEnvironment:
    def __init__(self, device):
        self.device = device
        self.normal_conditions = True
    
    def simulate_network_outage(self, duration=5):
        logger.info(f"Simulating network outage for {duration} seconds")
        self.normal_conditions = False
        # Force radio disconnection due to network issues
        if self.device.radio.is_connected():
            self.device.radio.disconnect()
        time.sleep(duration)
        self.normal_conditions = True
        logger.info
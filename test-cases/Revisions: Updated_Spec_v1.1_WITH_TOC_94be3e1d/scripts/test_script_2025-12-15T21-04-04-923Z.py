I'll convert the provided test case into a Python pytest script that simulates testing IoT device network connection behavior.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import time
import logging
import datetime
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("iot_network_test")

# --- Mock classes to simulate IoT device and network ---
@dataclass
class ConnectionEvent:
    """Represents a network connection state transition event"""
    timestamp: datetime.datetime
    event_type: str  # "activation" or "deactivation"
    reason: str

class MockIoTDevice:
    """Mock class to simulate an IoT device for testing purposes"""
    
    def __init__(self, device_id: str, config: Dict[str, Any]):
        self.device_id = device_id
        self.config = config
        self.is_powered_on = False
        self.is_registered = False
        self.connection_active = False
        self.events: List[ConnectionEvent] = []
        self.last_data_transmission = None
    
    def power_on(self) -> bool:
        """Power on the device"""
        logger.info(f"Powering on device {self.device_id}")
        self.is_powered_on = True
        return self.is_powered_on
    
    def register_to_network(self) -> bool:
        """Register the device to the mobile network"""
        if not self.is_powered_on:
            logger.error("Cannot register: Device is not powered on")
            return False
        
        logger.info(f"Registering device {self.device_id} to network")
        self.is_registered = True
        return self.is_registered
    
    def activate_connection(self, reason: str = "data_transmission") -> bool:
        """Activate network connection"""
        if not self.is_registered:
            logger.error("Cannot activate connection: Device is not registered")
            return False
        
        if self.connection_active:
            logger.warning("Connection is already active")
            return True
        
        logger.info(f"Activating network connection for {reason}")
        self.connection_active = True
        
        # Record activation event
        event = ConnectionEvent(
            timestamp=datetime.datetime.now(),
            event_type="activation",
            reason=reason
        )
        self.events.append(event)
        
        return True
    
    def deactivate_connection(self, reason: str = "idle_timeout") -> bool:
        """Deactivate network connection"""
        if not self.connection_active:
            logger.warning("Connection is already inactive")
            return True
        
        logger.info(f"Deactivating network connection due to {reason}")
        self.connection_active = False
        
        # Record deactivation event
        event = ConnectionEvent(
            timestamp=datetime.datetime.now(),
            event_type="deactivation",
            reason=reason
        )
        self.events.append(event)
        
        return True
    
    def transmit_data(self, payload: Any) -> bool:
        """Simulate data transmission"""
        if not self.connection_active:
            logger.info("Connection not active, activating for transmission")
            self.activate_connection(reason="data_transmission")
        
        logger.info(f"Transmitting data: {payload}")
        self.last_data_transmission = datetime.datetime.now()
        
        # Simulate data transmission process
        time.sleep(0.5)  # Simulate network delay
        
        return True
    
    def shutdown(self) -> bool:
        """Shut down the device"""
        if self.connection_active:
            self.deactivate_connection(reason="device_shutdown")
        
        logger.info(f"Shutting down device {self.device_id}")
        self.is_powered_on = False
        self.is_
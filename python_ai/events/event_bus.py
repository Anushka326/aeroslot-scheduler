import asyncio
from typing import Callable, Dict, List

class LightEventBus:
    """
    Decoupled Asynchronous Event Bus.
    Pushes system events preventing tight coupling across the ML, BFF, and C++ interfaces entirely natively.
    Replaces need for heavyweight Kafka/NATS during the Single-Machine prototype phase natively.
    """
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {
            "DATA_PLANE_TELEMETRY": [],
            "CONTROL_PLANE_ALERTS": [],
            "EMERGENCY_INTERRUPT": [],
            "SCHEDULER_ACK": []
        }

    def subscribe(self, topic: str, handler: Callable):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)

    async def publish(self, topic: str, event_data: dict):
        handlers = self.subscribers.get(topic, [])
        for handler in handlers:
            # Executes async mapping instantly 
            asyncio.create_task(handler(event_data))
            
event_bus = LightEventBus()

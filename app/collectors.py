import psutil
import logging
from prometheus_client import Gauge

memory_total = Gauge('memory_total_bytes', 'Total memory in bytes')
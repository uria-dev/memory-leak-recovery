from venv import logger
import psutil
import logging
from prometheus_client import Gauge

memory_total = Gauge('memory_total_percentage', 'Total memory in percentage')

logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s'
)
  
memory_threshold_percent = 80


class MemoryCollector:
  def collect_memory_metric(self):
    mem = psutil.virtual_memory()
    memory_total.set(mem.percent)
    if mem.percent > memory_threshold_percent:
        logger.error(f"Memory usage is high: {mem.percent}%")
    else:
      logger.info(f"Memory usage: {mem.percent}%")
    return mem.percent
    
    
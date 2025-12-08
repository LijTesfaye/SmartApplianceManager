import sys
from ingestion_system.src.IngestionSystemOrchestrator import IngestionSystemOrchestrator

if __name__ == '__main__':

    ingestion_system = IngestionSystemOrchestrator()
    try:
        ingestion_system.run()
    except KeyboardInterrupt:
        print("Ingestion System App terminated")
        sys.exit(0)
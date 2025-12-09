import sys
from development_system_localtest import DevelopmentSystemOrchestratorLocalhost
from development_system import DevelopmentSystemOrchestrator

if __name__ == '__main__':

    #development_system = DevelopmentSystemOrchestratorLocalhost() # for local test ONLY
    development_system = DevelopmentSystemOrchestrator()

    try:
        # Fully manual mode
        development_system.run()
        #Fully automated mode
        #development_system.run(productivity=True)
    except KeyboardInterrupt:
        print("Development App terminated")
        sys.exit(0)

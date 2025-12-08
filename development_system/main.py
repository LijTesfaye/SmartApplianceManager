import sys
from development_system.controller.development_system_localtest import DevelopmentSystemOrchestratorLocalhost

if __name__ == '__main__':

    development_system = DevelopmentSystemOrchestratorLocalhost()
    try:
        # Fully automated mode
        development_system.run()
        #Fully automated mode
        #development_system.run(productivity=True)
    except KeyboardInterrupt:
        print("Development App terminated")
        sys.exit(0)

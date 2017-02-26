__author__ = 'civa'
import time, logging, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from local.infrastructure.pipeline import Pipeline, Supervisor

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def main():
    pipeline = Pipeline('main', 'pipeline_config.json')
    pipeline.run()

    # supervisor = Supervisor('supervisor')
    # supervisor.run()

if __name__ == "__main__":
    main()
__author__ = 'civa'
import time, logging, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from local.infrastructure.pipeline import Pipeline

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def main():
    pipeline = Pipeline('main', 'pipeline_config.json')
    pipeline.run()

if __name__ == "__main__":
    main()
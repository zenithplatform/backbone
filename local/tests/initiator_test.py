__author__ = 'civa'
import time, logging, sys, multiprocessing
sys.path.append('D:\Programming\Astronomy\Dev\Zenith\src\Backend\Local')
from infrastructure.initiator import Initiator

def main():
    start_initiator_process()
    # worker_pool = range(3)
    # for wrk_num in range(len(worker_pool)):
    #     multiprocessing.Process(target=start_initiator, args=()).start()

def start_initiator_process():
    init_process = multiprocessing.Process(target=start_initiator, args=())
    init_process.daemon = True
    init_process.start()
    init_process.join()

def start_initiator():
    initiator = Initiator()
    initiator.run()

if __name__ == "__main__":
    main()


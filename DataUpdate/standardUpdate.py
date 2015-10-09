dname = os.path.dirname('../')
os.chdir(dname)

import sys
import threading
import numpy as np
sys.path.insert(0, 'DataUpdate')
from standardUpdateSlave import standardUpdateDef
sys.path.insert(0, 'SQL')
from DatabaseInteraction import DatabaseInteraction 
import time
import threading

def endGame():
    print 'And Now His Watch is Ended'

tStart = time.time()
dbInt = DatabaseInteraction('backtest_real')

#tickerList = np.loadtxt('data/tickerOverview.txt', delimiter=',', skiprows=0, usecols=(0,), unpack=False,dtype = 'str')
tickerList = dbInt.getAllTickers()

tickerListAssembly = []

targetSize = 50

a = int(len(tickerList)/targetSize) + 1
for i in range(a):
    tickerListAssembly.append(tickerList[i*targetSize:i*targetSize+targetSize])


threads = []
for i in range(len(tickerListAssembly)):
    thread = threading.Thread(target = standardUpdateDef, args = (tickerListAssembly[i],i))
    threads.append(thread)
    thread.start()
    
for thread in threads:
    thread.join()
    
print 'Total download Time:', time.time() - tStart
print 'Avg time per Stock:', (time.time() - tStart)/len(tickerList)


endGame()

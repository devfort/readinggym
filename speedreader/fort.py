from speedreader.settings import *

WAKE_ASSETS = Assets(
    wake  = os.path.join(os.getcwd(), 'node_modules', '.bin', 'wake'),
    root  = os.getcwd(),
    mode  = 'targets',
    cache = True,
)

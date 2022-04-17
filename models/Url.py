import sys
import yaml
sys.path.append('../')
from my_utils import my_utils
# from utils import Util
# from utils import *
class Url:              #class Url will be called outside combine with my_utils.py
    def __init__(self, schema, method, host, port, path, paramPath):
        self.schema = schema
        self.method = method
        self.host = host
        self.port = port
        self.path = path
        self.paramPath = paramPath
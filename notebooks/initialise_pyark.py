import os
import sys
import getpass
import pyark
from pyark.cva_client import CvaClient
from pyark.errors import CvaClientError, CvaServerError
import logging
from protocols.reports_6_0_0 import Program, Assembly
import pandas as pd
pd.options.display.float_format = '{:.3f}'.format
import matplotlib.pyplot as plt
import seaborn as sns
import cufflinks as cf
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import tools
import plotly.graph_objs as go
import numpy as np
import itertools
import warnings


warnings.filterwarnings('ignore')

init_notebook_mode(connected=True)
cf.go_offline()

# sets logging
logger = logging.getLogger()
formatter = logging.Formatter('%(message)s')
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

cva_url = os.environ.get("CVA_URL_BASE", "http://localhost:8090")
gel_user = os.environ.get("CVA_USER", None)
if not gel_user:
    gel_user = getpass.getpass("User:")
gel_password = os.environ.get("CVA_PASSWORD", None)
if not gel_password:
    gel_password = getpass.getpass("Password:")
cva = CvaClient(cva_url, user=gel_user, password=gel_password)
cases_client = cva.cases()
report_events_client = cva.report_events()
variants_client = cva.variants()
entities_client = cva.entities()
pedigrees_client = cva.pedigrees()
transactions_client = cva.transactions()
lift_overs_client = cva.lift_overs()
print("pyark version {}".format(pyark.VERSION))

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size
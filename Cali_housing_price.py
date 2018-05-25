
# The function to fetch the data

import os
import tarfile
from six.moves import urllib

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = "datasets/housing"
HOUSINGR_URL = DOWNLOAD_ROOT + HOUSING_PATH + "/housing.tgz"

def fetching_data_out (housing url = HOUSING_URL, housing path = HOUSING_PATH):
  if not os.path.isdir(

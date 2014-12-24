#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-

import logging

# log file name
LOGFILE = ''
# log format
LOGFORMAT = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'

# log object
Logger = logging.getLogger('LOGGER')

f = logging.FileHandler()
Logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOGFORMAT)
Logger.setFormatter(formatter)
Logger.addHandler(f)
#!/usr/bin/python3

import logging


def loggerGene():
   '''This function provides a simple logger object generation to other functions, especially the retryDecorator functions.'''
   logging.basicConfig(format='%(asctime)s - %(module)s.%(funcName)s - %(levelname)s - %(message)s', level=logging.INFO)
   logger = logging.getLogger(__name__)
   logging.getLogger('requests').setLevel(logging.CRITICAL) # Rule out the requests' common loggings since
                                                         # they are useless. 
   return logger
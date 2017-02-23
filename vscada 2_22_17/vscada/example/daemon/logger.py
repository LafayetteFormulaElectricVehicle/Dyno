#!/usr/bin/env python

import logging
import logging.config

logging.config.fileConfig('logging.conf')
# create logger
logger = logging.getLogger('VSCADA.logger')

logger.debug('logger program starts')

import vserver
logger.info('check TSV')
logger.info('send TSI signal')
logger.info('check motor')
logger.warn('the motor is not connected')
logger.info('start the server')
vserver.run()
logger.debug('startup program ends')


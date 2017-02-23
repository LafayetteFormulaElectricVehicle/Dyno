import logging
import time

logger = logging.getLogger('VSCADA.server')
logger.debug('server program starts')

def run():
	while 1:
		time.sleep(5)
		logger.info('I\'m a server!')
	logger.debug('server program ends')

if __name__ == '__main__':
	run()
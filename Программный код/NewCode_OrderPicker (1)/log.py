import logging

from mqtt import log_publish as mqtt_log

logfile_name = "py_log.log"
logfile_maxSize = 2<<20
logfile_count = 5

def log_init():
	logging.basicConfig(level=logging.INFO, filename=logfile_name ,filemode="w",
						format="%(asctime)s %(levelname)s %(message)s")
	logging.handlers.RotatingFileHandler(logfile_name, logfile_maxSize, logfile_count)
	#logging.debug("A DEBUG Message")
	#logging.info("An INFO")
	#logging.warning("A WARNING")
	#logging.error("An ERROR")
	#logging.critical("A message of CRITICAL severity")


def log_info(msg):
   logging.info(msg)

def log_debug(msg):
   logging.debug(msg)
	
def log_error(msg):
   logging.error(msg, exc_info=True)


def log(msg):
    log_info(msg)
    mqtt_log(msg)
	
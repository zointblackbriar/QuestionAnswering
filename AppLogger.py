import logging
from colored_logs import ColoredFormatter

# Create top level logger
log = logging.getLogger(__name__)

# Add console handler using our custom ColoredFormatter
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
cf = ColoredFormatter("[%(name)s][%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)")
ch.setFormatter(cf)
log.addHandler(ch)

# Add file handler
fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)
ff = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(ff)
log.addHandler(fh)

# Set log level
log.setLevel(logging.DEBUG)

# Log some stuff
# log.debug("app has started")
# log.info("app has started")
# log.warning("app has started")
# log.error("app has started")
# log.critical("app has started")




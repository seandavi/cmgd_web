import logging
import google.cloud.logging


client = google.cloud.logging.Client()
# Custom formatter returns a structure, than a string


class CustomFormatter(logging.Formatter):
    def format(self, record):
        logmsg = super(CustomFormatter, self).format(record)
        res = {'msg': logmsg}
        res.update(record.args)
        return res


# Setup handler explicitly -- different labels
handler = client.get_default_handler()
handler.setFormatter(CustomFormatter())

# Setup logger explicitly with this handler
logger = logging.getLogger()
logger.addHandler(handler)

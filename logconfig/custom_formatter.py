import json, logging, os

app_name = os.getenv("APP_NAME")
app_version = os.getenv("APP_VERSION")
app_lang = os.getenv("APP_LANG")


# Custom JSON Formatter
class CustomJSONFormatter(logging.Formatter):
    def format(self, record):
        formatted_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "location": "{}:{}:line {}".format(
                record.pathname, record.funcName, record.lineno
            ),
            "span ID": record.process,
            "app": {"name": app_name, "version": app_version, "language": app_lang},
        }

        if record.exc_info:
            formatted_record["exception"] = {
                "error": formatted_record.get(
                    "exception.error", record.exc_info[1].__class__.__name__
                ),
                "traceback": formatted_record.get(
                    "exception.traceback", self.formatException(record.exc_info)
                ),
            }

        return json.dumps(formatted_record)

import json, logging, os

app_name = os.getenv("APP_NAME")
app_version = os.getenv("APP_VERSION")
app_lang = os.getenv("APP_LANG")


# Custom JSON Formatter
class CustomJSONFormatter(logging.Formatter):
    def format_traceback(self, exc_info):
        _, exception_value, tb = exc_info
        traceback_info = {
            "path": tb.tb_frame.f_code.co_filename,
            "line": tb.tb_lineno,
            "location": tb.tb_frame.f_code.co_name,
            "error": str(exception_value),
        }
        return traceback_info

    def format(self, record):
        formatted_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "location": "{}:{}:line {}".format(
                record.pathname, record.funcName, record.lineno
            ),
            "span ID": record.process,
            "app": {"name": app_name, "version": app_version, "language": app_lang},
        }

        if record.exc_info:
            traceback_info = self.format_traceback(record.exc_info)
            formatted_record["exception"] = traceback_info

        return json.dumps(formatted_record, default=str)

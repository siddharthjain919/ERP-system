import sys,os,logging
import logging.handlers

class MyFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level
    
class MyLogger:
    def __init__(self, file_name='app'):
        
        if not os.path.exists('logs'):
            os.makedirs('logs')
        base_folder='logs'
        folders=file_name.replace('\\','.').replace('/','.').split('.')[:-1]
        current_folder=base_folder
        for subfolder in folders:
            current_folder = os.path.join(current_folder, subfolder)
            os.makedirs(current_folder, exist_ok=True)
        # create logger
        self.logger = logging.getLogger(file_name)
        self.logger.setLevel(logging.DEBUG)

        # Create file handlers for each log level
        debug_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(current_folder, 'debug.log'), 
            when='D', 
            interval=1, 
            backupCount=7
        )
        debug_handler.setLevel(logging.DEBUG)
        info_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(current_folder, 'info.log'), 
            when='D', 
            interval=1, 
            backupCount=7
        )
        info_handler.setLevel(logging.INFO)

        warning_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(current_folder, 'warning.log'), 
            when='D', 
            interval=1, 
            backupCount=7
        )
        warning_handler.setLevel(logging.WARNING)

        error_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(current_folder, 'error.log'), 
            when='D', 
            interval=1, 
            backupCount=7
        )
        error_handler.setLevel(logging.ERROR)

        critical_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(current_folder, 'critical.log'), 
            when='D', 
            interval=1, 
            backupCount=7
        )

        # Create formatters for each file handler
        log_format = "[%(asctime)s]-[%(levelname)s]-[%(name)s]-[%(filename)s]-[%(lineno)d]-%(message)s"

        formatter = logging.Formatter(log_format)
        debug_handler.setFormatter(formatter)
        info_handler.setFormatter(formatter)
        warning_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        critical_handler.setFormatter(formatter)

        # Add the filters to the handlers
        debug_handler.addFilter(MyFilter(logging.DEBUG))
        info_handler.addFilter(MyFilter(logging.INFO))
        warning_handler.addFilter(MyFilter(logging.WARN))
        error_handler.addFilter(MyFilter(logging.ERROR))
        critical_handler.addFilter(MyFilter(logging.CRITICAL))

        # Add the handlers to the logger object
        self.logger.addHandler(debug_handler)
        self.logger.addHandler(info_handler)
        self.logger.addHandler(warning_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(critical_handler)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        # Add console handler to the logger object
        self.logger.addHandler(console_handler)
        
    
    def get_logger(self):
        return self.logger
    

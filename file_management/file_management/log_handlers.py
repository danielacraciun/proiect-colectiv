import sqlite3
import logging
import time
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SQLiteHandler(logging.Handler):
    initial_sql = """CREATE TABLE IF NOT EXISTS log(
                        Created text,
                        Name text,
                        LogLevel int,
                        LogLevelName text,    
                        Message text,
                        Args text,
                        Module text,
                        FuncName text,
                        LineNo int,
                        Exception text,
                        Process int,
                        Thread text,
                        ThreadName text,
                        User text,
                        Document text,
                        Template text,
                        Step text,
                        Flow text
                   )"""

    insertion_sql = """INSERT INTO log(
                        Created,
                        Name,
                        LogLevel,
                        LogLevelName,
                        Message,
                        Args,
                        Module,
                        FuncName,
                        LineNo,
                        Exception,
                        Process,
                        Thread,
                        ThreadName,
                        User,
                        Document,
                        Template,
                        Step,
                        Flow
                   )
                   VALUES (
                        '%(dbtime)s',
                        '%(name)s',
                        %(levelno)d,
                        '%(levelname)s',
                        '%(msg)s',
                        '%(args)s',
                        '%(module)s',
                        '%(funcName)s',
                        %(lineno)d,
                        '%(exc_text)s',
                        %(process)d,
                        '%(thread)s',
                        '%(threadName)s',
                        '%(user)s',
                        '%(document)s',
                        '%(template)s',
                        '%(step)s',
                        '%(flow)s'
                   );
                   """

    def __init__(self, db=os.path.join(BASE_DIR, 'db.sqlite3')):
    
        logging.Handler.__init__(self)
        self.db = db
        # Create table if needed:
        conn = sqlite3.connect(self.db)
        conn.execute(SQLiteHandler.initial_sql)
        conn.commit()

    def formatDBTime(self, record):
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

    def emit(self, record):
       
        # Use default formatting:
        self.format(record)
        # Set the database time up:
        self.formatDBTime(record)
        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
        else:
            record.exc_text = ""
        # Insert log record:
        sql = SQLiteHandler.insertion_sql % record.__dict__
        conn = sqlite3.connect(self.db)
        conn.execute(sql)
        conn.commit()
from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler
from aiologger.handlers.streams import AsyncStreamHandler
from pathlib import Path
import datetime
import sys
from asyncio import Task


class Loggers(Logger):
    def __init__(self, filename: str, name: str):
        super().__init__(name=name)
        handler_file = AsyncFileHandler(filename=str(Path.cwd().joinpath(f"logs/{filename}")))
        handler_stdout = AsyncStreamHandler(stream=sys.stdout)
        self.add_handler(handler=handler_file)
        self.add_handler(handler=handler_stdout)

    def info(self, msg, *args, **kwargs) -> Task:
        msg = f"{msg}:{datetime.datetime.now()}"
        task = super(Loggers, self).info(msg=msg, *args, *kwargs)
        return task

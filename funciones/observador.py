from watchdog.events import FileSystemEventHandler
from pathlib import Path

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, cola, logger):
        self._cola = cola
        self.logger = logger
        super().__init__()

    def on_created(self, event):
        rutaCompletaArchivo = Path(event.src_path)
        self.logger.debug(f'Observador: {rutaCompletaArchivo}')
        self._cola.put(rutaCompletaArchivo)


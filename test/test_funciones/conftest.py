import pytest
from tempfile import TemporaryDirectory
from pathlib import Path
import logging

@pytest.fixture(scope="session")
def carpeta_origen():
    with TemporaryDirectory() as tmpdir:
        cOrigen = Path(tmpdir)
        yield cOrigen

@pytest.fixture(scope="session")
def carpeta_destino():
    with TemporaryDirectory() as tmpdir:
        cDestino = Path(tmpdir)
        yield cDestino

@pytest.fixture(scope="session")
def logger():
    logging.basicConfig()
    logger = logging.getLogger('My_Logger')
    logger.setLevel(logging.DEBUG)
    yield logger

@pytest.fixture(scope="session")
def dirTemp():
    with TemporaryDirectory() as tmpdir:
        carpetaTemp = Path(tmpdir)
    yield carpetaTemp
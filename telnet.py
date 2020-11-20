__all__ = [
    "connect",
]


# standard library
from logging import getLogger
from telnetlib import Telnet
from typing import Optional


# constants
ENCODING: str = "ascii"
END: str = "\n"
MODE: str = "eager"
TIMEOUT: Optional[float] = None


# module logger
logger = getLogger(__name__)


# helper features
class CustomTelnet(Telnet):
    def read(
        self,
        mode: str = MODE,
        encoding: str = ENCODING,
        **kwargs: dict,
    ) -> str:
        """Wrapper of Telnet.read_*() and returns string, not bytes."""
        received = getattr(super(), f"read_{mode}")(**kwargs)
        string = received.decode(encoding).rstrip()

        logger.info(f"{self.host}, {self.port}, {string}")
        return string

    def write(
        self,
        string: str,
        end: str = END,
        encoding: str = ENCODING,
    ) -> None:
        """Same as Telnet.write(), but accepts string, not bytes."""
        super().write((string + end).encode(encoding))
        logger.info(f"{self.host}, {self.port}, {string}")


def connect(host: str, port: int, timeout: Optional[float] = TIMEOUT) -> CustomTelnet:
    """Connect to a Telnet server and returns a custom Telnet object.

    Args:
        host: IP address or host name of the server.
        port: Port of the server.
        timeout: Timeout value in units of seconds.

    Returns:
        Custom Telnet object.

    Examples:
        To send a command to a server::

            with connect('192.168.1.3', 5000) as tn:
                tn.write('ls')

        To receive a message from a server::

            with connect('192.168.1.3', 5000) as tn:
                tn.write('ls')
                print(tn.read())

    """
    return CustomTelnet(host, port, timeout)

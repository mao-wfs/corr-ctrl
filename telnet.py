__all__ = [
    "connect",
]


# standard library
import os
import sys
from logging import basicConfig, INFO, getLogger
from logging import FileHandler, StreamHandler
from pathlib import Path
from telnetlib import Telnet
from typing import Optional


# constants
AUTO_READ: bool = True
ENCODING: str = "ascii"
END_WRITE: str = ";\n"
END_READ: str = ";\r"
KWD_COMMENT: str = "#"
KWD_QUERY: str = "?"
LOG_WIDTH: int = 100
TIMEOUT: Optional[float] = None


# module logger
logger = getLogger(__name__)


# main features
class CustomTelnet(Telnet):
    def read(self) -> str:
        """Wrapper of Telnet.read_eager() and returns string, not bytes."""
        string = self.read_eager().decode(ENCODING).rstrip(END_READ)

        logger.info(f"{self.host}:{self.port} <- {shorten(string, LOG_WIDTH)}")
        return string

    def write(self, string: str) -> None:
        """Same as Telnet.write(), but accepts string, not bytes."""
        super().write((string + END_WRITE).encode(ENCODING))
        logger.info(f"{self.host}:{self.port} -> {shorten(string, LOG_WIDTH)}")

    def write_from(self, path: Path, auto_read: bool = AUTO_READ) -> None:
        """Write line(s) written in a file and read data if exists."""
        with open(path) as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith(KWD_COMMENT):
                    continue

                self.write(line)

                if auto_read and line.endswith(KWD_QUERY):
                    self.read()


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


# helper features
def shorten(string: str, width: int, placeholder: str = "...") -> str:
    """Same as textwrap.shorten(), but compatible with string without whitespaces."""
    return string[:width] + (placeholder if string[width:] else "")


# main script
if __name__ == "__main__":
    """Mini tool to send line(s) written in a file.

    Usage:
        $ export CORR_HOST=<host name>
        $ export CORR_PORT=<port number>
        $ poetry run python telnet.py <file path>

    """
    basicConfig(
        level=INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=(StreamHandler(), FileHandler("telnet.log")),
    )

    host = os.environ["CORR_HOST"]
    port = os.environ["CORR_PORT"]
    path = sys.argv[1]

    with connect(host, port) as tn:
        tn.write_from(path)

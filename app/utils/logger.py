import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(funcName)s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename="logging.log",
    filemode="w",
)

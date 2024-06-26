from enum import StrEnum


class Headers(StrEnum):
    VERSION = 'Deplio-Version'
    FORWARD = 'Deplio-Forward'


class Environment(StrEnum):
    LOCAL = 'local'
    DEV = 'dev'
    PROD = 'prod'

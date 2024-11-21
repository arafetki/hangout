from nanoid import generate
from core.utils.constants import Constants


def nanoid() -> str:
    return generate(alphabet=Constants.NANOID_ALPHABET, size=Constants.NANOID_SIZE)
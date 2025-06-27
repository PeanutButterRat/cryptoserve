import pytest

from cryptoserve.exercises.simple_hash import simple_hash
from cryptoserve.types.errors import InvalidPaddingError
from tests.utils import run_exercise


@run_exercise([[b"abc", b"abc\x01"], [b"abc", b"abc"]])
async def test_padding_error(client):
    with pytest.raises(InvalidPaddingError):
        await simple_hash(client)

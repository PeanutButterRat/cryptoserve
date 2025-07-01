import aes


def sbox(x: int, inverse: bool = False) -> int:
    return aes.core.sbox(x) if not inverse else aes.core.rsbox(x)


def shift_rows(state: bytes, inverse: bool = False) -> bytes:
    return aes.core.shiftrows(state) if not inverse else aes.core.inv_shiftrows(state)


def mix_columns(state: bytes, inverse: bool = False) -> bytes:
    return aes.core.mixcolumns(state) if not inverse else aes.core.inv_mixcolumns(state)


def sub_bytes(state: bytes, inverse: bool = False) -> bytes:
    return aes.core.subbytes(state) if not inverse else aes.core.inv_mixcolumns(state)


def key_addition(state: bytes) -> bytes:
    return aes.core.addroundkey(state)

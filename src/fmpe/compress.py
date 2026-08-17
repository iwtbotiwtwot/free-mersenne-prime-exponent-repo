"""Deterministic Zstandard compression through the system libzstd."""
from __future__ import annotations
import ctypes, ctypes.util

LEVEL = 9

def compress(data: bytes, level: int = LEVEL) -> bytes:
    lib = ctypes.CDLL(ctypes.util.find_library("zstd"))
    lib.ZSTD_compressBound.argtypes = [ctypes.c_size_t]
    lib.ZSTD_compressBound.restype = ctypes.c_size_t
    lib.ZSTD_compress.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int]
    lib.ZSTD_compress.restype = ctypes.c_size_t
    source = ctypes.create_string_buffer(data)
    target = ctypes.create_string_buffer(lib.ZSTD_compressBound(len(data)))
    result = lib.ZSTD_compress(target, len(target), source, len(data), level)
    lib.ZSTD_isError.argtypes = [ctypes.c_size_t]
    lib.ZSTD_isError.restype = ctypes.c_uint
    if lib.ZSTD_isError(result):
        raise RuntimeError("libzstd compression failed")
    return target.raw[:result]

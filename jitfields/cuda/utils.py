import os
import torch
import numpy as np
from math import prod

_cuda_num_threads = None
_num_threads = None


def init_cuda_num_threads():
    set_cuda_num_threads(None)


def set_cuda_num_threads(n):
    globals()['_cuda_num_threads'] = n


def get_cuda_num_threads():
    return globals()['_cuda_num_threads'] or os.environ.get('CUDA_NUM_THREADS', 1024)


def init_num_threads():
    set_num_threads(None)


def set_num_threads(n):
    globals()['_num_threads'] = n


def get_num_threads():
    return globals()['_num_threads'] or torch.get_num_threads()


def get_cuda_blocks(n, max_threads_per_block=None):
    max_threads_per_block = max_threads_per_block or get_cuda_num_threads()
    return (n - 1) // max_threads_per_block + 1


def get_offset_type(*shapes):
    can_use_32b = True
    for shape in shapes:
        if prod(shape) >= np.iinfo('int32').max:
            can_use_32b = False
            break
    return np.int32 if can_use_32b else np.int64
# ----------------------------------------------------------------------------
# Copyright (c) 2018-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import numpy as np
from functools import wraps
from inspect import signature
import psutil
from biom import load_table


def _drop_undefined_samples(counts: np.ndarray, sample_ids: np.ndarray,
                            minimum_nonzero_elements: int) -> (np.ndarray,
                                                               np.ndarray):
    nonzero_elements_per_sample = (counts != 0).sum(1)
    fancy_index = np.where(
            nonzero_elements_per_sample < minimum_nonzero_elements)
    filtered_counts = np.delete(counts, fancy_index, 0)
    filtered_sample_ids = np.delete(sample_ids, fancy_index)
    return (filtered_counts, filtered_sample_ids)


def _disallow_empty_tables_passed_object(some_function):
    @wraps(some_function)
    def wrapper(*args, **kwargs):
        try:
            bound_signature = signature(some_function).bind(*args, **kwargs)
            table = bound_signature.arguments['table']
        except KeyError as ex:
            raise TypeError("The wrapped function has no parameter "
                            + str(ex) + ".")
        if table.is_empty():
            raise ValueError("The provided table object is empty")
        return some_function(*args, **kwargs)
    return wrapper


def _disallow_empty_tables_passed_filepath(some_function):
    @wraps(some_function)
    def wrapper(*args, **kwargs):
        try:
            bound_signature = signature(some_function).bind(*args, **kwargs)
            table = bound_signature.arguments['table']
        except KeyError as ex:
            raise TypeError("The wrapped function has no parameter "
                            + str(ex) + ".")
        biom_table = load_table(table)
        if biom_table.is_empty():
            raise ValueError("The provided table object is empty")
        return some_function(*args, **kwargs)
    return wrapper


def _safely_constrain_n_jobs(some_function):
    @wraps(some_function)
    def wrapper(*args, **kwargs):
        # If `Process.cpu_affinity` unavailable on system, fall back
        # https://psutil.readthedocs.io/en/latest/index.html#psutil.cpu_count
        bound_signature = signature(some_function).bind(*args, **kwargs)
        bound_signature.apply_defaults()
        try:
            n_jobs = bound_signature.arguments['n_jobs']
        except KeyError:
            raise TypeError("The _safely_constrain_n_jobs decorator may not be"
                            " applied to callables without 'n_jobs' parameter")
        try:
            cpus = len(psutil.Process().cpu_affinity())
        except AttributeError:
            cpus = psutil.cpu_count(logical=False)
        if n_jobs > cpus:
            raise ValueError('The value of n_jobs cannot exceed the'
                             ' number of processors (%d) available in'
                             ' this system.' % cpus)

        return some_function(*args, **kwargs)
    return wrapper
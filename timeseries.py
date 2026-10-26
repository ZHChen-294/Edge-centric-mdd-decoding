"""eTS construction and the original group-average eTS operation."""
import numpy as np
from scipy.stats import zscore


def build_ets(bold):
    """Return (time, edges) from already standardized (ROIs, time) BOLD.

    Edge order is np.triu_indices(n_rois, k=1). No preprocessing or
    additional normalization is performed here.
    """
    bold = np.asarray(bold)
    if bold.ndim != 2 or bold.shape[0] < 2:
        raise ValueError('Expected (ROIs, time) with at least two ROIs.')
    ts = bold.T
    u, v = np.triu_indices(bold.shape[0], k=1)
    return ts[:, u] * ts[:, v]


def average_ets(arrays):
    """Return (group average, accepted count) from an iterable of eTS arrays.

    As in the group script: float64 accumulation, per-subject temporal
    zscore (axis=0, ddof=0), nan_to_num, then a float32 mean. Arrays with
    a different shape from the first array are skipped, as in the source.
    The caller supplies the inclusion list; no subject selection occurs.
    """
    total = None
    count = 0
    for array in arrays:
        data = np.asarray(array, dtype=np.float64)
        if data.ndim != 2:
            raise ValueError('Expected (time, edges).')
        if total is None:
            total = np.zeros(data.shape, dtype=np.float64)
        normalized = np.nan_to_num(zscore(data, axis=0))
        if normalized.shape == total.shape:
            total += normalized
            count += 1
    if not count:
        raise ValueError('No accepted eTS arrays.')
    return (total / count).astype(np.float32), count

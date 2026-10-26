"""Hungarian matching of ROI participation columns to a reference."""
import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment


def align_communities(reference, target, edge_labels=None, label_base=0):
    """Return (aligned target, old-to-new mapping, aligned edge labels).

    Inputs are (ROIs, k). Matching minimizes correlation distance between
    columns, with NaN distances replaced by 2, as in the source script.
    mapping[old] = new is ZERO-BASED regardless of label_base. Optional
    edge_labels retains its declared label_base; absent labels return None.
    For the study use MDD as reference and HC as target. Individual K-means
    label identities are arbitrary until an explicit matching is applied.
    """
    reference, target = np.asarray(reference), np.asarray(target)
    if reference.ndim != 2 or reference.shape != target.shape:
        raise ValueError('Participation matrices must share (ROIs, k).')
    cost = cdist(reference.T, target.T, metric='correlation')
    if np.isnan(cost).any():
        cost = np.nan_to_num(cost, nan=2.0)
    new, old = linear_sum_assignment(cost)
    mapping = np.empty(reference.shape[1], dtype=np.int64)
    mapping[old] = new
    aligned = np.zeros_like(target)
    aligned[:, new] = target[:, old]
    labels = None
    if edge_labels is not None:
        x = np.asarray(edge_labels)
        if not np.all(np.isfinite(x)) or not np.all(x == np.floor(x)):
            raise ValueError('Labels must be finite integers.')
        x = x.astype(np.int64) - label_base
        if np.any(x < 0) or np.any(x >= mapping.size):
            raise ValueError('Label range does not match participation.')
        labels = mapping[x] + label_base
    return aligned, mapping, labels

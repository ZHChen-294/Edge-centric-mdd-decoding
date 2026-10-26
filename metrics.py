"""Incident-edge participation and Shannon entropy, without statistics."""
import numpy as np


def _labels(labels, n_rois, k, label_base):
    x = np.asarray(labels)
    if x.ndim != 1 or len(x) != n_rois * (n_rois - 1) // 2:
        raise ValueError('Edge labels must follow the strict upper triangle.')
    if not np.all(np.isfinite(x)) or not np.all(x == np.floor(x)):
        raise ValueError('Labels must be finite integers.')
    x = x.astype(np.int64) - label_base
    if k < 1 or np.any(x < 0) or np.any(x >= k):
        raise ValueError('Labels outside the declared community range.')
    return x


def _counts(labels, n_rois, k, label_base):
    x = _labels(labels, n_rois, k, label_base)
    u, v = np.triu_indices(n_rois, k=1)
    counts = np.zeros((n_rois, k), dtype=np.int64)
    for c in range(k):
        selected = x == c
        counts[:, c] = (np.bincount(u[selected], minlength=n_rois)
                        + np.bincount(v[selected], minlength=n_rois))
    return counts


def participation(labels, n_rois=123, k=10, label_base=0):
    """Return (ROIs, k): fraction of each ROI's n_rois-1 incident edges.

    K-means output uses label_base=0; bundled community labels use 1.
    This is not edge weight, functional connectivity, or a time fraction.
    """
    return _counts(labels, n_rois, k, label_base) / (n_rois - 1)


def nodal_entropy(labels, n_rois=123, k=10, label_base=0):
    """Return (normalized entropy, entropy in bits, incident-edge counts).

    H=-sum(p*log2(p)); normalized H=H/log2(k), with 0*log2(0)=0.
    K is the selected solution size (10 here), not a per-ROI label count.
    """
    counts = _counts(labels, n_rois, k, label_base)
    p = counts / counts.sum(axis=1, keepdims=True)
    terms = np.zeros_like(p)
    mask = p > 0
    terms[mask] = p[mask] * np.log2(p[mask])
    raw = -terms.sum(axis=1)
    normalized = raw / np.log2(k) if k > 1 else np.zeros(n_rois)
    return normalized, raw, counts


def network_entropy(nodal_values, network_labels):
    """Return eight ROI means in VIS,SMN,DAN,VAN,LIM,FPN,DMN,SUB order.

    nodal_values is (ROIs,) or (..., ROIs); network_labels is (ROIs,),
    integer 1..8. This averages normalized nodal entropies, NOT community
    probabilities pooled across a network.
    """
    values = np.asarray(nodal_values)
    labels = np.asarray(network_labels)
    if labels.ndim != 1 or values.shape[-1] != labels.size:
        raise ValueError('ROI dimensions do not match.')
    if set(np.unique(labels)) != set(range(1, 9)):
        raise ValueError('Expected all eight network labels 1..8.')
    return np.stack([values[..., labels == n].mean(axis=-1)
                     for n in range(1, 9)], axis=-1)


def edge_label_matrix(labels, n_rois=123, k=10, label_base=0):
    """Symmetric 1-based label matrix with zero diagonal (source format)."""
    x = _labels(labels, n_rois, k, label_base) + 1
    matrix = np.zeros((n_rois, n_rois), dtype=np.int64)
    u, v = np.triu_indices(n_rois, k=1)
    matrix[u, v] = x
    return matrix + matrix.T

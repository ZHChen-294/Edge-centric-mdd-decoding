"""The study's fixed ROI order, network mapping, and edge indexing."""
import csv
from pathlib import Path
import numpy as np

NETWORK_NAMES = ('VIS', 'SMN', 'DAN', 'VAN', 'LIM', 'FPN', 'DMN', 'SUB')


def load_roi_mapping():
    """Return tuple of dictionaries in native ROI order (IDs 1..123).

    CSV values are strings. Use int(row['network_id']) for numeric labels.
    Cerebellar parcels belong to their corresponding seven networks;
    SUB contains the 16 Tian subcortical ROIs only.
    """
    path = Path(__file__).resolve().parent.parent / 'atlas' / 'roi_mapping.csv'
    with path.open(encoding='utf-8', newline='') as stream:
        return tuple(csv.DictReader(stream))


def edge_pairs(n_rois=123):
    """Return (edges, 2) zero-based ROI indices, strict upper triangle."""
    return np.column_stack(np.triu_indices(n_rois, k=1))

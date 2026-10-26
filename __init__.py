"""Core edge-centric connectome operations; no analysis runs on import."""
from .timeseries import build_ets, average_ets
from .clustering import cluster_edges
from .metrics import participation, nodal_entropy, network_entropy, edge_label_matrix
from .alignment import align_communities
from .atlas import load_roi_mapping, edge_pairs, NETWORK_NAMES

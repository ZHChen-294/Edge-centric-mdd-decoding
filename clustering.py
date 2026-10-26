"""Original individual and group K-means parameterizations."""
import numpy as np
from sklearn.cluster import KMeans


def cluster_edges(ets, k=10, level='individual'):
    """Return (zero-based edge labels, inertia) from (time, edges) eTS.

    Individual: n_init=25, max_iter=1000, random_state=None.
    Group: init='k-means++', n_init=10, random_state=42; other defaults
    remain the estimator defaults used by the source group script.
    For group clustering supply the output of average_ets, not raw BOLD.
    """
    ets = np.asarray(ets)
    if ets.ndim != 2:
        raise ValueError('Expected (time, edges).')
    if level == 'individual':
        model = KMeans(n_clusters=k, max_iter=1000, n_init=25,
                       random_state=None)
    elif level == 'group':
        model = KMeans(n_clusters=k, init='k-means++', n_init=10,
                       random_state=42)
    else:
        raise ValueError("level must be 'individual' or 'group'.")
    model.fit(ets.T)
    return model.labels_, float(model.inertia_)

# PROJECT 6 SUBSPACE PROBE V1

## Overall Local Metrics
- digit_acc: 0.89
- carry_acc: 1.0
- exact_acc: 0.89

## Direction Alignment
- carry vs success/failure cosine: -0.8916541337966919

## Carry Direction Projection
- {'mean_label0': -20.185997009277344, 'mean_label1': 19.129840850830078, 'separation': 39.31583786010742}

## Success/Failure Direction Projection
- {'mean_label0': -13.385787010192871, 'mean_label1': 0.10812652111053467, 'separation': 13.493913531303406}

## Cross Projections
- carry_direction on success/failure labels: {'mean_label0': 10.180316925048828, 'mean_label1': -1.8515878915786743, 'separation': 12.031904816627502}
- success/failure direction on carry labels: {'mean_label0': 16.151857376098633, 'mean_label1': -18.904266357421875, 'separation': 35.05612373352051}

## Interpretation Boundary
- This probe asks whether carry and success/failure can be captured as meaningful directions in hidden space.
- It does not yet intervene causally on the subspaces themselves.

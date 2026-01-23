import sys
import os

# 👇 trỏ thẳng vào package circa thật
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))   # /app
CIRCA_PKG = os.path.join(PROJECT_ROOT, "circa")             # /app/circa
sys.path.append(CIRCA_PKG)


from collections import defaultdict
from typing import Dict, Sequence, Tuple

import networkx as nx
from sklearn.linear_model import LinearRegression

from circa.alg.ci import RHTScorer
from circa.alg.ci.anm import ANMRegressor
from circa.alg.common import Model
from circa.graph.common import StaticGraphFactory
from circa.model.case import CaseData
from circa.model.data_loader import MemoryDataLoader
from circa.model.graph import MemoryGraph, Node



def run_circa():
    # 1. Define nodes
    latency = Node("DB", "Latency")
    traffic = Node("DB", "Traffic")
    saturation = Node("DB", "Saturation")

    # 2. Define causal graph
    graph = MemoryGraph(
        nx.DiGraph(
            {
                traffic: [latency, saturation],
                saturation: [latency],
            }
        )
    )

    # 3. Assemble CIRCA model
    graph_factory = StaticGraphFactory(graph)
    scorers = [
        RHTScorer(
            regressor=ANMRegressor(regressor=LinearRegression())
        )
    ]
    model = Model(graph_factory=graph_factory, scorers=scorers)

    # 4. Prepare mock data (sẽ thay bằng data thật sau)
    mock_data = {
        latency: (10, 12, 11, 9, 100, 90),
        traffic: (100, 110, 90, 105, 200, 150),
        saturation: (5, 4, 5, 6, 90, 85),
    }

    mock_data_with_time: Dict[str, Dict[str, Sequence[Tuple[float, float]]]] = defaultdict(dict)
    for node, values in mock_data.items():
        mock_data_with_time[node.entity][node.metric] = [
            (i * 60, v) for i, v in enumerate(values)
        ]

    data = CaseData(
        data_loader=MemoryDataLoader(mock_data_with_time),
        sli=latency,
        detect_time=240,
        lookup_window=4,
        detect_window=2,
    )

    # 5. Run RCA
    scores = model.analyze(
        data=data,
        current=data.detect_time + 60
    )

    # 6. Format result for web
    return [
        {
            "entity": node.entity,
            "metric": node.metric,
            "score": score.value
        }
        for node, score in scores
    ]

"""
Copyrigth 2023 Muhammad Amrudien.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import numpy as np

class TransitionGraph:
    def __init__(self, n):
        self._matrix = np.zeros((n, n))
        self.size = n

    def link(self, src, dest, capacity=1):
        self._matrix[src][dest] += capacity

    def unlink(self, src, dest, capacity=1):
        self._matrix[src][dest] -= capacity

    def get_transition_probability(self, src, dest):
        return self._matrix[src][dest] / np.sum(self._matrix[src])
    
    def as_transition_matrix(self):
        return np.array([row / np.sum(row) for row in self._matrix]).T

def page_rank(graph: TransitionGraph):
    matrix = graph.as_transition_matrix()

    r = np.full(graph.size, 1/graph.size)

    while True:
        r_new = np.dot(matrix, r)

        if np.allclose(r, r_new):
            break

        r = r_new

    return r

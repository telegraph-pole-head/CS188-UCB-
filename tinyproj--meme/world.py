"""the world module"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from individual import Individual


@dataclass
class Culture:
    """Culture
    """
    ideology: Individual
    area: ((int, int), int, int)
    diversity: float


class World:
    """World
    """
    size: int
    population: np.ndarray

    def __init__(self, size, cultures: list[Culture] = None):
        self.size = size
        arr = np.empty((size, size))
        for i in range(size):
            for j in range(size):
                for cul in cultures:
                    match cul.area:
                        case ((x0, y0), w, h) if x0 <= i < x0+w and y0 <= j <= y0+h:
                            arr[i, j] = cul.ideology.diverse_individual(
                                (i, j), cul.diversity)
                            break
                        case _:
                            continue
                else:
                    arr[i, j] = np

        self.population = arr

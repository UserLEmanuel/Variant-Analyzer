from dataclasses import dataclass


@dataclass
class Variant:
    chromosome: str
    position: int
    reference: str
    alternative: str
    quality: float
    filter: str
    type: str
import random

from typing import Optional, Sequence

class Individual:
    def __init__(self: 'Individual', chromosome: Optional[Sequence[bool]] = None, chromosome_length: Optional[int] = None):
        if chromosome is not None:
            self.chromosome = chromosome[:chromosome_length] if chromosome_length is not None else chromosome
        elif chromosome_length is not None:
            self.chromosome = [random.choice([False, True]) for _ in range(chromosome_length)]
        else:
            self.chromosome = []

    def mutate(self: 'Individual'):
        return Individual([not gene for gene in self.chromosome])

    def crossover(self: 'Individual', other: 'Individual'):
        crossover_point = random.randint(1,len(self.chromosome)-1)
        first_childern = self.chromosome[:crossover_point] + other.chromosome[crossover_point:]
        second_childern = other.chromosome[:crossover_point] + self.chromosome[crossover_point:]

        return Individual(first_childern), Individual(second_childern)
    
    def __item__(self: 'Individual', index: int):
        return self.chromosome[index]


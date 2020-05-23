import json
import os


class Config:
    def __init__(self):
        self.selection = 0.2
        self.crossover = 0.5
        self.population = 1000
        self.top = 20
        self.generations = 100
        self.fps = 24
        self.mutation = 0.05
        self.width = 10
        self.height = 20
        self.seed = 2040
        self.tile = 20

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

    def save(self, filename='config/config.json'):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as jsonfile:
            json.dump(self.__dict__, jsonfile)

    @staticmethod
    def load(filename='config/config.json'):
        with open(filename) as jsonfile:
            data = json.load(jsonfile)
            config = Config()
            config.update(**data)
        return config

    def __str__(self):
        return (f'Population: {self.population} Top: {self.top} FPS: {self.fps}'
                f' Generation: {self.generations} Mutation: {self.mutation}'
                f' Selection: {self.selection} Crossover: {self.crossover}'
                f' Seed: {self.seed} Tile: {self.tile}'
                f' Width: {self.width} Height: {self.height}')

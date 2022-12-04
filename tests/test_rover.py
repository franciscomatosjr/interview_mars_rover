import os

import pytest
from pytest import mark
from os import getenv
from logger_python.logger_python import logger
from app.controller.mars_rover import Rover

rover_count = 2

logger.debug("orientation list")
orient = ['N', 'E', 'S', 'W']

logger.debug("movement of rovers, 1 grid point")
move = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}

logger.debug("commands sent to rovers")
instructions = {'L': 'tleft', 'R': 'tright', 'M': 'move'}

class TestClass:

    def test_rover_executar_arquivo_automatico(self):



        file = 'enhanced/input.txt'

        data = []

        logger.debug("get rover count")
        num_lines = sum(1 for line in open(file)) - 1

        logger.debug("get rover count")
        rover_count = int(num_lines / 2)

        logger.debug("get each line in input file and store to data")
        for line in open(file):
            data.append(line.rstrip())

        logger.debug("first line will always be grid size - we know this")
        xmax, ymax = map(int, data[0].split())
        intersection = set([])
        results = []
        check_coords = []

        logger.debug("count_a for rover_count for loop")
        count_a = 1

        logger.debug("count_b for instructions for loop")
        count_b = 2
        for _ in range(rover_count):
            x, y, bearing = data[count_a].split()
            count_a += 2

            logger.debug("check to see that you havent deployed rovers with the same coordinates")
            if [x, y, bearing] not in check_coords:
                check_coords.append([x, y, bearing])
                rover = Rover(int(x), int(y), xmax, ymax, bearing, intersection)

                logger.debug("iterate over instructions string")
                for i in data[count_b]:
                    if i not in 'MRL':

                        logger.debug("exit if not valid instruction")
                        print('invalid instruction "%s": use M or R or L - please try again' % i)
                        exit()
                    else:
                        logger.debug("store and run instructions")
                        getattr(rover, instructions[i])()
                count_b += 2
                intersection.add((rover.x, rover.y))
                results.append((rover.x, rover.y, rover.bearing))
            else:
                print('2 or more of your rovers share the same spot, please try again')
                exit()

        entrada = results

        esperado = [(1, 3, 'N'), (5, 1, 'E')]

        assert entrada == esperado


if __name__ == '__main__':
    teste = TestClass()
    resultado = teste.test_rover_executar_arquivo_automatico()
    print(resultado)

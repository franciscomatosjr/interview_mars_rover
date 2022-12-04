#!/usr/bin/python3
from logger_python.logger_python import logger
import argparse

import os.path

logger.debug("initialise global variables")
logger.debug("amount of rovers that landed")

rover_count = 2

logger.debug("orientation list")
orient = ['N', 'E', 'S', 'W']

logger.debug("movement of rovers, 1 grid point")
move = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}

logger.debug("commands sent to rovers")
instructions = {'L': 'tleft', 'R': 'tright', 'M': 'move'}

class Rover:
    """
    Description: calculate and return position of rovers based on input parameters
    """

    def __init__(self, x, y, xmax, ymax, bearing, intersection):

        logger.debug("Description: initialise parameters")

        self.x = x
        self.y = y
        self.xmax = xmax
        self.ymax = ymax
        self.bearing = bearing
        self.intersection = set(intersection)

    def tright(self):
        """
        Description: turning right method
        """
        self.bearing = orient[(orient.index(self.bearing) + 1) % len(orient)]

    def tleft(self):
        """
        Description: turning left method
        """
        self.bearing = orient[(orient.index(self.bearing) - 1) % len(orient)]

    def move(self):
        """
        Description: moving forward 1 grid point method
        """
        xmod = self.x + move[self.bearing][0]
        ymod = self.y + move[self.bearing][1]

        logger.debug("check intersection to see if nrover is not the same position as mrover")

        if (xmod, ymod) not in self.intersection:
            if xmod <= self.xmax and xmod >= 0:
                self.x = xmod
            if ymod <= self.ymax and ymod >= 0:
                self.y = ymod
            else:
                print("Out of bounds, please try again!!")
                exit()
        else:
            print("rovers cannot occupy the same spot, try again!!")
            exit()


if __name__ == '__main__':

    logger.debug("store auto/manual choice in variable")
    file_name = None

    try:
        args = argparse.ArgumentParser()
        args.add_argument('--type', help='manual override or auto')
        args.add_argument('--file_name', help='manual override or auto')
        parsed_args = args.parse_args()

        auto = parsed_args.type
        file_name = parsed_args.file_name

    except:
        auto = input('Manual override or Auto? Enter (A | auto) or (M | manual)\n')


    logger.debug("check to see if choice is correct")

    try:

        if auto in ['A', 'auto']:

            logger.debug("add file with instructions to input")
            if file_name:
                file = r'../../enhanced/'+file_name
            else:
                file = input('Select file name(make sure file is in this directory):\n')
                file = r'../../enhanced/' + file

            logger.debug("check if file exists")
            if os.path.exists(file):

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
                for x, y, z in results:
                    print(x, y, z)
            else:
                #print('file does not exist, make sure file is in this directory)')
                raise Exception('file does not exist, make sure file is in this directory)')
        elif auto in ['M', 'manual']:

            rover_count = int(input('How many rovers would you like to deploy?:'))

            logger.debug("get grid size from input")
            xmax, ymax = map(int, input('Enter grid size:\n').split())

            logger.debug("initialise intersection rovers soon to be positions")
            intersection = set([])
            check_coords = []
            results = []

            logger.debug("count_a for rover_count for loop")
            count_a = 1

            logger.debug("count_b for instructions for loop")
            count_b = 1

            logger.debug("iterate over rover count")
            for _ in range(rover_count):

                logger.debug("get rover coordinates and NESW bearing")
                x, y, bearing = input('coordinates for rover %d:\n' % count_a).split()
                count_a += 1

                logger.debug("check to see that you have not deployed rovers with the same coordinates")
                if [x, y, bearing] not in check_coords:

                    check_coords.append([x, y, bearing])
                    rover = Rover(int(x), int(y), xmax, ymax, bearing, intersection)

                    logger.debug("iterate over instructions string")

                    for i in input('instructions for rover %d:\n' % count_b):

                        if i not in 'MRL':

                            logger.debug("exit if not valid instruction")
                            print('invalid instruction "%s": use M or R or L - please try again' % i)
                            exit()
                        else:

                            logger.debug("store and run instructions")
                            getattr(rover, instructions[i])()
                    count_b += 1

                    logger.debug("add nrovers coords to intersection")
                    intersection.add((rover.x, rover.y))
                    results.append((rover.x, rover.y, rover.bearing))
                else:
                    print('2 or more of your rovers share the same spot, please try again')
                    exit()

            logger.debug("print results")
            for x, y, z in results:
                print(x, y, z)
        else:
            print('Are you sure you typed the correct choice? Enter (A | auto) or (M | manual)')
            exit()
    except Exception as err:
        logger.exception("Ocurred on error while execution program.", err, exc_info=True)

# all the logic for the actual creating of stuff

from PIL import Image
import random

from loggingAndOutput import Logging
Logging = Logging(False)

from statics import materials
from statics import chanceOfDecoration
from statics import decorationWeights
class Creation:
    def __init__(self):
        self.blockSize = None
        self.blocksWidth = None
        self.blocksHeight = None
        self.imgName = None
        self.imgWidth = None
        self.imgHeight = None
        self.generationIterations = None
        self.material = None
        self.continuousBorders = None

    # return RGB code for the selected material, with a randomization fuzzing
    def fuzzMaterialRGB(self, material):
        RGB = materials[material]
        materialRGB_randomized = [RGB[0]+random.randint(-15,15),
                                  RGB[1]+random.randint(-15,15),
                                  RGB[2]+random.randint(-15,15)]

        return materialRGB_randomized


    # draw a wall
    def wall(self, floorType, orientation):
        # generate a new image for this block
        blockImg = Image.new("RGB", (self.blockSize, self.blockSize), "black")  # Create a new black image
        block = blockImg.load()  # Create the pixel map
        block = self.fill(floorType)

        # specify that this is, in fact, a wall
        wallType = floorType + "Wall"

        # wall coloring + orientation
        if orientation == 'h':
            # wall
            for x in range(self.blockSize):
                for y in range(round(2 * self.blockSize / 5), round(3 * self.blockSize / 5)):
                    RGB = self.fuzzMaterialRGB(wallType)

                    # create borders of wall
                    if y == round(2 * self.blockSize / 5) or y == round(3 * self.blockSize / 5) - 1:
                        RGB = [abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10)]

                    block[x, y] = (RGB[0], RGB[1], RGB[2])

        elif orientation == 'v':
            # wall
            for y in range(self.blockSize):
                for x in range(round(2 * self.blockSize / 5), round(3 * self.blockSize / 5)):
                    RGB = self.fuzzMaterialRGB(wallType)

                    # create borders of wall
                    if x == round(2 * self.blockSize / 5) or x == round(3 * self.blockSize / 5) - 1:
                        RGB = [abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10)]

                    block[x, y] = (RGB[0], RGB[1], RGB[2])

        # corner... this'll be fun uwu
        elif orientation == 'c':
            for x in range(self.blockSize):
                for y in range(round(2 * self.blockSize / 5), round(3 * self.blockSize / 5)):
                    RGB = self.fuzzMaterialRGB(wallType)

                    # create borders of wall
                    if y == round(2 * self.blockSize / 5) or \
                            y == round(3 * self.blockSize / 5) - 1 or \
                            x == round(2 * self.blockSize / 5) or \
                            x == round(3 * self.blockSize / 5) - 1:
                        RGB = [abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10)]

                    block[x, y] = (RGB[0], RGB[1], RGB[2])

            for x in range(round(2 * self.blockSize / 5), round(3 * self.blockSize / 5)):
                for y in range(self.blockSize):
                    RGB = self.fuzzMaterialRGB(wallType)

                    # create borders of wall
                    if y == round(2 * self.blockSize / 5) or \
                            y == round(3 * self.blockSize / 5) - 1 or \
                            x == round(2 * self.blockSize / 5) or \
                            x == round(3 * self.blockSize / 5) - 1:
                        RGB = [abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10)]

                    block[x, y] = (RGB[0], RGB[1], RGB[2])

        # add decoration... maybe
        block = self.decoration('', floorType, block)

        return block

    # generate an area that is filled in
    def fill(self, material):
        # generate a new image for this block
        blockImg = Image.new("RGB", (self.blockSize, self.blockSize), "black")  # Create a new black image
        block = blockImg.load()  # Create the pixel map

        # populate this new block
        for i in range(self.blockSize):
            for j in range(self.blockSize):
                # import the RGB data for the selected material (this is randomized with narrow area)
                RGB = self.fuzzMaterialRGB(material)

                # create borders of block
                if i == self.blockSize-1 or j == self.blockSize-1 or i == 0 or j == 0:
                    RGB = [abs(RGB[0]-10), abs(RGB[1]-10), abs(RGB[2]-10)]

                block[i,j] = (RGB[0], RGB[1], RGB[2])

        #blockImg.show()
        return block

    # create a tree
    def tree(self, type, floorType):
        # generate a new image for this block
        blockImg = Image.new("RGB", (self.blockSize, self.blockSize), "black")  # Create a new black image
        block = blockImg.load()  # Create the pixel map
        block = self.fill(floorType)

        # create... basically a circle
        for x in range(self.blockSize):
            for y in range(self.blockSize):
                RGB = self.fuzzMaterialRGB('plant')
                # (x-h)2 + (y-k)2 = r2
                if ((x-round(self.blockSize/2))**2 + (y-round(self.blockSize/2))**2) <= round(self.blockSize/3)**2:
                    block[x, y] = (RGB[0], RGB[1], RGB[2])

        return block

    # create a plant
    def decoration(self, type, backgroundColor, block):

        # probability and implementation for decoration
        if not random.choices([1, 0], cum_weights=[chanceOfDecoration, 1 - chanceOfDecoration], k=1)[0]:
            return block

        decorationSize = round(self.blockSize / 4)
        decorationX, decorationY = random.randint(0, self.blockSize - decorationSize-1), random.randint(0, self.blockSize - decorationSize-1)


        # generate a new image for this block
        decorationWidth, decorationHeight = round(decorationSize), round(decorationSize)
        blockImg = Image.new("RGB", (decorationWidth, decorationHeight), "black")  # Create a new black image
        decorationBlock = blockImg.load()  # Create the pixel map

        # on the fly calculate the weights for generating different types of decorations
        decorWeights = []
        decors = []
        for decor in decorationWeights:
            Logging.log(f'decor = {decor}, value = {decorationWeights[decor]}', '\n')
            decors.append(decor)
            decorWeights.append(decorationWeights[decor])
        decoration = random.choices(decors, weights=decorWeights)[0]
        Logging.log(f'decoration is... {decoration}','\n')

        if decoration == 'plant':
            # populate this new block
            for x in range(decorationWidth):
                for y in range(decorationHeight):
                    # import the RGB data for the selected material (this is randomized with narrow area)
                    RGB = self.fuzzMaterialRGB('plant')

                    # (x-h)2 + (y-k)2 = r2
                    if ((x - round(decorationSize / 2)) ** 2 + (y - round(decorationSize / 2)) ** 2) <= round(
                            decorationSize / 2) ** 2:
                        decorationBlock[x, y] = (RGB[0]+10, RGB[1]+10, RGB[2]+10)
                    else:
                        backgroundColorRGB = self.fuzzMaterialRGB(backgroundColor)
                        decorationBlock[x, y] = (backgroundColorRGB[0], backgroundColorRGB[1], backgroundColorRGB[2])

        if decoration == 'chest':
            chestHeight = round(3 * decorationHeight / 4)
            stoneColor = materials['stone']
            # populate this new block
            for x in range(decorationWidth):
                for y in range(decorationHeight):
                    # import the RGB data for the selected material (this is randomized with narrow area)
                    RGB = self.fuzzMaterialRGB('chest')

                    if (y < chestHeight ):
                        decorationBlock[x, y] = (RGB[0] + 10, RGB[1] + 10, RGB[2] + 10)
                    else:
                        backgroundColorRGB = self.fuzzMaterialRGB(backgroundColor)
                        decorationBlock[x, y] = (backgroundColorRGB[0], backgroundColorRGB[1], backgroundColorRGB[2])
                    if(y<chestHeight+round(2 * decorationHeight / 10)
                            and y>chestHeight-round(2 * decorationHeight / 10)
                            and x<round((decorationHeight/2) + (2 * decorationHeight / 10))
                            and x>round((decorationHeight/2) - (2 * decorationHeight / 10)) ):
                        decorationBlock[x,y] = (stoneColor[0], stoneColor[1], stoneColor[2])

        for x in range(decorationSize):
            for y in range(decorationSize):
                block[decorationX + x, decorationY + y] = decorationBlock[x, y]

        return block

    # create a doorway
    def door(self, floorType, orientation):
        # generate a new image for this block
        blockImg = Image.new("RGB", (self.blockSize, self.blockSize), "black")  # Create a new black image
        block = blockImg.load()  # Create the pixel map
        block = self.fill(floorType)

        # specify that this is, in fact, a wall
        wallType = floorType+"Wall"

        # wall coloring + orientation
        if orientation == 'h':
            #wall
            for x in list(range(round(2 * self.blockSize / 5))) + \
                     list(range( round(3 * self.blockSize / 5), self.blockSize)):
                for y in range(round(2 * self.blockSize / 5), round(3 * self.blockSize / 5)):
                    RGB = self.fuzzMaterialRGB(wallType)

                    # create borders of wall
                    if y == round(2 * self.blockSize / 5) or y == round(3 * self.blockSize / 5 ) - 1:
                        RGB = [abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10)]

                    block[x, y] = (RGB[0], RGB[1], RGB[2])

            # door
            for x in range(round(2 * self.blockSize / 5), round(3 * self.blockSize / 5)):
                for y in range(round(23 * self.blockSize / 50), round(27 * self.blockSize / 50)):
                    RGB = materials[wallType]
                    RGB = [abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10)]
                    block[x, y] = (RGB[0], RGB[1], RGB[2])


        # logic for vertical orientation
        if orientation == 'v':
            #wall
            for y in list(range(round(2 * self.blockSize / 5))) + \
                     list(range( round(3 * self.blockSize / 5), self.blockSize)):
                for x in range(round(2 * self.blockSize / 5), round(3 * self.blockSize / 5)):
                    RGB = self.fuzzMaterialRGB(wallType)

                    # create borders of wall
                    if x == round(2 * self.blockSize / 5) or x == round(3 * self.blockSize / 5 ) - 1:
                        RGB = [abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10)]

                    block[x, y] = (RGB[0], RGB[1], RGB[2])

            # door
            for y in range(round(2 * self.blockSize / 5), round(3 * self.blockSize / 5)):
                for x in range(round(23 * self.blockSize / 50), round(27 * self.blockSize / 50)):
                    RGB = materials[wallType]
                    RGB = [abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10)]
                    block[x, y] = (RGB[0], RGB[1], RGB[2])

        # add decoration... maybe
        block = self.decoration('', floorType, block)

        return block

    # generate a road
    def road(self, type, orientation):
        # generate a new image for this block
        blockImg = Image.new("RGB", (self.blockSize, self.blockSize), "black")  # Create a new black image
        block = blockImg.load()  # Create the pixel map

        # after a bit of thinking, a road is just a stone-filled area... basically
        block = self.fill(type)
        # get color data for the material
        RGB = materials[type]

        # sidewalk details for horizontal ('h') and vertical ('v') orientations
        if orientation == 'h':
            # add road details
            for x in range(self.blockSize):
                for y in range(round(self.blockSize/5)):
                    block[x, y] = (abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10))

                for y in range(round(4 * self.blockSize / 5), self.blockSize):
                    block[x, y] = (abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10))

        elif orientation == 'v':
            # add road details
            for y in range(self.blockSize):
                for x in range(round(self.blockSize/5)):
                    block[x, y] = (abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10))

                for x in range(round(4 * self.blockSize / 5), self.blockSize):
                    block[x, y] = (abs(RGB[0] - 10), abs(RGB[1] - 10), abs(RGB[2] - 10))


        return block

    # after a bit of consideration... a floor is just a wood-filled area
    def floor(self, type):
        block = self.fill(type)
        return block

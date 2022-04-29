import re

def getWidth(string):
    x = string.split(" x ")
    width = str((x[0]))
    return width

def getHeight(string):
    x = string.split(" x ")
    height = str((x[1]))
    return height

def getDepth(string):
    x = string.split(" x ")
    depth = str((x[2]))
    return depth
#!/usr/bin/python
#Filename hw1.py
from collections import deque
import sys
DEBUG = 1
row = []
def init_board(row):
    row = []
    task = row[0]
    palyer = row[1]
    cutoff_depth = row[2]
    grid_value_1 = row[3].split(' ')
    grid_value_2 = row[4].split(' ')
    grid_value_3 = row[5].split(' ')
    grid_value_4 = row[6].split(' ')
    grid_value_5 = row[7].split(' ')
    cur_state_1 = row[8]
    cur_state_2 = row[9]
    cur_state_3 = row[10]
    cur_state_4 = row[11]
    cur_state_5 = row[12]
    size = len(grid_value_1)



def update_grid(self, position):
    return self.position
def greedy(board, player):
    if player == '1':
        board.update_pit()

class Board():
    def __init__(self, size, p1_score, p2_score, pit_array):
        self.size = size
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.pit_array = []
class grid(object):
    def __init__(self, position, stone):
        self.position = position
        self.stone = stone

    def get_stone(self):
        return self.stone

    def update_grid(self, num):
        self.stone += num

    def clear_stone(self):
        self.stone = 0

    def get_postion(self):
        return self.position

    def __repr__(self):
        return self.position

    def __cmp__(self, obj):
        return cmp(self.position, obj)

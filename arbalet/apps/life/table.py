from random import randint, uniform, choice


class Table:

    def __init__(self, height, width, rand_max, table=None):
        if table:
            self.table = table
            self.height = len(table)
            self.width = len(table[0])
        else:
            self.table = []
            self.height = height
            self.width = width
            for y in range(0,self.height):
                self.table.append([])
                for x in range(0,self.width):
                    rand = randint(0,rand_max)
                    if rand == 0:
                        self.table[y].append(1)
                    else:
                        self.table[y].append(0)

    def draw(self, screen):
        """(Re)draw table to screen."""
        y = 0
        x = 0
        for row in self.table:
            for col in row:
                if col == 0:
                    screen.addstr(y, x, ".")
                else:
                    screen.addstr(y, x, "o")
                x = x + 1
            y = y + 1
            x = 0

    def liveNeighbours(self, y, x):
        """Returns the number of live neighbours."""
        count = 0
        if y > 0:
            if self.table[y-1][x]:
                count = count + 1
            if x > 0:
                if self.table[y-1][x-1]:
                    count = count + 1
            if self.width > (x + 1):
                if self.table[y-1][x+1]:
                    count = count + 1

        if x > 0:
            if self.table[y][x-1]:
                count = count + 1
        if self.width > (x + 1):
            if self.table[y][x+1]:
                count = count + 1

        if self.height > (y + 1):
            if self.table[y+1][x]:
                count = count + 1
            if x > 0:
                if self.table[y+1][x-1]:
                    count = count + 1
            if self.width > (x + 1):
                if self.table[y+1][x+1]:
                    count = count + 1

        return count

    def turn(self):
        """Turn"""
        nt = copy.deepcopy(self.table)
        for y in range(0, self.height):
            for x in range(0, self.width):
                neighbours = self.liveNeighbours(y, x)
                if self.table[y][x] == 0:
                    if neighbours == 3:
                        nt[y][x] = 1
                else:
                    if (neighbours < 2) or (neighbours > 3):
                        nt[y][x] = 0
        self.table = nt

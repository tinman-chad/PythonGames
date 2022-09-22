class Piece(object):
    rows = 20
    columns = 10

    def __init__(self, column, row, shape, color):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = color
        self.rotation = 0 # direction of rotation (0 to 3 * 90 degrees)
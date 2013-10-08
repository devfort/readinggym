class PieceParser(object):

    def __init__(self, source):
        for line in source:
            if line.startswith("Title: "):
                self.title = line.split(" ", 1)[1].strip()

import tkinter as tk
SQUARE_SIZE = 90
WHITE_TO_MOVE = True
WHITE_CHECK = False
BLACK_CHECK = False
WHITE_CHECK_MAT = False
BLACK_CHECK_MAT = False
O_O_BLACK = True
O_O_WHITE = True
O_O_O_BLACK = True
O_O_0_WHITE = True


def is_in(elem,tab):
    for t in tab:
        if elem==t:
            return True
    return False

def code(x,y):
    return "ABCDEFGH"[x]+str(8-y)
def is_valide(x,y):
    return x>=0 and x<8 and y>=0 and y<8

def left_clic(event):
    global chess,canvas
    if Piece.is_selected is None:
        piece = chess.square(code(event.x//SQUARE_SIZE,event.y//SQUARE_SIZE)).piece
        if piece is not None and piece.movement_allowed():
            Piece.is_selected = piece
            piece.accessible_squares = piece.find_accessible_squares()
            Piece.is_selected_draw = canvas.create_rectangle(piece.square.coords[0]*SQUARE_SIZE,
                                                             piece.square.coords[1]*SQUARE_SIZE,
                                                            (piece.square.coords[0]+1)*SQUARE_SIZE,
                                                             (piece.square.coords[1] + 1) * SQUARE_SIZE,
                                                             width=5,outline='darkgreen')
    else:
        codeto = "ABCDEFGH"[event.x//SQUARE_SIZE]+str(8-(event.y//SQUARE_SIZE))
        codefrom = Piece.is_selected.square.name
        if codefrom == codeto:
            Piece.is_selected = None
            canvas.delete(Piece.is_selected_draw)
            Piece.is_selected_draw = None
        else:
            if Piece.is_selected.can_go_to(codeto):
                if Piece.is_selected.move(chess.square(codeto)):
                    Piece.is_selected = None
                    canvas.delete(Piece.is_selected_draw)
                    Piece.is_selected_draw = None







fenetre = tk.Tk()
fenetre.title("Whites to move !")
canvas = tk.Canvas(fenetre, width=SQUARE_SIZE*8, height=SQUARE_SIZE*8)
canvas.bind("<Button-1>", left_clic)
canvas.pack()






class Square:
    def __init__(self,coords):
        self.coords = coords
        self.name = "ABCDEFGH"[self.coords[0]] + str(8 - self.coords[1])
        self.piece = None
        if (self.coords[0]+self.coords[1])%2:
            self.color = "black"
            self.pic = tk.PhotoImage(file="emptyb.gif")
        else:
            self.color = "white"
            self.pic = tk.PhotoImage(file="emptyw.gif")
        self.draw = canvas.create_image(SQUARE_SIZE * self.coords[0]+SQUARE_SIZE/2, SQUARE_SIZE * self.coords[1]+SQUARE_SIZE/2, image=self.pic)

    def toString(self):
        if self.piece == None:
            tmp = "is empty."
        else:
            tmp = "contains a "+self.piece.color+" "+self.piece.type+"."
        print(self.name+" Square is "+self.color+" and "+tmp)
        pass

    def set_piece(self,piece):
        self.piece = piece
        self.pic = tk.PhotoImage(file=str(self.piece.type+self.piece.color[0]+self.color[0]+".gif"))
        canvas.delete(self.draw)
        self.draw = canvas.create_image(SQUARE_SIZE*self.coords[0]+SQUARE_SIZE/2,SQUARE_SIZE*self.coords[1]+SQUARE_SIZE/2,
                                        image=self.pic)

    def rmv_piece(self):
        self.piece = None
        canvas.delete(self.draw)
        if (self.coords[0] + self.coords[1]) % 2:
            self.color = "black"
            self.pic = tk.PhotoImage(file="emptyb.gif")
        else:
            self.color = "white"
            self.pic = tk.PhotoImage(file="emptyw.gif")
        self.draw = canvas.create_image(SQUARE_SIZE * self.coords[0] + SQUARE_SIZE / 2,
                                        SQUARE_SIZE * self.coords[1] + SQUARE_SIZE / 2,
                                        image=self.pic)

class Piece:
    is_selected = None
    is_selected_draw = None
    pieces = []
    def __init__(self,type,color,square):
        self.type = type
        self.color = color
        self.square = square
        square.set_piece(self)
        self.draw = None
        Piece.pieces.append(self)
        self.accessible_squares = self.find_accessible_squares()

    def find_accessible_squares(self):
        loc = []
        x, y = self.square.coords
        if self.type == "king":
            for i in range(3):
                for j in range(3):
                    x2,y2 = x+i-1,y+j-1
                    if is_valide(x2,y2) and (i!=1 or j!=1):
                        if chess.square(code(x2, y2)).piece is None:
                            loc.append(chess.square(code(x2, y2)))
                        else:
                            if chess.square(code(x2,y2)).piece.color != self.color:
                                loc.append(chess.square(code(x2,y2)))
        if self.type == "knight":
            cases = [[x - 2, y - 1], [x - 2, y + 1], [x - 1, y - 2], [x - 1, y + 2], [x + 1, y - 2], [x + 1, y + 2],
                     [x + 2, y - 1], [x + 2, y + 1]]
            for case in cases:
                x2, y2 = case
                if is_valide(x2, y2):
                    if chess.square(code(x2, y2)).piece is None:
                        loc.append(chess.square(code(x2, y2)))
                    else:
                        if chess.square(code(x2, y2)).piece.color != self.color:
                            loc.append(chess.square(code(x2, y2)))
        if self.type == "pawn":
            if self.color == "black":
                if y!=7:
                    if chess.square(code(x, y+1)).piece is None:
                        loc.append(chess.square(code(x, y+1)))
                        if y==1:
                            if chess.square(code(x, y + 2)).piece is None:
                                loc.append(chess.square(code(x, y + 2)))
                if is_valide(x+1,y+1):
                    if chess.square(code(x+1, y+1)).piece is not None:
                        if chess.square(code(x+1, y + 1)).piece.color != self.color:
                            loc.append(chess.square(code(x+1, y + 1)))
                if is_valide(x -1, y + 1):
                    if chess.square(code(x - 1, y + 1)).piece is not None:
                        if chess.square(code(x - 1, y + 1)).piece.color != self.color:
                            loc.append(chess.square(code(x - 1, y + 1)))

            if self.color == "white":
                if y != 0:
                    if chess.square(code(x, y - 1)).piece is None:
                        loc.append(chess.square(code(x, y - 1)))
                        if y == 6:
                            if chess.square(code(x, y - 2)).piece is None:
                                loc.append(chess.square(code(x, y - 2)))
                if is_valide(x + 1, y - 1):
                    if chess.square(code(x + 1, y - 1)).piece is not None:
                        if chess.square(code(x + 1, y - 1)).piece.color != self.color:
                            loc.append(chess.square(code(x + 1, y - 1)))
                if is_valide(x - 1, y - 1):
                    if chess.square(code(x - 1, y - 1)).piece is not None:
                        if chess.square(code(x - 1, y - 1)).piece.color != self.color:
                            loc.append(chess.square(code(x - 1, y - 1)))

        if self.type =="bishop" or self.type =="queen":
            for sensx in [-1,1]:
                for sensy in [-1,1]:
                    i = x+sensx
                    j = y+sensy
                    ok = True
                    while ok:
                        if is_valide(i,j):
                            if chess.square(code(i,j)).piece is None:
                                loc.append(chess.square(code(i,j)))
                                i += sensx
                                j += sensy
                            else:
                                ok = False
                                if chess.square(code(i,j)).piece.color != self.color:
                                    loc.append(chess.square(code(i, j)))
                        else:
                            ok = False

        if self.type == "rook" or self.type == "queen":
            for k in range(4):
                sensx = [1, 0, -1, 0][k]
                sensy = [0, 1, 0, -1][k]
                i = x + sensx
                j = y + sensy
                ok = True
                while ok:
                    if is_valide(i, j):
                        if chess.square(code(i, j)).piece is None:
                            loc.append(chess.square(code(i, j)))
                            i += sensx
                            j += sensy
                        else:
                            ok = False
                            if chess.square(code(i, j)).piece.color != self.color:
                                loc.append(chess.square(code(i, j)))
                    else:
                        ok = False







        return loc



    def movement_allowed(self):
        global WHITE_TO_MOVE
        if (WHITE_TO_MOVE and self.color =="white") or (not(WHITE_TO_MOVE) and self.color =="black"):
            return True

    def can_go_to(self,code):
        global chess
        return is_in(chess.square(code),self.accessible_squares)

    def toString(self):
        print("This piece is a "+self.color+" "+self.type+" on "+self.square.name+".")

    def move(self,square):
        square2 = square
        global WHITE_TO_MOVE,BLACK_CHECK,WHITE_CHECK
        re_add_piece = False
        if square.piece is not None:
            re_add_piece = True
            piece_save = square.piece
        square_save = self.square
        self.square.rmv_piece()
        self.square = square
        square.set_piece(self)
        if re_add_piece:
            Piece.pieces.remove(piece_save)
        BLACK_CHECK, WHITE_CHECK = False, False
        for piece in Piece.pieces:
            piece.accessible_squares = piece.find_accessible_squares()
            color = piece.color
            for square in piece.accessible_squares:
                if square.piece is not None:
                    if square.piece.type == "king" and square.piece.color != color:
                        if color =="white":
                            BLACK_CHECK=True
                        else:
                            WHITE_CHECK=True




        if (not(WHITE_TO_MOVE) and BLACK_CHECK) or (WHITE_TO_MOVE and WHITE_CHECK):
            self.square.rmv_piece()
            if re_add_piece:
                piece_save.square = square2
                piece_save.square.set_piece(piece_save)
                Piece.pieces.append(piece_save)

            self.square=square_save
            self.square.set_piece(self)
            mvmt = False
        else:
            WHITE_TO_MOVE = not(WHITE_TO_MOVE)
            mvmt = True
            if WHITE_TO_MOVE :
                if not(WHITE_CHECK):
                    fenetre.title("Whites to move !")
                else:
                    fenetre.title("Whites to move ! (Check)")
            else:
                if not (BLACK_CHECK):
                    fenetre.title("Blacks to move !")
                else:
                    fenetre.title("Blacks to move ! (Check)")

        return mvmt


class Chessboard:
    def __init__(self):
        self.squares = [[Square((j,i)) for i in range(8)] for j in range(8)]
    def square(self,name):
        coords = "ABCDEFGH".index(name[:-1]), 8 - int(name[1:])
        return self.squares[coords[0]][coords[1]]

    def ini(self):
        global WHITE_CHECK,WHITE_CHECK_MAT,BLACK_CHECK,BLACK_CHECK_MAT,WHITE_TO_MOVE
        WHITE_TO_MOVE = True
        BLACK_CHECK = False
        WHITE_CHECK = False
        BLACK_CHECK_MAT = False
        WHITE_CHECK_MAT = False
        for letter in ['A','B','C','D','E','F','G','H']:
            Piece("pawn","black",self.square(letter+"7"))
            Piece("pawn", "white", self.square(letter + "2"))
        tab = ["rook","knight","bishop","queen","king","bishop","knight","rook"]
        tab2 = ['A','B','C','D','E','F','G','H']
        for k in range(8):
            Piece(tab[k], "black", self.square(tab2[k] + "8"))
            Piece(tab[k], "white", self.square(tab2[k] + "1"))

chess = Chessboard()
chess.ini()
tk.mainloop()

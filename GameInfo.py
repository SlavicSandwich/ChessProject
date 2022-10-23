# Keeps the current information on the game, also checks for legal moves at the moment. +Infolog
class Game:
    def __init__(self):
        self.board = [
            ["bR", 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.white_move = True
        self.log = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = ()  # coords for the square where enpassant is possible
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    def make_move(self, move):
        self.board[move.startRow][move.startColumn] = '-'
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.log.append(move)
        self.white_move = not self.white_move

        # update King's location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endColumn)

        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endColumn)

        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endColumn] = move.pieceMoved[0] + 'Q'

        # enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endColumn] = '-'  # capturing the pawn

        # update enpassantPossible
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:  # only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startColumn)
        else:
            self.enpassantPossible = ()

        #castle move
        if move.isCastleMove:
            if move.endColumn - move.startColumn == 2: #kingSideCastle
                self.board[move.endRow][move.endColumn - 1] = self.board[move.endRow][move.endColumn + 1]
                self.board[move.endRow][move.endColumn + 1] = '-'
            else: #queenSideCastle
                self.board[move.endRow][move.endColumn + 1] = self.board[move.endRow][move.endColumn - 2]
                self.board[move.endRow][move.endColumn - 2] = '-'


        # update castling rights - update when rook or king has made a move
        self.update_castle_rights(move)
        self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    def undo_move(self):
        if self.log:
            move = self.log.pop(-1)
            self.board[move.endRow][move.endColumn] = move.pieceCaptured
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.white_move = not self.white_move

            # update king's position
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startColumn)

            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startColumn)

            # undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endColumn] = '-'
                self.board[move.startRow][move.endColumn] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endColumn)

            # undo 2 square pawn advance
            if move.pieceMoved[1] == 'P' and abs((move.startRow - move.endRow)) == 2:
                self.enpassantPossible = ()

            #undo castling rights
            self.castleRightLog.pop()
            newRights = self.castleRightLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            #undo castle move
            if move.isCastleMove:
                if move.endColumn - move.startColumn == 2:
                    self.board[move.endRow][move.endColumn + 1] = self.board[move.endRow][move.endColumn - 1]
                    self.board[move.endRow][move.endColumn - 1] = '-'
                else:
                    self.board[move.endRow][move.endColumn - 2] = self.board[move.endRow][move.endColumn + 1]
                    self.board[move.endRow][move.endColumn + 1] = '-'
    def update_castle_rights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        if move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False

        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startColumn == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startColumn == 7:
                    self.currentCastlingRight.wks = False

        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startColumn == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startColumn == 7:
                    self.currentCastlingRight.bks = False

        if move.pieceCaptured == 'wR':
            if move.endrow == 7:
                if move.endColumn == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endColumn == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endColumn == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endColumn == 7:
                    self.currentCastlingRight.bks = False

    def get_valid_moves(self):
        tempEnpassantPossible = self.enpassantPossible
        #copy current castling rights
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)

        moves = self.get_all_possible_moves()
        if self.white_move:
            self.get_castle_moves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.get_castle_moves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.white_move = not self.white_move
            if self.in_check():
                moves.remove(moves[i])

            self.white_move = not self.white_move
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True

        if self.checkmate:
            print('Checkmate!')
        if self.stalemate:
            print('Stalemate!')

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves


    def in_check(self):
        if self.white_move:
            return self.square_under_attack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.square_under_attack(self.blackKingLocation[0], self.blackKingLocation[1])


    def square_under_attack(self, row, column):
        self.white_move = not self.white_move
        oppMoves = self.get_all_possible_moves()
        self.white_move = not self.white_move
        for move in oppMoves:
            if move.endRow == row and move.endColumn == column:
                return True
        return False


    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                turn = self.board[row][column][0]
                if (turn == 'w' and self.white_move) or (turn == 'b' and not self.white_move):
                    piece = self.board[row][column][1]
                    match piece:
                        case 'P':
                            self.get_pawn_moves(row, column, moves)
                        case 'R':
                            self.get_rook_moves(row, column, moves)
                        case 'N':
                            self.get_knight_moves(row, column, moves)
                        case 'B':
                            self.get_bishop_moves(row, column, moves)
                        case 'Q':
                            self.get_queen_moves(row, column, moves)
                        case 'K':
                            self.get_king_moves(row, column, moves)

        return moves


    def get_pawn_moves(self, row, column, moves):
        if self.white_move:
            if self.board[row - 1][column] == '-':
                moves.append(Move((row, column), (row - 1, column), self.board))
                if row == 6 and self.board[row - 2][column] == '-':
                    moves.append(Move((row, column), (row - 2, column), self.board))

            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == 'b':
                    moves.append(Move((row, column), (row - 1, column - 1), self.board))

                elif (row - 1, column - 1) == self.enpassantPossible:
                    moves.append(Move((row, column), (row - 1, column - 1), self.board, isEnpassantMove=True))

            if column + 1 <= 7:
                if self.board[row - 1][column + 1][0] == 'b':
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))

                elif (row - 1, column + 1) == self.enpassantPossible:
                    moves.append(Move((row, column), (row - 1, column + 1), self.board, isEnpassantMove=True))

        else:
            if self.board[row + 1][column] == '-':
                moves.append(Move((row, column), (row + 1, column), self.board))
                if row == 1 and self.board[row + 2][column] == '-':
                    moves.append(Move((row, column), (row + 2, column), self.board))

            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0] == 'w':
                    moves.append(Move((row, column), (row + 1, column - 1), self.board))

                elif (row + 1, column - 1) == self.enpassantPossible:
                    moves.append(Move((row, column), (row + 1, column - 1), self.board, isEnpassantMove=True))

            if column + 1 <= 7:
                if self.board[row + 1][column + 1][0] == 'w':
                    moves.append(Move((row, column), (row + 1, column + 1), self.board))

                elif (row + 1, column + 1) == self.enpassantPossible:
                    moves.append(Move((row, column), (row + 1, column + 1), self.board, isEnpassantMove=True))


    def get_rook_moves(self, row, column, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            currow = row + d[0]
            curcol = column + d[1]
            while 0 <= currow <= 7 and 0 <= curcol <= 7:
                if self.white_move:
                    if self.board[currow][curcol][0] in ['-', 'b']:
                        moves.append(Move((row, column), (currow, curcol), self.board))
                    else:
                        break
                else:
                    if self.board[currow][curcol][0] in ['-', 'w']:
                        moves.append(Move((row, column), (currow, curcol), self.board))
                    else:
                        break
                currow += d[0]
                curcol += d[1]


    def get_knight_moves(self, row, column, moves):
        directions = ((2, 1), (2, -1), (-2, 1), (-2, -1), (-1, -2), (-1, 2), (1, -2), (1, 2))
        for d in directions:
            currow = row + d[0]
            curcol = column + d[1]
            if self.white_move:
                if 0 <= curcol <= 7 and 0 <= currow <= 7:
                    if self.board[currow][curcol][0] in ['-', 'b']:
                        moves.append(Move((row, column), (currow, curcol), self.board))

            else:
                if 0 <= curcol <= 7 and 0 <= currow <= 7:
                    if self.board[currow][curcol][0] in ['-', 'w']:
                        moves.append(Move((row, column), (currow, curcol), self.board))


    def get_bishop_moves(self, row, column, moves):
        directions = ((1, 1), (-1, -1), (1, -1), (-1, 1))
        for d in directions:
            currow = row + d[0]
            curcol = column + d[1]
            while 0 <= currow <= 7 and 0 <= curcol <= 7:
                if self.white_move:
                    if self.board[currow][curcol][0] in ['-', 'b']:
                        moves.append(Move((row, column), (currow, curcol), self.board))
                    else:
                        break
                else:
                    if self.board[currow][curcol][0] in ['-', 'w']:
                        moves.append(Move((row, column), (currow, curcol), self.board))
                    else:
                        break
                currow += d[0]
                curcol += d[1]


    def get_queen_moves(self, row, column, moves):
        directions = ((1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (1, 0), (-1, 0), (0, -1))
        for d in directions:
            currow = row + d[0]
            curcol = column + d[1]
            while 0 <= currow <= 7 and 0 <= curcol <= 7:
                if self.white_move:
                    if self.board[currow][curcol][0] in ['-', 'b']:
                        moves.append(Move((row, column), (currow, curcol), self.board))
                    else:
                        break
                else:
                    if self.board[currow][curcol][0] in ['-', 'w']:
                        moves.append(Move((row, column), (currow, curcol), self.board))
                    else:
                        break
                currow += d[0]
                curcol += d[1]


    def get_king_moves(self, row, column, moves):
        directions = ((1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (1, 0), (-1, 0), (0, -1))
        allyColor = 'w' if self.white_move else 'b'
        for d in directions:
            currow = row + d[0]
            curcol = column + d[1]
            if self.white_move:
                if 0 <= curcol <= 7 and 0 <= currow <= 7:
                    if self.board[currow][curcol][0] in ['-', 'b']:
                        moves.append(Move((row, column), (currow, curcol), self.board))

            else:
                if 0 <= curcol <= 7 and 0 <= currow <= 7:
                    if self.board[currow][curcol][0] in ['-', 'w']:
                        moves.append(Move((row, column), (currow, curcol), self.board))


    def get_castle_moves(self, row, column, moves):
        if self.square_under_attack(row, column):
            return #can's castle while in check

        if (self.white_move and self.currentCastlingRight.wks) or (not self.white_move and self.currentCastlingRight.bks):
            self.get_kingside_castle_moves(row, column, moves)
        if (self.white_move and self.currentCastlingRight.wqs) or (not self.white_move and self.currentCastlingRight.bqs):
            self.get_queenside_castle_move(row, column, moves)



    def get_kingside_castle_moves(self, row, column, moves):
        if self.board[row][column+1] == '-' and self.board[row][column+2] == '-':
            if not self.square_under_attack(row, column + 1) and not self.square_under_attack(row, column + 2):
                moves.append(Move((row, column), (row, column +2), self.board, isCastleMove=True))

    def get_queenside_castle_move(self, row, column, moves):
        if self.board[row][column-1] == '-' and self.board[row][column-2] == '-' and self.board[row][column - 3] == '-':
            if not self.square_under_attack(row, column - 1) and not self.square_under_attack(row, column - 2):
                moves.append(Move((row, column), (row, column - 2), self.board, isCastleMove=True))


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:
    ranksToRows = {'1': 7, '2': 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {7: '1', 6: "2", 5: "3", 4: "4", 3: "5", 2: "6", 1: "1", 0: "8"}
    filesToCols = {'a': 0, 'b': 1, "c": 2, "d": 3, "e": 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startColumn = startSq[1]
        self.endRow = endSq[0]
        self.endColumn = endSq[1]
        self.pieceMoved = board[self.startRow][self.startColumn]
        self.pieceCaptured = board[self.endRow][self.endColumn]
        self.isPawnPromotion = False
        # pawn promotion
        self.isPawnPromotion = (
                self.pieceMoved == 'wP' and self.endRow == 0 or self.pieceMoved == 'bP' and self.endRow == 7)
        # enpassant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

        #castle Move
        self.isCastleMove = isCastleMove

        self.moveId = self.startRow * 1000 + self.startColumn * 100 + self.endRow * 10 + self.endColumn

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.startRow, self.startColumn) + '-' + self.get_rank_file(self.endRow,
                                                                                              self.endColumn)

    def get_rank_file(self, row, column):
        return self.colsToFiles[column] + self.rowsToRanks[row]

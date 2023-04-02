import socket
import threading


class Tic_Tac_Toe:
    def __init__(self):
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.turn = 'X'
        self.you = 'X'
        self.opponent = 'O'
        self.winner = None
        self.game_over = False

        self.counter = 0

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.you = 'O'
        self.opponent = 'X'

        threading.Thread(target=self.main, args=(client,)).start()

    def main(self, client):
        while True:
            if self.game_over:
                break
            elif self.turn == self.you:
                row = input('row > ')
                col = input('col > ')
                if int(row) > 2 or int(col) > 2:
                    print('Invalid move!')
                    print('Numbers must be 0, 1 or 2.')
                elif self.board[int(row)][int(col)] == ' ':
                    move = f'{row}, {col}'
                    client.send(move.encode())
                    self.apply_move(row, col, self.turn)
                    self.turn = self.opponent
                else:
                    print('Invalid move!')
            else:
                data = client.recv(2048).decode('utf-8')
                data = data.split(', ')
                data0 = data[0]
                data1 = data[1]
                self.apply_move(data0, data1, self.turn)
                self.turn = self.you

    def apply_move(self, row, col, player):

        self.counter += 1
        self.board[int(row)][int(col)] = player
        self.print_board()

        if self.check_if_won():
            if self.winner == self.you:
                print('You win!')
                exit()
            elif self.winner == self.opponent:
                print('You lose!')
                exit()
        else:
            if self.counter == 9:
                print('It is a tie!')
                exit()

    def check_if_won(self):
        if self.game_over:
            return
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != ' ':
                self.winner = self.board[row][0]
                self.game_over = True
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                self.winner = self.board[0][col]
                self.game_over = True
                return True
            if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
                self.winner = self.board[0][0]
                self.game_over = True
                return True
            if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
                self.winner = self.board[0][2]
                self.game_over = True
                return True
            return False

    def print_board(self):
        print()
        print('    0   1   2')
        for row in range(3):
            print(row, end='   ')
            print(' | '.join(self.board[row]))
            if row != 2:
                print('   -----------')
        print()


game = Tic_Tac_Toe()
game.connect_to_game('localhost', 8974)

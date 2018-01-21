from Grid import Wall


class Map:

    def __init__(self, grid_list):
        self.grid_list = grid_list

    def make_map(self):

        wall_A = Wall([(0, 0), (1, 0), (2, 0)])
        wall_B = Wall([(0, 0)])
        wall_C = Wall([(0, 0), (0, 1), (0, 2)])
        wall_D = Wall([(0, 0), (0, 1), (1, 0), (1, 1)])
        wall_E = Wall([(0, 0), (0, 1), (1, 1), (1, 2)])
        wall_F = Wall([(1, 0), (1, 1), (0, 1), (0, 2)])
        wall_G = Wall([(0, 0), (1, 0), (1, 1), (2, 1)])
        wall_H = Wall([(0, 1), (1, 1), (1, 0), (2, 0)])

        wall_1 = Wall([(0, 2), (0, 1), (0, 0), (1, 0), (2, 0)])
        wall_2 = Wall([(2, 2), (2, 1), (0, 0), (1, 0), (2, 0)])
        wall_3 = Wall([(0, 2), (0, 1), (0, 0), (1, 2), (2, 2)])
        wall_4 = Wall([(2, 2), (2, 1), (0, 2), (1, 2), (2, 0)])
        wall_5 = Wall([(0, 0), (0, 1), (1, 1)])
        wall_6 = Wall([(0, 1), (1, 0), (1, 1)])
        wall_7 = Wall([(0, 0), (0, 1), (1, 0)])
        wall_8 = Wall([(0, 0), (1, 0), (1, 1)])
        sprites = []

        sprites.extend(wall_1.get_obsticle(self.grid_list[3][9], 36))
        sprites.extend(wall_3.get_obsticle(self.grid_list[10][9], 36))
        sprites.extend(wall_4.get_obsticle(self.grid_list[10][21], 36))
        sprites.extend(wall_2.get_obsticle(self.grid_list[3][21], 36))

        sprites.extend(wall_E.get_obsticle(self.grid_list[7][14], 36))
        sprites.extend(wall_E.get_obsticle(self.grid_list[6][17], 36))

        sprites.extend(wall_D.get_obsticle(self.grid_list[1][15], 36))
        sprites.extend(wall_D.get_obsticle(self.grid_list[1][16], 36))

        sprites.extend(wall_A.get_obsticle(self.grid_list[2][4], 36))
        sprites.extend(wall_C.get_obsticle(self.grid_list[1][5], 36))

        sprites.extend(wall_A.get_obsticle(self.grid_list[14][26], 36))
        sprites.extend(wall_C.get_obsticle(self.grid_list[13][27], 36))

        sprites.extend(wall_4.get_obsticle(self.grid_list[12][13], 36))
        sprites.extend(wall_3.get_obsticle(self.grid_list[12][17], 36))

        sprites.extend(wall_G.get_obsticle(self.grid_list[5][19], 36))
        sprites.extend(wall_H.get_obsticle(self.grid_list[9][19], 36))
        sprites.extend(wall_G.get_obsticle(self.grid_list[9][11], 36))
        sprites.extend(wall_H.get_obsticle(self.grid_list[5][11], 36))

        sprites.extend(wall_A.get_obsticle(self.grid_list[14][4], 36))
        sprites.extend(wall_C.get_obsticle(self.grid_list[13][5], 36))

        sprites.extend(wall_A.get_obsticle(self.grid_list[2][26], 36))
        sprites.extend(wall_C.get_obsticle(self.grid_list[1][27], 36))

        sprites.extend(wall_5.get_obsticle(self.grid_list[5][6], 36))
        sprites.extend(wall_7.get_obsticle(self.grid_list[9][6], 36))
        sprites.extend(wall_6.get_obsticle(self.grid_list[5][3], 36))
        sprites.extend(wall_8.get_obsticle(self.grid_list[9][3], 36))

        sprites.extend(wall_5.get_obsticle(self.grid_list[5][28], 36))
        sprites.extend(wall_7.get_obsticle(self.grid_list[9][28], 36))
        sprites.extend(wall_6.get_obsticle(self.grid_list[5][25], 36))
        sprites.extend(wall_8.get_obsticle(self.grid_list[9][25], 36))

        return sprites

    def get_box_position(self):
        pos_lst = []
        for i in range(33):
            pos_lst.append(self.grid_list[0][i])
        for j in range(33):
            pos_lst.append(self.grid_list[16][j])
        for k in range(0, 14):
            pos_lst.append(self.grid_list[7][k])
            pos_lst.append(self.grid_list[8][k])
        for h in range(19, 31):
            pos_lst.append(self.grid_list[7][h])
            pos_lst.append(self.grid_list[8][h])
        for l in range(6, 27):
            pos_lst.append(self.grid_list[15][l])

        pos_lst.extend([self.grid_list[1][0], self.grid_list[1][1],
                        self.grid_list[1][2], self.grid_list[1][3],
                        self.grid_list[1][4], self.grid_list[1][18],
                        self.grid_list[1][19], self.grid_list[1][20],
                        self.grid_list[1][21], self.grid_list[1][22],
                        self.grid_list[1][23], self.grid_list[1][24],
                        self.grid_list[1][25], self.grid_list[1][26],
                        self.grid_list[1][28], self.grid_list[1][29],
                        self.grid_list[1][30], self.grid_list[1][31],
                        self.grid_list[1][32], self.grid_list[2][7],
                        self.grid_list[2][8], self.grid_list[2][9],
                        self.grid_list[2][10], self.grid_list[2][11],
                        self.grid_list[2][12], self.grid_list[2][13],
                        self.grid_list[2][14], self.grid_list[2][18],
                        self.grid_list[2][19], self.grid_list[2][20],
                        self.grid_list[2][21], self.grid_list[2][22],
                        self.grid_list[2][23], self.grid_list[2][24],
                        self.grid_list[2][25], self.grid_list[1][6],
                        self.grid_list[1][7], self.grid_list[1][8],
                        self.grid_list[1][9], self.grid_list[1][10],
                        self.grid_list[1][11], self.grid_list[1][12],
                        self.grid_list[1][13], self.grid_list[1][14],
                        self.grid_list[4][0], self.grid_list[4][1],
                        self.grid_list[4][2], self.grid_list[4][3],
                        self.grid_list[4][4], self.grid_list[4][5],
                        self.grid_list[4][6], self.grid_list[4][7],
                        self.grid_list[4][8], self.grid_list[4][10],
                        self.grid_list[4][22], self.grid_list[4][24],
                        self.grid_list[4][25], self.grid_list[4][26],
                        self.grid_list[4][27], self.grid_list[4][28],
                        self.grid_list[4][29], self.grid_list[4][29],
                        self.grid_list[4][30], self.grid_list[4][31],
                        self.grid_list[4][32], self.grid_list[11][0],
                        self.grid_list[11][1], self.grid_list[11][2],
                        self.grid_list[11][3], self.grid_list[11][4],
                        self.grid_list[11][5], self.grid_list[11][6],
                        self.grid_list[11][7], self.grid_list[11][8],
                        self.grid_list[11][10], self.grid_list[11][22],
                        self.grid_list[11][24], self.grid_list[11][25],
                        self.grid_list[11][26], self.grid_list[11][27],
                        self.grid_list[11][28], self.grid_list[11][29],
                        self.grid_list[11][30], self.grid_list[11][31],
                        self.grid_list[11][32], self.grid_list[12][0],
                        self.grid_list[12][1], self.grid_list[12][2],
                        self.grid_list[12][3], self.grid_list[12][4],
                        self.grid_list[12][5], self.grid_list[12][6],
                        self.grid_list[12][7], self.grid_list[12][8],
                        self.grid_list[12][24], self.grid_list[12][25],
                        self.grid_list[12][26], self.grid_list[12][27],
                        self.grid_list[12][28], self.grid_list[12][29],
                        self.grid_list[12][30], self.grid_list[12][31],
                        self.grid_list[12][32]])

        return pos_lst

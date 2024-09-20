# -*- coding: UTF-8 -*-
"""Sudoku"""

import sys
import random

class Sudoku(object):
    """数独类"""


    def __init__(self)->None:
        """初始化数独求解器对象
        Args:无参数
        Returns:
            None
        """

        #声明成员
        """每行一个规则列表，用生成式构造0~9的列表，当数字被用掉时，从列表中删除"""
        self.row_rule_list = [[]] 
        """每列一个规则列表，用生成式构造0~9的列表，当数字被用掉时，从列表中删除"""
        self.col_rule_list = [[]] 
        """中央九宫格，三行三列，每格一个规则列表，用生成式构造0~9的列表，当数字被用掉时，从列表中删除"""
        self.nine_grid_rule_list = [[]] 
        """9*9的矩阵，初始化为0"""
        self.matrix = [[]] 


    def print_matrix(self, id='', format='text')->None:
        """打印二维矩阵，以3个元素为一组，每组之间以竖线“|”分隔，每三行打印一行分隔线。
        Args:
            id (str, optional): 矩阵标识符。默认为空字符串。
            format (str, optional): 输出格式。'text'为纯文本格式，'html'为HTML格式。默认为'text'。
        Returns:
            None
        """
        if format == 'html':
            print(f'<pre style="font-size:32pt;page-break-inside:avoid;page-break-after:always;text-align:center;vertical-align:middle;">', end='')
        print(f'{id}')
        
        for row in range(len(self.matrix)):
            if row % 3 == 0 and row != 0:
                print("-" * 20)
            
            for col in range(len(self.matrix[row])):
                if col % 3 == 0 and col != 0:
                    print("|", end="")
                x = self.matrix[row][col]
                s = " " if x == 0 else str(x)
                print(s + " ", end="")
            
            print()
        print()

        if format == 'html':
            print('</pre>')


    def generate_sudoku(self)->bool:
        """生成数独矩阵
        Args:无参数
        Returns:
            bool: 如果成功生成数独矩阵，则返回True；否则返回False
        """

        for i in range(10000):
            #为新的一次生成，重新初始化规则
            self.row_rule_list = [[i for i in range(1, 10)] for j in range(9)] #每行一个规则列表，用生成式构造0~9的列表，当数字被用掉时，从列表中删除
            self.col_rule_list = [[i for i in range(1, 10)] for j in range(9)] #每列一个规则列表，用生成式构造0~9的列表，当数字被用掉时，从列表中删除
            self.nine_grid_rule_list = [[i for i in range(1, 10)] for j in range(9)] #中央九宫格，三行三列，每格一个规则列表，用生成式构造0~9的列表，当数字被用掉时，从列表中删除
            self.matrix = [[0 for i in range(1, 10)] for j in range(9)] #9*9的矩阵，初始化为0

            x = 0 #单元格默认为不可用的0
            for row in range(len(self.matrix)):
                for col in range(len(self.matrix[row])):
                    #生成一个单元格
                    x = self.generate_sudoku_cell(row, col)
                    if x == 0: #任一单元格生成失败，则设定标志并退出循环
                        break
                    else:
                        self.matrix[row][col] = x
                if x == 0: #任一单元格生成失败，则设定标志并退出循环
                    break
            if x != 0: #如果所有单元格都生成成功，则退出循环，否则继续重试
                break
        return x != 0


    def generate_sudoku_cell(self, row, col)->int:
        """生成数独表中一个单元格的数字，该数字必须满足所在行、列、九宫格的规则。
        Args:
            row (int): 单元格所在的行数。
            col (int): 单元格所在的列数。
        Returns:
            int: 生成的数字，如果无法生成则返回0。
        """
        #尝试随机选取行规则中的数，直到找到数同时匹配到行、列、九宫格规则，然后将其从三个规则中移除

        #复制行规则，用于尝试
        choices = self.row_rule_list[row][:]
        for i in range(len(choices)):
            #随意选择一个选项
            x = random.choice(choices)
            choices.remove(x)

            #验证其他两个规则
            if x in self.col_rule_list[col] and x in self.nine_grid_rule_list[(row // 3) * 3 + (col // 3)]:
                #返回x，并从三个规则中移除
                self.row_rule_list[row].remove(x)
                self.col_rule_list[col].remove(x)
                self.nine_grid_rule_list[(row // 3) * 3 + (col // 3)].remove(x)
                return x
        return 0 # 如果没有可用的数字，返回0


    def print_debug(self)->None:
        """打印调试信息，输出行规则、列规则和九宫格规则。
        Args:
            无
        Returns:
            无返回值，直接打印输出调试信息。
        """
        print(f"debug: row {self.row_rule_list}, \ncol {self.col_rule_list}, \nnine grid {self.nine_grid_rule_list}")
    

    def generate_mask(self, difficulty = 3):
        """根据难度生成遮罩。
        Args:
            difficulty (int, optional): 难度等级，取值范围为1~9，默认为3。
        Returns:
            None
        """
        for row in range(len(self.matrix)):
            for j in range(difficulty):
                col = random.randint(0, 8)
                self.matrix[row][col] = 0

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        n = 1
    elif '-h' in sys.argv or '--help' in sys.argv:
        print(f'Usage: python {sys.argv[0]} <number of sudokus to generate>')
        exit(0)
    else:
        n = int(sys.argv[1])

    sudoku = Sudoku()
    for i in range(n):
        result = sudoku.generate_sudoku()
        if result:
            sudoku.print_matrix(id=f'#{i+1}', format='html')
            #sudoku.print_debug()
            sudoku.generate_mask(4)
            sudoku.print_matrix(id=f'#{i+1}', format='html')
        else:
            print(f'生成失败，第{i+1}次', file=sys.stderr)
            exit(-1)
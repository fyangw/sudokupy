import pytest
from unittest.mock import MagicMock
import random
from sudoku import Sudoku

def test_generate_sudoku_cell_success(monkeypatch):
    sudoku = Sudoku()
    # 设定一个可以成功生成数字的情况
    sudoku.row_rule_list[0] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    sudoku.col_rule_list[0] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    sudoku.nine_grid_rule_list[0] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Mock random.choice
    with monkeypatch.context() as m:
        m.setattr(random, 'choice', lambda x: 1)

        result = sudoku.generate_sudoku_cell(0, 0)

    assert result == 1


def test_generate_sudoku_cell_failure(monkeypatch):
    sudoku = Sudoku()
    # 设定一个无法成功生成数字的情况
    sudoku.row_rule_list[0] = [1]
    sudoku.col_rule_list[0] = [2]
    sudoku.nine_grid_rule_list[0] = [3]

    # Mock random.choice
    with monkeypatch.context() as m:
        m.setattr(random, 'choice', lambda x: x[0])

        result = sudoku.generate_sudoku_cell(0, 0)

    assert result == 0

# 运行测试
if __name__ == "__main__":
    pytest.main()
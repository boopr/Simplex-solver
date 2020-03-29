import numpy as np

from fractions import Fraction

from flask import Flask
from flask import render_template

from src.SimplexSolver import SimplexSolver

app = Flask(__name__)


def input_matrix(name):
    correct = False
    matrix = []

    print(f"Enter matrix {name}, MATLAB form ([x1 x2 x3; x4 x5 x6])")

    while not correct:
        matrix = []
        user_input = input(f"{name} = ")
        try:
            user_input = user_input.strip().strip('[').strip(']')
            rows = user_input.replace('; ', ';').split(';')
            for row in rows:
                frow = []
                for val in row.split(' '):
                    if val != ' ':
                        frow.append(Fraction(val.strip()))
                matrix.append(frow)

            matrix = np.asarray(matrix)

            to_print = []
            for i in matrix:
                r = []
                for j in i:
                    r.append(str(j))
                to_print.append(r)
            print(np.asarray(to_print))
            correct = input("Is it correct? [Y/n]").lower().strip() == 'y'
        except ValueError as e:
            print(f"Error while reading your entry, please try again ('{user_input}')")
            correct = False

    return matrix


@app.route('/')
def hello():
    A = input_matrix('A')
    c_T = input_matrix('c^T')
    b = input_matrix('b')

    s = SimplexSolver(A, b, c_T)
    s.solve()

    return render_template('output.html', content=s.output)
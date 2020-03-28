import numpy as np

from flask import Flask
from flask import render_template, request

from src.SimplexSolver import SimplexSolver

app = Flask(__name__)


def input_matrix(name):
    correct = False
    matrix = []

    print(f"Enter matrix {name}, MATLAB form ([x1 x2 x3; x4 x5 x6])")

    while not correct:
        user_input = input(f"{name} = ")

        user_input = user_input.strip().strip('[').strip(']')
        rows = user_input.replace('; ', ';').split(';')
        for row in rows:
            frow = []
            for val in row.split(' '):
                if val != ' ':
                    frow.append(float(val.strip()))
            matrix.append(frow)

        matrix = np.asarray(matrix)
        print(matrix)
        correct = input("Is it correct? [Y/n]").lower().strip() == 'y'


    return matrix


@app.route('/')
def hello():
    A = input_matrix('A')
    c_T = input_matrix('c^T')
    b = input_matrix('b')
    start_point = input_matrix('Start point')[0]

    s = SimplexSolver(A, b, c_T, start_point)
    s.solve()

    return render_template('output.html', content=s.output)
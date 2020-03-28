import numpy as np

from src.OutputFormater import OutputFormater


class SimplexSolver:
    def __init__(self, A: np.ndarray, b: np.ndarray, c_T: np.ndarray, start: tuple):
        self.A = A
        self.b = b
        self.c_T = c_T[0]

        nb_variables_not_nul = np.count_nonzero(self.c_T)

        self.indexes_non_base = np.arange(1, nb_variables_not_nul + 1)
        self.indexes_base = np.arange(nb_variables_not_nul + 1, self.c_T.size + 1)

        self.values = dict([*zip((*self.indexes_non_base, *self.indexes_base), self.c_T)])

        self.output = OutputFormater()

        self.output.add_section("Simplex method")
        self.output.add_matrix(self.A, name="A")
        self.output.add_matrix(self.b, name="b")
        self.output.add_array(self.c_T, name="c^T")

    def solve(self):
        o = OutputFormater()
        v = 1
        while True:
            o.add_subsection(f"Iteration #{v}")

            o.add_subsubsection(f"[{v}] Step 1 - Matrices \\(B\\) and \\(N\\)")
            # Step 1
            o.add_array([f"x_{i}" for i in self.indexes_base], "x_B")
            o.add_array([f"x_{i}" for i in self.indexes_non_base], "x_N")

            o.add_array([f"{self.values[i]}" for i in self.indexes_base], "c_B^T")
            o.add_array([f"{self.values[i]}" for i in self.indexes_non_base], "c_N^T")

            B = self.get_base()
            N = self.get_non_base()
            o.add_matrix(B, name="B")
            o.add_matrix(N, name="N")

            o.add_subsubsection(f"[{v}] Step 2 - Matrices \\(\\bar{{b}}\\) and \\(\\bar{{A}}\\)")
            # Step 2
            b_bar = np.linalg.inv(B) @ self.b
            A_bar = np.linalg.inv(B) @ N
            o.add_matrix(np.linalg.inv(B), name="B^{-1}")
            o.add_matrix(b_bar, name="\\bar{{b}} = B^{-1} \\times b")
            o.add_matrix(A_bar, name="\\bar{{A}} = B^{-1} \\times N")

            # Step 3
            o.add_subsubsection(f"[{v}] Step 3 - Reduced cost \\(\\bar{{c_N^T}}\\)")
            c_T_non_base_bar = self.get_c_T_non_base() - self.get_c_T_base() @ A_bar
            o.add_matrix(c_T_non_base_bar, name="\\bar{{c_N^T}} = c_N^T - c_B^T\\bar{A}")

            if np.all(c_T_non_base_bar >= 0):
                o.add_paragraph("\\(\\bar{{c_N^T}} \\geq 0\\), we have a local minimum : termination of the algorithm.")
                break

            # Step 4
            o.add_subsubsection(f"[{v}] Step 4 - Variable entering or leaving the basis \\(x_h\\)")
            smallest = c_T_non_base_bar[0, 0]
            in_index = self.indexes_non_base[0]
            h = 0
            output_temp = "\\text{min}\\left("
            for i, (_, value) in enumerate(zip(self.indexes_non_base, c_T_non_base_bar[0])):
                output_temp += f"{value}"
                if value < smallest:
                    smallest = value
                    h = i
                if i != len(self.indexes_non_base) - 1:
                    output_temp += ", "
            output_temp += f"\\right) = {smallest} \\implies h = {h + 1}"
            o.add_math(output_temp)

            l = self.argmin_simplex(b_bar.flatten(), A_bar[:, h], o)

            o.add_paragraph(f"Variable entering the basis: \\(x_{self.indexes_non_base[h]}\\)")
            o.add_paragraph(f"Variable leaving the basis: \\(x_{self.indexes_base[l]}\\)")

            self.indexes_non_base[h], self.indexes_base[l] = self.indexes_base[l], self.indexes_non_base[h]

            self.indexes_base = np.sort(self.indexes_base)
            self.indexes_non_base = np.sort(self.indexes_non_base)

            v += 1
        self.output.add_reveal(o, "development", "simplex_dev")
        self.output.add_matrix(b_bar, "Solution")
        return 0

    def get_base(self):
        return self.A[:, self.indexes_base - 1]

    def get_non_base(self):
        return self.A[:, self.indexes_non_base - 1]

    def get_c_T_base(self):
        return np.array([[self.values[i] for i in self.indexes_base]])

    def get_c_T_non_base(self):
        return np.array([[self.values[i] for i in self.indexes_non_base]])

    def argmin_simplex(self, numerators, denumerators, o=OutputFormater()):
        val = []
        output_temp = "l = \\text{argmin}\\left\\{"
        for i, (num, den) in enumerate(zip(numerators, denumerators)):
            if den != 0 and num / den >= 0:
                output_temp += f"{num/den}"
                val.append(num / den)
            else:
                output_temp += "+\\infty"
                val.append(np.inf)
            if i != len(numerators) - 1:
                output_temp += ", "
        output_temp += f"\\right\\}} = {val.index(min(val)) + 1}"

        o.add_math(output_temp)
        return val.index(min(val))

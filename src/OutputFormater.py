class OutputFormater:
    def __init__(self):
        self.output = ""

    def __str__(self):
        return self.output

    def add_block(self, type, content):
        self.output += f"<{type}>{content}</{type}>"

    def add_lonely(self, type):
        self.output += f"<{type} />"

    def add_math(self, content, inline=False):
        if inline:
            self.output += f"\\({content}\\)"
        else:
            self.output += f"$${content}$$"

    def add_reveal(self, content, title, id):
        self.output += f"<button onclick=\"reveal('{id}')\">Reveal {title}</button>"
        self.output += f"<div id=\"{id}\" style=\"display:none\">{content}</div>"

    def add_title(self, name, level):
        self.add_block(f"h{level}", name)

    def add_section(self, name):
        self.add_title(name, 1)

    def add_subsection(self, name):
        self.add_title(name, 2)

    def add_subsubsection(self, name):
        self.add_title(name, 3)

    def add_paragraph(self, content):
        self.add_block("p", content)

    def add_br(self):
        self.add_lonely("br")

    def add_matrix(self, matrix, name, compute_frac=False):
        content = f"{name} = \\left(\\begin{{matrix}}"

        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                if compute_frac:
                    content += str(float(val))
                else:
                    content += str(val)
                if j != len(row) - 1:
                    content += "&"
            if i != len(matrix) - 1:
                content += "\\\\"

        content += "\\end{matrix}\\right)"

        self.add_math(content)

    def add_array(self, array, name):
        content = f"{name} = \\left(\\begin{{matrix}}"
        for i, val in enumerate(array):
            content += str(val)
            if i != len(array) - 1:
                content += "&"

        content += "\\end{matrix}\\right)"
        self.add_math(content)

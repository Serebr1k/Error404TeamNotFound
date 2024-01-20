
def load_file(file:str):
    with open(file) as f:
       lines = f.readlines()

    matrix = []
    for i in lines:
        matrix.append(i.split())
    return matrix
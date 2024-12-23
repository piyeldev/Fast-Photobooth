def load_stylesheet(filename):
    with open(f'styles/{filename}', "r") as file:
        return file.read()
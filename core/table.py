class Table:
    def __init__(self, nrows, ncolumns):
        self.nrows = nrows
        self.ncolumns = ncolumns
        self.setup = [[1]*ncolumns for a in range(nrows)]
        self.id = "".join([str(x) for x in self.setup])
    
    
    def set_cable(self, row_index, row_column, value):
        if type(value) != int:
            return
            #raise Exception('La función "set_cable" solo acepta valores enteros')
    
        aux = self.setup[row_index][row_column]

        if aux % value == 0:
            return
            #raise Exception(f'El valor {value} ya no puede ser establecido')

        self.setup[row_index][row_column] = aux*value

        return value

if __name__ == "__main__":
    tablero = Table(5, 5)
    tablero.set_cable(3, 3, 4)
    tablero.set_cable(3, 3, 5)
    print(*tablero.setup, sep='\n')

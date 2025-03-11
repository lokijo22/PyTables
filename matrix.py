class Matrix:
    def __init__(self, data=None, dimensions:tuple=None) -> None:
        
        self.data:list = data if data else []

        if data and not dimensions:
            raise Exception("InputError: you must specify the size of the matrix when inputing data")
        
        if dimensions:
            self.rows, self.cols  = dimensions
        else:
            # number of rows and columns
            self.rows = 0
            self.cols = 0

    def append(self, row):
        """
        Appends a row to the end of the matrix
        """
        if self.data == []:
            self.cols = len(row)

        if len(row) == self.cols:
            self.data.extend(row)
            self.rows += 1
        else:
            raise ValueError(f"Row length {len(row)} does not match matrix column count {self.cols}")

    def getrow(self, index) -> list:
        """
        Retreive the data in the given row from the matrix

        Args:
            index (int): the index of the row to retreive

        Returns:
            list: A list of the data values in the given row 
        """
        if not (0 <= index < self.rows):
            raise IndexError(f"index {index} is not a valid row index. rows: {self.rows}. Did you forget to initialize dimensions?")
        
        start = index * self.cols
        end = start + self.cols
        return self.data[start:end]

    def getcol(self, index) -> list:
        """
        Retreive the data in the given column from the matrix

        Args:
            index (int): the index of the column to retreive

        Returns:
            list: A list of the data values in the given column 
        """
        if not (0 <= index < self.cols):
            raise IndexError(f"index {index} is not a valid column index. {self.cols}")
        
        return [self.data[i * self.cols + index] for i in range(self.rows)]

    def split(self, column, target, include_target=False) -> list:
        """
        Splits the matrix into sub-matrices based on the target value in the specified column.

        Args:
            column (int): The index of the column to check for the target value.
            target: The column index to split the matrix on.
            include_target (bool): Whether to include the target value in the sub-matrices.

        Returns:
            list: A list of sub-matrices.
        """
        col = self.getcol(column)
        sub_matrices = []
        sub_matrix = Matrix()

        last = None

        for index, item in enumerate(col):
            if ((last != item and item == target) or (last == target and item != target)) and sub_matrix.data:
                # Add the current sub-matrix to the list of sub-matrices
                sub_matrices.append(sub_matrix)
                # Start a new sub-matrix
                sub_matrix = Matrix()

            if item != target or (item == target and include_target):
                # Append the row to the current sub-matrix
                row = self.getrow(index)
                sub_matrix.append(row)

            last = item

        # Append the last sub-matrix if it has data
        if sub_matrix.data:
            sub_matrices.append(sub_matrix)

        return sub_matrices
        
    def size(self) -> int:
        """
        Returns the total number of elements in the matrix
        """
        size = self.rows * self.cols
        return size

    def is_valid_index(self, index) -> bool:
        """
        Evaluates whether or not an index would be inside the matrix or not
        """
        isvalid = 0 <= index < self.size()
        return isvalid

    @staticmethod
    def from_lists(lists:list[list]):
        #assumes all lists are columns of data
        if not lists:
            return None  # Handle empty list case

        matrix = Matrix()
        for row in lists:
            matrix.append(row)

        return matrix

    def __str__(self):
        def getsizes():
            """
            Get the max character count for each row to determine printout
            width
            """
            sizes = []
            for i in range(self.cols):
                col = self.getcol(i)
                largest = max(len(str(x)) for x in col)
                sizes.append(largest)
            return sizes

        def paddata():
            """
            Apply extra spacing to each elements string to make columnn
            spacing uniform between items in the same column
            """
            sizes = getsizes()
            padded_data = [str(i) for i in self.data]
            for i in range(len(self.data)):
                col_index = i % self.cols
                padded_data[i] = str(self.data[i]).ljust(sizes[col_index])
            return padded_data

        out = ''
        padded_data = paddata()

        for i in range(self.rows):
            start = i * self.cols
            end = start + self.cols
            row = padded_data[start:end]
            out += '   '.join(row) + '\n'

        return out


if __name__ == "__main__":

    rows = 20
    columns = 10

    # Usage with preinitalized data
    data = [i for i in range(rows * columns)]

    matrix = Matrix(data, dimensions=(rows, columns))

    print(matrix)

    print("Row Retreival:")
    print("4:\n", matrix.getrow(3))
    print("6:\n", matrix.getrow(5))

    print("\nColumn Retreival:")
    print("6:\n", matrix.getcol(5))
    print("2:\n", matrix.getcol(1))

    # Usage with traditional matrixes
    traditional_matrix = [[(i+1)*o + i for o in range(columns)] for i in range(rows)]
    
    matrix = Matrix.from_lists(traditional_matrix)

    print("\nFrom Traditional Matrix")
    print(matrix)
"""
Array class for assignment 2
"""

# used to easily find the number of elements in the array from the shape
from functools import reduce
from statistics import mean

class Array:

    def __init__(self, shape, *values):

        self.data = []
        self.shape = shape

        # why spend time vectorizing the array after creating it? It is already given to us
        # vectorized.
        self.flattened = list(values)
        self.type = ""

        """Initialize an array of 1-dimensionality. Elements can only be of type:

        - int
        - float
        - bool

        Make sure the values and shape are of the correct type.

        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either int, float or boolean.

        Raises:
            TypeError: If "shape" or "values" are of the wrong type.
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """


        # --------- error checking ---------

        # shape:
        if not isinstance(shape,tuple):
            raise TypeError("Shape must be a tuple")
        if len(shape) == 0:
            raise TypeError("Shape tuple cannot be empty")
        for val in shape:
            if not isinstance(val,int):
                raise TypeError("Values in shape must be integers")

        # values:

        # calculates the spots in the array by multiplying everything in shape
        total_values = reduce(lambda x,y: x*y, shape)

        if len(values) != total_values:
            raise ValueError("Number of values does not line up with shape of array")

        # we must check for bool before int because a bool is a subclass of integers
        if isinstance(values[0],bool):
            self.type = "bool"
        elif isinstance(values[0],int):
            self.type = "int"
        elif isinstance(values[0],float):
            self.type = "float"
        else:
            raise TypeError("Values must be integers, floats or booleans")

        for val in values:
            if type(val).__name__ != self.type:
                raise ValueError("Values must be homogeneous")

        # we make it into a list so we can pop
        values = list(values)
        self._fill_list(self.data, shape, values, 0)

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """
        string = self._get_str(self.data)
        # cleanup here because I didnt do it in the recursion
        return string.replace(",\n ]","]")

    def __getitem__(self, key):
        # this works even on multidimensional arrays because lists also implement this
        # function so it just gets called recursively
        return self.data[key]

    def _operator_precheck(self, other, no_bools):
        """Checks if it is legal to perform an operation between this object and other

        This function is called before every operator function. It raises an error if
        the operation would be illegal

        Args:
            other (Array, float, int): The array or number to check validity againts
            no_bools (boolean): Whether we accept booleans for the array

        Returns:
            Does not return anything

        Raises:
            NotImplementedError: If the operation is not implemented. This is only raised
            so that the calling function can handle it and return NotImplemented
            TypeError: If other is an illegal type
            ValueError: If other is an array with mismatched shape

        """
        if self.type == "bool" and no_bools:
            raise NotImplementedError
        if isinstance(other,Array):
            if other.type == "bool" and no_bools:
                raise NotImplementedError
            if other.shape != self.shape:
                raise ValueError("Shape mismatch between arrays")
        elif not (isinstance(other,int) or isinstance(other,float)):
            raise TypeError(f"Illegal operation between Array and {type(other).__name__}")

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        try:
            self._operator_precheck(other, True)
        except NotImplementedError:
            return NotImplemented

        if isinstance(other,Array):
            new_values = [self.flattened[i] + other.flattened[i] for i in range(len(self.flattened))]
        else:
            new_values = [self.flattened[i] + other for i in range(len(self.flattened))]

        return Array(self.shape, *new_values)



    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        # addition is commutative so this is easy
        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        try:
            self._operator_precheck(other, True)
        except NotImplementedError:
            return NotImplemented

        if isinstance(other,Array):
            new_values = [self.flattened[i] - other.flattened[i] for i in range(len(self.flattened))]
        else:
            new_values = [self.flattened[i] - other for i in range(len(self.flattened))]

        return Array(self.shape, *new_values)

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """

        # subtraction is not commutative so we actually have to write it again
        try:
            self._operator_precheck(other, True)
        except NotImplementedError:
            return NotImplemented

        if isinstance(other,Array):
            new_values = [other.flattened[i] - self.flattened[i] for i in range(len(self.flattened))]
        else:
            new_values = [other - self.flattened[i] for i in range(len(self.flattened))]

        return Array(self.shape, *new_values)

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        try:
            self._operator_precheck(other, True)
        except NotImplementedError:
            return NotImplemented

        if isinstance(other,Array):
            new_values = [self.flattened[i] * other.flattened[i] for i in range(len(self.flattened))]
        else:
            new_values = [self.flattened[i] * other for i in range(len(self.flattened))]

        return Array(self.shape, *new_values)

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        # Hint: this solution/logic applies for all r-methods
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it returns False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        self._operator_precheck(other, False)

        if not isinstance(other,Array):
            raise TypeError(f"Illegal operation between Array and {type(other).__name__}")
        for i in range(len(self.flattened)):
            if not self.flattened[i] == other.flattened[i]:
                return False
        return True



    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it returns TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        self._operator_precheck(other, False)

        if isinstance(other,Array):
            new_values = [self.flattened[i] == other.flattened[i] for i in range(len(self.flattened))]
        else:
            new_values = [self.flattened[i] == other for i in range(len(self.flattened))]

        return Array(self.shape, *new_values)


    def min_element(self):
        """Returns the smallest value of the array.

        Does not work for booleans

        Returns:
            float: The value of the smallest element in the array.

        """
        if self.type == "bool":
            raise TypeError("Cannot calculate min of boolean array")
        return min(self.flattened)

        pass

    def mean_element(self):
        """Returns the mean value of an array

        Does not work for booleans

        Returns:
            float: the mean value
        """
        if self.type == "bool":
            raise TypeError("Cannot calculate mean of boolean array")
        return mean(self.flattened)

    def _fill_list(self, parent, shape, values, index):
        """Fills a list with lists or values and recursively call this function

        Args:
            parent (list): the list to append to
            shape (tuple of ints): a tuple defining the shape of the final array
            values (tuple of ints, floats, or bools): the values to be added to the final lists
            index (int): chooses which number from shape we are working with for this iteration

        Returns:
            Does not return anything, but appends to parent list
        """

        # that means we are at the innermost list
        if index == (len(shape) - 1):
            for i in range(shape[index]):
                # because we pop, and because we call the recursions in the correct
                # order this ensures the array is filled as we would expect (row first)
                # without needing to keep track of which exact row this would be (to figure
                # out which values we need for this row).
                parent.append(values.pop(0))

        else:
            for i in range(shape[index]):
                inner_list = list()
                self._fill_list(inner_list,shape,values,index+1)
                parent.append(inner_list)

    def _get_str(self, cur_list):
        """Recursively return a string representation of the array

        Args:
            cur_list (list or int, float or bool): the list to give string representation of

        Returns:
            A string representation of the list, comprised of the string representations of the
            lists within it
        """
        string = ""

        if isinstance(cur_list[0],list):
            string += "["
            for inner_list in cur_list:
                string += self._get_str(inner_list) + ",\n "
            string += "]"
            return string
        else:
            return str(cur_list)



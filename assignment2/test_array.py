"""
Tests for our array class
"""

from array_class import Array

# 1D tests (Task 4)

# arrays used for unit tests
zero1d = Array((4,),0,0,0,0)
one1d = Array((4,),1,1,1,1)
a1d = Array((4,),1,2,3,4)
b1d = Array((4,),1,-2,3,-4)
bool11d = Array((4,),True,False,True,False)
bool21d = Array((4,),False,False,True,False)


zero2d = Array((4,2),0,0,0,0,0,0,0,0)
one2d = Array((4,2),1,1,1,1,1,1,1,1)
a2d = Array((4,2),1,2,3,4,5,6,7,8)
b2d = Array((4,2),1,-2,3,-4,5,-6,7,-8)

# sneakily make the 3d case have as many elements
# as the 2d case so we dont have to change any tests
zero3d = Array((2,2,2),0,0,0,0,0,0,0,0)
one3d = Array((2,2,2),1,1,1,1,1,1,1,1)
a3d = Array((2,2,2),1,2,3,4,5,6,7,8)
b3d = Array((2,2,2),1,-2,3,-4,5,-6,7,-8)

def test_str_1d():
    assert str(a1d) == "[1, 2, 3, 4]"
    assert str(b1d) == "[1, -2, 3, -4]"


def test_add_1d():
    assert a1d + zero1d == a1d
    assert a1d + b1d == b1d + a1d
    assert a1d + 1 == a1d + one1d
    assert 1 + a1d == a1d + one1d
    assert a1d + b1d == Array((4,),2,0,6,0)
    assert a1d + b1d + b1d == Array((4,),3,-2,9,-4)

def test_sub_1d():
    assert a1d - zero1d == a1d
    assert a1d - b1d != b1d + a1d
    assert a1d - 1 == a1d - one1d
    assert 1 - a1d != a1d - one1d
    assert a1d - b1d == Array((4,),0,4,0,8)
    assert a1d - b1d - b1d == Array((4,),-1,6,-3,12)

def test_mul_1d():
    assert a1d * zero1d == Array((4,),0,0,0,0)
    assert a1d * b1d == b1d * a1d
    assert a1d * 1 == a1d
    assert a1d * one1d == a1d
    assert a1d * b1d == Array((4,),1,-4,9,-16)
    assert a1d * 10 == Array((4,),10,20,30,40)


def test_eq_1d():
    assert (a1d == a1d) == True
    assert (a1d == b1d) == False
    assert (bool11d == bool11d) == True
    assert (bool21d == bool11d) == False


def test_same_1d():
    assert a1d.is_equal(a1d) == True
    assert a1d.is_equal(b1d) == False
    assert bool11d.is_equal(bool11d) == True
    assert bool11d.is_equal(bool21d) == False


def test_smallest_1d():
    assert a1d.min_element() == 1
    assert b1d.min_element() == -4


def test_mean_1d():
    assert a1d.mean_element() == 2.5
    assert b1d.mean_element() == -0.5


# 2D tests (Task 6)


def test_add_2d():
    assert a2d + zero2d == a2d
    assert a2d + b2d == b2d + a2d
    assert a2d + 1 == a2d + one2d
    assert 1 + a2d == a2d + one2d
    assert a2d + b2d == Array((4,2),2,0,6,0,10,0,14,0)
    assert a2d + b2d + b2d == Array((4,2),3,-2,9,-4,15,-6,21,-8)


def test_mult_2d():
    assert a2d * zero2d == Array((4,2),0,0,0,0,0,0,0,0)
    assert a2d * b2d == b2d * a2d
    assert a2d * 1 == a2d
    assert a2d * one2d == a2d
    assert a2d * b2d == Array((4,2),1,-4,9,-16,25,-36,49,-64)
    assert a2d * 10 == Array((4,2),10,20,30,40,50,60,70,80)


def test_same_2d():
    assert a2d.is_equal(a2d) == True
    assert a2d.is_equal(b2d) == False


def test_mean_2d():
    assert a2d.mean_element() == 4.5
    assert b2d.mean_element() == -0.5


# nd tests (only 3d because the amount of numbers you have to write is stupid for larger)

# same tests as 2d because the amount of elements is the same
def test_add_3d():
    assert a3d + zero3d == a3d
    assert a3d + b3d == b3d + a3d
    assert a3d + 1 == a3d + one3d
    assert 1 + a3d == a3d + one3d
    assert a3d + b3d == Array((2,2,2),2,0,6,0,10,0,14,0)
    assert a3d + b3d + b3d == Array((2,2,2),3,-2,9,-4,15,-6,21,-8)


def test_mult_3d():
    assert a3d * zero3d == Array((2,2,2),0,0,0,0,0,0,0,0)
    assert a3d * b3d == b3d * a3d
    assert a3d * 1 == a3d
    assert a3d * one3d == a3d
    assert a3d * b3d == Array((2,2,2),1,-4,9,-16,25,-36,49,-64)
    assert a3d * 10 == Array((2,2,2),10,20,30,40,50,60,70,80)


def test_same_3d():
    assert a3d.is_equal(a3d) == True
    assert a3d.is_equal(b3d) == False


def test_mean_3d():
    assert a3d.mean_element() == 4.5
    assert b3d.mean_element() == -0.5



if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """

    # Task 4: 1d tests
    test_str_1d()
    test_add_1d()
    test_sub_1d()
    test_mul_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d()
    test_mult_2d()
    test_same_2d()
    test_mean_2d()

    # Bonus task: nd tests
    test_add_3d()
    test_mult_3d()
    test_same_3d()
    test_mean_3d()

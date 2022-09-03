from array_class import Array

A = Array((4,2),1,2,3,4,5,6,7,8)
B = Array((4,2),1,-2,3,-4,5,-6,7,-8)
C = Array((2,2,2),111,112,121,122,211,212,221,222)
D = Array((2,2),3.14,2.71,1.57,1.41)

print(f"Array A: \n {A}\n")
print(f"Array B: \n {B}\n")
print(f"A + B: \n {A + B}\n")
print(f"A - B: \n {A - B}\n")
print(f"A * B: \n {A * B}\n")
print(f"A * 10: \n {A * 10}\n")
print(f"Array C: \n {C}\n")
print(f"C * 10: \n {C * 10}\n")
print(f"Array D: \n {D}\n")

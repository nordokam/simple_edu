# Программа получает на вход невозрастающую последовательность натуральных чисел.
# После этого вводится число X. Все числа во входных данных натуральные и не превышают 200.
# Выведите индекс, где окажется число Х.
# Если в списке есть элемент с таким значением, то число Х помещается после него.
l = list (input())
x = int (input())
r = l.index(x)
print (r)
n = l[:r+1]
n.append(x)
l=n+l[r+1:]
#print l #Это логично вывести, хоть по условию и не требуется.



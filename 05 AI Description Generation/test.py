def add(*i):
    r = 0
    for x in i:
        r += x
    return r

def concat(**words):
    print(words)
    r = ''
    for w in words.values():
        r += w
    return r

def x(a='a', b='b'):
    print(f'\'a\':\'{a}\', \'b\':\'{b}\'')


# print(f'add(1, 2, 3) = {add(1, 2, 3)}')
# print(concat(a='one', b='two'))
d = {'a':'one'}
# print(concat(**d))
print(x(**d))

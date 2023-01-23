from random import randint

'''
При 300 значениях NO в основном файле кода мы говорим кораблю не стрелять
и если рандом попадет на значение YES, то огонь. 
YES всегда генерируется в рандомных индексах дабы избежать закономерности выстрелов. 
Данная функция вызывается в файле shuter.py
'''
choice_shoots = []
def yes_or_no():
    for i in range(300):
        choice_shoots.append('no') # добавить 300 вариантов no
    for i in range(15):
        choice_shoots.insert(randint(0, 299), 'yes') # в рандомном месте добавить варианты yes
    
    return choice_shoots




size = 0

def increment(num):
    global size
    size += num

def decrement(num):
    global size
    size -= num

def reset():
    global size
    size = 0
    
def get():
    global size
    return size
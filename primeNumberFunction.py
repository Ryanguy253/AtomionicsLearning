from time import sleep

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def calculatePrimes(start,stop):
    res = []

    # Switch Numbers
    if start>stop:
        temp = stop
        stop = start
        start = temp

    for i in range(start,stop):
        if is_prime(i):
            res.append(i)

    # Simulate Long Function By adding sleep
    for i in range(10):
        sleep(1)
        print(f"Long Running Step : {i+1}")

    return res

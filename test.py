import time

start = time.time()
# some code to measure
for i in range(1000000):
    pass
end = time.time()

print("Execution time:", end - start, "seconds")

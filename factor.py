from Pyro4 import expose
from random import randint
import time

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        self.N = 1
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        self.N = self.read_input()
        N = self.N

        # map
        mapped = []
        steps = [1, 3, 5, 7]
        start_time = time.time()
        for i in range(0, len(steps)):
            worker_index = i % len(self.workers)
            mapped.append(self.workers[worker_index].mymap(N, steps[i]))
        print('Map finished: ', mapped)

        # reduce
        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))
        finish_time = time.time()
        
        # output
        self.write_output(reduced)
        print("Time: ",finish_time-start_time)
        print("Job Finished")

    @staticmethod
    @expose
    def mymap(N, step):
        def gcd(x, y):
            while (y):
                x, y = y, x % y
            return x

        x = randint(1, N - 2)
        y = 1
        i = 0
        stage = 2
        while gcd(N, abs(x - y)) == 1:
            if i == stage:
                y = x
                stage *= 2
            x = (x * x + step) % N
            i += 1
        return gcd(N, abs(x - y))

    @staticmethod
    @expose
    def myreduce(mapped):
        output = []
        for x in mapped:
            if x.value != 1:
                output.append(x.value)
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        if len(output) == 0:
            f.write("Could not find the divider")
        else:
            f.write(str(self.N) + " = " + str(output[0]) + " * " + str(self.N / output[0]))
        f.write('\n')
        f.close()

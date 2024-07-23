import sys
import math

# Via Discussion Forum, credit goes to Caleb C. for the following class.
# This class is used to generate random numbers for the CPU bound and IO bound processes.
# The random number generator is seeded with a given seed value.
class RandomNumberGenerator:
    def __init__(self):
        self.x_n = 0
    
    def srand48(self, seed):
        self.x_n= (seed << 16) + 0x330E
    
    def drand48(self):
        a = 0x5DEECE66D
        c = 0xB
        m = pow(2,48)
        x_n_plus_1 = (a * self.x_n + c) % m
        self.x_n = x_n_plus_1
        return x_n_plus_1/m


# This class represents a process. Each process has a process ID, arrival time, number of CPU bursts, CPU burst times, and IO burst times.
# Storing this for each process allows for easy access to the process information for the simulation.
# And presumably whatever else we are going to have to do.
class Process:
    def __init__(self):
        self.process_id = ""
        self.arrival_time = 0
        self.num_CPU_bursts = 0
        self.CPU_burst_times = []
        self.IO_burst_times = []
        self.is_CPU_bound = False
        self.is_IO_bound = False

    def __init__(self, process_id, arrival_time, num_CPU_bursts, CPU_burst_times, IO_burst_times, is_CPU_bound, is_IO_bound):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.num_CPU_bursts = num_CPU_bursts
        self.CPU_burst_times = CPU_burst_times
        self.IO_burst_times = IO_burst_times
        self.is_CPU_bound = is_CPU_bound
        self.is_IO_bound = is_IO_bound



# CPU class to store the inputs and generate the processes with the given seed and lambda values.
# The CPU class generates the processes and stores them in a list.
# The CPU class also has a method to print the processes in the required format.
class CPU:
    def __init__(self, num_processes, num_cpu_bound, seed, lambda_val, upper_bound):
        # Input parameters
        self.num_processes = num_processes
        self.num_cpu_bound = num_cpu_bound
        self.seed = seed
        self.lambda_val = lambda_val
        self.upper_bound = upper_bound

        # Create and seed the random number generator
        self.rng = RandomNumberGenerator()
        self.rng.srand48(seed)

        # List of processes
        self.processes = []


    # Not sure if this is the correct way to generate the next exponential value
    def next_exp(self):
        x = -math.log(self.rng.drand48()) / self.lambda_val
        while(x > self.upper_bound):
            x = -math.log(self.rng.drand48()) / self.lambda_val
        return x

    # Generate the CPU bound and IO bound processes following the instructions in the project description
    def generate_processes(self):
        # Generate CPU bound processes
        
        # POSSIBLE BUG: the order in which we generate the CPU bound and IO bound processes could be wrong
        # since we are supposed to get certain random numbers for each, thus we may need to follow a certain order
        # I'm not sure what that would be though...
        
        name_counter = 0
        for i in range(self.num_cpu_bound):
            # Set the process ID, arrival time, and number of CPU bursts
            process = Process(self.process_id_string(name_counter), math.floor(self.next_exp()), math.ceil(self.rng.drand48() * 32), [], [], True, False)

            # Generate the CPU burst times and IO burst times for the process
            for j in range(process.num_CPU_bursts):
                # for the last CPU burst, we don't need to generate an IO burst time
                if(j == process.num_CPU_bursts - 1):
                    process.CPU_burst_times.append(math.ceil(self.next_exp()) * 4) # CPU bound
                else:
                    process.CPU_burst_times.append(math.ceil(self.next_exp()) * 4) # CPU bound
                    process.IO_burst_times.append(math.ceil(self.next_exp()))

            # Add to list and increment the name counter
            self.processes.append(process)
            name_counter += 1
        
        # Generate IO bound processes
        for i in range(self.num_processes - self.num_cpu_bound):
            # Set the process ID, arrival time, and number of CPU bursts
            process = Process(self.process_id_string(name_counter), math.floor(self.next_exp()), math.ceil(self.rng.drand48() * 32), [], [], False, True)

            # Generate the CPU burst times and IO burst times for the process
            for j in range(process.num_CPU_bursts):
                if(j == process.num_CPU_bursts - 1):
                    process.CPU_burst_times.append(math.ceil(self.next_exp()))
                else:
                    process.CPU_burst_times.append(math.ceil(self.next_exp()))
                    process.IO_burst_times.append(math.ceil(self.next_exp()) * 8) # IO bound

            # Add to list and increment the name counter
            self.processes.append(process)
            name_counter += 1

    # IMPLEMENT ME
    def run_simulation(self):
        # this method is inteded to "run" the simulation, but in reality it will calculate certain statistics
        # From the project description:
        # - Turnaround Time:
        #       Turnaround times are to be measured for each process that you simulate. Turnaround time is
        #       defined as the end-to-end time a process spends in executing a single CPU burst.
        #       More specifically, this is measured from process arrival time through to when the CPU burst is
        #       completed and the process is switched out of the CPU. Therefore, this measure includes the second
        #       half of the initial context switch in and the first half of the final context switch out, as well as any
        #       other context switches that occur while the CPU burst is being completed (i.e., due to preemptions).
        # - Waiting Time:
        #       Wait times are to be measured for each CPU burst. Wait time is defined as the amount of time
        #       a process spends waiting to use the CPU, which equates to the amount of time the given process
        #       is actually in the ready queue. Therefore, this measure does not include context switch times that
        #       the given process experiences, i.e., only measure the time the given process is actually in the ready
        #       queue.
        # - CPU utilization:
        #       Calculate CPU utilization by tracking how much time the CPU is actively running CPU bursts
        #       versus total elapsed simulation time.
        pass

    # IMPLEMENT ME
    # Writes the summary statistics to the output file in the required format
    def write_output(self):
        filepath = "simout.txt"
        with open(filepath, 'w') as file:
            # Write the summary statistics to the file
            file.write(f"number of processes: {self.num_processes}\n")
            file.write(f"number of CPU-bound processes: {self.num_cpu_bound}\n")
            file.write(f"number of I/O-bound processes: {self.num_processes - self.num_cpu_bound}\n")

            # IMPLEMENT ME
            print("IMPLEMENT ME - write_output()")

            file.write(f"CPU-bound average CPU burst time: {0}ms\n")
            file.write(f"I/O-bound average CPU burst time: {0}ms\n")
            file.write(f"overall average CPU burst time: {0}ms\n")
            file.write(f"CPU-bound average I/O burst time: {0}ms\n")
            file.write(f"I/O-bound average I/O burst time: {0}ms\n")
            file.write(f"overall average I/O burst time: {0}ms\n")

    # Print the processes in the required format to the terminal
    def print_processes(self):
        # Sort processes so that CPU-bound processes come first
        self.processes.sort(key=lambda x: x.process_id)
        
        for process in self.processes:
            # Print the process information
            if(process.is_CPU_bound):
                print(f"CPU-bound process {process.process_id}: arrival time {process.arrival_time}ms; {process.num_CPU_bursts} CPU bursts:")
            else:
                print(f"I/O-bound process {process.process_id}: arrival time {process.arrival_time}ms; {process.num_CPU_bursts} CPU bursts:")

            
            # Print the CPU and IO burst times
            for i in range(len(process.CPU_burst_times)):
                if(i == len(process.CPU_burst_times) - 1):
                    print(f"==> CPU burst {process.CPU_burst_times[i]}ms")
                else:
                    print(f"==> CPU burst {process.CPU_burst_times[i]}ms ==> I/O burst {process.IO_burst_times[i]}ms")
            

    # returns the A0 - Z9 string representation of the process
    def process_id_string(self, process_number):
        letter = chr(ord('A') + process_number // 10)
        number = process_number % 10
        return f"{letter}{number}"

    # Prints the input parameters in the required format for the start of the terminal output
    def print_input(self):
        print("<<< PROJECT PART I")
        if(self.num_cpu_bound == 1):
            print(f"<<< -- process set (n={self.num_processes}) with {self.num_cpu_bound} CPU-bound process")
        else:
            print(f"<<< -- process set (n={self.num_processes}) with {self.num_cpu_bound} CPU-bound processes")
        print(f"<<< -- seed={self.seed}; lambda={self.lambda_val:.6f}; bound={self.upper_bound}")



# -----------------------------------------------------------------
#           MAIN 
# -----------------------------------------------------------------

# IMPLEMENT ERROR CHECKING ON INPUTS

if(len(sys.argv) != 6):
    sys.stderr.write("ERROR: <Incorrect number of arguments>")
    sys.exit(1)

num_processes = int(sys.argv[1])
num_cpu_bound = int(sys.argv[2])
seed = int(sys.argv[3])
lambda_val = float(sys.argv[4])
upper_bound = int(sys.argv[5])

if(num_processes <= 0 or num_cpu_bound < 0 or lambda_val <= 0 or upper_bound < 0):
    sys.stderr.write("ERROR: <Invalid input values>")
    sys.exit(1)


cpu = CPU(num_processes, num_cpu_bound, seed, lambda_val, upper_bound)
cpu.print_input()
cpu.generate_processes()
cpu.print_processes()

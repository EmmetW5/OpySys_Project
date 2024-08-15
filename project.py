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
    def __init__(self, num_processes, num_cpu_bound, seed, lambda_val, upper_bound, context_switch, alpha, time_slice):
        # Input parameters
        self.num_processes = num_processes
        self.num_cpu_bound = num_cpu_bound
        self.seed = seed
        self.lambda_val = lambda_val
        self.upper_bound = upper_bound
        self.context_switch = context_switch
        self.alpha = alpha
        self.time_slice = time_slice
        

        # Create and seed the random number generator
        self.rng = RandomNumberGenerator()
        self.rng.srand48(seed)

        # List of processes
        self.processes = []


    # Generate the next exponential random number
    def next_exp(self):
        x = -math.log(self.rng.drand48()) / self.lambda_val
        while(x > self.upper_bound):
            x = -math.log(self.rng.drand48()) / self.lambda_val
        return x

    # Generate the CPU bound and IO bound processes following the instructions in the project description
    def generate_processes(self):
        # Generate CPU bound processes
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
            # PROCESS -------- label -------------------------------- arrival time ------------- number of CPU bursts ---------------------------- CPU bound
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

    # Calls all the simulation methods, and keeps track of required statistics
    def run_simulation(self):
        self.FCFS()
        self.SJF()
        self.SRT()
        self.RR()

    # The FCFS algorithm is a non-preemptive algorithm in which processes simply line up in the ready
    # queue, waiting to use the CPU. This is your baseline algorithm.
    def FCFS(self):
        # print initial state and arrival time
        self.print_event(0, "Simulator started for FCFS", [])

        curr_process = self.processes[0]
        time = curr_process.arrival_time
        queue = [] + [curr_process]
        event = "Process " + curr_process.process_id + " arrived; added to ready queue"
        self.print_event(time, event, [])







    # In SJF, processes are stored in the ready queue in order of priority based on their anticipated CPU
    # burst times. More specifically, the process with the shortest predicted CPU burst time will be
    # selected as the next process executed by the CPU. SJF is non-preemptive.\
    def SJF(self):
        pass
    
    # The SRT algorithm is a preemptive version of the SJF algorithm. In SRT, when a process arrives,
    # if it has a predicted CPU burst time that is less than the remaining predicted time of the currently
    # running process, a preemption occurs. When such a preemption occurs, the currently running
    # process is added to the ready queue based on priority, i.e., based on its remaining predicted CPU
    # burst time.
    def SRT(self):
        pass
    
    # The RR algorithm is essentially the FCFS algorithm with time slice tslice. Each process is given
    # tslice amount of time to complete its CPU burst. If the time slice expires, the process is preempted
    # and added to the end of the ready queue.
    # If a process completes its CPU burst before a time slice expiration, the next process on the ready
    # queue is context-switched in to use the CPU.
    def RR(self):
        pass
    
    def print_event(self, time, event_details, queue):
        # convert the current contents of the queue to a string
        queue_string = ""
        for process in queue:
            queue_string += process.process_id + " "
        if (len(queue) == 0):
            queue_string = "empty"
        print(f"time {time}ms: {event_details} [Q {queue_string}]")

    # Writes the summary statistics to the output file in the required format
    # This thing is a bear fr fr
    def write_output(self):
        filepath = "simout.txt"
        with open(filepath, 'w') as file:
            # Write the summary statistics to the file
            file.write(f"-- number of processes: {self.num_processes}\n")
            file.write(f"-- number of CPU-bound processes: {self.num_cpu_bound}\n")
            file.write(f"-- number of I/O-bound processes: {self.num_processes - self.num_cpu_bound}\n")

            # Get the sum of the CPU burst times for CPU-bound and IO-bound processes
            sum_cpu_bound_cpu_burst_time = sum([sum(process.CPU_burst_times) for process in self.processes if process.is_CPU_bound])
            sum_io_bound_cpu_burst_time = sum([sum(process.CPU_burst_times) for process in self.processes if process.is_IO_bound])
            sum_overall_cpu_burst_time = sum([sum(process.CPU_burst_times) for process in self.processes])
            sum_cpu_bound_io_burst_time = sum([sum(process.IO_burst_times) for process in self.processes if process.is_CPU_bound])
            sum_io_bound_io_burst_time = sum([sum(process.IO_burst_times) for process in self.processes if process.is_IO_bound])
            sum_overall_io_burst_time = sum([sum(process.IO_burst_times) for process in self.processes])

            
            
            if(self.num_cpu_bound == 0):
                # If there are no CPU-bound processes, set the CPU-bound average burst times to 0
                cpu_bound_avg_cpu_burst_time = 0

                temp_denom = sum([len(process.CPU_burst_times) for process in self.processes if process.is_IO_bound])
                if (temp_denom > 0):
                    io_bound_avg_cpu_burst_time = sum_io_bound_cpu_burst_time / temp_denom
                else:
                    io_bound_avg_cpu_burst_time = 0
                overall_avg_cpu_burst_time = io_bound_avg_cpu_burst_time
                cpu_bound_avg_io_burst_time = 0

                temp_denom = sum([len(process.IO_burst_times) for process in self.processes if process.is_IO_bound])
                if (temp_denom > 0):
                    io_bound_avg_io_burst_time = sum_io_bound_io_burst_time / temp_denom
                else:
                    io_bound_avg_io_burst_time = 0

                overall_avg_io_burst_time = io_bound_avg_io_burst_time

            else:
                temp_denom = sum([len(process.CPU_burst_times) for process in self.processes if process.is_CPU_bound])
                if (temp_denom > 0):
                    cpu_bound_avg_cpu_burst_time = sum_cpu_bound_cpu_burst_time / temp_denom
                else:
                    cpu_bound_avg_cpu_burst_time = 0

                temp_denom = sum([len(process.CPU_burst_times) for process in self.processes if process.is_IO_bound])
                if (sum([len(process.CPU_burst_times) for process in self.processes if process.is_IO_bound]) > 0):
                    io_bound_avg_cpu_burst_time = sum_io_bound_cpu_burst_time / temp_denom
                else:
                    io_bound_avg_cpu_burst_time = 0

                temp_denom = sum([len(process.CPU_burst_times) for process in self.processes])
                if (temp_denom > 0):
                    overall_avg_cpu_burst_time = sum_overall_cpu_burst_time / temp_denom
                else:
                    overall_avg_cpu_burst_time = 0

                temp_denom = sum([len(process.IO_burst_times) for process in self.processes if process.is_CPU_bound])
                if(temp_denom > 0):
                    cpu_bound_avg_io_burst_time = sum_cpu_bound_io_burst_time / temp_denom
                else:
                    cpu_bound_avg_io_burst_time = 0

                temp_denom = sum([len(process.IO_burst_times) for process in self.processes if process.is_IO_bound])
                if (temp_denom > 0):
                    io_bound_avg_io_burst_time = sum_io_bound_io_burst_time / temp_denom
                else:
                    io_bound_avg_io_burst_time = 0

                temp_denom = sum([len(process.IO_burst_times) for process in self.processes])
                if (temp_denom > 0):
                    overall_avg_io_burst_time = sum_overall_io_burst_time / temp_denom
                else:
                    overall_avg_io_burst_time = 0 

                # Take the ceiling of the average burst times to 3 decimal places
                cpu_bound_avg_cpu_burst_time = math.ceil((cpu_bound_avg_cpu_burst_time) * 1000) / 1000
                io_bound_avg_cpu_burst_time = math.ceil((io_bound_avg_cpu_burst_time) * 1000) / 1000
                overall_avg_cpu_burst_time = math.ceil((overall_avg_cpu_burst_time) * 1000) / 1000
                cpu_bound_avg_io_burst_time = math.ceil((cpu_bound_avg_io_burst_time) * 1000) / 1000
                io_bound_avg_io_burst_time = math.ceil((io_bound_avg_io_burst_time) * 1000) / 1000
                overall_avg_io_burst_time = math.ceil((overall_avg_io_burst_time) * 1000) / 1000


            file.write(f"-- CPU-bound average CPU burst time: {cpu_bound_avg_cpu_burst_time:.3f} ms\n")
            file.write(f"-- I/O-bound average CPU burst time: {io_bound_avg_cpu_burst_time:.3f} ms\n")
            file.write(f"-- overall average CPU burst time: {overall_avg_cpu_burst_time:.3f} ms\n")
            file.write(f"-- CPU-bound average I/O burst time: {cpu_bound_avg_io_burst_time:.3f} ms\n")
            file.write(f"-- I/O-bound average I/O burst time: {io_bound_avg_io_burst_time:.3f} ms\n")
            file.write(f"-- overall average I/O burst time: {overall_avg_io_burst_time:.3f} ms\n")

    # Print the processes in the required format to the terminal
    def print_processes(self):
        # Sort processes so that CPU-bound processes come first
        self.processes.sort(key=lambda x: x.process_id)
        
        for process in self.processes:
            # Print the process information
            if(process.is_CPU_bound):
                if (process.num_CPU_bursts == 1):
                    print(f"CPU-bound process {process.process_id}: arrival time {process.arrival_time}ms; {process.num_CPU_bursts} CPU burst:")
                else:
                    print(f"CPU-bound process {process.process_id}: arrival time {process.arrival_time}ms; {process.num_CPU_bursts} CPU bursts:")
            else:
                if (process.num_CPU_bursts == 1):
                    print(f"I/O-bound process {process.process_id}: arrival time {process.arrival_time}ms; {process.num_CPU_bursts} CPU burst:")
                else:
                    print(f"I/O-bound process {process.process_id}: arrival time {process.arrival_time}ms; {process.num_CPU_bursts} CPU bursts:")


            # legacy code for part I, no longer needed to output here in this format

            # Print the CPU and IO burst times
            # for i in range(len(process.CPU_burst_times)):
            #     if(i == len(process.CPU_burst_times) - 1):
            #         print(f"==> CPU burst {process.CPU_burst_times[i]}ms")
            #     else:
            #         print(f"==> CPU burst {process.CPU_burst_times[i]}ms ==> I/O burst {process.IO_burst_times[i]}ms")
            
            # end legacy

    # returns the A0 - Z9 string representation of the process
    def process_id_string(self, process_number):
        letter = chr(ord('A') + process_number // 10)
        number = process_number % 10
        return f"{letter}{number}"

    # Prints the input parameters in the required format for the start of the terminal output
    def print_input_p1(self):
        # part I stuff
        print("<<< PROJECT PART I")
        if(self.num_cpu_bound == 1):
            print(f"<<< -- process set (n={self.num_processes}) with {self.num_cpu_bound} CPU-bound process")
        else:
            print(f"<<< -- process set (n={self.num_processes}) with {self.num_cpu_bound} CPU-bound processes")
        print(f"<<< -- seed={self.seed}; lambda={self.lambda_val:.6f}; bound={self.upper_bound}")
        
    def print_input_p2(self):
        # part II stuff
        print("\n<<< PROJECT PART II")
        print(f"<<< -- t_cs={self.context_switch}ms; alpha={self.alpha:.2f}; t_slice={self.time_slice}ms")

        
def check_input(num_processes, num_cpu_bound, seed, lambda_val, upper_bound, context_switch, alpha, time_slice):
    if(num_processes <= 0 or num_processes > 260):
        sys.stderr.write("ERROR: <Invalid number of processes>")
        sys.exit(1)
    if(lambda_val <= 0):
        sys.stderr.write("ERROR: <Invalid lambda value>")
        sys.exit(1)
    if(num_cpu_bound < 0 or num_cpu_bound > num_processes):
        sys.stderr.write("ERROR: <Invalid number of CPU-bound processes>")
        sys.exit(1)
    if(upper_bound <= 0):
        sys.stderr.write("ERROR: <Invalid upper bound>")
        sys.exit(1)
    if(context_switch <= 0):
        sys.stderr.write("ERROR: <Invalid context switch>")
        sys.exit(1)
    if(alpha < 0 or alpha > 1):
        sys.stderr.write("ERROR: <Invalid alpha>")
        sys.exit(1)
    if(time_slice <= 0):
        sys.stderr.write("ERROR: <Invalid time slice>")
        sys.exit(1)

    
# -----------------------------------------------------------------
#           MAIN 
# -----------------------------------------------------------------
if __name__ == "__main__":
    if(len(sys.argv) != 9):
        sys.stderr.write("ERROR: <Incorrect number of arguments>")
        sys.exit(1)

    # Get the input parameters
    num_processes = int(sys.argv[1])
    num_cpu_bound = int(sys.argv[2])
    seed = int(sys.argv[3])
    lambda_val = float(sys.argv[4])
    upper_bound = int(sys.argv[5])

    # implement error checking on the new inputs!!
    context_switch = int(sys.argv[6])
    alpha = float(sys.argv[7])
    time_slice = int(sys.argv[8])


    # Check the input parameters
    check_input(num_processes, num_cpu_bound, seed, lambda_val, upper_bound, context_switch, alpha, time_slice)

    # Create the CPU object and generate the output
    cpu = CPU(num_processes, num_cpu_bound, seed, lambda_val, upper_bound, context_switch, alpha, time_slice)
    cpu.print_input_p1()
    cpu.generate_processes()
    cpu.print_processes() # for part 1

    # Run simulation and output for part 2
    cpu.print_input_p2()
    cpu.run_simulation()
    cpu.write_output()
    print()
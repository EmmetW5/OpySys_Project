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
        
        # Edited In Functions
        self.burst_index = 0      # index of current Burst time, used in all
        self.IO_index = 0         # index of current IO Block Time, used in all
        self.IO_unblocked = 0     # time that this process is no longer blocked used in FCFS,
        self.remaining_time = []  # time process need to finish burst used in RR,

# CPU class to store the inputs and generate the processes with the given seed and lambda values.
# The CPU class generates the processes and stores them in a list.
# The CPU class also has a method to print the processes in the required format.
class CPU:
    def __init__(self, num_processes, num_cpu_bound, seed, lambda_val, upper_bound, context_switch, alpha, time_slice):
        # Input parameters
        self.num_processes = int(num_processes)
        self.num_cpu_bound = int(num_cpu_bound)
        self.seed = int(seed)
        self.lambda_val = float(lambda_val)
        self.upper_bound = int(upper_bound)
        self.context_switch = int(context_switch)
        self.alpha = float(alpha)
        self.time_slice = int(time_slice)

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
    
    # Calls all the simulation methods, and keeps track of required statistics
    def run_simulation(self):
        #self.FCFS()
        #print()
        self.SJF()
        print()
        self.SRT()
        print()
        self.RR()
        print()



















































    ############################################################################################################
    ###################                             FCFS                                     ###################
    ############################################################################################################


    def print_event(self, time, event_details, queue):
        # Convert the current contents of the queue to a string
        if(time < 10000):
            queue_string = " ".join(process.process_id for process in queue) if queue else "empty"
            print(f"time {time}ms: {event_details} [Q {queue_string}]")
        
    # The FCFS algorithm is a non-preemptive algorithm in which processes simply line up in the ready
    # queue, waiting to use the CPU. This is your baseline algorithm.
    # Potential Error, We assume nothing happens during a context Switch!!!!!!
    def FCFS(self):
        
        # loop Variables
        sorted_process = sorted(self.processes, key=lambda process: process.arrival_time)
        IO_block = []
        CPU_burst = []
        queue = []
        itr = 0                         # Current Time
        
        cpu_free = True                 # Nothing is running On CPU
        running_process: Process = None # Process Running On Cpu
        remove_time = -1                # Time To remove a Process
        
        context_switch_delay = False
        context_switch_add_IO = False
        context_switch_delay_itr = -1
        
        

        # if(queue empty & arrival_times empty & I/O block empty & CPU_burst empty) then loop ends (itr > 150000 infinte looping)
        self.print_event(itr, "Simulator started for FCFS", queue)
        while(queue or IO_block or CPU_burst or sorted_process):
            # Next Process is ready to Arrive add to Queue
            # Arrivals Do Not Effect Time at which processes are Unblocked or Removed or added
            if(sorted_process and sorted_process[0].arrival_time == itr):
                p: Process = sorted_process[0]
                queue.append(p)
                sorted_process.pop(0)
                
                event = "Process " + p.process_id + " arrived; added to ready queue"
                self.print_event(itr, event, queue)
                continue
            
            
            # IO Unblock Add To Queue ( IO_Block is sorted by eairliest Unblock Time)
            # UnBlocks Do Not Effect Time at which processes are Unblocked or Removed or Added
            if(IO_block and IO_block[0].IO_unblocked == itr):
                p: Process = IO_block[0]
                queue.append(p)
                IO_block.pop(0)
                
                event = "Process " + p.process_id + " completed I/O; added to ready queue"
                self.print_event(p.IO_unblocked, event, queue)
                continue
            
            
            # Handle Cpu Burst Remove
            # Removals Do Not Effect Time at which processes are Unblocked or Removed
            # Adds Half Context Switch Delay to Add Time
            if(not cpu_free and remove_time == itr):
                
                if(len(running_process.CPU_burst_times)-running_process.burst_index == 0):
                    # Termination Case
                    event = f"Process {running_process.process_id} terminated"
                    queue_string = " ".join(process.process_id for process in queue) if queue else "empty"
                    print(f"time {itr}ms: {event} [Q {queue_string}]")
                
                elif(len(running_process.CPU_burst_times)-running_process.burst_index == 1):
                    # 1 Bust Left 
                    event = f"Process {running_process.process_id} completed a CPU burst; {len(running_process.CPU_burst_times) - running_process.burst_index} burst to go"
                    self.print_event(itr, event, queue)
                    event = f"Process {running_process.process_id} switching out of CPU; blocking on I/O until time {running_process.IO_unblocked}ms"
                    self.print_event(itr, event, queue)
                else:
                    # Normal Case
                    event = f"Process {running_process.process_id} completed a CPU burst; {len(running_process.CPU_burst_times) - running_process.burst_index} bursts to go"
                    self.print_event(itr, event, queue)
                    event = f"Process {running_process.process_id} switching out of CPU; blocking on I/O until time {running_process.IO_unblocked}ms"
                    self.print_event(itr, event, queue)
                
                running_process = None
                cpu_free = True
                
                context_switch_add_IO = True
                continue
            
            
            # Handle CPU Addition context Switch
            if(queue and cpu_free and not context_switch_delay):
                # calculate the Time To Add Next Prossess
                if(context_switch_add_IO and remove_time == itr):
                    context_switch_delay_itr = itr + int(self.context_switch)
                else:
                    context_switch_delay_itr = itr + int(self.context_switch / 2)

                context_switch_delay = True
                context_switch_add_IO = False
                continue
            
            
            # Handle Add Process To Cpu
            # Calculates Remove Time
            # Calculates Unblock Time Aswell and Stores in Each Process
            if(itr == context_switch_delay_itr and context_switch_delay):
                # Remove Process From Queue
                p: Process = queue[0]
                queue.pop(0)

                # Print and Calculate Remove Time
                event = f"Process {p.process_id} started using the CPU for {p.CPU_burst_times[p.burst_index]}ms burst"
                self.print_event(itr, event, queue)
                remove_time = itr + p.CPU_burst_times[p.burst_index]
                p.burst_index += 1

                # Calculate The Unblock Time and Add to IO Block if theres more to do
                if(p.IO_index in range(len(p.IO_burst_times))):
                    p.IO_unblocked = remove_time + p.IO_burst_times[p.IO_index] + int(self.context_switch / 2)
                    p.IO_index += 1
                    IO_block.append(p)
                    IO_block.sort(key=lambda process: process.IO_unblocked)

                # change Current Running Process
                running_process = p
                cpu_free = False

                context_switch_delay = False
                continue

            itr += 1
        
        # Terminate Last Process and End Loop
        queue_string = " ".join(process.process_id for process in queue) if queue else "empty"
        event = f"Process {running_process.process_id} terminated"
        print(f"time {remove_time}ms: {event} [Q {queue_string}]")
        event = f"Simulator ended for FCFS"
        print(f"time {remove_time + int(self.context_switch / 2)}ms: {event} [Q {queue_string}]")
        
        # Fix Changed Variables :)
        self.processes.clear()
        self.generate_processes()

        
        














    
    ############################################################################################################
    ###################                             SJF                                      ###################
    ############################################################################################################

    # In SJF, processes are stored in the ready queue in order of priority based on their anticipated CPU
    # burst times. More specifically, the process with the shortest predicted CPU burst time will be
    # selected as the next process executed by the CPU. SJF is non-preemptive.
    def SJF(self):
        pass
    

    ############################################################################################################
    ###################                             SRT                                      ###################
    ############################################################################################################
    
    # The SRT algorithm is a preemptive version of the SJF algorithm. In SRT, when a process arrives,
    # if it has a predicted CPU burst time that is less than the remaining predicted time of the currently
    # running process, a preemption occurs. When such a preemption occurs, the currently running
    # process is added to the ready queue based on priority, i.e., based on its remaining predicted CPU
    # burst time.
    def SRT(self):
        pass































    
    ############################################################################################################
    ###################                              RR                                      ###################
    ############################################################################################################
    
    # The RR algorithm is essentially the FCFS algorithm with time slice tslice. Each process is given
    # tslice amount of time to complete its CPU burst. If the time slice expires, the process is preempted
    # and added to the end of the ready queue.
    # If a process completes its CPU burst before a time slice expiration, the next process on the ready
    # queue is context-switched in to use the CPU.
    def RR(self):
        # copy of burst times, so we can decrement them while saving orginal
        for p in self.processes:
            for time in p.CPU_burst_times:
                p.remaining_time.append(time)
        
        # loop Variables
        sorted_process = sorted(self.processes, key=lambda process: process.arrival_time)
        IO_block = []                    # processes that are IO and will return
        queue = []                       # processes that are ready to Run
        itr = 0                          # Current Time
        
        cpu_free = True                  # Nothing is running On CPU
        running_process: Process = None  # Process Running On CPU
        remove_time = -1                 # Time to remove a process
        
        context_switch_delay = False
        context_switch_add_IO = False
        context_switch_delay_itr = -1

        self.print_event(itr, "Simulator started for RR", queue)
        while(queue or IO_block or sorted_process or running_process):
        # Normal Arrival
            # Next Process is ready to Arrive add to Queue
            # Arrivals Do Not Effect Time at which processes are Unblocked or Removed or added
            if(sorted_process and sorted_process[0].arrival_time == itr):
                p: Process = sorted_process[0]
                queue.append(p)
                sorted_process.pop(0)
                
                event = "Process " + p.process_id + " arrived; added to ready queue"
                self.print_event(itr, event, queue)
                continue
            
        # IO Unblock
            # IO Unblock Add To Queue ( IO_Block is sorted by eairliest Unblock Time)
            # UnBlocks Do Not Effect Time at which processes are Unblocked or Removed or Added
            if(IO_block and IO_block[0].IO_unblocked == itr):
                p: Process = IO_block[0]
                queue.append(p)
                IO_block.pop(0)
                
                event = "Process " + p.process_id + " completed I/O; added to ready queue"
                self.print_event(p.IO_unblocked, event, queue)
                continue
            
        
        # Handle Cpu Burst Remove
            # Removals Do Not Effect Time at which processes are Unblocked or Removed
            # Adds Half Context Switch Delay to Add Time
            if(not cpu_free and remove_time == itr):
                p: Process = running_process
                
                if(p.remaining_time[p.burst_index] - self.time_slice <= 0):
                    # Finsihed Burst
                    p.burst_index += 1
                    if(len(p.CPU_burst_times)-p.burst_index == 0):
                        # Termination Case
                        event = f"Process {p.process_id} terminated"
                        queue_string = " ".join(process.process_id for process in queue) if queue else "empty"
                        print(f"time {itr}ms: {event} [Q {queue_string}]")
                    else:
                        # Normal Case
                        if len(p.CPU_burst_times)-p.burst_index == 1:
                            # 1 Bust Left
                            event = f"Process {p.process_id} completed a CPU burst; {len(p.CPU_burst_times) - p.burst_index} burst to go"
                        else:
                            # ? Bursts left
                            event = f"Process {p.process_id} completed a CPU burst; {len(p.CPU_burst_times) - p.burst_index} bursts to go"
                        
                        # Calculate The Unblock Time and Add to IO Block, if theres more to do, 1 burst has no next IO Block Time
                        if(p.IO_index in range(len(p.IO_burst_times))):
                            p.IO_unblocked = remove_time + p.IO_burst_times[p.IO_index] + int(self.context_switch / 2)
                            IO_block.append(p)
                            IO_block.sort(key=lambda process: process.IO_unblocked)
                            p.IO_index += 1
                        
                        self.print_event(itr, event, queue)
                        event = f"Process {p.process_id} switching out of CPU; blocking on I/O until time {p.IO_unblocked}ms"
                        self.print_event(itr, event, queue)
                    
                    running_process = None
                    cpu_free = True
                    context_switch_add_IO = True
                elif(queue):
                    # Preemed and Something to replace it
                    event = f"Time slice expired; preempting process {p.process_id} with {p.remaining_time[p.burst_index] - self.time_slice}ms remaining"
                    self.print_event(itr, event, queue)
                    p.remaining_time[p.burst_index] -= self.time_slice
                    queue.append(p)
                
                    running_process = None
                    cpu_free = True
                    context_switch_add_IO = True
                else:
                    # Preemed, but Nothing to replace it
                    event = f"Time slice expired; no preemption because ready queue is empty"
                    self.print_event(itr, event, queue)
                    p.remaining_time[p.burst_index] -= self.time_slice
                    if(self.time_slice < p.remaining_time[p.burst_index]):
                        remove_time += self.time_slice
                    else:
                        remove_time += p.remaining_time[p.burst_index]
                continue
            
            
        # Handle CPU Addition context Switch
            if(queue and cpu_free and not context_switch_delay):
                # calculate the Time To Add Next Prossess
                if(context_switch_add_IO and remove_time == itr):
                    context_switch_delay_itr = itr + int(self.context_switch)
                else:
                    context_switch_delay_itr = itr + int(self.context_switch / 2)

                context_switch_delay = True
                context_switch_add_IO = False
                continue
            
            
        # Handle Add Process To Cpu
            # Calculates Remove Time
            # Calculates Unblock Time Aswell and Stores in Each Process
            if(itr == context_switch_delay_itr and context_switch_delay):
                # Remove Process From Queue
                p: Process = queue[0]
                queue.pop(0)

                # Print and Calculate Remove Time
                if(p.remaining_time[p.burst_index] == p.CPU_burst_times[p.burst_index]):
                    event = f"Process {p.process_id} started using the CPU for {p.CPU_burst_times[p.burst_index]}ms burst"
                else:
                    event = f"Process {p.process_id} started using the CPU for remaining {p.remaining_time[p.burst_index]}ms of {p.CPU_burst_times[p.burst_index]}ms burst"
                self.print_event(itr, event, queue)
                if(self.time_slice < p.remaining_time[p.burst_index]):
                    remove_time = itr + self.time_slice
                else:
                    remove_time = itr + p.remaining_time[p.burst_index]
                # change Current Running Process
                running_process = p
                cpu_free = False
                
                context_switch_delay = False
                continue
            
            itr += 1
        event = f"Simulator ended for RR"
        print(f"time {remove_time + int(self.context_switch / 2)}ms: {event} [Q {queue_string}]")
        
        # Fix Changed Variables :)
        self.processes.clear()
        self.generate_processes()
        
        
        
    
    



























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
    
    # 2
    # 3 1 32 0.001000 1024 4 0.75 256
    
    # 3
    # 8 6 512 0.001000 1024 6 .90 128
    
    # 4
    # 16 2 256 0.001000 2048 4 0.50 32
    
    # 5
    # 20 12 128 0.010000 4096 4 0.96 64
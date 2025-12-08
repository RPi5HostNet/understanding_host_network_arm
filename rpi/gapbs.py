import subprocess, os, signal, time


class GAPBSRunner:
    def __init__(self, output_path, cores, mem_numa, base_path, workload):
        self.gapbs_path = os.path.join(base_path, workload)
        self.output_path = output_path
        self.cores = cores
        self.mem_numa = mem_numa

        # Default parameters
        self.graph_size = 21 # 2^21 nodes
        self.iterations0 = 30
        self.iterations = self.iterations0

        self.proc = None
        out_f = open(self.output_path, 'w')
        # numactl --membind 3 --physcpubind 3 /path/to/pr -u 21 -n 2
        cores_str = ','.join([str(x) for x in self.cores])
        args = ['numactl', '--membind', str(self.mem_numa), '--physcpubind', ','.join([str(x) for x in self.cores]), self.gapbs_path, '-u', str(self.graph_size), '-n', str(self.iterations)]

        self.proc = subprocess.Popen(args, stdout=out_f, stderr=subprocess.STDOUT)
        # Wait for graph to be initialized
        while True:
            if self.proc.poll():
                # Process has already exited (likely due to error)
                raise Exception('GAPBS process exited before initilization hook')
            read_f = open(self.output_path, 'r')
            done = False
            for line in read_f:
                if 'Graph has' in line:
                    os.kill(self.proc.pid, signal.SIGSTOP)
                    done = True
            if done:
                break
            time.sleep(1)

        print('Initilized GAPBS')

    def run(self, duration):
        # Duration is ignored

        # Simply resume the process
        os.kill(self.proc.pid, signal.SIGCONT)

    def end(self):
        os.kill(self.proc.pid, signal.SIGINT)

    def wait(self):
        if self.proc:
            self.proc.wait()

    def cleanup(self):
        if self.proc:
            self.proc.kill()

if __name__ == "__main__":
    gapbs_core_list = [0,1,2]
    gapbs_runner = GAPBSRunner('./data/gapbs_rpi', gapbs_core_list, 1, '/home/pi/src/gapbs', 'pr')
    gapbs_runner.run(60)  # Run for 60 seconds (duration is ignored)
    gapbs_runner.wait()
    gapbs_runner.cleanup()

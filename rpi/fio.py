import subprocess, os, signal, datetime


class FIORunner:
    def __init__(self, output_path, cores, mem_numa, io_size, io_depth, write_frac, disk):
        self.fio_path = "fio" # os.path.join(path, 'fio')
        self.output_path = output_path
        self.cores = cores
        self.mem_numa = mem_numa

        # Default parameters
        self.io_size = io_size
        self.io_depth = io_depth
        self.write_frac = write_frac
        self.disk = disk
        self.rate_cap = None

        self.proc = None

    def run(self, duration):
        out_f = open(self.output_path, 'w')
        # numactl --membind 3 ./fio --filename=/dev/nvme0n1 --name=test  --ioengine=libaio  --direct=1  --rw=randread  --gtod_reduce=0  --cpus_allowed_policy=split  --time_based  --size=1G  --runtime=10  --cpus_allowed=3,7  --numjobs=2  --bs=$((4*1024))  --iodepth=64 --group_reporting
        cores_str = ','.join([str(x) for x in self.cores])
        args = ['numactl', self.fio_path, '--name=test', '--ioengine=posixaio', '--direct=1', '--gtod_reduce=0', '--cpus_allowed_policy=split', '--time_based', '--runtime=%d'%(duration), '--size=1G', '--cpus_allowed=%s'%(cores_str), '--numjobs=1', '--group_reporting', '--scramble_buffers=0']
        args.append('--filename=%s'%(self.disk))
        args.append('--bs=%d'%(self.io_size))
        args.append('--iodepth=%d'%(self.io_depth))
        
        if self.write_frac == 0:
            args.append('--rw=randread')
        elif self.write_frac == 100:
            args.append('--rw=randwrite')

        if self.rate_cap:
            args.append('--rate_iops=%d'%(self.rate_cap))

        print("Running fio with args: ", args)
        
        self.proc = subprocess.Popen(args, stdout=out_f, stderr=subprocess.STDOUT)

    def end(self):
        os.kill(self.proc.pid, signal.SIGINT)

    def set_ratecap(self, val):
        self.rate_cap = val

    def wait(self):
        if self.proc:
            self.proc.wait()

    def cleanup(self):
        if self.proc:
            self.proc.kill()

if __name__ == "__main__":
    fio_core_list = [0]
    fio_runner = FIORunner('./data/fio_rpi', fio_core_list, 0, 4096, 64, 100, '/dev/nvme0n1')
    start_time = datetime.datetime.now()
    fio_runner.run(60)  # Run for 60 seconds (duration is ignored)
    fio_runner.wait()
    print(datetime.datetime.now() - start_time)
    fio_runner.cleanup()
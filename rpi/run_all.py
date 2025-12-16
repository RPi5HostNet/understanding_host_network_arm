from redis import *
from stream import *
from fio import *
import os

def redis_fio(redis_rw, fio_rw):
    filename = f"./data/redis_{redis_rw}_fio_{fio_rw}"
    os.makedirs(filename, exist_ok=True)
    redis_runner = RedisRunner(filename + "/redis", [0,1], 0, {}, 100000000)
    if redis_rw == 'read':
        redis_runner.set_writefrac(0)
    else:
        redis_runner.set_writefrac(100)
    fio_runner = FIORunner(filename + "/fio", [2, 3], 2, 4096, 64, 100 if fio_rw == 'write' else 0, '/dev/nvme0n1')

    fio_runner.run(60)  # Run for 60 seconds
    redis_runner.run(60)  # Run for 60 seconds (duration is ignored)

    redis_runner.wait()
    fio_runner.wait()
    redis_runner.cleanup()
    fio_runner.cleanup()

def stream_fio(stream_rw, fio_rw, stream_cores):
    filename = f"./data/stream_{stream_rw}_{''.join(str(a) for a in stream_cores)}_fio_{fio_rw}"
    os.makedirs(filename, exist_ok=True)
    stream_runner = STREAMRunner(filename + "/stream", stream_cores, {})
    stream_runner.set_writefrac(0 if stream_rw == 'read' else 100)
    fio_runner = FIORunner(filename + "/fio", [3], 8*1024*1024, 64, 100 if fio_rw == 'write' else 0, '/dev/nvme0n1')

    stream_runner.run(60)  # Run for 60 seconds (duration is ignored)
    fio_runner.run(60)  # Run for 60 seconds

    stream_runner.wait()
    fio_runner.wait()
    stream_runner.cleanup()
    fio_runner.cleanup()


if __name__ == "__main__":
    # redis_fio('read', 'read')
    # redis_fio('read', 'write')
    # redis_fio('write', 'read')
    # redis_fio('write', 'write')
    # redis_runner = RedisRunner('./data/redis_rpi', [0,1,2,3], 0, {}, 10000000)
    # redis_runner.set_writefrac(100)

    for stream_cores in (list(range(n)) for n in range(1,4)):
        stream_fio('read', 'read', stream_cores)
        stream_fio('read', 'write', stream_cores)
        stream_fio('write', 'read', stream_cores)
        stream_fio('write', 'write', stream_cores)
        for stream_rw in ['read', 'write']:
            filename = f'./data/stream_alone_{stream_rw}_{''.join(str(a) for a in stream_cores)}'
            os.makedirs(filename, exist_ok=True)
            stream_runner = STREAMRunner(filename + "/stream", stream_cores, {})
            #stream_runner.init('./data/stream-data', [0], 0, {})
            stream_runner.set_writefrac(0 if stream_rw == 'read' else 100)
            stream_runner.run(60)  # Run for 60 seconds (duration is ignored)
            stream_runner.wait()
            stream_runner.cleanup()

    for fio_rw in []: #['read', 'write']:
        filename = f"./data/fio_alone_{fio_rw}"
        os.makedirs(filename, exist_ok=True)
        fio_runner = FIORunner(filename + "/fio", [3],8*1024*1024, 64, 100 if fio_rw == 'write' else 0, '/dev/nvme0n1')
        fio_runner.run(60)  # Run for 60 seconds
        fio_runner.wait()
        fio_runner.cleanup()

    # redis_runner.set_writefrac(0)
    # redis_runner.run(60)  # Run for 60 seconds (duration is ignored)

    # redis_runner.wait()
    # redis_runner.cleanup()
    #stream_fio('read', 'read')

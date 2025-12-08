from redis import *
from stream import *
from fio import *
import os

def redis_fio(redis_rw, fio_rw):
    filename = f"redis_{redis_rw}_fio_{fio_rw}"
    os.mkdir(f"./{filename}")
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

# def redis_w_fio_w():
#     os.mkdir('redis_w_fio_w')
#     redis_runner = RedisRunner('./redis_w_fio_w/redis', [0,1], 0, {}, 10000000)
#     redis_runner.set_writefrac(100)
#     fio_runner = FIORunner('./redis_w_fio_w/fio', [2, 3], 2, 4096, 64, 100, '/dev/nvme0n1')
#     redis_runner.set_writefrac(100)

#     fio_runner.run(60)  # Run for 60 seconds
#     redis_runner.run(60)  # Run for 60 seconds (duration is ignored)

#     redis_runner.wait()
#     fio_runner.wait()
#     redis_runner.cleanup()
#     fio_runner.cleanup()

if __name__ == "__main__":
    redis_fio('read', 'read')
    redis_fio('read', 'write')
    redis_fio('write', 'read')
    redis_fio('write', 'write')
    # redis_runner = RedisRunner('./data/redis_rpi', [0,1,2,3], 0, {}, 10000000)
    # redis_runner.set_writefrac(100)
    # stream_runner = STREAMRunner('./data/stream_rpi')
    # stream_runner.init('./data/stream-data', [0], 0, {})

    # redis_runner.set_writefrac(0)
    # stream_runner.set_writefrac(0)

    # stream_runner.run(60)  # Run for 60 seconds (duration is ignored)
    # redis_runner.run(60)  # Run for 60 seconds (duration is ignored)

    # redis_runner.wait()
    # stream_runner.wait()
    # redis_runner.cleanup()
    # stream_runner.cleanup()
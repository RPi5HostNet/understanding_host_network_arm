CC = gcc
CFLAGS = -O

FF = g77
FFLAGS = -O2

all: stream.out

stream_f.exe: stream.f mysecond.o
	$(CC) $(CFLAGS) -c mysecond.c
	$(FF) $(FFLAGS) -c stream.f
	$(FF) $(FFLAGS) stream.o mysecond.o -o stream_f.exe

stream.out: stream.c
	$(CC) $(CFLAGS) stream.c -o stream.out -DSTREAM_ARRAY_SIZE=125000000 # 1 GB array, doubles are 8 bytes

clean:
	rm -f stream_f.exe stream_c.exe *.o *.out

# an example of a more complex build line for the Intel icc compiler
stream.icc: stream.c
	icc -O3 -xCORE-AVX2 -ffreestanding -qopenmp -DSTREAM_ARRAY_SIZE=80000000 -DNTIMES=20 stream.c -o stream.omp.AVX2.80M.20x.icc
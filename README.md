#### Compile & Run locally
```
cargo build
mpirun -n 2 ./target/debug/one_many_ping_pong rma 8
mpirun -n 2 ./c_rma 8
mpicc -O3 src/c_rma.c -o c_rma -lm
```

#### Run MPI code in DAS6
```
prun -np 2 -1 -script $PRUN_ETC/prun-openmpi `pwd`/./target/release/one_many_ping_pong rma 8
prun -np 2 -1 OMPI_OPTS="--mca btl tcp,self --mca btl_tcp_if_include ib0" -script $PRUN_ETC/prun-openmpi `pwd`/./target/release/one_many_ping_pong rma 32
prun -np 2 -1 -script $PRUN_ETC/prun-openmpi `pwd`/./c_rma 8
```
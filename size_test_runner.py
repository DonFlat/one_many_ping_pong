import argparse
import subprocess
import os

def run_command(command):
    # Execute the command without capturing output
    subprocess.run(command, shell=True)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Execute network commands for varying message sizes and manage output files based on the network mode.')
    parser.add_argument('node_num', type=int, help='Number of nodes')
    parser.add_argument('max_size', type=int, help='Maximum exponent for size 2^max_size')
    parser.add_argument('network_mode', choices=['ib', 'ip'], help='Network mode (ib or ip)')

    # Parse arguments
    args = parser.parse_args()

    # Calculate sizes from 2^0 to 2^max_size
    sizes = [2**i for i in range(args.max_size + 1)]

    # Define commands and filenames based on network mode
    if args.network_mode == 'ib':
        base_command = f"prun -np {args.node_num} -1 -script $PRUN_ETC/prun-openmpi `pwd`/"
        filenames = ["rma_size_direct_ib.csv", "c_rma_size_direct_ib.csv"]
        programs = ["./target/release/one_many_ping_pong rma ", "./c_rma "]
    else:  # network_mode == 'ip'
        base_command = f"prun -np {args.node_num} -1 OMPI_OPTS=\"--mca btl tcp,self --mca btl_tcp_if_include ib0\" -script $PRUN_ETC/prun-openmpi `pwd`/"
        filenames = ["rma_size_direct_ip.csv", "c_rma_size_direct_ip.csv"]
        programs = ["./target/release/one_many_ping_pong rma ", "./c_rma "]

    # Execute commands for each size
    for size in sizes:
        for program, filename in zip(programs, filenames):
            command = f"{base_command}{program}{size}"
            print(f"Running command: {command}")
            run_command(command)

    if os.path.exists("rma.csv"):
        os.rename("rma.csv", f"rma_size_{args.network_mode}.csv")
    if os.path.exists("c_rma.csv"):
        os.rename("c_rma.csv", f"c_rma_size_{args.network_mode}.csv")


if __name__ == "__main__":
    main()

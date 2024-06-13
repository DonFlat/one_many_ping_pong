import argparse
import subprocess
import os

def run_command(command):
    # Execute the command without capturing output
    subprocess.run(command, shell=True)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Execute network commands and manage output files based on the network mode.')
    parser.add_argument('node_num', type=int, help='Number of nodes')
    parser.add_argument('max_size', type=int, help='Maximum size')
    parser.add_argument('network_mode', choices=['ib', 'ip'], help='Network mode (ib or ip)')

    # Parse arguments
    args = parser.parse_args()

    # Define and run commands based on network mode
    if args.network_mode == 'ib':
        commands = [
            f"prun -np {args.node_num} -1 -script $PRUN_ETC/prun-openmpi `pwd`/./target/release/one_many_ping_pong rma {args.max_size}",
            f"prun -np {args.node_num} -1 -script $PRUN_ETC/prun-openmpi `pwd`/./c_rma {args.max_size}"
        ]
        filenames = ["rma_size_direct_ib.csv", "c_rma_size_direct_ib.csv"]
    else:  # network_mode == 'ip'
        commands = [
            f"prun -np {args.node_num} -1 OMPI_OPTS=\"--mca btl tcp,self --mca btl_tcp_if_include ib0\" -script $PRUN_ETC/prun-openmpi `pwd`/./target/release/one_many_ping_pong rma {args.max_size}",
            f"prun -np {args.node_num} -1 OMPI_OPTS=\"--mca btl tcp,self --mca btl_tcp_if_include ib0\" -script $PRUN_ETC/prun-openmpi `pwd`/./c_rma {args.max_size}"
        ]
        filenames = ["rma_size_ip_over_ib.csv", "c_rma_size_ip_over_ib.csv"]

    # Run commands and rename output files
    for cmd, filename in zip(commands, ["rma.csv", "c_rma.csv"]):
        run_command(cmd)
        # Rename file if it exists
        if os.path.exists(filename):
            os.rename(filename, filenames[0 if filename == "rma.csv" else 1])


if __name__ == "__main__":
    main()

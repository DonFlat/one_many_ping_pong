import argparse
import subprocess
import os

def run_command(command):
    # Execute the command without capturing output
    subprocess.run(command, shell=True)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Execute network commands for varying node numbers and manage output files based on the network mode.')
    parser.add_argument('size', type=int, help='Fixed message size for the test')
    parser.add_argument('network_mode', choices=['ib', 'ip'], help='Network mode (ib or ip)')

    # Parse arguments
    args = parser.parse_args()

    # Define node number range from 2 to 16
    node_numbers = range(2, 17)

    # Define commands and filename templates based on network mode
    if args.network_mode == 'ib':
        base_command = "-1 -script $PRUN_ETC/prun-openmpi `pwd`/"
        programs = ["./target/release/one_many_ping_pong rma ", "./c_rma "]
    else:  # network_mode == 'ip'
        base_command = "-1 OMPI_OPTS=\"--mca btl tcp,self --mca btl_tcp_if_include ib0\" -script $PRUN_ETC/prun-openmpi `pwd`/"
        programs = ["./target/release/one_many_ping_pong rma ", "./c_rma "]

    # Execute commands for each node number
    for node_num in node_numbers:
        for program, output_file in zip(programs, ["rma.csv", "c_rma.csv"]):
            command = f"prun -np {node_num} {base_command}{program}{args.size}"
            print(f"Running command: {command}")
            run_command(command)
            # Rename file if it exists

    for filename in ["rma.csv", "c_rma.csv"]:
        new_filename = f"{filename[:-4]}_node_{args.network_mode}.csv"
        os.rename(filename, new_filename)


if __name__ == "__main__":
    main()

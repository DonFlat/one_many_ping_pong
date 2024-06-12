#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>

void write_to_csv(double window_size, int node_num, double* latency) {
    // Open a file for appending
    FILE *fpt = fopen("c_rma.csv", "a");
    if (fpt == NULL) {
        printf("Error opening the file.\n");
        return;
    }

    // Write the window_size as the first column
    fprintf(fpt, "%d", (int)window_size);
    fprintf(fpt, ",%d", (int)node_num);

    // Write the elements of the latency array as the rest of the columns
    for (int i = 0; i < 12; i++) {
        fprintf(fpt, ",%f", latency[i]);
    }

    // End the line for CSV row
    fprintf(fpt, "\n");

    // Close the file
    fclose(fpt);

    printf("Data appended to c_rma.csv\n");
}

double* powers_of_two(double size) {
    double* result = malloc(size * sizeof(double));
    if (result == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    for (int i = 0; i < size; i++) {
        result[i] = pow(2, i);
    }

    return result;
}

void ping_pong(char *argv[], int window_size, int node_num, int rank) {
    //  ---- Start RMA
    // Initialize Window
    double *window_base;
    MPI_Win window_handle;

    MPI_Win_allocate(window_size * sizeof(double), sizeof(double), MPI_INFO_NULL, MPI_COMM_WORLD, &window_base, &window_handle);
    // latency data
    double latencies[12];
    // start
    for (int i = 0; i < 12; i++) {
        double start_time = MPI_Wtime();
        MPI_Win_fence(0, window_handle);

        if (rank == 0) {
            for (int i = 1; i < node_num; i++) {
                MPI_Put(window_base,window_size, MPI_DOUBLE, i, 0, window_size, MPI_DOUBLE, window_handle);
            }
        }
        MPI_Win_fence(0, window_handle);
        if (rank != 0) {
            MPI_Put(window_base, window_size, MPI_DOUBLE, 0, 0, window_size, MPI_DOUBLE, window_handle);
        }
        MPI_Win_fence(0, window_handle);

        double end_time = MPI_Wtime();
        latencies[i] = (end_time - start_time) * 1000000;
    }
    if (rank == 0) {
        write_to_csv(window_size, node_num, latencies);
        printf("Done with vector size: %d\n", window_size);
    }
    MPI_Win_free(&window_handle);
    return;
}

int main(int argc, char *argv[]) {

    //  ---- Initialize MPI environment
    MPI_Init(&argc, &argv);

    int rank, numprocs;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);

    //  ---- Generate test data
    int size = atoi(argv[1]);
    double* powers = powers_of_two(size);

    for (int i = 0; i < size; i++) {
        ping_pong(argv, powers[i], numprocs, rank);
    }

    MPI_Finalize();
    return 0;
}
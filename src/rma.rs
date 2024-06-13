use mpi::Rank;
use mpi::topology::{Communicator, SimpleCommunicator};
use mpi::window::{AllocatedWindow, WindowOperations};
use crate::test_utils::{append_to_csv, powers_of_two};

pub fn ping_pong(size: u32) {
    let universe = mpi::initialize().unwrap();
    let world = universe.world();
    let rank = world.rank();
    let world_size = world.size();

    run_ping_pong(size as usize, rank, world_size, &world);
}

fn run_ping_pong(vector_size: usize, rank: Rank, world_size: Rank, world: &SimpleCommunicator) {
    // *****************
    // * Set up window *
    // *****************
    let mut win: AllocatedWindow<f64> = world.allocate_window(vector_size);
    let mut latency_data = Vec::new();
    // **********************
    // * Start of ping pong *
    // **********************
    for _ in 0..12 {
        let t_start = mpi::time();

        // rank 0 sends to every else
        win.fence();
        if rank == 0 {
            for i in 1..world_size {
                win.put_whole_vector(i as usize);
            }
        }
        win.fence();
        if rank != 0 {
            // win.window_vector.iter_mut().for_each(|x| *x += 1f64);
            win.put_whole_vector(0);
        }
        win.fence();

        let t_end = mpi::time();
        if rank == 0i32 {
            latency_data.push((t_end - t_start) * 1000000f64);
        }
    }
    if rank == 0 {
        // println!("Rank: {}, vec: {:?}", rank, win.window_vector);
        append_to_csv("rma.csv", vector_size, world_size as usize, &latency_data).expect("Failed to write csv");
        println!("Done with: Rank 0: run ping pong with size: {}", vector_size);
    }
}

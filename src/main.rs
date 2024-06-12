extern crate core;

use std::env;
use mpi::topology::Communicator;
mod rma;
mod test_utils;

fn main() {
    let args: Vec<String> = env::args().collect();
    let mpi_type: &str = &args[1];
    let size: u32 = args[2].parse().expect("Failed to parse args[2] as u32");
    match mpi_type {
        "rma" => rma::ping_pong(size),
        _ => println!("Invalid argument, run either ping pong | sor_source_data, rma | norm"),
    }
}

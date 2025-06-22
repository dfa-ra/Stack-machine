import struct
from typing import Tuple


def parse_exec(input_path: str, memory_size: int) -> Tuple[bytearray, bytearray]:
    with open(input_path, "rb") as f:
        data_memory = bytearray(memory_size)

        num_clusters = struct.unpack("<I", f.read(4))[0]

        for _ in range(num_clusters):
            cluster_size = struct.unpack("<I", f.read(4))[0]
            cluster_addr = struct.unpack("<I", f.read(4))[0]

            cluster_data = f.read(cluster_size)

            if cluster_addr < 0 or cluster_addr + cluster_size > memory_size:
                raise ValueError(
                    f"Cluster at address {cluster_addr} exceeds memory bounds"
                )

            data_memory[cluster_addr : cluster_addr + cluster_size] = cluster_data

        start_address = struct.unpack("<I", f.read(4))[0]

        instruction_data = bytearray()
        instruction_data.extend(
            struct.pack("<I", start_address)
        )

        while True:
            instruction_byte = f.read(1)
            if not instruction_byte:
                break
            instruction_data.append(instruction_byte[0])

        return data_memory, instruction_data

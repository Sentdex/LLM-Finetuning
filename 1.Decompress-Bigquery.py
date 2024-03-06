import os
import gzip
import shutil
from concurrent.futures import ProcessPoolExecutor
import time


YEAR = 2016
START = time.time()

total_files_decompressed = 0

compressed_dir = f"{YEAR}_j_c"
decompressed_dir = f"{YEAR}_j"

# Create the decompressed directory if it doesn't exist
if not os.path.exists(decompressed_dir):
    os.makedirs(decompressed_dir)

# Define a function to decompress a file and move it to the decompressed directory
def decompress_file(file_path):
    # if this filepath isn't already in decompressed dir:
    if os.path.exists(os.path.join(decompressed_dir, os.path.basename(file_path))):
        print("Already here! Skipping: ", file_path)
    else:
        # Decompress the file
        with open(file_path, 'rb') as f_in:
            with gzip.open(f_in, 'rb') as f_out:
                shutil.copyfileobj(f_out, open(os.path.join(decompressed_dir, os.path.basename(file_path)), 'wb'))
                print("done ", file_path)
    # Delete the compressed file
    #os.remove(file_path) #  LOL this is why we test with copies... 

# Get a list of all the compressed files in the compressed directory
compressed_files = [os.path.join(compressed_dir, f) for f in os.listdir(compressed_dir) if os.path.isfile(os.path.join(compressed_dir, f))]

# Use a ProcessPoolExecutor to run the decompression process in parallel
with ProcessPoolExecutor() as executor:
    # Use the map function to apply the decompress_file function to each compressed file
    executor.map(decompress_file, compressed_files)

end = time.time()

print(f"time taken: {(end-START)/60} minutes")
print(f"total files decompressed: {total_files_decompressed}")


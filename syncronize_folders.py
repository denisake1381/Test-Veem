# Please implement a program that synchronizes two folders: source and
# replica. The program should maintain a full, identical copy of source
# folder at replica folder. Solve the test task by writing a program in
# Python.
# Synchronization must be one-way: after the synchronization content of the
#  replica folder should be modified to exactly match content of the source
#  folder;
# Synchronization should be performed periodically;

# File creation/copying/removal operations should be logged to a file and to the
#  console output;
# Folder paths, synchronization interval and log file path should be provided
#  using the command line arguments;
# It is undesirable to use third-party libraries that implement folder
#  synchronization;
# It is allowed (and recommended) to use external libraries implementing other
#  well-known algorithms. For example, there is no point in implementing yet
#  another function that calculates MD5 if you need it for the task – it is perfectly
#  acceptable to use a third-party (or built-in) library. 


import os
import shutil
import hashlib
import argparse
import time
import logging

logging.basicConfig(filename='sync.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def calculate_hash(file_path):
    
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(source_folder, replica_folder):
    
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    source_files = os.listdir(source_folder)

    for file_name in source_files:
        source_file_path = os.path.join(source_folder, file_name)
        replica_file_path = os.path.join(replica_folder, file_name)

        if not os.path.exists(replica_file_path):
            shutil.copy2(source_file_path, replica_file_path)
            logging.info(f"Copied: {source_file_path} -> {replica_file_path}")

        elif os.path.isfile(replica_file_path):
            source_file_hash = calculate_hash(source_file_path)
            replica_file_hash = calculate_hash(replica_file_path)

            if source_file_hash != replica_file_hash:
                shutil.copy2(source_file_path, replica_file_path)
                logging.info(f"Updated: {source_file_path} -> {replica_file_path}")

    for file_name in os.listdir(replica_folder):
        replica_file_path = os.path.join(replica_folder, file_name)
        source_file_path = os.path.join(source_folder, file_name)

        if not os.path.exists(source_file_path) and os.path.isfile(replica_file_path):
            os.remove(replica_file_path)
            logging.info(f"Removed: {replica_file_path}")

def main():
    parser = argparse.ArgumentParser(description='Sync two folders periodically')
    parser.add_argument('source_folder', type=str, help='Path to the source folder')
    parser.add_argument('replica_folder', type=str, help='Path to the replica folder')
    parser.add_argument('interval', type=int, help='Sync interval in seconds')
    
    args = parser.parse_args()
    
    source_folder = args.source_folder
    replica_folder = args.replica_folder
    interval = args.interval

    while True:
        sync_folders(source_folder, replica_folder)
        time.sleep(interval)

if __name__ == "__main__":
    main()

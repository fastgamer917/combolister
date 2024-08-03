import os
import multiprocessing
import queue as Queue

def find_lines_with_keyword(file_path, file_name, keyword, output_queue):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if keyword in line:
                    try:
                        output_queue.put((file_name, line.strip()), block=False)
                    except Queue.Full:
                        return
    except Exception as e:
        output_queue.put((file_path, f"Error reading file: {str(e)}"))

def process_files_in_folder(folder_path, keyword, num_processes=4):
    manager = multiprocessing.Manager()
    output_queue = manager.Queue(maxsize=20000)  # Limit queue size to 20000 items
    processes = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            p = multiprocessing.Process(target=find_lines_with_keyword, args=(file_path, file, keyword, output_queue))
            processes.append(p)
            p.start()

            # Limit the number of concurrent processes
            if len(processes) >= num_processes:
                for p in processes:
                    p.join()
                processes = []

    # Ensure all remaining processes are joined
    for p in processes:
        p.join()

    # Collect results from queue
    matches = []
    while not output_queue.empty():
        matches.append(output_queue.get())

    return matches

# Usage example
def search_folder_files(folder_path:str,keyword:str)->list:
    num_processes = 15  # Adjust this based on your system's capabilities
    to_return_list=[]
    matches = process_files_in_folder(folder_path, keyword, num_processes)
    for file_name, combo in matches:
        to_return_list.append({
            "combo":combo,
            "source":file_name,
        })
    return to_return_list

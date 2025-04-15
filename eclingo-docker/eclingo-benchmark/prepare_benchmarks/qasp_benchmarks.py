import os

def prepare_benchmark_bomb_qasp(benchmark_path, BENCHMARK_RUNNING):
    # Create directory for different set of problems. Encoding Directory
    # print(benchmark_path)
    benchmark_name = os.path.basename(benchmark_path)
    dir = os.path.join(BENCHMARK_RUNNING,"experiments","instances", benchmark_name)
    os.mkdir(dir)
    
    # Get both instances and many subdirs
    directories = os.listdir(benchmark_path)
    for directory in directories:
        
        # Path to the current directory (Instances, many)
        current_dir = os.path.join(benchmark_path, directory)
        
        if os.path.isdir(current_dir):
            # Access every different bomb problem set (bt, btc, ...)
            subdirs = os.listdir(current_dir)
            for entry in subdirs:
                
                # Get the full path of the entry
                entry_path = os.path.join(current_dir, entry)
                
                # Check if the entry is a directory
                if os.path.isdir(entry_path):
                    for file_name in os.listdir(entry_path):
                        
                        # Move file to experiments
                        file_path = os.path.join(entry_path, file_name)
                        output_path = os.path.join(dir, os.path.basename(file_name))  
                        
                        os.system(f"cat {file_path} > {output_path}")
                        
def prepare_benchmark_yale_qasp(benchmark_path, BENCHMARK_RUNNING):
    benchmark_name = os.path.basename(benchmark_path)
    dir = os.path.join(BENCHMARK_RUNNING,"experiments","instances", benchmark_name)
    os.mkdir(dir)
    
    current_dir = os.path.join(benchmark_path)
    instances = (instance for instance in os.listdir(current_dir) if instance.endswith(".sh")) 
    for file_name in instances:
        # Move file to experiments
        file_path = os.path.join(current_dir, file_name)
        output_path = os.path.join(dir, os.path.basename(file_name))  
        os.system(f"cat {file_path} > {output_path}")
        
def prepare_benchmark_eligible_qasp(benchmark_path, BENCHMARK_RUNNING):
    benchmark_name = os.path.basename(benchmark_path)
    dir = os.path.join(BENCHMARK_RUNNING,"experiments","instances", benchmark_name)
    os.mkdir(dir)
    
    current_path = os.path.join(benchmark_path)
    instances_path = os.path.join(current_path, "scripts")
    instances = (instance for instance in os.listdir(instances_path) if instance.endswith(".sh")) 
    for file_name in instances:
        # Move file to experiments
        file_path = os.path.join(instances_path, file_name)
        output_path = os.path.join(dir, os.path.basename(file_name))  
        
        os.system(f"cat {file_path} > {output_path}")

def prepare_benchmarks_qasp(benchmark_origin, BENCHMARK_RUNNING):
    for benchmark_path in os.listdir(benchmark_origin):
        benchmark_path = os.path.join(benchmark_origin, benchmark_path)
        if os.path.isdir(benchmark_path):
            if os.path.basename(benchmark_path) == "bomb_problems":
                print("Working on BOMB Problems")
                prepare_benchmark_bomb_qasp(benchmark_path, BENCHMARK_RUNNING)
                # pass
            elif os.path.basename(benchmark_path) == "eligible":
                print("Working on ELIGIBLE Problems")
                prepare_benchmark_eligible_qasp(benchmark_path, BENCHMARK_RUNNING)
                # pass
            else:
                print("Working on YALE Problems")
                prepare_benchmark_yale_qasp(benchmark_path, BENCHMARK_RUNNING)
                # pass
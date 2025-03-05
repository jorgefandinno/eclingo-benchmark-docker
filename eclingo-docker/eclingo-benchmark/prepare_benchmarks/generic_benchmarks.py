import os
        
def prepare_any_benchmarks(benchmark, benchmark_path, BENCHMARK_RUNNING, max_instances):
    benchmark_name = os.path.basename(benchmark_path)
    dir = os.path.join(BENCHMARK_RUNNING,"experiments","instances", benchmark_name)
    
    all_benchmarks = os.listdir(benchmark_path)
    for benchmark_name in all_benchmarks:
        if benchmark != "all" and benchmark != benchmark_name:
            continue
        
        # Path to the current directory, subsequently encoding and instance directory
        current_dir = os.path.join(benchmark_path, benchmark_name)
        encoding_dir = os.path.join(current_dir, "encodings")
        instance_dir = os.path.join(current_dir, "instances")
        
        if os.path.isdir(encoding_dir):
            encodings = os.listdir(encoding_dir)

            for encoding in encodings:
                # Get the full path of the encoding
                encoding_path = os.path.join(encoding_dir, encoding)
                
                # Check if the entry is a directory
                if os.path.isdir(instance_dir):
                    instances = os.listdir(instance_dir)
                    if max_instances is not None:
                        instances = sorted(instances)[:max_instances]

                    for instance in instances:
                        instance_path = os.path.join(instance_dir, instance)

                        output_dir = os.path.join(dir, os.path.basename(benchmark_name))
                        print(output_dir)
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = os.path.join(output_dir, encoding + "_" + instance)
                        
                        os.system(f"cat {encoding_path} {instance_path}  > {output_path}")

if __name__ == "__main__":
    prepare_any_benchmarks("weighted-sequence", "../benchmarks/ezsmt", "../running/benchmark-tool-ezsmt", 2)

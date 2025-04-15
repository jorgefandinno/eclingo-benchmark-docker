import os
        
def prepare_any_benchmarks(benchmark, benchmark_origin, BENCHMARK_RUNNING, max_instances):
    for benchmark_path in os.listdir(benchmark_origin):
        benchmark_path = os.path.join(benchmark_origin, benchmark_path)
        if not os.path.isdir(benchmark_path):
            continue
        
        benchmark_name = os.path.basename(benchmark_path)
        output_dir = os.path.join(BENCHMARK_RUNNING,"experiments","instances", benchmark_name)
        
        if benchmark != "all" and benchmark_name not in benchmark:
            continue
        
        # Path to the benchmark encodings and instances directory
        encoding_dir = os.path.join(benchmark_path, "encodings")
        instance_dir = os.path.join(benchmark_path, "instances")
        
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

                        print(output_dir)
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = os.path.join(output_dir, encoding + "_" + instance)
                        
                        os.system(f"cat {encoding_path} {instance_path}  > {output_path}")

if __name__ == "__main__":
    prepare_any_benchmarks("weighted-sequence", "../benchmarks/ezsmt", "../running/benchmark-tool-ezsmt", 2)

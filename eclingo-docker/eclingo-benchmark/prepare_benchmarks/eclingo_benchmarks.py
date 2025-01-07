import os

def prepare_benchmark_bomb(benchmark_path, BENCHMARK_RUNNING, max_instances=None):
    # Create directory for different set of problems. Encoding Directory
    benchmark_name = os.path.basename(benchmark_path)
    dir = os.path.join(BENCHMARK_RUNNING,"experiments","instances", benchmark_name)
    os.mkdir(dir)
    
    many_dir = os.path.join(dir, "many")
    os.mkdir(many_dir)
    
    base_dir = os.path.join(dir, "base")
    os.mkdir(base_dir)

    # print("\nThe dir: ", dir)
    # print("\nThe dir: ", many_dir)
    # print("\nThe dir: ", base_dir)
    # print()
        
    # For every encoding, run every subset.
    encodings = (encoding for encoding in os.listdir(benchmark_path) if encoding.endswith(".lp")) # encodings
    base_encoding = "./benchmarks/eclingo/bomb_problems/bt_base.lp"
    for encoding in encodings:
        if encoding == "bt_base.lp":
            continue
        else:    
            encoding_path = os.path.join(benchmark_path, os.path.basename(encoding))
            encoding = encoding.split('.')[0]
            
        # print("The encoding path: ", encoding_path)
        # print("The base encoding: ", base_encoding)
        
        instances_path = os.path.join(benchmark_path, "instances")
        # print("The instances path: ", instances_path)
        
        instances_many_path = os.path.join(benchmark_path, "instances_many")
        #print(instances_many_path)
    
        instances = (instance for instance in os.listdir(instances_path) if instance.endswith(".lp"))
        many_instances = (instance for instance in os.listdir(instances_many_path) if instance.endswith(".lp")) 
        if max_instances is not None:
            instances = (instance for instance in sorted(instances)[:max_instances])
            many_instances = (instance for instance in sorted(many_instances)[:max_instances])
        
        if os.path.basename(encoding) == "bmtc" or os.path.basename(encoding) == "bmtuc":
            # Get all instances_many
            
            for many_instance in many_instances:
                instance_many_path = os.path.join(instances_many_path,os.path.basename(many_instance))
                instance = encoding + "_" + many_instance
                
                # Make output paths for every encoding + instance
                output_path = os.path.join(many_dir, os.path.basename(instance)) 
                # print(base_encoding, encoding_path, instance_many_path, output_path) 
                os.system(f"cat {base_encoding} {encoding_path} {instance_many_path} > {output_path}")
        else:
            # Get all instances
            for instance in instances:
                instance_path = os.path.join(instances_path, os.path.basename(instance))
                instance = encoding + "_" + instance            
                
                # Make output paths for every encoding + instance
                output_path = os.path.join(base_dir, os.path.basename(instance))    
                # print(base_encoding, encoding_path, instance_path) 
                os.system(f"cat {base_encoding} {encoding_path} {instance_path} > {output_path}")
                
                
def prepare_benchmark_action(benchmark_path, BENCHMARK_RUNNING, max_instances=None):
    # Create directory for different set of problems. Encoding Directory
    benchmark_name = os.path.basename(benchmark_path)
    dir = os.path.join(BENCHMARK_RUNNING,"experiments","instances", benchmark_name)
    os.mkdir(dir)
    
    encodings = (encoding for encoding in os.listdir(benchmark_path) if encoding.endswith(".eclingo.lp")) # encodings
    for encoding in encodings:
        encoding_path = os.path.join(benchmark_path, os.path.basename(encoding))
        encoding = encoding.split('.')[0]
        # print("The encoding path: ", encoding_path, " on ", encoding)
        
        instances_path = os.path.join(benchmark_path, "instances")
        # print("The instances path: ", instances_path)
        
        instances = (instance for instance in os.listdir(instances_path) if instance.endswith(".lp")) 
        if max_instances is not None:
            instances = (instance for instance in sorted(instances)[:max_instances])
            
        # Get all instances
        for instance in instances:
            instance_path = os.path.join(instances_path, os.path.basename(instance))
            instance = encoding + "_" + instance            
            
            # Make output paths for every encoding + instance
            output_path = os.path.join(dir, os.path.basename(instance))    
            # print(instance_path)
            
            # print(encoding_path, instance_path, output_path)
            os.system(f"cat {encoding_path} {instance_path}  > {output_path}")

def prepare_benchmark_yale(benchmark_path, BENCHMARK_RUNNING, max_instances=None):
    # Create directory for different set of problems. Encoding Directory
    benchmark_name = os.path.basename(benchmark_path)
    dir = os.path.join(BENCHMARK_RUNNING, "experiments", "instances", benchmark_name)
    os.mkdir(dir)
    
    encodings = (encoding for encoding in os.listdir(benchmark_path) if encoding.endswith(".lp")) # encodings
    for encoding in encodings:
        encoding_path = os.path.join(benchmark_path, os.path.basename(encoding))
        encoding = encoding.split('.')[0]
        #print("The encoding path: ", encoding_path, " on ", encoding)
        
        instances_path = os.path.join(benchmark_path, "input")
        # print("The instances path: ", instances_path)
        
        instances = (instance for instance in os.listdir(instances_path) if instance.endswith(".lp")) 
        if max_instances is not None:
            instances = (instance for instance in sorted(instances)[:max_instances])
        
        # Get all instances
        for instance in instances:
            instance_path = os.path.join(instances_path, os.path.basename(instance))
            instance = encoding + "_" + instance            
            
            # Make output paths for every encoding + instance
            output_path = os.path.join(dir, os.path.basename(instance))    
            # print("The output path: ", output_path)
            
            # print(encoding_path, instance_path, output_path)
            os.system(f"cat {encoding_path} {instance_path}  > {output_path}")
            
def prepare_benchmark_eligible_eclingo(benchmark_path, BENCHMARK_RUNNING, max_instances=None):
    # Create directory for different set of problems. Encoding Directory
    benchmark_name = os.path.basename(benchmark_path)
    dir = os.path.join(BENCHMARK_RUNNING, "experiments", "instances", benchmark_name)
    os.mkdir(dir)
    
    encodings = (encoding for encoding in os.listdir(benchmark_path) if encoding.endswith(".lp"))
    for encoding in encodings:
        encoding_path = os.path.join(benchmark_path, os.path.basename(encoding))
        encoding = encoding.split('.')[0]
        #print("The encoding path: ", encoding_path, " on ", encoding)
        
        instances_path = os.path.join(benchmark_path, "input")
        instances = (instance for instance in os.listdir(instances_path) if instance.endswith(".lp"))
        if max_instances is not None:
            instances = (instance for instance in sorted(instances)[:max_instances])
        
        # Get all instances
        for instance in instances:
            instance_path = os.path.join(instances_path, os.path.basename(instance))
            instance = encoding + "_" + instance            
            
            # Make output paths for every encoding + instance
            output_path = os.path.join(dir, os.path.basename(instance))    
            # print("The output path: ", output_path)
            
            # print(encoding_path, instance_path, output_path)
            os.system(f"cat {encoding_path} {instance_path}  > {output_path}")

def prepare_eclingo_benchmarks(benchmark, benchmark_origin, BENCHMARK_RUNNING, max_instances):
    print(f"\nUsing solver: Eclingo")
    for benchmark_path in os.listdir(benchmark_origin):
        benchmark_path = os.path.join(benchmark_origin, benchmark_path)
        if os.path.isdir(benchmark_path):

            if os.path.basename(benchmark_path) == "bomb_problems":
                if benchmark == "all" or "bomb" in benchmark:
                    print("Working on BOMB Problems")
                    prepare_benchmark_bomb(benchmark_path, BENCHMARK_RUNNING, max_instances)
                # pass
            elif os.path.basename(benchmark_path) == "action-reversibility":
                if benchmark == "all" or "reversibility" in benchmark:
                    print("Working on ACTION Problems")
                    prepare_benchmark_action(benchmark_path, BENCHMARK_RUNNING, max_instances)
                    # pass
            elif os.path.basename(benchmark_path) == "eligible":
                if benchmark == "all" or "eligible" in benchmark:
                    print("Working on ELIGIBLE Problems")
                    prepare_benchmark_eligible_eclingo(benchmark_path, BENCHMARK_RUNNING, max_instances)
                    # pass
            else:
                if benchmark == "all" or "yale" in benchmark:
                    print("Working on YALE Problems")
                    prepare_benchmark_yale(benchmark_path, BENCHMARK_RUNNING, max_instances)
                    # pass
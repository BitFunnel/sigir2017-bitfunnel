from bf_utilities import run
from experiment import Experiment
import os
import re

# for each term table configuration:
#   for each density:
#     make a directory
#     build new term table
#     run qps measurement
#     extract qps and bits/posting
#     write out results

def measure_innovations(experiment, treatments, densities):
    bf_index_path = os.path.join(experiment.bf_index_path, "innovations")

    if not os.path.exists(bf_index_path):
        os.makedirs(bf_index_path)

    # We're currently restricted to a single shard,
    # so create an empty ShardDefinition file.
    open(os.path.join(bf_index_path, "ShardDefinition.csv"), "w").close()

    # Run statistics builder
    args = ("{0} statistics {1} {2} -text").format(experiment.bf_executable,
                                                   experiment.manifest,
                                                   bf_index_path)
    statistics_log = os.path.join(bf_index_path, "statistics-log.txt")
    print(args)
    # run(args, bf_index_path, statistics_log)

    # Make the repl script
    repl_script = os.path.join(bf_index_path, "repl-script")
    print(repl_script)
    with open(repl_script, "w") as file:
        file.write("threads {0}\n".format(experiment.ingestion_thread_count))
        file.write("load manifest {0}\n".format(experiment.manifest));
        file.write("status\n");
        file.write("compiler\n");
        file.write("threads {0}\n".format(experiment.max_thread_count))
        file.write("cd {0}\n".format(bf_index_path))
        file.write("query log {0}\n".format(experiment.filtered_query_file))
        file.write("quit\n")

    for treatment in treatments:
        for density in densities:
            # Build the termtable
            args = ("{} termtable {} {} {}").format(experiment.bf_executable, bf_index_path, density, treatment)
            termtable_log = os.path.join(bf_index_path, "termtable-log-{}-{}.txt".format(treatment, density))
            print(args)
            run(args, bf_index_path, termtable_log)

            args = ("{} repl {} -script {}").format(experiment.bf_executable,
                                                    bf_index_path,
                                                    repl_script)
            repl_log = os.path.join(bf_index_path, "repl-log-{}-{}.txt".format(treatment, density))
            print(args)
            run(args, bf_index_path, repl_log)


def analyze_innovations(experiment, labels, treatments, densities):
    print("{:<10} {:>10} {:>10} {:>10} {:>10}".format("Treatment",
                                                      "Density",
                                                      "Bits",
                                                      "QPS",
                                                      "DQ"))

    bf_index_path = os.path.join(experiment.bf_index_path, "innovations")

    for i, treatment in enumerate(treatments):
        for density in densities:
            repl_log = os.path.join(bf_index_path, "repl-log-{}-{}.txt".format(treatment, density))
            with open(repl_log, 'r') as myfile:
                run_queries_log = myfile.read()
                bpp = float(re.findall("Bits per posting: (\d+\.?\d+)", run_queries_log)[0])
                qps = float(re.findall("QPS: (\d+\.?\d+)", run_queries_log)[0])
                print("{:<10} {:>10.2f} {:>10.2f} {:>10,.0f} {:>10,.0f}".format(labels[i],
                                                  density,
                                                  bpp,
                                                  qps,
                                                  qps / bpp))
        print()


def innovations(experiment, labels, treatments, densities):
    # measure_innovations(experiment, treatments, densities)
    analyze_innovations(experiment, labels, treatments, densities)


experiment_windows_273_1024_2047 = Experiment(
    # Paths to tools
    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    r"D:\git\mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"D:\temp\indexes",
    r"273-1024-2047",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-1024-2047",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # Min and max thread counts
    8,
    1,
    8
)

# labels =["BSS", "BSS-FC", "BTFNL"]
# treatments = ["PrivateRank0", "PrivateSharedRank0", "Optimal"]

labels =["BSS", "BSS-FC", "BTFNL"]
treatments = ["ClassicBitsliced", "PrivateSharedRank0", "Optimal"]
densities = [0.05, 0.10, 0.15, 0.20, 0.25]

# labels =["BSS"]
# treatments = ["ClassicBitsliced"]
# densities = [0.10]


innovations(experiment_windows_273_1024_2047, labels, treatments, densities)

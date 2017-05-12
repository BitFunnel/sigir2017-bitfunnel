from bf_utilities import run
import csv
from experiment import Experiment
import itertools
import os
import random
import re


def generate_query_log(experiment, sample_count):
    bf_index_path = os.path.join(experiment.bf_index_path, "quadwords")

    if not os.path.exists(bf_index_path):
        os.makedirs(bf_index_path)

    with open(experiment.filtered_query_file, 'r') as infile:
        words = sorted(set(infile.read().split()))
        if sample_count <= len(words):
            samples = [words[i] for i in sorted(random.sample(range(len(words)), sample_count))]
            query_log = os.path.join(bf_index_path, "single-term-queries.txt")
            with open(query_log, 'w') as output:
                for word in samples:
                    print(word, file=output)
            print("Wrote {} single-term queries to {}".format(len(samples), query_log))
        else:
            print("ERROR: requested sample size {} exceeds unique word count of {}", sample_count, len(words))


def measure_quadwords(experiment, iterations):
    bf_index_path = os.path.join(experiment.bf_index_path, "quadwords")

    def results_path(iteration):
        return os.path.join(bf_index_path, "run-{}".format(iteration))

    if not os.path.exists(bf_index_path):
        os.makedirs(bf_index_path)

    # We're currently restricted to a single shard,
    # so create an empty ShardDefinition file.
    open(os.path.join(bf_index_path, "ShardDefinition.csv"), "w").close()

    # Make the repl script
    # query_log = os.path.join(bf_index_path, "single-term-queries.txt")
    query_log = experiment.filtered_query_file

    repl_script = os.path.join(bf_index_path, "repl-script")
    print(repl_script)
    with open(repl_script, "w") as file:
        file.write("threads {0}\n".format(experiment.ingestion_thread_count))
        file.write("load manifest {0}\n".format(experiment.manifest));
        file.write("status\n");
        file.write("compiler\n");
        file.write("threads {0}\n".format(experiment.max_thread_count))
        for iteration in range(iterations):
            file.write("cd {0}\n".format(results_path(iteration)))
            file.write("query log {0}\n".format(query_log))
        file.write("quit\n")


    # Make the directories for the results.
    for iteration in range(iterations):
        results_dir = results_path(iteration)

        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

    # Finally, run the queries.
    args = ("{} repl {} -script {}").format(experiment.bf_executable,
                                            experiment.bf_index_path,
                                            repl_script)
    repl_log = os.path.join(bf_index_path, "run-log.txt")
    print(args)
    run(args, bf_index_path, repl_log)


def analyze_quadwords(experiment, iterations):
    bf_index_path = os.path.join(experiment.bf_index_path, "quadwords")
    results_file = os.path.join(bf_index_path, "results.csv")

    with open(results_file, 'w') as output:
        print("query,matches,quadwords,min,median,max,ratio1,ratio2", file=output)

        files = [os.path.join(bf_index_path, "run-{}".format(iteration), "QueryPipelineStatistics.csv" ) for iteration in range(iterations)]
        readers = [csv.reader(open(file, newline=''), delimiter=',', quotechar='|') for file in files]
        counter = 0
        for rows in itertools.zip_longest(*readers):
            # print(rows)
            if counter > 0:
                query = rows[0][0]
                matches = int(rows[0][2])
                quadwords = int(rows[0][3])
                times = sorted([float(row[7]) for row in rows])
                min_time = times[0]
                median_time = times[int(iterations/2)]
                max_time = times[iterations-1]
                ratio = max_time / min_time
                ratio2 = times[int(iterations/2) + 1] / median_time
                # print("{:>10},{:>10},{:>12.9f},{:>12.9f},{:>12.9f},{:>12.9f},{:>12.9f}\n".format(
                #     matches, quadwords, min_time, median_time, max_time, ratio, ratio2))
                print("{},{},{},{},{},{},{},{}".format(
                    query, matches, quadwords, min_time, median_time, max_time, ratio, ratio2), file=output)
            counter += 1
            # if counter > 20:
            #     break



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

# generate_query_log(experiment_windows_273_1024_2047, 20000)
measure_quadwords(experiment_windows_273_1024_2047, 9)
analyze_quadwords(experiment_windows_273_1024_2047, 9)
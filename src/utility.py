import sys


def get_paths(n_dataset):
    paths = {
        "neural_network": f"/Users/francesco/Desktop/Argumentation/models/neural_network_ep50_typesingle_cpu_dataset_e{n_dataset}.nn",
        "word2vec": f"/Users/francesco/Desktop/Argumentation/models/word2vec_e{n_dataset}.model",
        "activities": f"/Users/francesco/Desktop/Argumentation/buildjar/support/activitiesForLog_{n_dataset}.txt",
        "events": f"/Users/francesco/Desktop/Argumentation/buildjar/support/eventsForLog_{n_dataset}.txt",
        "raw_dataset": f"/Users/francesco/Desktop/Argumentation/Datasets/e{n_dataset}",
        "processes": "/Users/francesco/Desktop/Argumentation/buildjar/support/processForLog.txt",
        "jar_tool": "/Users/francesco/Desktop/Argumentation/Argumentation.jar",
        "canen_tool": "/Users/francesco/Desktop/Argumentation/Canen",
        "support_folder": "/Users/francesco/Desktop/Argumentation/Tmp",
        "statistics_file": f"/Users/francesco/Desktop/Argumentation/results_hard_admissibility_dataset_{n_dataset}.csv",
        "statistics_file_admissibility": f"/Users/francesco/Desktop/Argumentation/results_soft_admissibility_dataset_{n_dataset}.csv",
        "times_file": f"/Users/francesco/Desktop/Argumentation/times_all_dataset_{n_dataset}.csv"
    }
    return paths


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    if iteration == total:
        print("\n")

raw_dataset_folder = "/Users/francesco/Desktop/Argumentation/buildjar"
trace_size = 41
input_name_file = "{}/trace{}-{}.txt"
twins = {}

sum = 0
for index_file in range(10000):
    trace = open(input_name_file.format(raw_dataset_folder, trace_size, index_file), "r")
    trace_lines = trace.readlines()

    for i in range(1, trace_size + 1):
        sum += 1
        tokens_trace = trace_lines[i].split()
        raw_event = tokens_trace[0]
        raw_activity = tokens_trace[2]
        merged = "{}-{}".format(raw_event, raw_activity)
        if merged in twins:
            twins[merged] += 1

        else:
            twins[merged] = 1

twins_percentaged = {}
for i in twins.keys():
    percentage = (twins[i]/sum) * 100
    twins_percentaged[i] = percentage
    print("{}\t{:.2f}%".format(i, percentage))

print("-"*70)
sorted_twins = sorted(twins_percentaged.items(), key=lambda x:x[1])

for i in range(len(sorted_twins) - 1, -1, -1):
    print("{}\t{:.2f}%".format(sorted_twins[i][0], sorted_twins[i][1]))

print("+"*70)
for j in range(1, 17):
    print("Current event: e{}".format(j))
    current_event = "e{}-".format(j)
    total = 0
    for i in twins.keys():
        if current_event in i:
            total += twins[i]

    for i in twins.keys():
        if current_event in i:
            percentage = (twins[i] / total) * 100
            print("{}\t{:.2f}%".format(i.split("-")[1], percentage))

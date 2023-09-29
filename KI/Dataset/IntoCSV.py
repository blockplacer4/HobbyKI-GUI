import csv

with open('D:\HobbyKI\HobbyKI-GUI\KI\Dataset\dataset.txt', 'r') as in_file, open('D:\HobbyKI\HobbyKI-GUI\KI\Dataset\dataset.csv', 'w', newline='') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(["Input", "Output"])

    for line in in_file:
        input_part, output_part = line.replace('"', '').split(',', 1)
        writer.writerow([input_part, output_part])

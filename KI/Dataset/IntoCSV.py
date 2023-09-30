import csv

with open('D:\HobbyKI\HobbyKI-GUI\KI\Dataset\dataset.txt', 'r') as in_file, open('D:\HobbyKI\HobbyKI-GUI\KI\Dataset\dataset.csv', 'w', newline='') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(["Input", "Output", "Text"])

    for line in in_file:
        input_part, output_part = line.replace('"', '').split(',', 1)
        text_part = "###Human:\n" + input_part + "\n\n" +  "###Assistant:\n" + output_part
        writer.writerow([input_part, output_part, text_part])

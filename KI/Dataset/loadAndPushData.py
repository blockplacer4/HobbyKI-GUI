from datasets import load_dataset

dataset = load_dataset("csv", data_files="D:\HobbyKI\HobbyKI-GUI\KI\Dataset\dataset.csv")

dataset.push_to_hub("")
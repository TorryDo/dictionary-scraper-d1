import sys
import time

import wik_def_crawler as wik

# print("choose folder to save txt file: ")
#
# folder_destination: str = input()
#
# print(folder_destination)

start_time = time.time()

folder_path = "C:\\Users\\trido\\Documents\\db\\dict\\eng-eng"
file_name = "test_file.txt"
file_path = f"{folder_path}/{file_name}"


file = open(file_path, "w", encoding="utf-8")
result: str = ""

count = 0
limit_word = 20

with open("../raw/words_alpha.txt") as f:
    lines = [line.rstrip() for line in f]
    for word in lines:
        if count > limit_word:
            break
        vocab = wik.crawl_word(word)

        result += str(vocab.toJson())
        result += "\n"

        count += 1

print(result)

file.write(result)

print(f"\n<>Crawler took: {(time.time() - start_time).__round__(3)}s to run")

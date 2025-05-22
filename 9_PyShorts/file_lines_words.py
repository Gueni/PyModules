
filename    = "file.txt"
path        = "insert_path_here"
file_path   = path + filename  # replace with the path to your file

with open(file_path, "r") as file:
    # read the file contents
    text = file.read()

    # count the number of characters
    num_chars = len(text)

    # count the number of words
    words = text.split()
    num_words = len(words)

    # count the number of spaces
    num_spaces = text.count(" ")

    # count the number of lines
    lines = text.split("\n")
    num_lines = len(lines)

print(f"Number of characters: {num_chars}")
print(f"Number of words: {num_words}")
print(f"Number of spaces: {num_spaces}")
print(f"Number of lines: {num_lines}")

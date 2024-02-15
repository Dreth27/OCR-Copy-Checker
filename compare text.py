import difflib

def read_file_without_last_line(file_path):
    """Reads a file and returns its content as a list of lines, excluding the last line."""
    with open(file_path, "r") as f:
        lines = f.readlines()[:-1]  # Exclude the last line
    return lines

def compare_files(file1, file2):
    """Compares two files word by word and returns the percentage similarity."""
    
    # Read the contents of file1 and file2 into lists of lines, excluding the last line.
    file1_lines = read_file_without_last_line(file1)
    file2_lines = read_file_without_last_line(file2)
    
    # Initialize lists to store words in each file.
    file1_words = []
    file2_words = []
    
    # Process lines to extract words.
    for line in file1_lines:
        file1_words.extend(line.split())
    
    for line in file2_lines:
        file2_words.extend(line.split())
    
    # Compare the two lists of words using the difflib library.
    diff = difflib.SequenceMatcher(None, file1_words, file2_words)
    matches = diff.ratio() * 100

    # Return the percentage similarity.
    return matches

# Get the percentage similarity of the two files.
similarity = compare_files("output.txt", "output2.txt")

# Display the percentage similarity.
print("The two files are {:.2f}% similar.".format(similarity))

# Open the percentage.txt file for writing.
with open("D:\Downloads\Python_OCR\input\percentage.txt", "w") as f:
    # Write the percentage similarity to the file.
    f.write("{:.2f}%\n".format(similarity))
    if similarity >= 0 and similarity <= 50:
        f.write("Copying is unlikely.")
    elif similarity >= 51 and similarity <= 75:
        f.write("Copying is likely.")
    elif similarity >= 76 and similarity <= 90:
        f.write("Copying is highly likely.")
    elif similarity >= 91 and similarity <= 99:
        f.write("Copying is extremely likely.")
    elif similarity == 100:
        f.write("The two files are an exact copy of each other.")
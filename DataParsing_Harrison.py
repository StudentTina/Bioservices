import re


def search_file(search_term, file):
    """Search file for search term. When search term is found,
    compile line that search_term is found on, as well as all
    subsequent lines until a line starting with no more than two
    spaces followed by two capital letter is found.
    """
    output = []  # Initialize output array to store results
    # Flag is used to determine if the search line has been found. When
    # the search term is found, flag is set to true and all subsequent
    # lines are written to output array until flag is turned back to False.
    flag = False
    with file as f:
        for line in f:
            if re.search(search_term, line) and not(flag):
                output.append(line)
                flag = True
            elif not(re.search(r'^[\s]{0,2}[A-Z]{2}', line)) and flag:
                output.append(line)
            else:
                flag = False
    # This next term strips the search term from the first line of output
    output[0] = re.sub(search_term, '', output[0])

    # This for loop strips the leading spaces, as well as the newline
    # character from each entry in the output
    ix = 0
    for i in output:
        output[ix] = re.sub(r'\n$', '', i.lstrip())
        ix += 1

    return output


targets = search_file('TARGET', open("D00454.txt"))
pathways = search_file('PATHWAY', open("D00454.txt"))

# Print the searches in a pretty manor
print("The targets are:")
for i in targets: print('    ' + i)
print('\nThe pathways are:')
for i in pathways: print('    ' + i)

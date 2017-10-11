from sys import argv

script, file_to_open = argv

text = open(file_to_open, 'r')
new_data = text.read().replace('\n', ' ')
text = open(file_to_open, 'w')
text.write(new_data)
text.close()

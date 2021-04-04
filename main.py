import re

d = 'IF М2'

print(re.search(r'М\d+', d).group(0))
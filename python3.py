import re
import collections

NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPARENT = r'(?P<LPARENT>\()'
RPARENT = r'(?P<RPARENT>\))'
WS = r'(?P<WS>\s+)'


master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES, DIVIDE, LPARENT, RPARENT, WS]))
Token = collections.namedtuple('Token', ['type', 'value'])

def generate_tokens(text):
	scanner = master_pat.scanner(text)
	for m in iter(scanner.match, None):
		tok = Token(m.lastgroup, m.group())
		if tok.type != 'WS':
			yield tok 

PLUS = r'(?P<PLUS>\+)'
plus_pat = re.compile(PLUS)
scanner = plus_pat.scanner("2 + 3")
for m in iter(scanner.match, None):
	print m.lastgroup, m.group()

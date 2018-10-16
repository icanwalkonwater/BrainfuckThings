import re
import sys


def cleanup(code: str):
	return re.sub(
		r'[^+\-<>\[\].,]',
		'',
		code
	)


if __name__ == '__main__':
	data = sys.stdin.readlines()
	data = cleanup(data)

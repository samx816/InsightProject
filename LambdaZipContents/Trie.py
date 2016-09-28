#Credit to senderle on stackoverflow for help on python implementation of make_trie

def make_trie(*theSet):
	_end = '_end_'
	root = dict()
	for phrases in theSet:
		current = root
		for phrase in phrases:
			for word in phrase.split():
				#print word
				current = current.setdefault(word, {})
			current[_end] = _end
			current = root
	return root


def in_trie(trie, phrase) :
	phrase = phrase.split()
	for i in range(0, len(phrase)):
		current = trie
		if phrase[i] in current:
			current = current[phrase[i]]
			answer = rec(current, phrase, i+1)
			if answer[0] == True:
				answer[1] = phrase[i] + ' ' + answer[1]
				return answer
			else:
				continue
	return [False, '']


#recusive helper for in_trie
#tuple return value represents whether phrase is in trie, and what the path was
def rec(trie, phrase, i):
	if i == len(phrase):
		if '_end_' in trie:
			answer = [True, '']
			return answer
		else:
			return [False, '']
	if phrase[i] in trie:
		current = trie[phrase[i]]
		answer = rec(current, phrase, i+1)
		if answer[0] == True:
			answer[1] = phrase[i] + ' ' + answer[1]
			return answer
		else:
			return [False, '']
	else:
		if '_end_' in trie:
			return [True, '']
		else:
			return [False, '']
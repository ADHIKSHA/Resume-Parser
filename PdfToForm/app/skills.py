


def isskill(line):
	skills=["python","customer support","sales","c++","programming","android","css","python","adobe","google","processing","sql","django","cloud","drawing","painting","html","algorithms","excel","analytics","data structures","dbms","php","R","science","machine","tally","accountancy","chemistry","physics"]
	#print(skills)
	for s in skills:
		if line.find(s)!=-1:
			#print(s)
			return True
	return False
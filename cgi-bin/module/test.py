with open('./data_alex/seg1533_prepare2.csv', 'w', encoding='utf8') as file:
	file.write('\ufeff')
	with open('./data_alex/seg1533_prepare.csv', 'r', encoding='utf8') as f:
		line = []
		for i in f.readlines():
			x = i.strip().split(',')
			if x[0] == '':
				if line:
					file.write(','.join(line))
					file.write('\n')
					line = []
			elif x[0] == '，':
				line.append(x[0]+'%2F'+x[1]+'%2F'+x[2])
				file.write(','.join(line))
				file.write('\n')
				line = []
			else:
				line.append(x[0]+'%2F'+x[1]+'%2F'+x[2])
			


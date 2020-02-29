import AccRecognition

AccRecognition.getData()

while True:
	a = AccRecognition.read()
	if not a=="X":
		print(a)


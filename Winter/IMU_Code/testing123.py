import GestureRecognition

while True:
	a = GestureRecognition.read()
	if not a=="X":
		print(a)


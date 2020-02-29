import GestureRecognition

GestureRecognition.getData()

while True:
	a = GestureRecognition.read()
	if not a=="X":
		print(a)


import numpy as np

class EnigmaPython:
	alpha = np.array([
		'a', 'b', 'c', 'd', 'e', 'f', 'g',
		'h', 'i', 'j', 'k', 'l', 'm', 'n',
		'o', 'p', 'q', 'r', 's', 't', 'u',
		'v', 'w', 'x', 'y', 'z'
		])
	rotorFixed = [
		3, 8, 7, 24, 16, 18, 20,
		25, 2, 0, 5, 17, 6, 13,
		14, 4, 22, 12, 10, 11,
		19, 1, 15, 21, 9, 23
		]
	frontPanelConf = [
		4, 14, 2, 12, 22, 7, 3,
		1, 5, 6, 13, 15, 9, 17,
		20, 19, 16, 25, 10, 8,
		0, 11, 18, 21, 23, 24
		]
	rotorRedirect = np.array([[
			10, 8, 23, 19, 2, 22, 20,
			1, 16, 18, 9, 3, 13, 7, 5,
			17, 14, 6, 25, 0, 24, 4,
			15, 21, 12, 11
		],
		[
			12, 0, 15, 13, 21, 9,
			24, 23, 20, 17, 1, 18,
			7, 2, 14, 16, 8, 3, 10,
			4, 6, 11, 19, 22, 5, 25
		],
		[
			16, 10, 7, 22, 6, 2, 15,
			13, 25, 0, 4, 24, 9, 1,
			14, 17, 23, 19, 21, 18,
			3, 8, 20, 12, 5, 1
		]])
	rotorPos = np.zeros(3)
	frontPannelConf = np.arange(26)
	encryptLetters = ''
		
	def moveRotors(self):
		self.rotorPos[0] += 1
		
		for i in range(1, len(self.rotorPos)):
			self.rotorPos[i] = np.where(self.rotorPos[i-1] > 26, self.rotorPos[i] + 1, 0)
			
		self.rotorPos[0] = np.where(self.rotorPos[0] > 26, 0, self.rotorPos[0])
	
	def getEcryptLetters(self):
		return self.encryptLetters

	def inputOutput(self, letter):
		print(letter)
		out = self.encrypt(letter)
		print(out)
		self.encryptLetters += out
		return out

	def encrypt(self, letter):
		num = np.where(self.alpha == letter)[0][0]

		enc = self.toCase(self.frontPanel(self.calculatePosOutRotors(self.frontPanel(num))))
		self.moveRotors()

		return enc
 
	def calculatePosOutRotors(self, num):
		pos = (num + int(self.rotorPos[0])) % 26  # Utilisation de l'opérateur modulo pour gérer les débordements
		pos = int(self.rotorRedirect[0, pos])

		for i in range(1, len(self.rotorRedirect)):
			pos = (pos + int(self.rotorPos[i])) % 26  # Utilisation de l'opérateur modulo pour gérer les débordements
			pos = int(self.rotorRedirect[i, pos])

		pos = int(self.rotorFixed[pos])

		for i in range(0, len(self.rotorRedirect)):
			pos = (pos + int(self.rotorPos[-i])) % 26  # Utilisation de l'opérateur modulo pour gérer les débordements
			pos = int(self.rotorRedirect[-i, pos])

		return pos

	def frontPanel(self, pos):
		return self.frontPannelConf[pos]
	
	def toCase(self, case):
		return self.alpha[case]
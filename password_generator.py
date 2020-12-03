import random as r
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits, punctuation
from pyperclip import copy

class PasswordGenerator:
	lower, upper, numbers, symbols = ascii_lowercase, ascii_uppercase, digits, punctuation
	ALL = {'lower': lower, 'upper': upper, 'numbers': numbers, 'symbols': symbols}
	ALL_STR = ''.join(list(ALL.values()))
	
	def __init__(self, length=12, unique_letters=False, no_double=False):
		self.length = length
		self.wanted_args = {}
		self.wanted_groups = {}
		self.unique_letters = unique_letters
		self.no_double = no_double
		self.double_bool = True

	def generator(self, lower=True, upper=True, numbers=True, symbols=True, copying=False):
		self.args = {'lower': lower, 'upper': upper, 'numbers': numbers, 'symbols': symbols}
		
		for arg in self.args: # collect what groups are wanted
			if self.args[arg]:
				self.wanted_args[arg] = 0
				self.wanted_groups[arg] = PasswordGenerator.ALL[arg]

		self.wanted_string = ''.join(list(self.wanted_groups.values()))

		if self.unique_letters: self.unique()
		else: self.un_unique()
		if copying: copy(''.join(self.password))
		return ''.join(self.password)

	def un_unique(self):
		while not all(self.wanted_args.values()):
			self.password = r.choices(self.wanted_string, k=self.length)

			for letter in self.password:
				for name, group in self.wanted_groups.items(): # name = key, group = value
					if letter in group:
						self.wanted_args[name] = 1

		if self.no_double:
			while self.double_check():
				self.shuffle()
				
	def unique(self):
		assert (self.length <= len(self.wanted_string)), "PasswordLengthError: the length you want MUST be <= length of choosen characters"

		while not all(self.wanted_args.values()):
			self.password = r.sample(self.wanted_string, k=self.length)

			for letter in self.password:
				for name, group in self.wanted_groups.items(): # name = key, group = value
					if letter in group:
						self.wanted_args[name] = 1

	def double_check(self): # True ==> There's a double. | False ==> There's no double.
		for n, letter in enumerate(self.password):
			# Last letter (break the loop to avoid 'IndexError: list index out of range')
			if n == len(self.password)-1: break 

			if letter == self.password[n+1]:
				return True
		return False

	def shuffle(self, Reverse=False):
		if Reverse:
			r.shuffle(list(reversed(self.pasِsword)))
		else:
			r.shuffle(self.password)

	def lowercase(self):
		return self.password.lower()

	def uppercase(self):
		return self.password.upper()

# Example:
Pass = PasswordGenerator(50) # the password will be 50 characters
print(Pass.generator(symbols=False, copying=True)) # password will contain all letters (uppera and lowercase), and numbers.
# after making the password: it will be copied to your clipboard

import random as r
import argparse # if you want to use it as a CLI tool
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits, punctuation
from pyperclip import copy

class PasswordGenerator:
	lower, upper, numbers, symbols = ascii_lowercase, ascii_uppercase, digits, punctuation
	ALL = {'lower': lower, 'upper': upper, 'numbers': numbers, 'symbols': symbols}
	ALL_STR = ''.join(list(ALL.values()))
	def __init__(self, length:int=16, unique_letters:bool=False, no_double:bool=False):
		self.length = length
		self.wanted_args = {}
		self.wanted_groups = {}
		self.unique_letters = unique_letters
		self.no_double = no_double
		self.double_bool = True

	def generator(self, lower:bool=True, upper:bool=True, numbers:bool=True, symbols:bool=True, copying:bool=False) -> str:
		self.args = {'lower': lower, 'upper': upper, 'numbers': numbers, 'symbols': symbols}

		for arg in self.args: # collect the groups which are wanted
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

	def double_check(self) -> bool: # True ==> There's a double. | False ==> There's no double.
		for n, letter in enumerate(self.password):
			# Last letter (break the loop to avoid 'IndexError: list index out of range')
			if n == len(self.password)-1: break

			if letter == self.password[n+1]:
				return True
		return False

	def shuffle(self, Reverse=False):
		if Reverse:
			r.shuffle(list(reversed(self.password)))
		else:
			r.shuffle(self.password)

	def lowercase(self) -> str:
		return self.password.lower()

	def uppercase(self) -> str:
		return self.password.upper()


# Example:
Pass = PasswordGenerator(50) # the password will be 50 characters
print(Pass.generator(symbols=False, copying=True)) # password will contain all letters (uppera and lowercase), and numbers.
# after making the password: it will be copied to your clipboard

# comment lines down if you don't wanna use it as a CLI tool..

parser = argparse.ArgumentParser(description='Generates a random series of numbres, letters, and symbols, with given length.')


parser.add_argument('-l','--length', type=int, metavar='', help="Length of the series (password). [Default=16]")

parser.add_argument('-n','--numbers', type=int, metavar='', help="Include numbers or not. [Default=True]")
parser.add_argument('-c','--capital', type=int, metavar='', help="Include capital letters or not. [Default=True]")
parser.add_argument('-s','--small', type=int, metavar='', help="Include small letters or not. [Default=True]")
parser.add_argument('-p','--punctuation', type=int, metavar='', help="Include punctuations (symbols) or not. [Default=True]")

parser.add_argument('-nd','--no_double', type=int, metavar='', help="Want creating series without repeating characters or allow repeating. [Default=False]")
parser.add_argument('-u','--unique_letters', type=int, metavar='', help="Want series characters to bo unique or not. [Default=False]")
parser.add_argument('-C','--copy', type=int, metavar='', help="Copying the series to clipboard or not. (must have pyperclip library) [Default=False]")

args = parser.parse_args()

length = args.length if args.length is not None else 16
lower = bool(args.small) if args.small is not None else True
upper = bool(args.capital) if args.capital is not None else True
numbers = bool(args.numbers) if args.numbers is not None else True
symbols = bool(args.punctuation) if args.punctuation is not None else True
no_double = bool(args.no_double) if args.no_double is not None else False
unique_letters = bool(args.unique_letters) if args.unique_letters is not None else False
copying = bool(args.copy) if args.copy is not None else False

# Example:
my_password = PasswordGenerator(length, unique_letters, no_double)
# prints ten passwords:
for i in range(10): print(my_password.generator(lower, upper, numbers, symbols, copying))

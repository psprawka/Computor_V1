import sys

class settings:
	NORMAL = "\x1B[0m"
	RED = "\x1B[31m"
	GREEN = "\x1B[32m"
	YELLOW = "\x1B[33m"
	BLUE = "\x1B[34m"
	MAGNETA = "\x1B[35m"
	CYAN = "\x1B[36m"
	WHITE = "\x1B[37m"
	PINK = "\033[38;5;200m"
	ORANGE = "\033[38;5;208m"
	PURPLE = "\033[38;5;55m"
	MAROON = "\033[38;5;88m"
	GREY = '\033[38;5;246m'
	verbose = False
	allowed_char_set = "X+-*/1234567890^ .="

# ---------------------------------------- MATHS ----------------------------------------
def square_root(number):
	return number ** (1/2)

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


# --------------------------------------- PARSING ---------------------------------------
def get_coeff(equation):
	l_coeff = []
	minus = False
	for x in equation.split(" "):
		if x == '-':
			minus = True
			continue
		if x.isdigit():
			l_coeff.append(int(x)) if not minus else l_coeff.append(int(x) * -1)
		elif isfloat(x):
			l_coeff.append(float(x)) if not minus else l_coeff.append(float(x) * -1)
		minus = False
	return l_coeff

def parse_equation(equation):
	left_right = equation.split("=")
	print_info(-1, obj1=left_right[0].strip(), obj2=left_right[1].strip())
	left_right = [get_coeff(left_right[0]), get_coeff(left_right[1])]
	print_info(-2, obj1=left_right[0], obj2=left_right[1])
	longer, shorter = (left_right[0], left_right[1]) if len(left_right[0]) >= len(left_right[1]) else (left_right[1], left_right[0])
	for i in range(len(shorter)):
		longer[i] -= shorter[i]
	for x in longer[1:][::-1]:
		if x != 0:
			break
		longer = longer[0:-1]
	print_info(-3, obj1=longer)
	return longer

def valid_equation(equation):
	for x in equation:
		# print(settings.GREEN, equation, settings.NORMAL)
		if x not in settings.allowed_char_set:
			print_info(101, obj1=x, obj2=equation)
			print_info(1)
			exit(0)

# -------------------------------------- PRINTING --------------------------------------
def concat_reduced(coeff):
	if len(coeff) == 1:
		return str(coeff[0]) + " = 0"
	res = []
	for i in range(len(coeff)):
		if coeff[i] < 0:
			res.append("- " + str(abs(coeff[i])) + " * X^" + str(i) + " ")
		elif coeff[i] >= 0 and i != 0:
			res.append("+ " + str(coeff[i]) + " * X^" + str(i) + " ")
		else:
			res.append(str(coeff[i]) + " * X^" + str(i) + " ")
	res.append("= 0")
	return "".join(res)

def print_info(argument, x=0, y=0, obj1=[0], obj2=[0]):
	logs = {
		# Required logs start from 1 and grow up
		1: "Usage: python3 computor_v1.py [-v | --verbose] [-f filename | --file filename] <equation[s]>",
		2: "The polynomial degree is stricly greater than 2, I can't solve.",
		3: "Discriminant is strictly positive, the two solutions are:\nx = %g or x = %g" % (x, y),
		4: "Discriminant is zero, one solution: x = %g" % x,
		5: "Discriminant is less than 0, no solution.",
		6: "The solution is: x = %g" % x,
		7: "Identity - all of real numbers are the solution.",
		8: "Contradiction - none of real nuumers is the solution.",
		9: "Equation: %s" % obj1,
		10: "Reduced:  %s" % obj1,
		11: "Polynomial degree: %d" % x,
		# Error handling starts from 100 and grows up
		# 100: ,
		101: "Error: Invalid character '%s' in equation '%s'" % (obj1, obj2),
		# Addictional logs start from -1 grows down
		-1: "Left side of equation: [%s] | Right side of equation: [%s]" % (obj1, obj2),
		-2: "Left coefficients: %s | Right coefficients: %s" % (obj1, obj2),
		-3: "Reduced coefficients: %s" % obj1,
		-4: "Discriminant = b^2 - 4ac = %d" % x
	}
	if argument > 0 and argument < 100:
		print(logs.get(argument))
	elif argument >= 100:
		print(settings.RED, logs.get(argument), settings.NORMAL, sep="")
	elif settings.verbose:
		print(settings.CYAN, logs.get(argument), settings.NORMAL, sep="")


# ---------------------------------- HANDLE EQUATIONS ----------------------------------
def handle_equation(equation):
	valid_equation(equation)
	print("--------------------------------------------------")
	print_info(9, obj1=equation)
	coefficients = parse_equation(equation)
	print_info(10, obj1=concat_reduced(coefficients))
	print_info(11, len(coefficients) - 1)
	compute_result(coefficients)

def handle_args_equations():
	for i in range(1 if not settings.verbose else 2, len(sys.argv)):
		# try:
		handle_equation(str(sys.argv[i]))
		# except:
		# 	print_info(1)
		# 	return 1

def handle_file_equations(filename):
	with open(filename) as file:
		
		for cnt, line in enumerate(file):
			
			try:
				if line and '#' in line:
					line = line.split("#")[0]
			except:
				print("WEIRD LOG LOG LOG CHECK THIAS OUT 0")
				print_info(1)
				return 1
			try:
				if len(line.strip()) > 0:
					handle_equation(line.strip())
			except:
				print("WEIRD LOG LOG LOG CHECK THIAS OUT 1")
				print_info(1)
				return 1


# ----------------------------------- MAIN FUNCTIONS -----------------------------------
def compute_result(coeff):
	len_coeff = len(coeff)
	if len_coeff > 3:
		print_info(2)
	elif len_coeff == 3:
		c, b, a = coeff[0], coeff[1], coeff[2]
		delta = (b ** 2) - (4 * a * c)
		print_info(-4, delta)
		if delta > 0:
			s1, s2 = (-b-square_root(delta)) / (2*a), (-b+square_root(delta)) / (2*a)
			print_info(3, s1, s2)
		elif delta == 0:
			print_info(4, (-b) / (2*a))
		else: 
			print_info(5)
	elif len_coeff == 2:
		print_info(6, 0 if coeff[1] == 0 else -(coeff[0]/coeff[1]))
	elif len_coeff == 1:
		print_info(7 if coeff[0] == 0 else 8)

def main():
	if len(sys.argv) < 2:
		inp = input("Insert equation here: ")
		try:
			handle_equation(inp)
		except:
			print("WEIRD LOG LOG LOG CHECK THIAS OUT 2")
			print_info(1)
		return 0
	
	if len(sys.argv) == 2 and (str(sys.argv[1]) == "-v" or str(sys.argv[1]) == "--verbose"):
		settings.verbose = True
		inp = input("Insert equation here: ")
		try:
			handle_equation(inp)
		except:
			print("WEIRD LOG LOG LOG CHECK THIAS OUT 3")
			print_info(1)
		return 0
	
	for i in range(1, len(sys.argv)):
		if str(sys.argv[i]) == "-v" or str(sys.argv[i]) == "--verbose":
			settings.verbose = True
			continue
		try:
			if str(sys.argv[i]) == "-f" or str(sys.argv[i]) == "--file":
				handle_file_equations(str(sys.argv[i+1]))
				return 0
		except:
			print("WEIRD LOG LOG LOG CHECK THIAS OUT 4")
			print_info(1)
			return 1
	handle_args_equations()


if __name__ == '__main__':
	main()



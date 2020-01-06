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
	allowed_char_set = "Xx+-*/=1234567890^. ²³⁴⁵⁶⁷"
	improved_form = False

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
	if len(left_right)!= 2 or len(left_right[0]) == 1 or len(left_right[0]) == 1:
		print_logs(103, obj1=equation)
		return 1
	print_logs(-1, obj1=left_right[0].strip(), obj2=left_right[1].strip())
	left_right = [get_coeff(left_right[0]), get_coeff(left_right[1])]
	print_logs(-2, obj1=left_right[0], obj2=left_right[1])
	longer, shorter = (left_right[0], left_right[1]) if len(left_right[0]) >= len(left_right[1]) else (left_right[1], left_right[0])
	for i in range(len(shorter)):
		longer[i] -= shorter[i]
	for x in longer[1:][::-1]:
		if x != 0:
			break
		longer = longer[0:-1]
	print_logs(-3, obj1=longer)
	return longer

def valid_equation(equation):
	for x in equation:
		if x not in settings.allowed_char_set:
			print_logs(101, obj1=x, obj2=equation)
			print_logs(1)
			return 1

# -------------------------------------- PRINTING --------------------------------------
def concat_reduced(coeff):
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

def concat_reduced_improved(coeff):
	if len(coeff) > 7:
		print_logs(105)
		return 1
	powers=["", "x", "x²", "x³", "x⁴", "x⁵", "x⁶", "x⁷"]
	res = [settings.ORANGE]
	for i in range(len(coeff)):
		if coeff[i] < 0:
			res.append("- " + str(abs(coeff[i])))
		elif coeff[i] >= 0 and i != 0:
			res.append("+ " + str(coeff[i]))
		else:
			res.append(str(coeff[i]))
		res.append(powers[i] + " ")
	res.append("= 0 (improved)" + settings.NORMAL)
	return "".join(res)

def print_logs(argument, x=0, y=0, obj1=[0], obj2=[0]):
	logs = {
		# Required logs start from 1 and grow up
		1: "usage: python3 computor_v1.py [-h] [-v | --verbose] [--improved] [-f fil | --file file] <equation[s]>",
		2: "The polynomial degree is stricly greater than 2, I can't solve.",
		3: "Discriminant is strictly positive, the two solutions are:\nx = %g or x = %g" % (x, y),
		4: "Discriminant is zero, one solution: x = %g" % x,
		5: "Discriminant is less than 0, the two complex solutions are:\nx = %g + %gj or x = %g - %gj" % (x, y, x, y),
		6: "The solution is: x = %g" % x,
		7: "Identity - all of real numbers are the solution.",
		8: "Contradiction - none of real numbers is the solution.",
		9: "Equation: %s" % obj1,
		10: "Reduced:  %s" % obj1,
		11: "Polynomial degree: %d" % x,
		# Error handling starts from 100 and grows up
		# 100: ,
		101: "Error: Invalid character '%s' in equation '%s'" % (obj1, obj2),
		102: "Error: File '%s' does not exist" % obj1,
		103: "Error: Invalid form of equation '%s' ('<left part of equation> = <right part of equation>')" % obj1,
		104: "Error: Invalid form of equation '%s' (no coefficients)" % obj1,
		105: "Error: Improved form handles max 7 exponentials",
		# Addictional logs start from -1 grows down
		-1: "Left side of equation: [%s] | Right side of equation: [%s]" % (obj1, obj2),
		-2: "Left coefficients: %s | Right coefficients: %s" % (obj1, obj2),
		-3: "Reduced coefficients: %s" % obj1,
		-4: "Discriminant = b² - 4ac = %d" % x
	}
	if argument > 0 and argument < 100:
		print(logs.get(argument))
	elif argument >= 100:
		print(settings.RED, logs.get(argument), settings.NORMAL, sep="")
	elif settings.verbose:
		print(settings.CYAN, logs.get(argument), settings.NORMAL, sep="")


def print_help_info():
	print("usage: python3 computor_v1.py [-h] [-v | --verbose] [--improved] [-f file | --file file] <equation[s]>\n\
Computor_v1 is a program that solves polynomial equations up to 2nd degree, thus quadratic, linear and monomial equations.\n\
Options and arguments:\n\
	-h     			: display extended usage of computor_v2\n\
	-v | --verbose		: display verbose logs of equation solving process\n\
	--improved		: 'reduced' part of solving process will be display in more elegant style,\n\
					i.e. x² insted of X^2, 9 instead of 9 * X^0 etc.\n\
	-f || --file file	: take <file> with test cases instead of arguments from command line. Once\n\
					the program encounters this flag, it ignores all of the following parameters.\n\
					Valid file is constructed from the equations = one per line. It can contain\n\
					the comments with '#', meaning everything after '#' sign will be ignored\n\
	<equation[s]>	: the equations to solve. There should be at least one equation, otherwise\n\
					computor_v1 will sit and wait for the equation in command line. Equation\n\
					should be composed in the following way:\n\
					'a₀ * X^0 + a₁ * X^1 + ... + an * X^n = a₀ * X^0 + a₁ * X^1 + ... + an * X^n',\n\
					meaning:\n\
					- it has one equal sign,\n\
					- all terms are in the form of a * xⁿ,\n\
					- the powers are well ordered and all present.")
	

# ---------------------------------- HANDLE EQUATIONS ----------------------------------
def handle_equation(equation):
	if valid_equation(equation):
		return 1
	print("--------------------------------------------------")
	print_logs(9, obj1=equation)
	coeff = parse_equation(equation)
	if coeff == 1:
		return 1
	if len(coeff) < 1:
		print_logs(104, obj1=equation)
		return 1
	reduced = concat_reduced(coeff) if not settings.improved_form else concat_reduced_improved(coeff)
	if reduced == 1:
		return 1
	print_logs(10, obj1=reduced)
	print_logs(11, len(coeff) - 1)
	compute_result(coeff)
	return 0

def handle_args_equations():
	for i in range(1, len(sys.argv)):
		if handle_equation(str(sys.argv[i])):
			return 1

def handle_file_equations(filename):
	try:
		with open(filename) as file:
			for cnt, line in enumerate(file):
				if line and '#' in line:
					line = line.split("#")[0]
				if len(line.strip()) > 0 and handle_equation(line.strip()):
					return 1
	except:
		print_logs(102, obj1=filename)
		

# ----------------------------------- MAIN FUNCTIONS -----------------------------------
def compute_result(coeff):
	len_coeff = len(coeff)
	if len_coeff > 3:
		print_logs(2)
	elif len_coeff == 3:
		c, b, a = coeff[0], coeff[1], coeff[2]
		delta = (b ** 2) - (4 * a * c)
		print_logs(-4, delta)
		if delta > 0:
			s1, s2 = (-b-square_root(delta)) / (2*a), (-b+square_root(delta)) / (2*a)
			print_logs(3, s1, s2)
		elif delta == 0:
			print_logs(4, (-b) / (2*a))
		else:
			s1 = (-b-square_root(delta))
			print_logs(5, s1.real, s1.imag)
	elif len_coeff == 2:
		print_logs(6, 0 if coeff[1] == 0 else -(coeff[0]/coeff[1]))
	elif len_coeff == 1:
		print_logs(7 if coeff[0] == 0 else 8)

def main():
	i = 1
	length = len(sys.argv)
	while (i < length):
		if str(sys.argv[i]) == "-v" or str(sys.argv[i]) == "--verbose":
			settings.verbose = True
			sys.argv.remove(sys.argv[i])
			length -= 1
		elif str(sys.argv[i]) == "-i" or str(sys.argv[i]) == "--improved":
			settings.improved_form = True
			sys.argv.remove(sys.argv[i])
			length -= 1
		elif str(sys.argv[i]) == "-h":
			print_help_info()
			return 0
		elif str(sys.argv[i]) == "-f" or str(sys.argv[i]) == "--file":
			handle_file_equations(str(sys.argv[i+1]))
			return 0
		else:
			i += 1

	if len(sys.argv) == 1:
		inp = input("Insert equation here: ")
		handle_equation(inp)
		return 0
	handle_args_equations()


if __name__ == '__main__':
	main()



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
	print_info(20, True, obj=left_right)
	left_right = [get_coeff(left_right[0]), get_coeff(left_right[1])]
	print_info(21, True, obj=left_right)
	longer, shorter = (left_right[0], left_right[1]) if len(left_right[0]) >= len(left_right[1]) else (left_right[1], left_right[0])
	for i in range(len(shorter)):
		longer[i] -= shorter[i]
	print_info(22, True, obj=longer)
	return longer


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

def print_info(argument, is_verbose, x=0, y=0, obj=[0,0]):
	prints = {
		1: "Usage: python3 computor_v1.py [-v] <equation>",
		2: "The polynomial degree is stricly greater than 2, I can't solve.",
		3: "Discriminant is strictly positive, the two solutions are:\n%f\n%f" % (x, y),
		4: "Discriminant is zero, one solution:\n%f" % x,
		5: "Discriminant is less than 0, no solution.",
		6: "The solution is: %f" % x,
		7: "Identity - all of real numbers are the solution.",
		8: "Contradiction - none of real nuumers is the solution.",
		9: "Equation: %s" % obj,
		10: "Reduced:  %s" % obj,
		11: "Polynomial degree: %d" % x,
		20: "Left side of equation: [%s] | Right side of equation: [%s]" % (obj[0], obj[1]),
		21: "Left coefficients: %s | Right coefficients: %s" % (obj[0], obj[1]),
		22: "Reduced coefficients: %s" % obj,
		23: "Discriminant = b^2 - 4ac = %d" % x
	}
	if is_verbose and settings.verbose:
		print(settings.CYAN, end="")
	print(prints.get(argument), settings.NORMAL)


# ----------------------------------- MAIN FUNCTIONS -----------------------------------
def compute_result(coeff):
	len_coeff = len(coeff)
	if len_coeff > 3:
		print_info(2, False)
	elif len_coeff == 3:
		c, b, a = coeff[0], coeff[1], coeff[2]
		delta = (b ** 2) - (4 * a * c)
		print_info(23, True, delta)
		if delta > 0:
			s1, s2 = (-b-square_root(delta)) / (2*a), (-b+square_root(delta)) / (2*a)
			print_info(3, False, s1, s2)
		elif delta == 0:
			print_info(4, False, (-b) / (2*a))
		else:
			print_info(5, False)
	elif len_coeff == 2:
		print_info(6, False, -(coeff[0]/coeff[1])) #not fully working  
	elif len_coeff == 1:
		print_info(7 if coeff[0] == 0 else 8, False)

def main():
	if len(sys.argv) < 2 or (len(sys.argv) == 2 and str(sys.argv) == "-v"):
		print_info(1, False)
		exit(0)

	if str(sys.argv[1]) == "-v":
		settings.verbose = True

	for i in range(1 if not settings.verbose else 2, len(sys.argv)):
		try:
			print("\n---------------------------------------------------")
			print_info(9, False, obj=str(sys.argv[i]))
			coefficients = parse_equation(str(sys.argv[i]))
			print_info(10, False, obj=concat_reduced(coefficients))
			print_info(11, False, len(coefficients) - 1)
			compute_result(coefficients)
			print("---------------------------------------------------")
		except:
			print_info(1, False)
			exit(0)


if __name__ == '__main__':
	main()

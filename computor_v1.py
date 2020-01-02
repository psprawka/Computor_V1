import sys
import numbers

def square_root(number):
	return number ** (1/2)


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def get_coefficients(equation):
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


def substract_lists(longer, shorter):
	for i in range(len(shorter)):
		longer[i] -= shorter[i]
	return longer


def parse_equation(equation):
	left_right = equation.split("=")
	coeff_left = get_coefficients(left_right[0])
	coeff_right = get_coefficients(left_right[1])
	return substract_lists(coeff_left, coeff_right) if len(coeff_left) >= len(coeff_right) else substract_lists(coeff_right, coeff_left)

def compute_result(coeff):
	len_coeff = len(coeff)
	if len_coeff > 3:
		print("The polynomial degree is stricly greater than 2, I can't solve.")
	elif len_coeff == 3:
		c, b, a = coeff[0], coeff[1], coeff[2]
		delta = (b ** 2) - (4 * a * c)
		if delta > 0:
			s1, s2 = (-b-square_root(delta)) / (2*a), (-b+square_root(delta)) / (2*a)
			print("Discriminant is strictly positive, the two solutions are:\n%f\n%f" % (s1, s2))
		elif delta == 0:
			print("Discriminant is zero, one solution:\n%f", (-b) / (2*a))
		else:
			print("Discriminant is less than 0, no solution.")
	elif len_coeff == 2:
		print("The solution is:", -(coeff[0]/coeff[1])) #not fully working  
	elif len_coeff == 1:
		if coeff[0] == 0:
			print("All real numbers are the solution.")
		else:
			print("The solution is:")

def create_reduced(coeff):
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


def main():
	if len(sys.argv) < 2:
		print("Usage: python3 computor_v1.py <equation>")
		exit(0)

	for i in range(1, len(sys.argv)):
		print("\n---------------------------------------------------")
		print("Equation: %s" % str(sys.argv[i]))
		coefficients = parse_equation(str(sys.argv[i]))
		print("Reduced:  %s" % create_reduced(coefficients))
		print("Polynomial degree:", len(coefficients) - 1)
		compute_result(coefficients)
		print("---------------------------------------------------")
	print("\n")

if __name__ == '__main__':
	main()





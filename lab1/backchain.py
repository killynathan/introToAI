import copy

from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
	 match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
	matches = [hypothesis]	
	for rule in rules:
		var_names =  match(rule.consequent()[0], hypothesis)
		if var_names is not None:
			temp = copy.deepcopy(rule.antecedent())
			if isinstance(temp, list):
				for i in range(len(temp)):
					temp[i] = simplify(backchain_to_goal_tree(rules, populate(temp[i], var_names)))
				matches.append(simplify(temp))
			else:
				matches.append(simplify(populate(backchain_to_goal_tree(rules, temp), var_names)))	
	
	return simplify(OR(matches))

# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
testie = [0,1,2]



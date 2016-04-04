from __future__ import generators
import sys
import string
import itertools
import re
import copy
class Substitution:

    mSubst = {}
    def __init__(self):
        self.mSubst = {}
    def Substitution(self, s):
        for (k, v) in s.mSubst.items():
            self.mSubst[k] = v
        return self
    def toString(self):
        return str(self.mSubst)

class Clause:
    mVariables = []
    mPredicate = ""
    def __init__(self):
        self.mVariables = []
        self.mPredicate = ""

    def Clause_clause(self, c):  #c:Clause
        self.mPredicate = c.mPredicate
        for v in c.mVariables:
            c.mVariables.append(v)
    def Clause_string(self, clause): #clause:string
        # print "clause:", clause
        split1 = clause.split('(')
        self.mPredicate = split1[0]
        vars = (split1[1].split(')')[0]).split(', ')
        for i in range(len(vars)):
            self.mVariables.append(vars[i])
        return self

    def toString(self):
        sb = ""
        sb += (self.mPredicate)+'('
        # self.mVariables.reverse()
        for v in self.mVariables:
            sb += v + ","
        re.sub(',$', ')', sb)
        sb = self.replace_last(sb, ',', ')')
        return sb

    def replace_last(self, source_string, replace_what, replace_with):
        head, sep, tail = source_string.rpartition(replace_what)
        return head + replace_with + tail

    def isConstant(self):
        for v in self.mVariables:
            if v[0].islower():
                return False
        return True

class Rule:
    mRight = Clause()
    mLefts = None
    def toString(self):
        sb = ""
        if self.mLefts != None and len(self.mLefts) != 0:
            for v in self.mLefts:
                sb += v.toString() + " && "
            # sb[len(sb)-3] = ""
            sb = re.sub(' && $', ')', sb)
            sb += " => "
        sb += self.mRight.toString()
        return sb

class KnowledgeBase:
    mKB = {}
    mSearchedRight = []
    def __init__(self):
        self.mKB = {}
        self.mSearchedRight = []
        self.mStandardizedClause = {}
        self.mVariableCount = 0

    def canBeInfered(self, goal):
        self.reset()
        p = Substitution()

        try:
            next(self.backChainingAnd(goal, p))
        except StopIteration:
            return False
            # print "final:", goal.toString()
        return True
    def isCircle(self, c):
        if c.toString() in self.mSearchedRight:
            return True
        else:
            return False

    def tryAddConstant(self, c):
        if c.toString() not in self.mSearchedRight and (c.isConstant() == True):
            self.mSearchedRight.append(c.toString())

    def tryRemoveConstant(self, c):
        if c.toString() in self.mSearchedRight:
            self.mSearchedRight.remove(c.toString())

    def print_ask_result(self, goal, theta):
        ask_variable = goal.mPredicate+"("
        for var in goal.mVariables:
            if self.isVariable(var):
                if var in theta.mSubst.keys():
                    if self.isVariable(theta.mSubst[var]):
                        variable = theta.mSubst[theta.mSubst[var]]
                    else:
                        variable = theta.mSubst[var]
                else:
                    variable = "_"
            else:
                variable = var
            ask_variable += variable + ", "
        ask_variable = re.sub(', $', ')', ask_variable)
        # print "Ask:", ask_variable
        global final_result
        final_result += "Ask: "+ask_variable+"\n"

    def backChainingOr(self, goal, theta):
        res = []
        mVariables_string = '('
        rules = []
        count = 0
        #self.print_ask_result(goal, theta)
        count = 1
        for rule in self.mKB.get(goal.mPredicate):
            # print "rule:\t", rule.toString()
            # print "rule.mRgiht.mvariable:\t", rule.mRight.mVariables
            # for left in rule.mLefts:
            #     for i in left.mVariables:
            #         for j in rule.mRight.mVariables:
            #             if self.isVariable(j):
            #                 j = "x"+`count`
            #             if self.isVariable(i) and self.isVariable(j) and i != j:
            #                 if
            #                 i = "y"
            #                 j = "x"
            #     print "new rule:\t", rule.toString()
            b = False
            for i in range(len(goal.mVariables)):
                if not self.isVariable(goal.mVariables[i]) and not self.isVariable(rule.mRight.mVariables[i]) and not goal.mVariables[i] == rule.mRight.mVariables[i]:
                    b = True
                    break
            if not b:
                rules.append(rule)
        flag = False


        global final_result

        rule_flag = 0
        if not rules:
            self.print_ask_result(goal, theta)
        for rule in rules:
            # print "rule:\t", rule.toString()
            if rule.mLefts != None or rule_flag == 0:
                self.print_ask_result(goal, theta)
            rule_flag = 1

            if self.isCircle(goal) == True:
                continue
            standardizeRule = self.standardizeVariables(rule, goal, theta)

            # print "rule:\t", standardizeRule.toString()
            self.tryAddConstant(goal)
            sub = Substitution()
            temp = self.unify_clause(standardizeRule.mRight, goal, sub.Substitution(theta))
            if count == 1:
                count = 0
            # else:
                # print "!!!!!!!!!"
                # self.print_ask_result(goal, theta)
                # print "========="
                # count = 0
            self.tryRemoveConstant(goal)

            for theta1 in self.backChainingAnd(standardizeRule.mLefts, temp):

                flag = True
                new_var = ""
                var_result = ""
                for var in goal.mVariables:
                    if self.isVariable(var):
                        if var in theta1.mSubst.keys():
                            if self.isVariable(theta1.mSubst[var]):
                                if theta1.mSubst[var] in theta1.mSubst.keys():
                                    new_var += theta1.mSubst[theta1.mSubst[var]]+", "
                            else:
                                new_var += theta1.mSubst[var] + ", "

                    else:
                        new_var += var+', '
                var_result = goal.mPredicate + "(" + new_var
                var_result = re.sub(', $', ')', var_result)

                # print "True:", var_result
                final_result += "True: "+var_result+"\n"
                rule_flag = 0
                yield theta1
                    # res.append(theta1)
                # break

        if flag == False:
            False_variable = goal.mPredicate+"("
            for var in goal.mVariables:
                if self.isVariable(var):
                    if var in theta.mSubst.keys():
                        if self.isVariable(theta.mSubst[var]):
                            variable = theta.mSubst[theta.mSubst[var]]
                        else:
                            variable = theta.mSubst[var]
                    else:
                        variable = "_"
                else:
                    variable = var
                False_variable += variable + ", "
            False_variable = re.sub(', $', ')', False_variable)
            # print "False:", False_variable
            final_result += "False: "+False_variable+"\n"

            # return None
        # else:
        #     return
    def backChainingAnd(self, goals, theta):
        if theta == None:
            return
        res = []
        if not goals:
            # print "backChainingAnd goals == empty"
            # if theta != None:
            # res.append(theta)
            yield theta
            return
            # return res
        #first = Clause()
        first = goals[0]
        rest = goals[1:]
        outer_flag = False
        for goal in rest:
            for var in first.mVariables:
                if var in goal.mVariables and self.isVariable(var):
                    outer_flag = True
                else:
                    pass
        # print "goals:\t", goals
        # first = copy.deepcopy(goals)
        # print "theta:\t", theta
        # print "first:", first.toString()
        # theta1s = self.backChainingOr(self.substitute(theta, first), theta)
        # if theta1s != None:
        # print "theta,first:", theta.mSubst.items(), first.toString()
        # print "goal = ", self.substitute(theta, first).toString()

        for theta1 in self.backChainingOr(self.substitute(theta, first), theta):
           # self.print_ask_result(self.substitute(theta, first), theta)
            sub = Substitution()
            flag = False
            # theta2s = self.backChainingAnd(goals, sub.Substitution(theta1))\
            # if theta2s != None:
            # visited = set()
            # if sub.Substitution(theta1) in visited:
            #     continue
            # visited.add(sub.Substitution(theta1))
            for theta2 in self.backChainingAnd(rest, sub.Substitution(theta1)):
                flag = True
                yield theta2
            if not flag:
                if outer_flag == True:
                    continue
                # goals_copy = copy.deepcopy(goals)
                # goals_copy.remove(first)

                break
                    # res.append(theta2)
        # if flag == False:
        #     return
        # else:
        #     return res

    def substitute(self, theta, c):
        q = Clause()
        q.mPredicate = c.mPredicate
        for v in c.mVariables:
            if v not in theta.mSubst.keys():
                q.mVariables.append(v)
            else:
                subst = theta.mSubst[v]
                q.mVariables.append(subst)
        return q

    def isVariable(self, s):
        if s != None and s[0].islower():
            return True
        else:
            return False
    def unify_clause(self, mRight, goal, theta):
        # print "unify_clause"
        # print "theta in unify_clause:", theta.mSubst
        # print "mRight:", mRight.mPredicate, mRight.mVariables
        # print "goal:", goal.mPredicate, goal.mVariables
        rhs = copy.deepcopy(mRight.mVariables)
        gs = copy.deepcopy(goal.mVariables)
        # print "unify_clause rhs:\t", rhs
        # print "unify_clause gs:\t", gs
        result_clause = self.unify(rhs, gs, theta)
        # print goal.toString()
        return result_clause

    def unify(self, x, y, theta):
        # print "get into unify!!"
        if None == theta:
            return None
        if x == y:
            # print "x is y!!!!!!!!"
            return theta
        if len(x) == 1 and len(y) == 1:
            # print "x.remove[0]:", x
            xv = x.pop(0)
            # print "xv:", xv
            yv = y.pop(0)
            # print "yv:", yv
            if self.isVariable(xv):
                # print "xv is variable:\t", xv
                # print "theta.mSubst in xv:", theta.toString()
                result = self.unifyVar(xv, yv, theta)
                # print "result:", result.mSubst
                return result
                # return self.unifyVar(xv, yv, theta)
            if self.isVariable(yv):
                # print "yv is variable:\t", yv
                # print "theta.mSubst in yv:", theta.toString()
                result = self.unifyVar(yv, xv, theta)
                # print "result:", result.mSubst
                return result
            if xv == yv:
                # print "xv is yv!!!!!!"
                s = Substitution()
                return s
        if len(x) > 1 and len(y) > 1:
            # print "len(x)>1!!!!!!"
            firstx = []
            firstx.append(x.pop(0))
            firsty = []
            firsty.append(y.pop(0))
            # print "firstx:\t", firstx, "firsty:\t", firsty
            return self.unify(x, y, self.unify(firstx, firsty, theta))
        # print "False:"
        return None

    def unifyVar(self, var, x, theta):
        # print "unifyvar theta:", theta.mSubst
        if var in theta.mSubst.keys():
            val = []
            val.append(theta.mSubst[var])
            xl = []
            xl.append(x)
            # print "unifyvar in if var:", theta.mSubst
            return self.unify(val, xl, theta)
        if x in theta.mSubst.keys():
            # print "go into if x in theta.m...."
            self.unifyVar(x, var, theta)
        theta.mSubst[var] = x
        # print "theta.mSubset in end of unifyvar:", theta.mSubst

        return theta
    def addRule(self, input):
        # print "addRule"
        line = input.readline() ## read one line
        pq = line.split(" => ")
        r = Rule()
        r.mRight = Clause()
        r.mRight = r.mRight.Clause_string(pq[len(pq)-1])
        if r.mRight.mPredicate not in self.mKB.keys():
            self.mKB[r.mRight.mPredicate] = []
        if len(pq) > 1:
            r.mLefts = []
            ps = pq[0].split(" && ")
            for i in range(len(ps)):
                p = Clause()
                r.mLefts.append(p.Clause_string(ps[i]))
        # if None == r.mLefts:
        #     self.mKB[r.mRight.mPredicate].insert(0, r)
        # else:
        self.mKB[r.mRight.mPredicate].append(r)

    def addKB(self, scanner, numKB):
        while numKB != 0:
            self.addRule(scanner)
            numKB -= 1
    mVariableCount = 0
    def newVariableName(self):
        res = "x"
        res += `self.mVariableCount`
        self.mVariableCount += 1
        # print "newVariableName:", res
        return res
    mStandardizedClause = {}
    def reset(self):
        self.mStandardizedClause = {}
        self.mSearchedRight = []
        self.mVariableCount = 0
    def isStandardized(self, c):
        return False
    def addStandardized(self, c):
        self.mStandardizedClause[c.mPredicate] = c
    def getStandardized(self, c):
        return self.mStandardizedClause[c.mPredicate]
    def varReplacementTable(self, c, table):

        # print "table: \t", table

        if self.isStandardized(c) == True:
            sc = Clause()
            sc = self.getStandardized(c)
            for i in range(len(c.mVariables)):
                v = c.mVariables[i]
                if v not in table.keys():
                    table[v] = sc.mVariables[i]
        else:
            # print "varreplacementtable else:"
            # print "c.var:", c.mVariables
            for v in c.mVariables:
                # print "c.mVariables( v ):", v
                if v not in table.keys():
                    if self.isVariable(v) and v not in table.values():
                        # print "table values:", table.values()
                        # print "v:", v
                        table[v] = self.newVariableName()
                    else:
                        table[v] = v
                    # print "table[v]: ", v
            # print "final table:", table
    def standardizedClause(self, c, table):
        # print "#####!!!!!standardizedclause c:", c.mPredicate, c.mVariables
        if self.isStandardized(c):
            return self.getStandardized(c)
        sc = Clause()
        sc.mPredicate = c.mPredicate
        for v in c.mVariables:
            sc.mVariables.append(table[v])
        self.addStandardized(sc)
        # print "end of standardizedclause(sc):", sc.toString()
        return sc

    def standardizeVariables(self, rule, goal, theta):
        # table = {}
        # for i in range(len(goal.mVariables)):
        #     # for j in range(len(rule.mRight.mVariables)):
        #     if goal.mVariables[i] != rule.mRight.mVariables[i] and self.isVariable(goal.mVariables[i]) == False:
        #         table[goal.mVariables[i]] = rule.mRight.mVariables[i]
        #     for left in rule.mLefts:
        #         for j in range(len(left.mVariables)):
        #             if left.mVariables[j] in table.keys():
        #                 left.mVariables[j] = table[left.mVariables[j]]
        #


        standardized = Rule()
        if None == rule.mLefts:
            standardized.mLefts = []
            standardized.mRight = rule.mRight
            return standardized

        table = {}
        self.varReplacementTable(rule.mRight, table)
        for c in rule.mLefts:
            self.varReplacementTable(c, table)
        standardized.mRight = self.standardizedClause(rule.mRight, table)
        standardized.mLefts = []
        for c in rule.mLefts:
            standardized.mLefts.append(self.standardizedClause(c, table))
        return standardized

class Inference:
    def readQueries(self, scanner):
        qs = []
        clause = scanner.readline()
        clause_all = clause.split(" && ")
        # print "clause_all:", clause_all
        for c in clause_all:
            # print "c:\t", c
            test = None
            q = Clause()
            test = q.Clause_string(c)
            # print "test:", test.toString()
            qs.append(test)
        # print "qs:", qs
        return qs

if __name__ == '__main__':
    # Inference().main()
    infer = Inference()
    # global final_result
    fo = open("output.txt", "w")
    # result = ""
    global final_result
    final_result = ""
    scanner = open(sys.argv[-1])
    # numQuery = 1
    queries = infer.readQueries(scanner)
    # for q in queries:
        # print q.mPredicate
    # print "queries:", queries
    kb = KnowledgeBase()
    numKB = int(scanner.readline())
    # print "numKB:", numKB
    kb.addKB(scanner, numKB)
    val_i = False
    val = 0
    # print "queris:\t", queries
    # for q in queries:
        # print "q:\t", q.toString()
    # print "queries:", queries

    val_i = kb.canBeInfered(queries)
    if val_i == True:
        val += 0
    else:
        val += 1

    if val == 0:
        # print "True"
        final_result += "True"
    else:
        # print "False"
        final_result += "False"

    scanner.close()
    fo.write(final_result)
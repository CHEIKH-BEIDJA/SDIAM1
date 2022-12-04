import sys
from collections import deque
class Node(object):
    def __init__(self, data):
        """
        Initialize the tree with user expression(algebraic expression)
    
        Args:
            data(str): string representation of math expression
        """
        self.data = data
        self.right = None
        self.left = None
        # flag for operators to distinguish from operands
        self.operator = False

    def __repr__(self) -> str:
        """Return a string representation of this parse tree node."""
        return 'Node({!r})'.format(self.data)

    def is_leaf(self) -> bool:
        """Return True if this node is a leaf(that is operand)."""
        return self.left is None and self.right is None


class AST(object):
    def __init__(self, expression: str = None):
        print(f"Infix expresion est : {expression}")

        self.root = None
        self.size = 0
        if expression is not None:
            self.insert(expression)


    def is_empty(self) -> bool:
        """Return True if this binary search tree is empty (has no nodes)."""
        return self.root is None

    def insert(self, expression: str):
        """
        Insert the postfix expression into the tree using stack
        """
        postfix_exp = self.infix_to_postfix(expression)
        # stack
        stack = deque()
        char = postfix_exp[0]
        # créer un nœud pour le premier élément de l'expression
        node = Node(char)
        # push it to stack 
        stack.appendleft(node)
        # itérateur d'expression
        i = 1
        while len(stack) != 0:
            char = postfix_exp[i]
            # if char is float or int
            if '.' in char or char.isdigit():
                # créer un nœud et pousser le nœud dans la pile
                node = Node(char)
                stack.appendleft(node)
            else:
                # créer un nœud parent (opérateur) pour les opérandes
                operator_node = Node(char)
                operator_node.operator = True
                # pop le dernier élément poussé et créer right_child
                right_child = stack.popleft()
                # pop élément un avant le dernier élément et créer left_child
                left_child = stack.popleft()
                # attribuez-les en tant L'Enfant de l'opérateur (parent)
                operator_node.right = right_child
                operator_node.left = left_child
                # repousser le nœud opérateur (sous-arbre) vers la pile
                stack.appendleft(operator_node)
                # vérifier si nous atteignons le dernier élément de l'expression
                # on peut donc définir la racine de l'arbre
                if len(stack) == 1 and i == len(postfix_exp) - 1:
                    self.root = stack.popleft()
            # incrément i
            i += 1
            self.size += 1
        print(f"le  nombre de noeuds ajoutés est : {i} noeuds   ")

    def infix_to_postfix(self, infix_input: list) -> list:
        priority = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2}
        # clean the infix expression
        clean_infix = self.token_input(infix_input)
        i = 0
        postfix = []
        operators = "+-/*"
        stack = deque()
        while i < len(clean_infix):
            char = clean_infix[i]
            # vérifier si char est un opérateur
            if char in operators:
                # check if the stack is empty or the top element is '('
                if len(stack) == 0 or stack[0] == '(':
                    # just push the operator into stack
                    stack.appendleft(char)
                    i += 1
                # otherwise compare the curr char with top of the element
                else:
                    # peek the top element
                    top_element = stack[0]
                    # check for precedence
                    # if they have equal precedence
                    if priority[char] >= priority[top_element]:
                        popped_element = stack.popleft()
                        postfix.append(popped_element)
                        stack.appendleft(char)
                        i += 1
                    elif priority[char] < priority[top_element]:
                        # pop the top element
                        popped_element = stack.popleft()
                        postfix.append(popped_element)
            elif char == '(':
                # add it to the stack
                stack.appendleft(char)
                i += 1
            elif char == ')':
                top_element = stack[0]
                while top_element != '(':
                    popped_element = stack.popleft()
                    postfix.append(popped_element)
                    # update the top element
                    top_element = stack[0]
                # maintenant nous sautons les parenthèses ouvrantes et les supprimons
                stack.popleft()
                i += 1
            # char is operand
            else:
                postfix.append(char)
                i += 1
        if len(stack) > 0:
            for i in range(len(stack)):
                postfix.append(stack.popleft())
        print(f"postfix expression est : {postfix}")
        return postfix

    def token_input(self, infix_exp):
        expresion = []
        for i in infix_exp:
            if i.isdigit() or i == '.':
                if expresion and (expresion[-1].isdigit() or '.' in expresion[-1]):
                    expresion[-1] += i
                else:
                    expresion.append(i)
            elif i in '*/()+-':
                expresion.append(i)
        print(f"token expression : {expresion}")
        return expresion

    # parcours prefixe RGD
    def prefix(self, root):
        if root is not None:
            print(root.data, end="\t")
            self.prefix(root.left)
            self.prefix(root.right)

    # parcours infixe GRD
    def infix(self, root):
        if root is not None:
            self.infix(root.left)
            print(root.data, end="\t")
            self.infix(root.right)

        # parcours postfix GDR
    def postfix(self, root):
        if root is not None:
            self.postfix(root.left)
            self.postfix(root.right)
            print(root.data, end="\t")

    def display(self, root):
        if root is not None:
            print('(', end='')
            if root.left is not None:
                self.display(root.left)
                print(',', end='')
            print(root.data, end='')
            if root.right is not None:
                print(',', end='')
                self.display(root.right)
            print(')', end='')

    def evaluate(self, root) -> float:
        # Arbre vide
        if root is None:
            return 0
        # vérifier si nous sommes à la feuille, cela signifie que c'est un opérande
        if root.is_leaf():
            val = float(root.data)
            return val

        #  Évaluer le sous-arbre de gauche
        left_value = self.evaluate(root.left)
        #  Évaluer le sous-arbre droit
        right_value = self.evaluate(root.right)
        # addition
        if root.data == "+":
            return left_value + right_value
        # subtraction
        elif root.data == "-":
            return left_value - right_value
        # division
        elif root.data == "/":
            if right_value !=0:
             return left_value / right_value
            else:
                sys.exit('impossible de diviser par zéro')

        # multiplication
        else:
            return left_value * right_value


if __name__ == "__main__":
    user_input = input("Enter une expresion ne contient pas un puissance (^): ")
    tree_obj = AST(user_input)
    # print(f"arbre: {tree_obj}")
    root = tree_obj.root
    print("prefix :")
    tree_obj.prefix(root)
    print()
    print("infix :")
    tree_obj.infix(root)
    print()
    print("postfix :")
    tree_obj.postfix(root)
    print()
    print("arbre :")
    tree_obj.display(root)
    print()
    print("resultat :")
    print(f"{user_input} = {tree_obj.evaluate(root)} ")

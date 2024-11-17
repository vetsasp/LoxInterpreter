class Parent1:
    def method1(self):
        print("Parent 1 method")

class Parent2:
    def method2(self):
        print("Parent 2 method")

class Child(Parent1, Parent2):
    def method3(self):
        print("Child method")


if __name__ == "__main__":
    child = Child()
    child.method1()  # Output: Parent 1 method
    child.method2()  # Output: Parent 2 method
    child.method3()  # Output: Child method
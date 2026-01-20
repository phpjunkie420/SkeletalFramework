import types


class Class:
    x = 100  # Class Variable

    def __init__(self):
        # Use 'self.x' to write to the INSTANCE
        self.x = 1

        # Use 'Class.x' to write to the CLASS
        Class.x += 1

    def instance_method(self):
        print(self.x)

    @staticmethod
    def static_method():
        print(Class.x)


# --- INSTANTIATION ---
instance = Class()

print(f'Instance: {instance.x}')
print(f'Class:    {Class.x}')
print(f'{'-' * 20}\n')

# --- INSTANCE VARIABLES ---
# This looks at cls.__dict__
# It will print 'x: 1' because we assigned to self.x
instance_dict = {k: v for k, v in instance.__dict__.items() if not k.startswith('_')}
print("Instance Dict (Self):")
for k, v in instance_dict.items():
    print(f"  {k}: {v}")
print(f'{'-' * 20}\n')

# --- CLASS VARIABLES ---
# This looks at Class.__dict__
# It will print 'x: 101' because the class template assigned it
# to Class.x and Class.x += 1 was used inside the __init__ method.
class_dict_of_the_instance = {
    k: v for k, v in instance.__class__.__dict__.items()  # instance.__class__ is type of <Class>
    if not k.startswith('_')
    # and not isinstance(v, types.FunctionType)
}
print("Class Dict (Template):")
for k, v in class_dict_of_the_instance.items():
    print(f"  {k}: {v}")
print(f'{'-' * 20}\n')

# I did a bit of reading on this. It really just comes down to the self keyword. When you are inside __init__, self refers specifically to the instance being created, not the class template.
# So when you write self.var = ..., Python targets the instance's dictionary immediately. It doesn't matter if the Class has a variable with that name; the assignment forces Python to create a new entry on the instance itself, which effectively 'shadows' the class variable.

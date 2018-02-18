class MetaMerge(type):

    def __init__(cls, name, bases, attributes, merge=()):
        for mtd_name in merge:
            setattr(cls, mtd_name, type(cls)._generate_mtd(
                    [getattr(base, mtd_name) for base in bases])
            )

    @staticmethod
    def _generate_mtd(methods_to_call):
        def new_mtd(self, *args, **kwargs):
            for mtd in methods_to_call:
                mtd(self, *args, **kwargs)

        return new_mtd

    def __new__(mcs, name, bases, attributes, merge=()):
        return type.__new__(mcs, name, bases, attributes)




class A:
    def foo(self):
        print('a')

class B:
    def foo(self):
        print('b')

class AB(A, B, metaclass=MetaMerge, merge=('foo',)):
    pass


ab = AB()
ab.foo()  # ab



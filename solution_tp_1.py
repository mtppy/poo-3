from collections import OrderedDict

 
class MetaTable(type):
    def __init__(cls, name, bases, attributs):
        if bases:
            template = '|'
            for attr_name, value in attributs.items():
                if not attr_name.startswith('_'):
                    template += '{{{}:<{}}}|'.format(attr_name, value)

            cls._template = template

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return OrderedDict()


class BaseTable(metaclass=MetaTable):

    def __init__(self, **fields):
        self._fields = fields

    def __str__(self):
        cls = type(self)
        return cls._template.format(**self._fields)


class PersonneTable(BaseTable):
    nom = 12
    prenom = 4


p1 = PersonneTable(prenom='Tom', nom='Hatecerise')
p2 = PersonneTable(prenom='Jean', nom='Bonbeure')

print(p1)  # '|Tom |Hatecerise  |'
print(p2)  # '|Jean|Bonbeure    |'


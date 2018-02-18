Les Metaclasses
===============


**type** est la metaclass par défault.
C'est elle qui est appellé pour créer une classe.

La création d'une classe peut être statique::

    class Prof:
        def __init__(self, nom):
            self.nom = nom

Ou dynamique::

    def __init__(self, nom):
        self.nom = nom

    Prof = type('Prof', (), {'__init__': __init__})

Regarder dans une console python ce que renvoie:: 

    >>> issubclass(type, object)

Que peut on en conclure ?


**type** est également une classe, on peut donc créer ça propre 
métaclass en héritant de class::

    class MetaLog(type):
        def __init__(cls, name, bases, attributs):
            print(cls, name, bases, attributs)

et l'utiliser comme ceci::

    MaClass = MetaLog('MaClass', (), {})

Ou comme cela::

    class MaClass(metaclass=MaClass):
        pass


2) Pattern par défaut
---------------------


Pour éviter à l'utilisateur d'utiliser des métaclasses on va lui fournir 
une classe de base qui sera une instance de notre metaclasse::

    class MetaFoo(type):
        def __init__(cls, name, bases, attributs):
            if bases:        
                print(cls, name, bases, attributs)


    class BaseFoo(metaclass=MetaFoo):
        pass


    class MyFoo(BaseFoo):
        pass


3) Exo 
------   

On va créer une métaclasse **MetaTable** qui va nous permetre de créer des classes pour définir 
simplement comment doivent s'afficher les objets::


    class PersonneTable(BaseTable):
        nom = 12
        prenom = 4


    p1 = PersonneTable(prenom='Tom', nom='Hatecerise')
    p2 = PersonneTable(prenom='Jean', nom='Bonbeure')

    print(p1) # '|Tom |Hatecerise  |'
    print(p2) # '|Jean|Bonbeure    |'


Il faudra pour cela compléter le code de la métaclass::

    class MetaTable(type):
        def __init__(cls, name, bases, attributs):
            if bases:
                print(cls, name, bases, attributs)


    class BaseTable(metaclass=MetaTable):

        def __init__(self, **fields):
            self._fields = fields

        def __str__(self):
            cls = type(self)
            return cls._template.format(self._fields)





3.1) Experience
---------------

Créer une sous classe de **BaseTable** avec plusieurs attributs de classes:

    class FooTable(BaseTable):
        attr_a = 1
        attr_b = 2
        attr_c = 3
        attr_d = 4
        attr_e = 5


Que contiend le paramète attributs du la method **__init__** de **MetaTable** ?

::
    {'attr_b': 2,
     '__module__': '__main__',
     'attr_a': 1,
     'attr_e': 5,
     '__qualname__': 'FooTable',
     'attr_d': 4,
     'attr_c': 3}

On peut remarqué que les attributs sont stoqué dans un dictionnaire et donc ne sont pas ordonnée
On peut modifier la façon dont les attribus d'une classe sont stockés en redéfinissant la méthod 
**__prepare__** de la metaclasse::


    from collections import OrderedDict

     
    class MetaTable(type):
        def __init__(cls, name, bases, attributs):
            if bases:
                print(cls, name, bases, attributs)

        @classmethod
        def __prepare__(mcs, name, bases, **kwargs):
            return OrderedDict()


Regardez ce que contient le paramète attributs du la method **__init__** de MetaTable

    OrderedDict([('__module__', '__main__'), 
                 ('__qualname__', 'FooTable'), 
                 ('attr_a', 1),
                 ('attr_b', 2),
                 ('attr_c', 3),
                 ('attr_d', 4),
                 ('attr_e', 5)])



3.2) Formatage de chaine de caractère (la méthode format)
---------------------------------------------------------


:: 

    >>> template = "Salut {nom} {prenom}"
    >>> template.format(nom='Jean', prenom='Bonbeur')
    'Salut Jean Bonbeur'
    >>> fields = {
        'nom': 'Jean', 
        'prenom': 'Bonbeur'
    }
    >>> template.format(**fields)
    'Salut Jean Bonbeur'

    >>> "Salut {nom:<6} {prenom:<6}".format(**fields)
    'Salut Jean   Bonbeur'
           ^    ^ ^    ^
           123456 123456


    >>> "{{".format() 
    '{'
    >>> "{{{var}}}".format(var='prenom') 
    '{prenom}'


    Iterer sur un dict:
    >>> fields = {
    ...     'prenom': 3,
    ...     'nom': 6
    ... }
    >>> for key, value in fields.items():
    ...     print(key, value)
    prenom 3
    nom 6


Generer dans le **__init__** de **MetaTable** le template permettant d'afficher les 
attributs de la classe et stocké le dans **_template**

Ainsi la déclaration ci-dessous devra appeler générer le template::

    class PersonneTable(BaseTable):
        nom = 12
        prenom = 4

    
    # MetaTable doit générer l'attribut _template
    print(PersonneTable._template) # '|{nom:<12}|{prenom:<4}|'


TP 2 merge de classes
=====================

En python, lors d'héritage multiple, si les deux parents définissent une même méthode, 
un appel de cette méthode par la classe fille appellera la méthode du premier parent

class A:
    def foo(self):
        print('a')

class B:
    def foo(self):
        print('b')

# La classe AB hérite de la classe A et B
class AB(A, B):
    pass


ab = AB()
ab.foo()  # Affiche a


On souhaiterait avoir une méta-classe qui change ce comportement et pouvoir indiquer des méthodes à merger comme ceci::

    class AB(A, B, metaclass=MetaMerge, merge=('foo',)):
        pass

Pour que::

    ab = AB()
    ab.foo()  # Affiche: ab


Il va falloir créer une méta-classe dans laquelle on redéfinie **__new_\_** et **__init_\_** pour
pour faire passer le paramètre **merge** qui contiendra le nom des méthodes à merger::

    class MetaMerge(type):

        def __init__(cls, name, bases, attributes, merge=()):
            pass

        def __new__(mcs, name, bases, attributes, merge=()):
            return type.__new__(mcs, name, bases, attributes)


Dans le **__init_\_** récupérer la liste des méthodes à merger de chaque classe de base
vous utiliserai pour cela ``getattr(cls_de_base, nom_de_la_method_a_merger)``.

Passer cette liste à la fonction ``_generate_mtd`` qui vous generera la nouvelle method.
vous injecterais cette nouvelle méthod en utilisant ``setattr(cls, method_name, method)``

::

    class MetaMerge(type):

        def __init__(cls, name, bases, attributes, merge=()):
            pass

        @staticmethod
        def _generate_mtd(methods_to_call):
            def new_mtd(self, *args, **kwargs):
                for mtd in methods_to_call:
                    mtd(self, *args, **kwargs)

            return new_mtd

        def __new__(mcs, name, bases, attributes, merge=()):
            return type.__new__(mcs, name, bases, attributes)

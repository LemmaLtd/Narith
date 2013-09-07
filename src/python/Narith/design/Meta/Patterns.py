'''
[Narith]
Author: Saad Talaat
Date:    6th September 2013
Brief:    Design patterns for classes
'''


class Pattern(type):
    def __init__(self, name, bases, attrs):
        super(Pattern, self).__init__(name, bases, attrs)

    def __call__(self, *args, **kwargs):
        return super(Pattern, self).__call__(*args, **kwargs)


class Singleton(Pattern):

    def __call__(self, *args, **kwargs):
        if not hasattr(self, '_single'):
            self._single = super(Singleton, self).__call__(*args, **kwargs)
        return self._single

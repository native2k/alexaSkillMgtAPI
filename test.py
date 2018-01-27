#!/usr/bin/env python
# -*- coding: utf-8 -*-

class VarProxy(object):
        def __init__(self, key, **kwargs):
            # self._data = data
            self._key = key

        def __set__(self, obj, val):
            print "__set__ %s %s" % (obj, val)
            # self._data[self._key] = val
            obj._obj.setval(self._key, val, **obj._kwargs)

        def __get__(self, obj, objtype):
            print "__get__ %s %s" % (obj, objtype)
            # return self._data.get(self._key)

            return obj._obj.getval(self._key, **obj._kwargs)


class SubContainer(object):
    """docstring for SubContainer"""

    def __init__(self, obj, **kwargs):
        super(SubContainer, self).__init__()
        self._kwargs = kwargs
        self._obj = obj



class Test(object):

    availKeys = [
        'test1', 'test2',
    ]

    # test1 = VarProxy('test1')
    # test2 = VarProxy('test2')

    class locale(SubContainer):
        test5 = VarProxy('test5')



    def setval(self, param, value, lang=''):
        print "setval: %s %s %s %s" % (self, param, value, lang)

        self.val[lang + param] = value

    def getval(self, param, lang=''):
        print "getval self: %s param: %s arg2: %s" % (self, param, lang)
        return self.val.get(lang + param, '-')


    def __init__(self):
        self._kwargs = {}
        self._obj = self
        self.val = {}

        setattr(self, 'de', self.locale(self, lang='de-DE'))


def ClassFactory():
    baseClass = Test
    for key in Test.availKeys:
        setattr(baseClass, key, VarProxy(key))

    return Test()


if __name__ == '__main__':

    test = ClassFactory()
    print dir(test)
    print 'test.val ', test.val
    print 'test.test2 ', test.test2
    print 'test.test1 ', test.test1
    test.test1 = 'blub'
    test.test2 = 'foo'
    print 'test.val ', test.val
    # test.set_test1('foor')
    print 'test.test1 ', test.test1
    print 'test.test2 ', test.test2
    test.de.test5 = 'check this out'
    print 'test.de.test5 ', test.de.test5
    # print 'test.bar ', test.bar
    # print 'test.bar ', test.bar
    # print 'test.bar ', test.bar
    print 'test.val ', test.val



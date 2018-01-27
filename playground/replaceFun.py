import unittest
import sympy

def handleReplace(unsafe, keys):
    idxes = []
    i = 0

    original = unsafe

    keys = sorted(keys)[::-1]
    for key in keys:
        for i in range(len(unsafe)):
            if unsafe[i:].startswith(key):
                idxes.append((i, i+len(key)))
                unsafe = unsafe[:i] + "@"*len(key) + unsafe[i+len(key):]

    idxes = sorted(idxes)

    unsafe = original
    for idx in idxes[::-1]:
        key = unsafe[idx[0]:idx[1]]
        target = 'self.varDic["'+key+'"]'
        unsafe = unsafe[:idx[0]] + target + unsafe[idx[1]:]
    return unsafe



class TestReplacementMethods(unittest.TestCase):

    def testOne(self):
        unsafe = "And(y<=0,t>=0.2,v>=-0.1)"
        keys = ['y', 't', 'v']
        result = handleReplace(unsafe, keys)
        self.assertEqual(result, 'And(self.varDic["y"]<=0,self.varDic["t"]>=0.2,self.varDic["v"]>=-0.1)')

    def testTwo(self):
        unsafe = "And(y_a<=0,t_a>=0.2,v_a>=-0.1)"
        keys = ['y_a', 't_a', 'v_a']
        result = handleReplace(unsafe, keys)
        self.assertEqual(result, 'And(self.varDic["y_a"]<=0,self.varDic["t_a"]>=0.2,self.varDic["v_a"]>=-0.1)')

    # def testThree(self):
    #     unsafe = "And(y_a<=0,y_aa>=0.2,v_a>=-0.1)"
    #     keys = ['y_a', 'y_aa', 'v_a']
    #     result = handleReplace(unsafe, keys)
    #     self.assertEqual(result, 'And(self.varDic["y_a"]<=0,self.varDic["y_aa"]>=0.2,self.varDic["v_a"]>=-0.1)')
    #

if __name__ == '__main__':
    unittest.main()
    unsafe = "And(x1<=0,x11>=0.2,v_a>=-0.1)"
    keys = ['x1', 'x11', 'v_a']
    result = handleReplace(unsafe, keys)
    print result

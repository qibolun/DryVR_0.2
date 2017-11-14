import unittest

def handleReplace(unsafe, keys):
    idxes = []
    i = 0
    while i < len(unsafe):
        tempStr = ''
        while unsafe[i].isalpha():
            tempStr += unsafe[i]
            i+=1
        if tempStr in keys:
            idxes.append((i-len(tempStr), i))
        i+=1

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
        print result
        self.assertEqual(result, 'And(self.varDic["y"]<=0,self.varDic["t"]>=0.2,self.varDic["v"]>=-0.1)')

if __name__ == '__main__':
    unittest.main()
    # unsafe = "And(y<=0,t>=0.2,v>=-0.1)"
    # keys = ['y', 't', 'v']
    # result = handleReplace(unsafe, keys)
    # print result

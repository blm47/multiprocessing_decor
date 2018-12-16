# is OS ==windows multiprocessing.freeze_support()
import multiprocessing
import functools

class my_decorator(object):
    def __init__(self, target):
        self.target = target
        try:
            functools.update_wrapper(self, target)
        except:
            pass

    def __call__(self, candidates, args):
        f = []
        for candidate in candidates:
            f.append(self.target([candidate], args)[0])
        return f

def func(candidates, args):
    f = []
    foo = args.pop('func')
    for c in candidates:
        try:
            res = foo(c, **args)
            f.append({str(c): res})
        except Exception as err:
            f.append({str(c): 'Failed with error: %s'%err})
    return f


def run_multi_worker(List, Func, processes=100, **kwargs):
    kwargs.update({'func': Func})
    pool = multiprocessing.Pool(processes=len(List))
    results = [pool.apply_async(my_decorator(func), ([c], kwargs)) for c in List]
    pool.close()
    res = {}
    for r in results:
        res.update(r.get()[0])
    return res

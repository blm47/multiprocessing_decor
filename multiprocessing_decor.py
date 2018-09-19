import multiprocessing
import functools
import paramiko

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
    #command = args['command']
    for c in candidates:
        #res = test(c, args)
        try:
            res = foo(c, **args)
            f.append({str(c): res})
        except Exception as err:
            f.append({str(c): 'Failed with error: %s'%err})
        #res = sum(c)
        
    return f

# multi_worker = my_decorator(func)
def run_multi_worker(List, Func, processes=4, **kwargs):
    kwargs.update({'func': Func})
    pool = multiprocessing.Pool(processes=processes)
    results = [pool.apply_async(my_decorator(func), ([c], kwargs)) for c in List]
    pool.close()
    res = {}
    for r in results:
        res.update(r.get()[0])
    return res#[r.get()[0] for r in results]



def test(x, oper):
    #print(x)
    if oper == '+':
        return x + x
    else:
        return x - x
    
    
def SSHRequest(ip, command, user='admin', passw='85Bs341p'):
    sshcli = paramiko.SSHClient()
    sshcli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        sshcli.connect(ip, port=22, username=user, password=passw, allow_agent=False, look_for_keys=False)
        stdin, stdout, stderr = sshcli.exec_command('{com}'.format(com=command))
        data = (stdout.read() + stderr.read()).decode('utf-8').strip().split("\n")
        sshcli.close()
    except Exception as err:
        return err
    return data





L = [4,5,6,7,8]
run_multi_worker(L, test, oper='-')

run_multi_worker(data, SSHRequest, processes= 70, command=comm)

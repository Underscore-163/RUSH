import multiprocessing

def function_wrapper(function,*args,**kwargs):
    function(*args,**kwargs)

def class_wrapper(cls,*args,**kwargs):
    obj=cls(*args,**kwargs)
    conn1,conn2=multiprocessing.Pipe()
    conn2.send(obj)

def class_creator(cls,*args,**kwargs):
    proc=multiprocessing.Process(target=class_wrapper,args=args,kwargs=kwargs)
    proc.start()
    conn1,conn2=multiprocessing.Pipe()
    obj= conn1.recv()
    proc.join()
    return obj

def repeated_process(function,args:list):
    processes=[]
    for i in range(len(args)):
        processes.append(multiprocessing.Process(target=function_wrapper(function,*args[i])))
    for process in processes:
        process.start()
    for process in processes:
        process.join()


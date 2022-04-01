from IPython import get_ipython

def isnotebook():
    """
    A function for determining if the program is being run in a notebook or command line.
    """
    try:
        shell = get_ipython().__class__
        if hasattr(shell, '__name__') & (shell.__name__ == 'ZMQInteractiveShell'):
            return True
        else:
            return False
    except NameError:
        return False

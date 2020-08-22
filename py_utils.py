"""Utilities to process python files for indexing."""
import dis
import re
from inspect import getsource


def camel_case_split(identifier):
    """Split camelCase function names to tokens.

    Args:
        identifier (str): Identifier to split

    Returns:
        (list): lower case split tokens. ex: ['camel', 'case']
    """
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


def snake_case_split(identifier):
    """Split snake_case funtion names to tokens.

    Args:
        identifier (str): Identifier to split

    Returns:
        (list): lower case split tokens. ex: ['snake', 'case']
    """
    return [token.lower() for token in identifier.split('_')]


def process_docstring(doc_string):
    """Process docstring

    Args:
        doc_string (str): docstring for a function

    Returns:
        (list): list of tokens
    """
    tokens = []
    for token in re.findall(r'\w+', doc_string):
        camel_case_tokens = camel_case_split(token)
        snake_case_tokens = [snake_case_split(c) for c in camel_case_tokens]
        tokens.extend([ item for sublist in snake_case_tokens for item in sublist])
    return tokens


def process_name(func_name):
    """Process func_name

    Args:
        func_name (str): function name

    Returns:
        (list): list of tokens
    """
    camel_case_tokens = camel_case_split(func_name)
    snake_case_tokens = [snake_case_split(c) for c in camel_case_tokens]
    tokens = [ item for sublist in snake_case_tokens for item in sublist]
    return tokens


def process_funcs(functions):
    """Process functions

    Args:
        functions (list): list of function names

    Returns:
        (list): list of tokens
    """
    tokens = []
    for func_name in functions:
        tokens.extend(process_name(func_name))
    return tokens


def process_methods(methods):
    """Process methods

    Args:
        methods (list): list of method names

    Returns:
        (list): list of tokens
    """
    tokens = []
    for mname in methods:
        camel_case_tokens = camel_case_split(mname)
        snake_case_tokens = [snake_case_split(c) for c in camel_case_tokens]
        tokens.extend([ item for sublist in snake_case_tokens for item in sublist])
    return tokens


def tokenize(annotation):
    """Series of tokenization steps.

    Args:
        annotation (dict): dictionary of function name, docstring,
        internal method and function calls.

    Returns:
        tokens (list): list of tokens for a given annotation
    """
    tokens = []
    tokens.extend(process_docstring(annotation['doc']))
    tokens.extend(process_name(annotation['name']))
    tokens.extend(process_funcs(annotation['functions']))
    tokens.extend(process_methods(annotation['methods']))
    return tokens


def annotate(func):
    """Annotate a function with doc string, functions, methods and name

    Args:
        func (module): python module

    Returns:
        d (dict): [description]
    """
    
    # docstring can be empty for functions
    # consider function and method calls within functions alone, not classes
    d = {
        "doc": func.__doc__ if func.__doc__ else '',
        "name": func.__name__,
        "functions": _func_calls(func) if func.__class__ != type else [],
        "methods": _method_calls(func) if func.__class__ != type else []
    }
    return d


def _func_calls(fn):
    """Determine function calls within a function

    Args:
        fn (module): python module

    Returns:
        funcs (list): list of function calls within a function
    """
    funcs = []
    bytecode = dis.Bytecode(fn)
    for itr in bytecode:
        if itr.opname in ["LOAD_GLOBAL", "LOAD_METHOD"]:
            funcs.append(itr.argval)
    return funcs


def _method_calls(fn):
    """Determine method calls within a function

    Args:
        fn (module): python module

    Returns:
        (list): list of method calls within a function
    """
    return [x[1] for x in re.findall(METHOD, getsource(fn))]


def find_functions(module):
    """Determine method calls within a function

    Args:
        module (module): python module

    Returns:
        attr (list): list of method calls within a function
    """
    for attrname in dir(module):
        attr = getattr(module, attrname)
        # iteratively get __module__ or __class__ (where __module__ fails for clas
        if callable(attr) and getattr(attr, '__module__', getattr(attr, '__class__', '')) == module.__name__:
            yield attr


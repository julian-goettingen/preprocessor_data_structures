import c_functions as cf

def test_trivial():
    f = cf.read_func_decl("int foo()")
    assert(f.name == 'foo')
    assert (f.rettype == 'int')
    assert (len(f.params) == 0)

def test_easy():
    f = cf.read_func_decl("int foo(double x)")
    assert (f.name == 'foo')
    assert (f.rettype == 'int')
    assert (len(f.params) == 1)
    assert (f.params[0] == cf.CFunctionPrimitiveParam('x', 'double'))

def test_more_complex():
    f = cf.read_func_decl("int foo(double x, const int y, char character)")
    assert (f.name == 'foo')
    assert (f.rettype == 'int')
    assert (len(f.params) == 3)
    assert (f.params[0] == cf.CFunctionPrimitiveParam('x', 'double'))
    assert (f.params[1] == cf.CFunctionPrimitiveParam('y', 'int'))
    assert (f.params[2] == cf.CFunctionPrimitiveParam('character', 'char'))

def test_find_repl():
    s, ls = cf._find_and_replace_arr_defs("int bar(ARR1D_ARG(X,double *x, size_t n))")
    assert("ARR1D" not in s)
    assert(len(ls) == 1)

def test_with_simple_array():
    f = cf.read_func_decl("int bar(ARR1D_ARG(X,double *x, size_t n))")
    assert(f.name == 'bar')
    assert(f.rettype == "int")
    assert(f.params == [None])
    pass


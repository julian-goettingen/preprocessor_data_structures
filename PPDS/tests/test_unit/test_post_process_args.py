from src.post_process_args import post_process_args_in_place

def simple_args():
    return {'func_name': 'hello_world', 'definition': 'char *hello_world()'}

def test_post_process_args_in_place():

    args = simple_args()
    post_process_args_in_place(args, "FUNCTION")
    assert args["func_precon_checks"] == []
    assert args["func_args_unexpanded_names"] == []
    assert args["func_args_expanded_names"] == []
    assert args["func_args_expanded_with_types"] == []

    for k,v in simple_args().items():
        assert args[k] == v

from src.c_functions import read_func_decl


def post_process_args_in_place(argdict, ppds_class_name):

    if ppds_class_name == "FUNCTION":

        print(argdict["definition"])
        cfunc = read_func_decl(argdict["definition"])
        # issue warning on bad name? - no, alternative name and definition-name allowed
        argdict["func_args_unexpanded_names"] = []
        argdict["func_args_expanded_names"] = []
        argdict["func_args_expanded_with_types"] = []
        for p in cfunc.params:
            argdict["func_args_unexpanded_names"].append(p.name)
            argdict["func_args_expanded_names"].extend(p.get_expanded_names())
            argdict["func_args_expanded_with_types"].extend(p.get_expanded_with_types())

        argdict["func_precon_checks"] = []





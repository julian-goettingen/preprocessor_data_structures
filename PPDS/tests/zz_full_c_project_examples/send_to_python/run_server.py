from ppds_generated_python import server_utils


class ExampleServer(server_utils.PythonSimpleDataServer):
    def foo(self, a):
        print("foo was called with a ==", a)
        assert a == 2

if __name__ == "__main__":

    s = ExampleServer()
    s.run()

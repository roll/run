from box.importlib import check_module

if check_module('packgram'):
    import run
    from packgram.nose import SetupTest


    class SetupTest(SetupTest):

        # Public

        __test__ = True
        package = run

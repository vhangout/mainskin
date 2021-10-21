import inspect

pagesizes = {m[0]: m[1] for m in inspect.getmembers(__import__('reportlab.lib.pagesizes').lib.pagesizes,
                                                    lambda m: type(m) is tuple and len(m) == 2)}
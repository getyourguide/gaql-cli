def chain(*fns):
    """Chain multiple single argument function calls together"""

    def chained_fns(arg):
        result = arg
        for f in fns:
            result = f(result)
        return result

    return chained_fns

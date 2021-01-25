import datetime as dt

def logg(f):
    def wrapper(dataframe, *args, **kwargs):
        tic = dt.datetime.now()
        result = f(dataframe, *args, **kwargs)
        toc = dt.datetime.now()
        print(f"{f.__name__} took {toc-tic}")
        # print(result.info())

        return result
    return wrapper
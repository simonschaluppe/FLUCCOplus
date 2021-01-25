import datetime as dt

PJ_TO_GWH = 277.7778 # [GWh / PJ]
GWH_TO_PJ = 1/PJ_TO_GWH #[PJ/GWH]


def log(f):
    def wrapper(*args, **kwargs):
        tic = dt.datetime.now()
        result = f(*args, **kwargs)
        toc = dt.datetime.now()
        print(f"{f.__name__} took {toc-tic}")
        return result
    return wrapper

def logg(f):
    def wrapper(dataframe, *args, **kwargs):
        tic = dt.datetime.now()
        result = f(dataframe, *args, **kwargs)
        toc = dt.datetime.now()
        print(f"{f.__name__} took {toc-tic}")
        # print(result.info())

        return result
    return wrapper

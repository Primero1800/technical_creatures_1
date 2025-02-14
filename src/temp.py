explorer_kwargs = {
    "name": "ex_name",
    "country": "ex_cou",
    "description": "ex_des"
}

kwargs = {
    # "name": "kw_name",
    "country": "kw_cou",
    # "description": "kw_des",
    "addit": "kw_addit",
}

if __name__ == "__main__":

    kwargs = {key:kwargs[key] if key in kwargs else val for key, val in explorer_kwargs.items()}
    print(kwargs)

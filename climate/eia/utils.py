def nonnull_unq_str(l):
    return "|".join(set([str(i) for i in l if not l is None]))

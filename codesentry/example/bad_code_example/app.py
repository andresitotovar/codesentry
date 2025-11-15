import os


def bad_function(x, y):
    # terrible style and maybe a bug
    if x == 1:
        print("Debug:", x, y)
    return x + y + 1  # off-by-one?


def insecure():
    api_key = "HARDCODED_SUPER_SECRET"
    print("Doing insecure stuff", api_key)


if __name__ == "__main__":
    bad_function(1, 2)
    insecure()

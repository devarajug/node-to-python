from handler import healthHandler


def exports(path):
    switcher = {
        "/hoover-health" : {"GET":healthHandler, "POST": healthHandler}
    }
    return switcher.get(path, "Invalid Path")

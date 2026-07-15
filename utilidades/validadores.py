import re


def archivo_csv_valido(nombre_archivo):

    return bool(
        re.match(
            r".+\.csv$",
            nombre_archivo,
            re.IGNORECASE
        )
    )
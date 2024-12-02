_prettify_translation = str.maketrans("hMb#", "ø△♭♯")


def prettify(s):
    return s.translate(_prettify_translation).replace("dim", "°")

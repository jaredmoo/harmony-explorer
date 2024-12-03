_prettify_translation = str.maketrans("hMb#", "ø△♭♯")


def prettify(s):
    return (
        s.replace("bb", "𝄫")
        .replace("##", "𝄪")
        .translate(_prettify_translation)
        .replace("dim", "°")
    )

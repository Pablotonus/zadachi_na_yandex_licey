def get_span(toponym):
    env = toponym["boundedBy"]["Envelope"]
    bottom = env["lowerCorner"].split(" ")
    top = env["upperCorner"].split(" ")
    dx = abs(float(top[0]) - float(bottom[0]))
    dy = abs(float(top[1]) - float(bottom[1]))
    return f"{dx},{dy}"
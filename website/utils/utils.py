from mpmath import mp


def is_empty(data):
    return data['fractions']


def create_time_string(hours, minutes, seconds, milliseconds, microseconds):
    response = ''

    response = add_time_substring(response, hours, 'hour')
    response = add_time_substring(response, minutes, 'minute')
    response = add_time_substring(response, seconds, 'second')
    response = add_time_substring(response, milliseconds, 'millisecond')
    response = add_time_substring(response, microseconds, 'microsecond')

    return response


def add_time_substring(string, unit, unit_name):
    if unit:
        string += f'{unit} ' + (f'{unit_name}s, ' if unit > 1 else f'{unit_name}, ')

    return string


def humanize_seconds(seconds):
    milliseconds = seconds * 1000 % 1000
    microseconds = round(milliseconds * 1000 % 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    milliseconds = int(milliseconds)
    seconds = int(seconds)
    minutes = int(minutes)
    hours = int(hours)

    response = create_time_string(hours, minutes, seconds, milliseconds, microseconds)

    li = response.rsplit(', ', 2)
    if len(li) > 2:
        response = li[0] + ' and ' + li[1] + ' ' + li[2]
    response = response.rstrip(', ')

    return response


def ratio(fraction):
    return mp.mpf(fraction.numerator) / mp.mpf(fraction.denominator)


def inverse_ratio(fraction):
    return mp.mpf(1) / ratio(fraction)

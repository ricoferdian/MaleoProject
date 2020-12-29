"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Copyright (C) 2020 Henrico Aldy Ferdian & Lennia Savitri Azzahra Loviana
Udayana University, Bali, Indonesia

This part of python program consist of the number conversion from str to float or int
"""

def str_to_num(x):
    if is_integer(x):
        return int(x)
    elif is_float(x):
        return float(x)
    else:
        return x

def is_num(x):
    if is_integer(x):
        return True
    elif is_float(x):
        return True
    else:
        return False

def is_float(x):
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True

def is_integer(x):
    try:
        a = int(x)
    except (TypeError, ValueError):
        return False
    else:
        return True
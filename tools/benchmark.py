"""
Basic performance benchmark for safe_radix32.

:copyright: 2021 Nándor Mátravölgyi
:license: Apache2, see LICENSE for more details.
"""
import random
import timeit

try:
    import safe_radix32._cython as sr32c
except ImportError:
    sr32c = None
import safe_radix32.pure as sr32p


def benchmark(name, fn, ns):
    t = timeit.timeit(lambda: [fn(n) for n in ns], number=2000)
    print("%-26s %10d/s" % (name, len(ns) / (t / 2000)))


def main():
    ns = [random.randint(-(2 ** 63), 2 ** 63 - 1) for _ in range(100)]
    es = [(sr32c if sr32c else sr32p).encode_safe_radix32(n) for n in ns]
    if sr32c:
        benchmark("encode safe_radix32-c", sr32c.encode_safe_radix32, ns)
        benchmark("decode safe_radix32-c", sr32c.decode_safe_radix32, es)
    benchmark("encode safe_radix32-pure", sr32p.encode_safe_radix32, ns)
    benchmark("decode safe_radix32-pure", sr32p.decode_safe_radix32, es)


if __name__ == "__main__":
    main()

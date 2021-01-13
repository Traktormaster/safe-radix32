# safe_radix32
A simple Python package that encodes any 64bit integer (long) into to
a string that is free from accidentally intelligible words.

## What?
The primary use-case for this library is to encode (and decode) 64bit database IDs
into compact strings. This functionality was defined by a few goals:
 - translated IDs must be string-type to be compatible with JavaScript where 64bit integers are not (well) supported
 - IDs must be usable in URLs (path, query-value and fragment) without escaping
 - IDs must avoid translating into intelligible words
 - the translated form has to be as compact as feasible

## Why?
There are numerous well supported and established encodings to represent an integer as string, but
hardly any (here I mean I could not find one suitable) where the translated value is guaranteed
to... look and feel professional.

Examples:
 - A system generates a database ID randomly for an account: `6733255313934373709`.
 It seems perfectly innocuous, but if you base64 encode it the result is highly undesirable: `XXFUCKER000`.
 Normal base32 has similar issues, but without both letter cases.
 - Encoding into hexadecimal representation is mostly acceptable. Some undesired values: `B00B5`, `DEAD`, `FACE`, etc.
 One could argue that these are not very bad... maybe childish, but certainly not "professional".

I'll leave even worse randomly translated words up to imagination. The point is that immutable database IDs for a
business account **mustn't** have such handles.

## How?
I could not find many detailed sources/references on how to construct a suitable alphabet. After
gathering some information from the internet, some good ideas were presented and those were combined:
 - Avoid vowels. This greatly limits random word creation. There are less vowels than consonants so excluding the
 smaller group leaves us more to work with.
 - Avoid visually similar characters: `5Ss`, `i1Il`, `o0O`, etc. (depends on font, but generally true)
 - Trim further letters in order of their frequency in the language (english).

I've started out with the base64 alphabet and reduced it. To make processing easy I wished to use a base that is a
power of 2. Thankfully trimming half of the base64 alphabet seemed to be just about optimal. A base16 alphabet would
not yield meaningful benefits.

The safe_radix32 alphabet is `2346789BCFGJKLMPQVWZbcfgjkmpqvwz` which was generated by the script at `tools/alphabet.py`.

## Implementation
There is a Cython extension implementation with *good* performance and a pure python fallback module for compatibility.

# Install
A source distribution is available on PyPI:

```console
$ python -m pip install safe_radix32
```

Python 3.6+ and PyPy3 are supported.

# Usage

```pycon
>>> import safe_radix32
>>> safe_radix32.encode(1234567890987654321)
'34CQQwWjfjB8V'
>>> safe_radix32.decode(_)
1234567890987654321
```

# Security
Encoding and decoding will raise `OverflowException` if the value cannot be faithfully represented in a C long.

Decoding a string will also raise `OverflowException` if an invalid character is found. If the input is badly
formatted or invalid `UnicodeError` will be raised.

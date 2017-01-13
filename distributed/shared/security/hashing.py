__author__ = 'civa'

import hashlib
import hmac
import pbkdf2
from struct import Struct
from os import urandom
from operator import xor
from base64 import b64encode, b64decode
from itertools import izip, starmap
import jwt
from datetime import datetime, timedelta

_pack_int = Struct('>I').pack

SALT_LENGTH = 16
KEY_LENGTH = 20
HASH_FUNCTION = 'sha1'
NUM_OF_ITERATIONS = 10000

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20

def make_hash(password, has_leading_signature):
    if isinstance(password, unicode):
        password = password.encode('utf-8')

    salt = b64encode(urandom(SALT_LENGTH))
    password_hash = b64encode(pbkdf2_bin(password, salt, NUM_OF_ITERATIONS, KEY_LENGTH, getattr(hashlib, HASH_FUNCTION)))

    if has_leading_signature:
        return 'PBKDF2${}${}${}${}'.format(
                                        HASH_FUNCTION,
                                        NUM_OF_ITERATIONS,
                                        salt,
                                        password_hash)
    else:
        return password_hash

def check_hash(password, existing_hash, has_leading_signature=False):
    salt = None
    key = None

    if isinstance(password, unicode):
        password = password.encode('utf-8')

    if has_leading_signature:
        algorithm, hash_function, num_of_iterations, salt, key = existing_hash.split('$')

        key = b64decode(key)
        supplied_pass_hash = pbkdf2_bin(password, salt, int(num_of_iterations), len(key), getattr(hashlib, hash_function))
    else:
        existing_hash = b64decode(existing_hash)
        key = existing_hash[SALT_LENGTH:]
        salt = existing_hash[:SALT_LENGTH]

        supplied_pass_hash =  pbkdf2_bin(password, salt, int(NUM_OF_ITERATIONS), len(key), getattr(hashlib, HASH_FUNCTION))

        if len(key) != len(supplied_pass_hash):
            return False

        diff = 0
        for char_a, char_b in izip(key, supplied_pass_hash):
            diff |= ord(char_a) ^ ord(char_b)
        return diff == 0

# From https://github.com/mitsuhiko/python-pbkdf2
def pbkdf2_hex(data, salt, iterations, keylen, hashfunc=None):
    """Like :func:`pbkdf2_bin` but returns a hex encoded string."""
    return pbkdf2_bin(data, salt, iterations, keylen, hashfunc).encode('hex')

# From https://github.com/mitsuhiko/python-pbkdf2
def pbkdf2_bin(data, salt, iterations, keylen, hashfunc=None):
    """Returns a binary digest for the PBKDF2 hash algorithm of `data`
    with the given `salt`.  It iterates `iterations` time and produces a
    key of `keylen` bytes.  By default SHA-1 is used as hash function,
    a different hashlib `hashfunc` can be provided.
    """
    hashfunc = hashfunc or hashlib.sha1
    mac = hmac.new(data, None, hashfunc)
    def _pseudorandom(x, mac=mac):
        h = mac.copy()
        h.update(x)
        return map(ord, h.digest())
    buf = []
    for block in xrange(1, -(-keylen // mac.digest_size) + 1):
        rv = u = _pseudorandom(salt + _pack_int(block))
        for i in xrange(iterations - 1):
            u = _pseudorandom(''.join(map(chr, u)))
            rv = starmap(xor, izip(rv, u))
        buf.extend(rv)
    return ''.join(map(chr, buf))[:keylen]

def create_user_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }

    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

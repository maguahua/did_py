from ring.utils import *


def sbmul(s):
    return multiply(G, s)


# 将一个二维仿射坐标点转换为三维扩展坐标点
def xform_affine_to_extended(pt):
    (x, y) = pt
    return x % q, y % q, 1, (x * y) % q  # (X,Y,Z,T)


def xform_extended_to_affine(pt):
    (x, y, z, _) = pt
    return (x * inv(z)) % q, (y * inv(z)) % q


def add_elements(pt1, pt2):
    (X1, Y1, Z1, T1) = pt1
    (X2, Y2, Z2, T2) = pt2
    A = ((Y1 - X1) * (Y2 - X2)) % q
    B = ((Y1 + X1) * (Y2 + X2)) % q
    C = T1 * (2 * d) * T2 % q
    D = Z1 * 2 * Z2 % q
    E = (B - A) % q
    F = (D - C) % q
    G = (D + C) % q
    H = (B + A) % q
    X3 = (E * F) % q
    Y3 = (G * H) % q
    T3 = (E * H) % q
    Z3 = (F * G) % q
    return X3, Y3, Z3, T3


def double_element(pt):
    (X1, Y1, Z1, _) = pt
    A = (X1 * X1)
    B = (Y1 * Y1)
    C = (2 * Z1 * Z1)
    D = (-A) % q
    J = (X1 + Y1) % q
    E = (J * J - A - B) % q
    G = (D + B) % q
    F = (G - C) % q
    H = (D - B) % q
    X3 = (E * F) % q
    Y3 = (G * H) % q
    Z3 = (F * G) % q
    T3 = (E * H) % q
    return X3, Y3, Z3, T3


def _add_elements_nonunfied(pt1, pt2):
    (X1, Y1, Z1, T1) = pt1
    (X2, Y2, Z2, T2) = pt2
    A = ((Y1 - X1) * (Y2 + X2)) % q
    B = ((Y1 + X1) * (Y2 - X2)) % q
    C = (Z1 * 2 * T2) % q
    D = (T1 * 2 * Z2) % q
    E = (D + C) % q
    F = (B - A) % q
    G = (B + A) % q
    H = (D - C) % q
    X3 = (E * F) % q
    Y3 = (G * H) % q
    Z3 = (F * G) % q
    T3 = (E * H) % q
    return X3, Y3, Z3, T3


def scalarmult_element(pt, n):
    assert n >= 0
    if n == 0:
        return xform_affine_to_extended((0, 1))
    _ = double_element(scalarmult_element(pt, n >> 1))
    return _add_elements_nonunfied(_, pt) if n & 1 else _


def add(P1, P2):
    pt1 = xform_affine_to_extended(P1)
    pt2 = xform_affine_to_extended(P2)
    rt = add_elements(pt1, pt2)
    r = xform_extended_to_affine(rt)
    return r


def multiply(p1, n):
    pt1 = xform_affine_to_extended(p1)
    rt = scalarmult_element(pt1, n)
    r = xform_extended_to_affine(rt)
    return r

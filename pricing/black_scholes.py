import math


def _d1_d2(S0, K, T, r, sigma):
    if S0 <= 0:
        raise ValueError("S0 doit être > 0")

    if K <= 0:
        raise ValueError("K doit être > 0")

    if T <= 0:
        raise ValueError("T doit être > 0")

    if sigma <= 0:
        raise ValueError("sigma doit être > 0")

    d1 = (
        math.log(S0 / K)
        + (r + 0.5 * sigma**2) * T
    ) / (sigma * math.sqrt(T))

    d2 = d1 - sigma * math.sqrt(T)

    return d1, d2


def normal_cdf(x):
    """
    Fonction de répartition de la loi normale standard.
    """
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def black_scholes_call(S0, K, T, r, sigma):
    """
    Prix d'un Call européen selon Black-Scholes.
    """

    d1, d2 = _d1_d2(S0, K, T, r, sigma)

    call = (
        S0 * normal_cdf(d1)
        - K * math.exp(-r * T) * normal_cdf(d2)
    )

    return call


def black_scholes_put(S0, K, T, r, sigma):
    """
    Prix d'un Put européen selon Black-Scholes.
    """

    d1, d2 = _d1_d2(S0, K, T, r, sigma)

    put = (
        K * math.exp(-r * T) * normal_cdf(-d2)
        - S0 * normal_cdf(-d1)
    )

    return put


def black_scholes_price(
    S0,
    K,
    T,
    r,
    sigma,
    option_type="call"
):
    """
    Fonction générale Black-Scholes.
    """

    option_type = option_type.lower()

    if option_type == "call":
        return black_scholes_call(S0, K, T, r, sigma)

    elif option_type == "put":
        return black_scholes_put(S0, K, T, r, sigma)

    else:
        raise ValueError("option_type doit être 'call' ou 'put'")
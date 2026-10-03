import time
import statistics


def measure_runtime(
    pricing_function,
    S0,
    K,
    T,
    r,
    sigma,
    N,
    option_type="call",
    exercise_type="european",
    repetitions=10
):
    """
    Mesure le temps d'exécution d'une méthode de pricing
    sur plusieurs répétitions.

    Retourne :
    - price : prix calculé
    - average_time : temps moyen d'exécution
    - median_time : temps médian d'exécution
    """

    if repetitions <= 0:
        raise ValueError("repetitions doit être > 0")

    times = []
    price = None

    for _ in range(repetitions):

        start = time.perf_counter()

        price = pricing_function(
            S0,
            K,
            T,
            r,
            sigma,
            N,
            option_type,
            exercise_type
        )

        elapsed_time = time.perf_counter() - start

        times.append(elapsed_time)

    average_time = statistics.mean(times)
    median_time = statistics.median(times)

    return {
        "price": price,
        "average_time": average_time,
        "median_time": median_time
    }
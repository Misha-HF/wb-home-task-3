import time
import multiprocessing

def worker(num, start, end, result=None):
    if result is None:
        result = []
    for i in range(start, end):
        if num % i == 0:
            result.append(i)
    return result

def factorize_sync(number):
    num_cores = 1  # Використовуємо лише одне ядро, оскільки це синхронна версія
    chunk_size = number // num_cores
    results = []

    for i in range(num_cores):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1 if i != num_cores - 1 else number + 1
        results.extend(worker(number, start, end))

    return sorted(results)

def factorize_parallel(number):
    num_cores = multiprocessing.cpu_count()
    chunk_size = number // num_cores
    manager = multiprocessing.Manager()
    result = manager.list()
    processes = []

    for i in range(num_cores):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1 if i != num_cores - 1 else number + 1
        p = multiprocessing.Process(target=worker, args=(number, start, end, result))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return sorted(result)

# Перевірка роботи функції
def factorize(*numbers):
    results_sync = []
    results_multiprocessing = []
    for number in numbers:
        results_sync.append(factorize_sync(number))
        results_multiprocessing.append(factorize_parallel(number))
    return results_sync, results_multiprocessing

if __name__ == "__main__":
    numbers = (128, 255, 99999, 10651060)

    # Вимірювання часу виконання синхронної версії
    start_time_sync = time.time()
    results_sync, results_multiprocessing = factorize(*numbers)
    end_time_sync = time.time()
    print("Час виконання синхронної версії: {:.4f} секунди".format(end_time_sync - start_time_sync))

    # Вимірювання часу виконання паралельної версії
    start_time_parallel = time.time()
    results_parallel = [factorize_parallel(n) for n in numbers]
    end_time_parallel = time.time()
    print("Час виконання паралельної версії: {:.4f} секунди".format(end_time_parallel - start_time_parallel))

    # Перевірка результатів
    for i, (sync_result, multiprocessing_result) in enumerate(zip(results_sync, results_multiprocessing)):
        assert sync_result == multiprocessing_result, f"Різниця в результатах для числа {numbers[i]}"


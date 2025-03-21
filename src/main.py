import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal, ROUND_CEILING

def parse_line(line):
    city, score = line.strip().split(';')
    return city, Decimal(score)

def process_chunk(chunk):
    city_stats = defaultdict(lambda: [Decimal('Infinity'), Decimal('0'), Decimal('-Infinity'), 0])
    for line in chunk:
        city, score = parse_line(line)
        city_stats[city][0] = min(city_stats[city][0], score)  # min
        city_stats[city][2] = max(city_stats[city][2], score)  # max
        city_stats[city][1] += score  # sum
        city_stats[city][3] += 1  # count
    return city_stats

def merge_results(results):
    final_stats = defaultdict(lambda: [Decimal('Infinity'), Decimal('0'), Decimal('-Infinity'), 0])
    for result in results:
        for city, (min_val, sum_val, max_val, count) in result.items():
            final_stats[city][0] = min(final_stats[city][0], min_val)
            final_stats[city][2] = max(final_stats[city][2], max_val)
            final_stats[city][1] += sum_val
            final_stats[city][3] += count
    return final_stats

def ieee_754_round(value):
    return value.quantize(Decimal('0.1'), rounding=ROUND_CEILING)

def main():
    with open("testcase.txt", "r") as f:
        lines = f.readlines()
    
    chunk_size = max(1, len(lines) // 8)
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_chunk, chunks))
    
    final_stats = merge_results(results)
    sorted_cities = sorted(final_stats.keys())
    
    with open("output.txt", "w") as f:
        for city in sorted_cities:
            min_val, sum_val, max_val, count = final_stats[city]
            mean_val = sum_val / count
            output = f"{city}={ieee_754_round(min_val)}/{ieee_754_round(mean_val)}/{ieee_754_round(max_val)}\n"
            f.write(output)

if __name__ == "__main__":
    main()

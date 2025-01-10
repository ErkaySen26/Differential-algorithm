import numpy as np
import random

# Generatör parametreleri: maliyet katsayıları, güç sınırları, yasak bölgeler
generators = [
    {"a": 0.007, "b": 7.0, "c": 240, "P_min": 100, "P_max": 500, "no_zones": [(210, 240), (350, 380)]},
    {"a": 0.0095, "b": 10.0, "c": 200, "P_min": 50, "P_max": 200, "no_zones": [(90, 110), (140, 160)]},
    {"a": 0.009, "b": 8.5, "c": 220, "P_min": 80, "P_max": 300, "no_zones": [(150, 170), (210, 240)]},
    {"a": 0.009, "b": 11.0, "c": 200, "P_min": 50, "P_max": 150, "no_zones": [(80, 90), (110, 120)]},
    {"a": 0.008, "b": 10.5, "c": 220, "P_min": 50, "P_max": 200, "no_zones": [(90, 110), (140, 150)]},
    {"a": 0.0075, "b": 12.0, "c": 190, "P_min": 50, "P_max": 120, "no_zones": []},
]

# Sistem parametreleri
total_demand = 1263  # MW
population_size = 25
max_generations = 300
F = 0.5  # Ölçekleme faktörü
CR = 0.8  # Çaprazlama oranı

def fitness_function(power_outputs):
    """Yakıt maliyet fonksiyonunu hesaplar ve toplam talebi karşılamazsa ceza ekler."""
    total_cost = 0
    total_power = np.sum(power_outputs)
    penalty = 0
    if abs(total_power - total_demand) > 1e-3:  # Küçük tolerans
        penalty = 1e6 * abs(total_power - total_demand)  # Büyük bir ceza

    for i, generator in enumerate(generators):
        P = power_outputs[i]
        total_cost += generator["a"] * P ** 2 + generator["b"] * P + generator["c"]
    return total_cost + penalty

def repair_solution(solution):
    """Çözümü sınırlar ve yasak bölgeler doğrultusunda düzeltir."""
    repaired_solution = []
    for i, P in enumerate(solution):
        P_min = generators[i]["P_min"]
        P_max = generators[i]["P_max"]
        no_zones = generators[i]["no_zones"]

        # Güç sınırlarını uygula
        if P < P_min:
            P = P_min
        elif P > P_max:
            P = P_max

        # Yasak bölgeleri kontrol et ve düzelt
        for zone in no_zones:
            if zone[0] <= P <= zone[1]:
                if P - zone[0] < zone[1] - P:
                    P = zone[0] - 1e-3  # Alt sınırın hemen altına taşı
                else:
                    P = zone[1] + 1e-3  # Üst sınırın hemen üstüne taşı

        repaired_solution.append(P)

    # Toplam gücü ayarla
    total_power = np.sum(repaired_solution)
    if abs(total_power - total_demand) > 1e-3:
        factor = total_demand / total_power
        repaired_solution = [max(min(P * factor, generators[i]["P_max"]), generators[i]["P_min"])
                              for i, P in enumerate(repaired_solution)]

    return np.array(repaired_solution)

def initialize_population():
    """Rastgele bir popülasyon başlatır ve toplam talebi karşılamayı sağlar."""
    population = []
    for _ in range(population_size):
        individual = []
        remaining_demand = total_demand
        for generator in generators:
            P_min = generator["P_min"]
            P_max = generator["P_max"]
            no_zones = generator["no_zones"]

            # Jeneratör için uygun bir değer seç
            while True:
                P = random.uniform(P_min, P_max)
                in_no_zone = any(zone[0] <= P <= zone[1] for zone in no_zones)
                if not in_no_zone:
                    break

            individual.append(P)
            remaining_demand -= P

        # Toplam talebi karşılamak için son jeneratörün gücünü ayarla
        adjustment = remaining_demand / len(generators)
        individual = [max(min(P + adjustment, generators[i]["P_max"]), generators[i]["P_min"])
                      for i, P in enumerate(individual)]

        population.append(np.array(individual))
    return population

def differential_evolution():
    """Diferansiyel Gelişim Algoritması."""
    # Popülasyonu başlat
    population = initialize_population()

    best_solution = None
    best_fitness = float("inf")

    for generation in range(max_generations):
        new_population = []

        for i in range(population_size):
            # Rastgele üç farklı birey seç
            indices = list(range(population_size))
            indices.remove(i)
            r1, r2, r3 = random.sample(indices, 3)

            # Mutasyon
            mutant = population[r1] + F * (population[r2] - population[r3])
            mutant = repair_solution(mutant)

            # Çaprazlama
            trial = []
            for j in range(len(mutant)):
                if random.random() < CR or j == random.randint(0, len(mutant) - 1):
                    trial.append(mutant[j])
                else:
                    trial.append(population[i][j])

            trial = repair_solution(np.array(trial))

            # Seçim
            trial_fitness = fitness_function(trial)
            target_fitness = fitness_function(population[i])
            if trial_fitness < target_fitness:
                new_population.append(trial)
                if trial_fitness < best_fitness:
                    best_solution = trial
                    best_fitness = trial_fitness
            else:
                new_population.append(population[i])

        population = new_population
        print(f"Generation {generation + 1}: Best Fitness = {best_fitness:.4f}")

    return best_solution, best_fitness

# Algoritmayı çalıştır
best_solution, best_fitness = differential_evolution()

# Sonuçları yazdır
print("Optimal Güç Dağılımı (MW):", best_solution)
print("Toplam Yakıt Maliyeti (R/h):", best_fitness)

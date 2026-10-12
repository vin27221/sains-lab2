"""Reusable science calculations and quiz content for SainsLab."""

from __future__ import annotations

import math
from typing import Any


PLANETS: tuple[dict[str, Any], ...] = (
    {"name": "Merkurius", "color": "#a8a29e", "distance_au": 0.39, "period_days": 88, "diameter_km": 4879, "fact": "Planet terkecil dan paling dekat dengan Matahari."},
    {"name": "Venus", "color": "#f2b66d", "distance_au": 0.72, "period_days": 225, "diameter_km": 12104, "fact": "Atmosfer tebalnya memerangkap panas; permukaannya paling panas."},
    {"name": "Bumi", "color": "#56a8ff", "distance_au": 1.00, "period_days": 365, "diameter_km": 12742, "fact": "Satu-satunya dunia yang diketahui mendukung kehidupan."},
    {"name": "Mars", "color": "#f07858", "distance_au": 1.52, "period_days": 687, "diameter_km": 6779, "fact": "Jejak air purba menjadikannya target eksplorasi robotik."},
    {"name": "Jupiter", "color": "#e7b17c", "distance_au": 5.20, "period_days": 4333, "diameter_km": 139820, "fact": "Planet terbesar; Bintik Merah Besar adalah badai raksasa."},
    {"name": "Saturnus", "color": "#e6d28d", "distance_au": 9.58, "period_days": 10759, "diameter_km": 116460, "fact": "Sistem cincinnya luas dan terutama tersusun atas es."},
    {"name": "Uranus", "color": "#78d5d1", "distance_au": 19.2, "period_days": 30687, "diameter_km": 50724, "fact": "Sumbu rotasinya sangat miring dibandingkan planet lain."},
    {"name": "Neptunus", "color": "#6584ff", "distance_au": 30.05, "period_days": 60190, "diameter_km": 49244, "fact": "Angin di atmosfernya dapat bertiup dengan kecepatan sangat tinggi."},
)


QUIZ: tuple[dict[str, Any], ...] = (
    {
        "question": "Sebuah benda bermassa 2 kg mengalami percepatan 3 m/s². Berapa gaya resultannya?",
        "options": ("2 N", "5 N", "6 N", "9 N"),
        "answer": 2,
        "explanation": "Hukum II Newton: F = m × a = 2 × 3 = 6 N.",
    },
    {
        "question": "Apa yang terjadi pada periode ayunan sederhana jika panjang tali diperbesar?",
        "options": ("Periode mengecil", "Periode membesar", "Periode tetap", "Ayunan berhenti"),
        "answer": 1,
        "explanation": "T = 2π√(L/g). Periode bertambah seiring akar panjang tali.",
    },
    {
        "question": "Planet manakah yang memiliki jarak rata-rata sekitar 1 AU dari Matahari?",
        "options": ("Venus", "Bumi", "Mars", "Jupiter"),
        "answer": 1,
        "explanation": "Satu satuan astronomi (AU) didefinisikan berdasarkan jarak rata-rata Bumi–Matahari.",
    },
    {
        "question": "Berapa energi kinetik benda 4 kg yang bergerak dengan kecepatan 3 m/s?",
        "options": ("6 J", "12 J", "18 J", "36 J"),
        "answer": 2,
        "explanation": "Eₖ = ½mv² = ½ × 4 × 3² = 18 J.",
    },
    {
        "question": "Dalam eksperimen ayunan, parameter apa yang tidak mengubah periode (untuk simpangan kecil)?",
        "options": ("Panjang tali", "Percepatan gravitasi", "Massa beban", "Tidak ada"),
        "answer": 2,
        "explanation": "Model T = 2π√(L/g) tidak memuat massa; ini dapat diuji dengan mengubah massa beban.",
    },
)


def free_fall_distance(time_seconds: float, gravity: float = 9.81) -> float:
    """Return distance fallen from rest in metres."""
    if time_seconds < 0:
        raise ValueError("Waktu tidak boleh negatif.")
    if gravity <= 0:
        raise ValueError("Gravitasi harus lebih besar dari nol.")
    return 0.5 * gravity * time_seconds**2


def calculate_formula(formula: str, first: float, second: float) -> float:
    """Calculate a two-input introductory science formula."""
    if first < 0 or second < 0:
        raise ValueError("Nilai masukan tidak boleh negatif.")

    if formula == "Gaya (F = m × a)":
        return first * second
    if formula == "Energi kinetik (Ek = ½ × m × v²)":
        return 0.5 * first * second**2
    if formula == "Kecepatan (v = s ÷ t)":
        if second == 0:
            raise ValueError("Waktu harus lebih besar dari nol.")
        return first / second
    if formula == "Berat (w = m × g)":
        return first * second
    if formula == "Hukum Ohm (V = I × R)":
        return first * second
    if formula == "Massa jenis (ρ = m ÷ V)":
        if second == 0:
            raise ValueError("Volume harus lebih besar dari nol.")
        return first / second
    raise ValueError(f"Rumus tidak dikenali: {formula}")


def pendulum_period(length_m: float, gravity: float = 9.81) -> float:
    """Return the small-angle period of a simple pendulum in seconds."""
    if length_m <= 0 or gravity <= 0:
        raise ValueError("Panjang dan gravitasi harus lebih besar dari nol.")
    return 2 * math.pi * math.sqrt(length_m / gravity)


def quiz_score(answers: list[int]) -> int:
    """Count correct answers; unanswered or out-of-range choices are incorrect."""
    return sum(
        index < len(QUIZ) and answer == QUIZ[index]["answer"]
        for index, answer in enumerate(answers)
    )

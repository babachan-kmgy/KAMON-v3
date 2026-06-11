import random

from locust import HttpUser, between, task

# Test scenarios dataset
SURNAMES = [
    "佐藤", "鈴木", "高橋", "田中", "渡辺", "伊藤", "山本", "中村", "小林", "加藤",
    "髙橋", "嶋田", "﨑山", "邉見", "𠮷田", # variants
]

ROMAJI_SURNAMES = [
    "sato", "suzuki", "takahashi", "tanaka", "watanabe", "ito", "yamamoto",
    "nakamura", "kobayashi", "kato"
]

class KamonApiUser(HttpUser):
    # Simulated wait time between requests (0.2s to 1.0s)
    wait_time = between(0.2, 1.0)

    @task(1)
    def read_root(self):
        """Simulate a user accessing the API root endpoint."""
        self.client.get("/")

    @task(8)
    def search_surname_kanji(self):
        """Simulate a user searching for a surname using Kanji."""
        q = random.choice(SURNAMES)
        self.client.get(f"/search?q={q}", name="/search (kanji)")

    @task(4)
    def search_surname_romaji(self):
        """Simulate a user searching for a surname using Romaji."""
        q = random.choice(ROMAJI_SURNAMES)
        self.client.get(f"/search?q={q}", name="/search (romaji)")

    @task(3)
    def normalize_query(self):
        """Simulate a user normalizing a query via the /normalize endpoint."""
        q = random.choice(SURNAMES)
        self.client.get(f"/normalize?q={q}", name="/normalize")

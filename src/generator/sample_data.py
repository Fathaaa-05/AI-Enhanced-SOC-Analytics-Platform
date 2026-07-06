import random

USERS = [
    "admin",
    "john",
    "alice",
    "abdul",
    "emma",
    "michael",
    "david",
    "robert",
    "sarah",
    "james"
]

SOURCES = [
    "Windows",
    "Linux",
    "Firewall"
]

EVENT_TYPES = [
    "Login",
    "Network Traffic",
    "File Access"
]

LOGIN_STATUS = [
    "Successful Login",
    "Failed Login"
]

NETWORK_STATUS = [
    "ALLOW",
    "DENY"
]

SEVERITIES = [
    "Low",
    "Medium",
    "High"
]


def random_ip():
    return f"192.168.1.{random.randint(1,254)}"
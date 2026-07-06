from src.auth.auth_service import authenticate_user

print("===== VALID LOGIN =====")

result = authenticate_user("admin", "admin123")

print(result)

print()

print("===== INVALID LOGIN =====")

result = authenticate_user("admin", "wrongpassword")

print(result)
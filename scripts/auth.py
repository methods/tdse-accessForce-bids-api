import requests


def simulate_login(username):
    try:
        payload = {"username": username}
        response = requests.post("http://localhost:5000/authorise", json=payload)
        response.raise_for_status()  # Raise an exception for any HTTP errors

        token_data = response.json()
        token = token_data

        return token
    except requests.exceptions.RequestException as e:
        print("Request Error:", e)
        return None
    except ValueError as e:
        print("Value Error:", e)
        return None


def post_bid(jwt_token):
    try:
        tender = input("Enter the tender: ")
        client = input("Enter the client: ")
        bid_date = input("Enter the bid date (YYYY-MM-DD): ")
        bid_folder_url = input("Enter the bid folder URL(https://path-here): ")
        payload = {
            "tender": tender,
            "client": client,
            "bid_date": bid_date,
            "bid_folder_url": bid_folder_url,
        }
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.post(
            "http://localhost:8080/api/bids", json=payload, headers=headers
        )
        response.raise_for_status()  # Raise an exception for any HTTP errors

        data = response.json()
        print("Post Success (id):", data["_id"])
    except requests.exceptions.RequestException as e:
        print("Request Error:", e)
        return None


def delete_bid(jwt_token):
    try:
        bid_id = input("Enter the bid ID to delete: ")
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.delete(
            f"http://localhost:8080/api/bids/{bid_id}", headers=headers
        )
        response.raise_for_status()  # Raise an exception for any HTTP errors

        print(f"Bid with ID {bid_id} deleted successfully.")
    except requests.exceptions.RequestException as e:
        print("Request Error:", e)


def find_bid_by_id():
    try:
        API_KEY = input("Enter the API key (THIS_IS_THE_API_KEY): ")
        headers = {"X-API-Key": API_KEY}
        bid_id = input("Enter the bid ID to find: ")
        response = requests.get(
            f"http://localhost:8080/api/bids/{bid_id}", headers=headers
        )
        response.raise_for_status()  # Raise an exception for any HTTP errors

        bid_data = response.json()
        print("Bid Data:")
        print(bid_data)
    except requests.exceptions.RequestException as e:
        print("Request Error:", e)


def find_all_bids():
    try:
        API_KEY = input("Enter the API key (THIS_IS_THE_API_KEY): ")
        headers = {"X-API-Key": API_KEY}
        response = requests.get("http://localhost:8080/api/bids", headers=headers)
        response.raise_for_status()  # Raise an exception for any HTTP errors

        all_bids_data = response.json()
        print("All Bids Data:")
        print(all_bids_data)
    except requests.exceptions.RequestException as e:
        print("Request Error:", e)


def access_level(admin):
    admin_users = ["Julio", "Pira", "Nathan"]
    if admin in admin_users:
        print("You are an admin user.")
    else:
        print("You are not an admin user.")


def main():
    menu_choices = [
        "token",
        "post",
        "delete",
        "find id",
        "find all",
        "access level",
        "exit",
    ]
    username = input("Enter the username for login: ")
    jwt_token = simulate_login(username)
    while True:
        if jwt_token:
            print("Menu:")
            for i, choice in enumerate(menu_choices):
                print(f"{i + 1}. {choice}")
            choice = input("Enter your choice: ")
            if choice == "1":
                print("JWT Token:", jwt_token)
            elif choice == "2":
                post_bid(jwt_token)
            elif choice == "3":
                delete_bid(jwt_token)
            elif choice == "4":
                find_bid_by_id()
            elif choice == "5":
                find_all_bids()
            elif choice == "6":
                access_level(username)
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
        else:
            print("Login failed. Try again.")


if __name__ == "__main__":
    main()

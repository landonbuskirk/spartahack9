import requests

# The base URL of the FastAPI server
    # Replace with the actual server URL

# The 'message' to include in the URL path
message = "This is your message content."

# Construct the full URL with the message in the path
url = f"{base_url}/sendMessage/{message}"

try:
    # Send a POST request to the constructed URL
    response = requests.post(url)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        print("Success! Server Response:")
        print(response.json())
    elif response.status_code == 500:
        # Internal Server Error
        print("Internal Server Error:")
        print(response.text)
    else:
        # Handle other status codes if needed
        print(f"Error: Unexpected Status Code - {response.status_code}")
        print(response.text)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

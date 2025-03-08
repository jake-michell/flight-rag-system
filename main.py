from query_handler import process_response
import mdv
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    user_query = input("Enter your flight query: ")
    try:
        response = process_response(user_query)
        print(mdv.main(response))
    except Exception as e:
        print(f"An error has occured: {e}")

main()
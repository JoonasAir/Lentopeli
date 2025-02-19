import multiprocessing


print(1)
if __name__ == "__main__":
    print("Before Manager")
    try:
        print(2)
        manager = multiprocessing.Manager()
        print("Manager created successfully")
    except Exception as e:
        print(3)
        print(f"An error occurred: {e}")
    print("After Manager")
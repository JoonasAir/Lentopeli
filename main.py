from main_menu import main_menu
import cProfile




if __name__ == "__main__":
    # Generate the call tree starting from the main function
    # profiler = cProfile.Profile()
    # profiler.enable()

    main_menu()

    # profiler.disable()
    # profiler.dump_stats('my_program.prof')
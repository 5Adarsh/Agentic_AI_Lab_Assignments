    display_header(f"RUNNING {label}")

    try:
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(path.parent),
            check=False,
        )

        if result.returncode == 0:
            print("\n[COMPLETED] Program finished successfully.")
        else:
            print(f"\n[EXIT CODE {result.returncode}] Program finished with an error.")

    except KeyboardInterrupt:
        print("\n[STOPPED] Execution interrupted by user.")
    except OSError as error:
        print(f"\n[ERROR] Unable to start program: {error}")


def show_assignment_question(directory, assignment_number):
    """Display the Markdown question for an assignment."""
    question_path = (
        directory
        / f"Assignment_{assignment_number}"
        / "ASSIGNMENT_QUESTION.md"
    )

    display_header(f"ASSIGNMENT {assignment_number} QUESTION")

    if not question_path.is_file():
        print("Assignment question file not found.")
    else:
        try:
            print(question_path.read_text(encoding="utf-8"))
        except OSError as error:
            print(f"Unable to read question file: {error}")

    print("=" * 70)


def pause():
    input("\nPress Enter to continue...")


def week_menu(number, title):
    """Display the menu for a selected week."""
    directory = week_dir(number, title)

    while True:
        display_header(f"WEEK {number}: {title.upper()}")
        print("1. Run main lab program")
        print("2. Run Assignment 1")
        print("3. Run Assignment 2")
        print("4. View Assignment 1 question")
        print("5. View Assignment 2 question")
        print("0. Back to week selection")

        choice = input("\nChoose an option: ").strip()

        if choice == "0":
            return
        elif choice == "1":
            run_program(directory / "main.py", f"Week {number} Main Lab")
        elif choice == "2":
            run_program(
                directory / "Assignment_1" / "main.py",
                f"Week {number} Assignment 1",
            )
        elif choice == "3":
            run_program(
                directory / "Assignment_2" / "main.py",
                f"Week {number} Assignment 2",
            )
        elif choice == "4":
            show_assignment_question(directory, 1)
        elif choice == "5":
            show_assignment_question(directory, 2)
        else:
            print("\n[INVALID] Choose an option from 0 to 5.")

        pause()


def main():
    """Display the 14-week master menu."""
    while True:
        display_header("AGENTIC AI SYSTEMS — MASTER LAB CONSOLE")

        for number, title in WEEKS:
            print(f"{number:02d}. Week {number}: {title}")

        print("\n0. Exit")

        choice = input("\nEnter week number (0-14): ").strip()

        if choice == "0":
            print("\nGoodbye!")
            return

        try:
            week_number = int(choice)
        except ValueError:
            print("\n[INVALID] Enter a valid number.")
            continue

        selected_week = next(
            (week for week in WEEKS if week[0] == week_number),
            None,
        )

        if selected_week is None:
            print("\n[INVALID] Choose a week from 1 to 14, or 0 to exit.")
            continue

        week_menu(*selected_week)


if __name__ == "__main__":
    main()
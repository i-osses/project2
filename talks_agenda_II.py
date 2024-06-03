import csv
import sys
from datetime import datetime

TALKS = "talks.csv"
AGENDA = "agenda.csv"


def main():
    while True:
        print("-" * 30)
        print("Main Menu For Talks Assignments")
        print("-" * 30)
        print("1. Assign talks")
        print("2. Edit talks")
        print("3. List and count talks")
        print("4. Calculate talks per member")
        print("5. Exit")
        option = input("Select an option: ")

        if option.isdigit():
            option = int(option)
        else:
            print("Please enter a valid number.")
            continue

        if option == 1:
            handle_assign_talk()
        elif option == 2:
            handle_edit_talk()
        elif option == 3:
            handle_list_talks()
        elif option == 4:
            calculate_talks_per_member()
        elif option == 5:
            print("Thanks for using this program")
            sys.exit()
        else:
            print("Invalid option. Please try again.")


def handle_assign_talk():
    name = input("Search by first name or last name: ").strip()
    while not name:
        print("Please type a name.")
        name = input("Search by first name or last name: ").strip()

    selected_member = search_individual(AGENDA, name)
    if selected_member:
        assign_talk(selected_member)
    else:
        print("No member selected.")


def handle_list_talks():
    name = input("Search by first name or last name: ").strip()
    while not name:
        print("Please type a name.")
        name = input("Search by first name or last name: ").strip()

    selected_member = search_individual(AGENDA, name)
    if selected_member:
        list_assigned_talks(TALKS, selected_member)


def read_file(file_path):
    with open(file_path, "rt", encoding="utf-8") as csv_file:
        dictionary = []
        reader = csv.reader(csv_file)
        header = next(reader)
        for row in reader:
            dictionary.append(row)
        return dictionary, header


def write_file(file_path, row_data):
    with open(file_path, "a", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row_data)


def overwrite_file(file_path, header, data):
    with open(file_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)


def search_individual(file_path, name):
    dictionary, _ = read_file(file_path)
    occurrences = [
        row[0]
        for row in dictionary
        if any(name.lower() in part.lower() for part in row[0].split())
    ]

    if not occurrences:
        print("\nNo matches found\n")
        return

    print("\nMatches Found\n")
    for index, member in enumerate(occurrences, start=1):
        print(f"{index}: {member}")

    selection = input("\nSelect the number of the member: ")
    if selection.isdigit():
        selection = int(selection)
        if 1 <= selection <= len(occurrences):
            selected_member = occurrences[selection - 1]
            print(f"Selected Member: {selected_member}")
            return selected_member
        else:
            print("Invalid selection.")
    else:
        print("Please enter a valid number.")


def assign_talk(selected_member):
    talk = input("Enter the talk assignment: ").strip()
    date = input("Enter the date of the talk (YYYY-MM-DD): ").strip()
    saved_data_date = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    new_row = [selected_member, talk, date, saved_data_date]
    print(f"\nTalk '{talk}' on '{date}' has been assigned to {selected_member}\n")
    write_file(TALKS, new_row)


def list_assigned_talks(file_path, name):
    dictionary, header = read_file(file_path)
    occurrences = [row for row in dictionary if name.lower() in row[0].lower()]

    if not occurrences:
        print("\nNo matches found\n")
        return

    print("\nMatches Found\n")
    for index, row in enumerate(occurrences, start=1):
        print(f"{index}: {row}")

    main()


def handle_edit_talk():
    name = input("Search by first name or last name to edit talks: ").strip()
    while not name:
        print("Please type a name.")
        name = input("Search by first name or last name: ").strip()

    edit_talk(TALKS, name)


def edit_talk(file_path, search_name):
    data, header = read_file(file_path)
    occurrences = [
        row
        for row in data
        if any(search_name.lower() in part.lower() for part in row[0].split())
    ]

    if not occurrences:
        print("\nNo matches found\n")
        return

    print("\nMatches Found\n")
    for index, row in enumerate(occurrences, start=1):
        print(f"{index}: {row}")

    selection = input("\nSelect the number of the talk to edit: ")
    if selection.isdigit():
        selection = int(selection)
        if 1 <= selection <= len(occurrences):
            selected_row = occurrences[selection - 1]
            print(f"Selected Row: {selected_row}")

            # Get the index of the selected row in the original data
            original_index = data.index(selected_row)

            # Input new data
            new_name = (
                input(
                    f"Enter new name (or press Enter to keep '{selected_row[0]}'): "
                ).strip()
                or selected_row[0]
            )
            new_talk = (
                input(
                    f"Enter new talk (or press Enter to keep '{selected_row[1]}'): "
                ).strip()
                or selected_row[1]
            )
            new_date = (
                input(
                    f"Enter new date (or press Enter to keep '{selected_row[2]}'): "
                ).strip()
                or selected_row[2]
            )
            saved_data_date = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

            # Update the row
            data[original_index] = [new_name, new_talk, new_date, saved_data_date]

            # Write updated data to the file
            overwrite_file(file_path, header, data)

            print(f"\nData updated for {new_name}\n")
        else:
            print("Invalid selection.")
    else:
        print("Please enter a valid number.")


def calculate_talks_per_member():
    data, _ = read_file(TALKS)
    talks_count = {}
    for row in data:
        member_name = row[0]
        if member_name in talks_count:
            talks_count[member_name] += 1
        else:
            talks_count[member_name] = 1
    print(talks_count)
    return talks_count


if __name__ == "__main__":
    main()

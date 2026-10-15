"""
Author: Anthony Gollihar
Course: EE 21
"""

import csv
import math
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# FUNCTION: Get a positive number from the user
# ---------------------------------------------------------

def get_positive_number(prompt):

    while True:
        try:
            value = float(input(prompt))

            if value > 0:
                return value

            print("Please enter a number greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a number.")


# ---------------------------------------------------------
# FUNCTION: Get circuit type
# ---------------------------------------------------------

def get_circuit_type():


    while True:

        print("\nChoose the circuit type:")
        print("1. Series")
        print("2. Parallel")

        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            return "series"

        elif choice == "2":
            return "parallel"

        else:
            print("Invalid choice. Please enter 1 or 2.")


# ---------------------------------------------------------
# FUNCTION: Enter resistor values manually
# ---------------------------------------------------------

def enter_resistors():

    resistors = []

    while True:
        try:
            number = int(input("\nHow many resistors are in the circuit? "))

            if number >= 2:
                break

            print("Please enter at least 2 resistors.")

        except ValueError:
            print("Please enter a whole number.")
    for i in range(number):

        resistance = get_positive_number(
            f"Enter the resistance of R{i + 1} in ohms: "
        )

        resistor = {
            "name": f"R{i + 1}",
            "resistance": resistance
        }

        resistors.append(resistor)

    return resistors



# FUNCTION: Calculate equivalent resistance


def calculate_equivalent_resistance(resistors, circuit_type):

    if circuit_type == "series":

        equivalent = 0

        for resistor in resistors:
            equivalent += resistor["resistance"]

        return equivalent

    elif circuit_type == "parallel":

        inverse_total = 0

        for resistor in resistors:
            inverse_total += 1 / resistor["resistance"]

        return 1 / inverse_total

    return 0

# FUNCTION: Calculate circuit results

def calculate_results(resistors, circuit_type, source_voltage):

    equivalent_resistance = calculate_equivalent_resistance(
        resistors,
        circuit_type
    )

    total_current = source_voltage / equivalent_resistance

    for resistor in resistors:

        resistance = resistor["resistance"]

        if circuit_type == "series":

            current = total_current

            voltage = current * resistance

        elif circuit_type == "parallel":

            voltage = source_voltage

            current = voltage / resistance

        else:
            voltage = 0
            current = 0

        power = voltage * current

        resistor["voltage"] = voltage
        resistor["current"] = current
        resistor["power"] = power

    return equivalent_resistance, total_current


# FUNCTION: Display results
def display_results(
        resistors,
        circuit_type,
        source_voltage,
        equivalent_resistance,
        total_current):

    print("\n")
    print("=" * 70)
    print("              RESISTOR NETWORK ANALYSIS")
    print("=" * 70)

    print(f"Circuit type:          {circuit_type.capitalize()}")
    print(f"Source voltage:        {source_voltage:.2f} V")
    print(f"Equivalent resistance: {equivalent_resistance:.2f} ohms")
    print(f"Total current:         {total_current:.4f} A")

    print("-" * 70)

    print(
        f"{'Resistor':<12}"
        f"{'Resistance':<15}"
        f"{'Voltage':<15}"
        f"{'Current':<15}"
        f"{'Power':<15}"
    )

    print(
        f"{'':<12}"
        f"{'(ohms)':<15}"
        f"{'(V)':<15}"
        f"{'(A)':<15}"
        f"{'(W)':<15}"
    )

    print("-" * 70)

    for resistor in resistors:

        print(
            f"{resistor['name']:<12}"
            f"{resistor['resistance']:<15.2f}"
            f"{resistor['voltage']:<15.4f}"
            f"{resistor['current']:<15.4f}"
            f"{resistor['power']:<15.4f}"
        )

    print("=" * 70)

# FUNCTION: Save results to CSV


def save_results(
        resistors,
        circuit_type,
        source_voltage,
        equivalent_resistance,
        total_current):

    filename = input(
        "\nEnter a filename for the results "
        "(example: results.csv): "
    )

    if not filename.lower().endswith(".csv"):
        filename += ".csv"

    try:

        with open(filename, "w", newline="") as file:

            writer = csv.writer(file)

            # Write circuit information
            writer.writerow(["Circuit Type", circuit_type])
            writer.writerow(["Source Voltage (V)", source_voltage])
            writer.writerow(
                ["Equivalent Resistance (ohms)", equivalent_resistance]
            )
            writer.writerow(["Total Current (A)", total_current])

            writer.writerow([])

            # Write columns
            writer.writerow([
                "Resistor",
                "Resistance (ohms)",
                "Voltage (V)",
                "Current (A)",
                "Power (W)"
            ])

            # Write each resistor
            for resistor in resistors:

                writer.writerow([
                    resistor["name"],
                    resistor["resistance"],
                    resistor["voltage"],
                    resistor["current"],
                    resistor["power"]
                ])

        print(f"\nResults successfully saved to {filename}")

    except OSError:
        print("\nError: Could not save the file.")



# FUNCTION: values from CSV


def load_resistors_from_csv():

    filename = input(
        "\nEnter the CSV filename containing the resistors: "
    )

    resistors = []

    try:

        with open(filename, "r", newline="") as file:

            reader = csv.reader(file)

            header_found = False

            for row in reader:

                # Skip empty rows
                if not row:
                    continue

                # Find the resistor data header. This works for both
                # the simple input file and the results file created
                # by this program.
                if (
                    len(row) >= 2
                    and row[0].strip().lower() == "resistor"
                    and row[1].strip().lower() in
                    ["resistance", "resistance (ohms)"]
                ):
                    header_found = True
                    continue

                # Ignore everything before the resistor header.
                if not header_found:
                    continue

                # Stop if there is not enough data in the row.
                if len(row) < 2:
                    continue

                name = row[0].strip()

                try:
                    resistance = float(row[1])

                except ValueError:
                    # Ignore rows that are not resistor data.
                    continue

                if name and resistance > 0:

                    resistor = {
                        "name": name,
                        "resistance": resistance
                    }

                    resistors.append(resistor)

        if len(resistors) < 2:

            print(
                "\nThe file must contain at least "
                "2 valid resistors."
            )

            print(
                "The program can read both a simple resistor "
                "CSV and a results CSV produced by this program."
            )

            return None

        print(
            f"\nSuccessfully loaded {len(resistors)} resistors."
        )

        return resistors

    except FileNotFoundError:

        print("\nError: File could not be found.")
        return None

    except OSError:

        print("\nError: Could not read the file.")
        return None

# FUNCTION: Create graph

def create_graph(resistors, circuit_type):

    print("\nChoose what you want to graph:")
    print("1. Resistance")
    print("2. Voltage")
    print("3. Current")
    print("4. Power")

    while True:

        choice = input("Enter your choice (1-4): ")

        if choice in ["1", "2", "3", "4"]:
            break

        print("Please enter a number from 1 to 4.")

    names = [resistor["name"] for resistor in resistors]

    if choice == "1":

        values = [
            resistor["resistance"]
            for resistor in resistors
        ]

        title = "Resistance of Each Resistor"
        ylabel = "Resistance (ohms)"

    elif choice == "2":

        values = [
            resistor["voltage"]
            for resistor in resistors
        ]

        title = "Voltage Across Each Resistor"
        ylabel = "Voltage (V)"

    elif choice == "3":

        values = [
            resistor["current"]
            for resistor in resistors
        ]

        title = "Current Through Each Resistor"
        ylabel = "Current (A)"

    else:

        values = [
            resistor["power"]
            for resistor in resistors
        ]

        title = "Power Dissipated by Each Resistor"
        ylabel = "Power (W)"

    # Create the graph
    plt.figure(figsize=(9, 6))

    plt.bar(names, values)

    plt.title(
        f"{title} - {circuit_type.capitalize()} Circuit"
    )

    plt.xlabel("Resistor")
    plt.ylabel(ylabel)

    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.show()



# FUNCTION: Run a new analysis


def run_analysis(resistors):

    circuit_type = get_circuit_type()

    source_voltage = get_positive_number(
        "\nEnter the source voltage in volts: "
    )

    equivalent_resistance, total_current = calculate_results(
        resistors,
        circuit_type,
        source_voltage
    )

    display_results(
        resistors,
        circuit_type,
        source_voltage,
        equivalent_resistance,
        total_current
    )

    return (
        resistors,
        circuit_type,
        source_voltage,
        equivalent_resistance,
        total_current
    )



# MAIN PROGRAM

def main():

    print("\n")
    print("=" * 60)
    print("          RESISTOR NETWORK ANALYZER")
    print("=" * 60)

    # Store the most recent analysis
    analysis = None

    while True:

        print("\nMain Menu")
        print("-" * 30)

        print("1. Enter resistors manually")
        print("2. Load resistors from CSV")
        print("3. Save current results")
        print("4. Create a graph")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        # OPTION 1: Manual resistor entry

        if choice == "1":

            resistors = enter_resistors()

            analysis = run_analysis(resistors)


        # OPTION 2: Load CSV

        elif choice == "2":

            resistors = load_resistors_from_csv()

            if resistors is not None:

                analysis = run_analysis(resistors)

        # OPTION 3: Save results


        elif choice == "3":

            if analysis is None:

                print(
                    "\nThere are no analysis results to save."
                )

                print(
                    "Please analyze a circuit first."
                )

            else:

                (
                    resistors,
                    circuit_type,
                    source_voltage,
                    equivalent_resistance,
                    total_current
                ) = analysis

                save_results(
                    resistors,
                    circuit_type,
                    source_voltage,
                    equivalent_resistance,
                    total_current
                )

        # OPTION 4: Create graph
        elif choice == "4":

            if analysis is None:

                print(
                    "\nThere are no analysis results to graph."
                )

                print(
                    "Please analyze a circuit first."
                )

            else:

                resistors = analysis[0]
                circuit_type = analysis[1]

                create_graph(
                    resistors,
                    circuit_type
                )


        # OPTION 5: Exit

        elif choice == "5":

            print("\nThank you for using the Resistor Network Analyzer!")
            print("Goodbye.")

            break

        # INVALID MENU OPTION
        else:

            print(
                "\nInvalid choice. "
                "Please select an option from 1 to 5."
            )


# Start the program

if __name__ == "__main__":
    main()
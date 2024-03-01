from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Define route to clear previous data from data.txt
def clear_data_file():
    if os.path.exists("data.txt"):
        with open("data.txt", "w") as file:
            file.write("")  # Clear the file

# Define the function to calculate health percentage
def calculate_health_percentage_from_file(file_path):
     # Initialize variables to store extracted data
    smoke = None
    chain_smoker = None
    cigarettes_per_day = None
    hours_of_sleep = None
    exercise_weekly = None
    fruits_veggies = None
    sugary_beverages = None
    processed_foods = None
    stress_level = None
    stress_relief_techniques = None
    mental_health_checkups = None
    water_glasses = None
    caffeinated_beverages = None
    dehydration_symptoms = None
    screen_time_hours = None
    screen_time_digital_detox = None
    screen_time_eye_strain = None

    # Read data from the file and extract relevant information
    with open(file_path, 'r') as file:
        for line in file:
            key, value = map(str.strip, line.split(':', 1))
            if key == 'Do you smoke?':
                smoke = value
            elif key == 'Are you a chain smoker?':
                chain_smoker = value
            elif key == 'How many cigarettes a day?':
                cigarettes_per_day = int(value) if value.isdigit() else 0
            elif key == 'How many hours do you sleep per night?':
                hours_of_sleep = int(value) if value.isdigit() else 0
            elif key == 'Do you exercise once a week?':
                exercise_weekly = value
            elif key == 'Do you eat fruits and vegetables daily?':
                fruits_veggies = value
            elif key == 'How often do you consume sugary beverages?':
                sugary_beverages = value
            elif key == 'Do you consume processed foods regularly?':
                processed_foods = value
            elif key == 'How would you rate your stress level on a scale from 1 to 10?':
                stress_level = int(value) if value.isdigit() else 0
            elif key == 'Do you practice stress-relief techniques such as meditation or deep breathing?':
                stress_relief_techniques = value
            elif key == 'Do you get regular mental health check-ups?':
                mental_health_checkups = value
            elif key == 'How many glasses of water do you drink per day?':
                water_glasses = int(value) if value.isdigit() else 0
            elif key == 'Do you consume caffeinated beverages regularly?':
                caffeinated_beverages = value
            elif key == 'Do you experience symptoms of dehydration?':
                dehydration_symptoms = value
            elif key == 'How many hours per day do you spend in from of screens?':
                screen_time_hours = int(value) if value.isdigit() else None
            elif key == 'Do you practice digital detox or screen-free time regularly?':
                screen_time_digital_detox = value
            elif key == 'Do you experience eye strain or headaches due to excessive screen time?':
                screen_time_eye_strain = value

    # Calculate health percentage based on the extracted information
    health_percentage = 100

    # Adjust health percentage based on various factors
    
    # Calculate health points based on smoking habits
    if smoke == 'Yes':
        health_percentage -= 3.5
        if chain_smoker == 'Yes':
            health_percentage -= 2.11 * cigarettes_per_day

    # Calculate health points based on sleep duration
    if hours_of_sleep is not None and hours_of_sleep < 6:
        health_percentage -= (6 - hours_of_sleep) * 1.5

    # Calculate health points based on exercise habits
    if exercise_weekly == 'No':
        health_percentage -= 0.5

    # Calculate health points based on dietary habits
    if fruits_veggies == 'No':
        health_percentage -= 3.22
    if sugary_beverages == 'Occasionally':
        health_percentage -= 1.8
    elif sugary_beverages == 'Frequently':
        health_percentage -= 2.88
    if processed_foods == 'Yes':
        health_percentage -= 5

    # Calculate health points based on stress level
    if stress_level is not None:
        if stress_level >= 1 and stress_level <= 5:
            health_percentage -= 0
        elif stress_level >= 6 and stress_level <= 10:
            health_percentage -= (stress_level - 5) * 0.9

    # Calculate health points based on stress-relief techniques
    if stress_relief_techniques == 'No':
        health_percentage -= 2

    # Calculate health points based on regular mental health check-ups
    if mental_health_checkups == 'No':
        health_percentage -= 0.3

    # Calculate health points based on water consumption
    if water_glasses is not None and water_glasses < 4:
        health_percentage -= 2

    # Calculate health points based on consumption of caffeinated beverages
    if caffeinated_beverages == 'No':
        health_percentage -= 0.3

    # Calculate health points based on symptoms of dehydration
    if dehydration_symptoms == 'Yes':
        health_percentage -= 3

    # Adjust health percentage based on screen time
    if screen_time_hours is not None and screen_time_hours > 6:
        health_percentage -= 4

    if screen_time_digital_detox == 'No':
        health_percentage -= 3

    if screen_time_eye_strain == 'Yes':
        health_percentage -= 3

    return health_percentage

# Define the function to calculate health percentage and write it to the result file
def calculate_and_write_health_percentage(health_percentage, data):
    with open("result.txt", "w") as file:
        file.write(f"Health Percentage: {health_percentage}\n")
        file.write("Calculation Details:\n")
        for line in data:
            file.write(line)

# Define routes for each question thread

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/smoking')
def smoking():
    return render_template('smoking.html')

@app.route('/sleeping')
def sleeping():
    return render_template('sleeping.html')

@app.route('/exercise')
def exercise():
    return render_template('exercise.html')

@app.route('/dietary_habits')
def dietary_habits():
    return render_template('dietary_habits.html')

@app.route('/process_stress_and_mental_health')
def stress_and_mental_health():
    return render_template('stress_and_mental_health.html')

@app.route('/process_hydration')
def hydration():
    return render_template('hydration.html')

@app.route('/process_screen_time')
def screen_time():
    return render_template('screen_time.html')
# Define routes for processing user answers

@app.route('/process_smoking', methods=['POST'])
def process_smoking():
    smoke = request.form['smoke']
    with open("data.txt", "a") as file:
        file.write(f"Do you smoke?: {smoke}\n")
        if smoke == 'Yes':
            chain_smoker = request.form['chain_smoker']
            file.write(f"Are you a chain smoker?: {chain_smoker}\n")
            if chain_smoker == 'Yes':
                cigarettes_per_day = request.form.get('cigarettes_per_day', '')
                if cigarettes_per_day:
                    file.write(f"How many cigarettes a day?: {cigarettes_per_day}\n")
            # If not a chain smoker, move to the next question
            else:
                return redirect(url_for('sleeping'))
    # Calculate health percentage after processing smoking data
    health_percentage = calculate_health_percentage_from_file("data.txt")
    # Write the health percentage to the result file
    with open("data.txt", "r") as file:
        data = file.readlines()
    calculate_and_write_health_percentage(health_percentage, data)
    return redirect(url_for('sleeping'))

@app.route('/process_sleeping', methods=['POST'])
def process_sleeping():
    hours_of_sleep_str = request.form['hours_of_sleep']
    if hours_of_sleep_str.isdigit():  # Check if the input is a valid integer
        hours_of_sleep = int(hours_of_sleep_str)
        with open("data.txt", "a") as file:
            file.write(f"How many hours do you sleep per night?: {hours_of_sleep}\n")
            if hours_of_sleep < 6:
                cover_sleeps = request.form['cover_sleeps']
                file.write(f"Do you cover up your sleeps at day?: {cover_sleeps}\n")
        # Calculate health percentage after processing sleeping data
        health_percentage = calculate_health_percentage_from_file("data.txt")
        # Write the health percentage to the result file
        with open("data.txt", "r") as file:
            data = file.readlines()
        calculate_and_write_health_percentage(health_percentage, data)
        return redirect(url_for('exercise'))
    else:
        # Handle the case where hours_of_sleep is not a valid integer
        # You may want to display an error message or redirect the user back to the form
        pass

@app.route('/process_exercise', methods=['POST'])
def process_exercise():
    exercise_weekly = request.form['exercise_weekly']
    with open("data.txt", "a") as file:
        file.write(f"Do you exercise once a week?: {exercise_weekly}\n")
    # Read the content of the data.txt file
    with open("data.txt", "r") as file:
        data = file.readlines()
    # Calculate health percentage after processing exercise data
    health_percentage = calculate_health_percentage_from_file("data.txt")
    # Write the health percentage and calculation details to the result file
    calculate_and_write_health_percentage(health_percentage, data)
    return redirect(url_for('dietary_habits'))

@app.route('/process_dietary_habits', methods=['POST'])
def process_dietary_habits():
    fruits_veggies = request.form['fruits_veggies']
    sugary_beverages = request.form['sugary_beverages']
    processed_foods = request.form['processed_foods']
    with open("data.txt", "a") as file:
        file.write(f"Do you eat fruits and vegetables daily?: {fruits_veggies}\n")
        file.write(f"How often do you consume sugary beverages?: {sugary_beverages}\n")
        file.write(f"Do you consume processed foods regularly?: {processed_foods}\n")
    # Read the content of the data.txt file
    with open("data.txt", "r") as file:
        data = file.readlines()
    # Calculate health percentage after processing dietary habits data
    health_percentage = calculate_health_percentage_from_file("data.txt")
    # Write the health percentage and calculation details to the result file
    calculate_and_write_health_percentage(health_percentage, data)
    return redirect(url_for('process_stress_and_mental_health'))

@app.route('/process_stress_and_mental_health', methods=['POST'])
def process_stress_and_mental_health():
    # Extract stress and mental health information from the form submission
    stress_level = request.form.get('stress_level')
    stress_relief_techniques = request.form.get('stress_relief_techniques')
    mental_health_checkups = request.form.get('mental_health_checkups')
    
    # Write the stress and mental health information to the data file
    with open("data.txt", "a") as file:
        file.write(f"Stress level: {stress_level}\n")
        file.write(f"Do you practice stress-relief techniques?: {stress_relief_techniques}\n")
        file.write(f"Do you get regular mental health check-ups?: {mental_health_checkups}\n")

    # Calculate health percentage after processing stress and mental health data
    health_percentage = calculate_health_percentage_from_file("data.txt")
    
    # Write the health percentage and calculation details to the result file
    calculate_and_write_health_percentage(health_percentage, "data.txt")
    
    return redirect(url_for('process_hydration'))

@app.route('/process_hydration', methods=['POST'])
def process_hydration():
    # Extract hydration information from the form submission
    water_glasses = int(request.form.get('water_glasses'))
    caffeinated_beverages = request.form.get('caffeinated_beverages')
    dehydration_symptoms = request.form.get('dehydration_symptoms')

    # Write the hydration information to the data file
    with open("data.txt", "a") as file:
        file.write(f"How many glasses of water do you drink per day?: {water_glasses}\n")
        file.write(f"Do you consume caffeinated beverages regularly?: {caffeinated_beverages}\n")
        file.write(f"Do you experience symptoms of dehydration?: {dehydration_symptoms}\n")

    # Calculate health percentage based on the extracted information
    health_percentage = calculate_health_percentage_from_file("data.txt")

    # Write the health percentage and calculation details to the result file
    calculate_and_write_health_percentage(health_percentage, "data.txt")

    # Redirect to a success page or return a success message
    return redirect(url_for('process_screen_time'))

@app.route('/process_screen_time', methods=['POST'])
def process_screen_time():
    # Extract screen time information from the form submission
    screen_time_hours = int(request.form['hours_per_day'])
    screen_time_digital_detox = request.form['digital_detox']
    screen_time_eye_strain = request.form['eye_strain']

    # Write the screen time information to the data file
    with open("data.txt", "a") as file:
        file.write(f"How many hours per day do you spend in front of screens?: {screen_time_hours}\n")
        file.write(f"Do you practice digital detox or screen-free time regularly?: {screen_time_digital_detox}\n")
        file.write(f"Do you experience eye strain or headaches due to excessive screen time?: {screen_time_eye_strain}\n")

        health_percentage = calculate_health_percentage_from_file("data.txt")

    # Write the health percentage and calculation details to the result file
        calculate_and_write_health_percentage(health_percentage, "data.txt")

    # Redirect to a success page or return a success message
    return f"Data submitted successfully! Health Percentage: {health_percentage}"



clear_data_file()

if __name__ == '__main__':
    # Clear the data file when the application is first loaded
    clear_data_file()
    app.run(debug=True)

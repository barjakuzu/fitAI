import os
import openai
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# Set up the OpenAI API client
openai.api_key = "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"  # Replace with your actual API key

def post_process_workout_plan(workout_plan):
    lines = workout_plan.split('\n')
    processed_lines = []

    day = 1
    for line in lines:
        if 'Day' in line:
            processed_lines.append(f"Day {day}")
            day += 1
        else:
            parts = line.split(':')
            if len(parts) >= 3:
                exercise, sets, reps = parts
                sets, reps = sets.strip().split(' x ')
                processed_lines.append(f"-{exercise}: {sets} sets of {reps} reps")
            else:
                processed_lines.append(line)

    return '\n'.join(processed_lines)


def generate_workout_plan(age, height, weight, gender, body_type, workout_days):
    prompt = (f"Create a workout plan for a {age} year old, {height} cm tall, {weight} kg {gender} "
              f"with a {body_type} body type, who wants to work out {workout_days} days per week. "
              f"Please provide the plan with each day on a new line such as Day 1, Day2 and etc, each exercise formatted as "
              f"'-Exercise name: Sets x Reps such as 3 Sets x 12 Reps'.")

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    workout_plan = response.choices[0].text.strip()
    processed_workout_plan = post_process_workout_plan(workout_plan)

    return processed_workout_plan

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        gender = request.form['gender']
        body_type = request.form['body_type']
        workout_days = request.form['workout_days']

        # Generate workout plan
        workout_plan = generate_workout_plan(age, height, weight, gender, body_type, workout_days)

        return render_template('result.html', name=name, workout_plan=workout_plan)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)






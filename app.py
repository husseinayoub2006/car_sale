#missing marks: 
# #comments 10% - 
# commit save changes to github -5%-10%
# search 10%
# readme 15 % 
# simialrity 10% copy paste all files and codes inside a wordfile or pdf
import csv
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to load cars from the CSV file
def load_cars_from_csv():
    cars = []
    with open('cars.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['id'] = int(row['id'])  # Convert ID to integer
            row['price'] = int(row['price'])  # Convert price to integer
            cars.append(row)
    return cars

# Load cars into a global variable
cars = load_cars_from_csv()

# Route for the car list with search and sort functionality
@app.route("/", methods=["GET", "POST"])
def car_list():
    search_query = request.form.get("search_query", "").lower() if request.method == "POST" else ""
    sort_order = request.form.get("sort_order", "default")  # Get the sorting preference from the form

    # Filter cars based on search query
    filtered_cars = [car for car in cars if search_query in car["brand"].lower() or search_query in car["model"].lower()]

    # Sort cars by price based on the selected sort order
    if sort_order == "high_to_low":
        filtered_cars.sort(key=lambda x: x["price"], reverse=True)  # High to Low
    elif sort_order == "low_to_high":
        filtered_cars.sort(key=lambda x: x["price"])  # Low to High

    return render_template("car_list.html", cars=filtered_cars, search_query=search_query, sort_order=sort_order)

# Route for car details
@app.route("/car/<int:car_id>")
def car_detail(car_id):
    car = next((car for car in cars if car["id"] == car_id), None)
    if car:
        return render_template("car_detail.html", car=car)
    return "Car not found", 404

# Run the application
if __name__ == "__main__":
    app.run(debug=True)



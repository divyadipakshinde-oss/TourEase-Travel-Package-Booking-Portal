from flask import Flask, render_template, request, redirect, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key ="tourease_secret_key"

# Home page
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/my_bookings')
def my_bookings():

    email = session.get("email")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE email=?",
        (email,)
    )

    bookings = cursor.fetchall()

    conn.close()

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )
@app.route("/profile")
def profile():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users LIMIT 1")
    user = cursor.fetchone()

    conn.close()

    return render_template("profile.html", user=user)

@app.route("/admin")
def admin_dashboard():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM packages")
    total_packages = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM contact_messages")
    total_messages = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_bookings=total_bookings,
        total_packages=total_packages,
        total_messages=total_messages
    )


@app.route("/itinerary/<int:booking_id>")
def itinerary(booking_id):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE id=?",
        (booking_id,)
    )

    booking = cursor.fetchone()

    conn.close()

    return render_template(
        "itinerary.html",
        booking=booking
    )

@app.route("/invoice/<int:id>")
def invoice(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE id=?",
        (id,)
    )

    booking = cursor.fetchone()

    conn.close()

    return render_template(
        "invoice.html",
        booking=booking
    )

@app.route("/package_details/<int:id>")
def package_details(id):

    package_data = {

        1: {
            "name": "Goa Beach Tour",
            "image": "goa.jpg",
            "price": "₹14,999",
            "location": "Goa",
            "duration": "5 Days / 4 Nights"
        },

        2: {
            "name": "Manali Adventure",
            "image": "manali.jpg",
            "price": "₹18,999",
            "location": "Manali",
            "duration": "6 Days / 5 Nights"
        },

        3: {
            "name": "Kerala Backwaters",
            "image": "kerala.jpg",
            "price": "₹22,999",
            "location": "Kerala",
            "duration": "7 Days / 6 Nights"
        },

        4: {
            "name": "Kashmir Paradise",
            "image": "kashmir.jpg",
            "price": "₹24,999",
            "location": "Kashmir",
            "duration": "5 Days / 4 Nights"
        },

        5: {
            "name": "Dubai Luxury Tour",
            "image": "dubai.jpg",
            "price": "₹39,999",
            "location": "Dubai",
            "duration": "4 Days / 3 Nights"
        },

        6: {
            "name": "Bali",
            "image": "bali.jpg",
            "price": "₹49,999",
            "location": "Bali",
            "duration": "6 Days / 5 Nights"
        }
    }

    return render_template(
        "package_details.html",
        package=package_data[id]
    )

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"] 
       
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["email"] =email
            session["user_id"] =email
            flash("Login Sccessful!")
            return redirect("/my_bookings")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

@app.route('/logout')
def logout():
     session.clear()
     return redirect('/login')

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()
        flash("Registration Successful!")
        return redirect("/login")

    return render_template("register.html")
# Booking page
@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        package_name = request.form["package"]
        travel_date = request.form["travel_date"]
        travelers = request.form["travelers"] 
        message = request.form["message"] 

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO bookings (name, email, phone, package_name,travel_date,travelers,message) VALUES (?, ?, ?, ?,?,?,?)",
            (name, email, phone, package_name,travel_date,travelers,message)
        )

        conn.commit()
        conn.close()

        return redirect("/my_bookings")

    return render_template("booking.html")

###
@app.route('/manage_packages')
def manage_packages():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, package_name, price FROM packages")
    packages = cursor.fetchall()

    print(packages)

    conn.close()

    return render_template(
        'manage_packages.html',
        packages=packages
    )

@app.route('/manage_users')
def manage_users():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, role FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template(
        'manage_users.html',
        users=users
    )

@app.route("/packages")
def packages():
    search = request.args.get("search", "").lower()

    if search == "goa" or search == "goa beach tour":
        return redirect("/package_details/1")

    elif search == "manali" or search == "manali adventure":
        return redirect("/package_details/2")

    elif search == "kerala" or search == "kerala backwaters":
        return redirect("/package_details/3")

    elif search == "kashmir" or search == "kashmir paradise":
        return redirect("/package_details/4")

    elif search == "dubai" or search == "dubai luxury tour":
        return redirect("/package_details/5")

    elif search == "bali":
        return redirect("/package_details/6")

    return render_template("packages.html")

@app.route('/delete_user/<int:id>')
def delete_user(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/manage_users')


@app.route("/feedback", methods=["GET", "POST"])
def feedback():

    if request.method == "POST":

        customer_name = request.form["customer_name"]
        review = request.form["review"]
        rating = request.form["rating"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO testimonials
            (customer_name, review, rating)
            VALUES (?, ?, ?)
        """, (customer_name, review, rating))

        conn.commit()
        conn.close()

        flash("Feedback submitted successfully!")
        return redirect("/feedback")

    return render_template("feedback.html")

@app.route('/manage_bookings')
def manage_bookings():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    conn.close()

    return render_template(
        'manage_bookings.html',
        bookings=bookings
    )

@app.route('/delete_booking/<int:id>')
def delete_booking(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bookings WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/manage_bookings')

# Dashboard page
@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    conn.close()

    return render_template("dashboard.html", bookings=bookings)


if __name__ == "__main__":
    app.run(debug=True)
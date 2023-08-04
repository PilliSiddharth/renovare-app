import os
from flask import Flask, request, render_template, send_from_directory, render_template_string
from pip._vendor import cachecontrol
import mixpanel

mixpanel_token = "b525720c506fe413923068ed77f6c2fd"
mp = mixpanel.Mixpanel(mixpanel_token)

app = Flask("Renovare", template_folder='./templates', static_folder='./css')

# Dictionary to store the generated notes content
books = [
    {"id": 1, "title": "Wings of Fire", "price":"₹230.00", "description":"Wings of Fire is the powerful autobiography of Dr. A.P.J. Abdul Kalam, tracing his journey from humble beginnings to becoming India's 11th President.", "image": "https://upload.wikimedia.org/wikipedia/en/3/3a/Wings_of_Fire_by_A_P_J_Abdul_Kalam_Book_Cover.jpg"},
    {"id": 2, "title": "The Universe in a Nutshell", "price": "₹1134.99", "description": "The Universe in a Nutshell is a 2001 book about theoretical physics by Stephen Hawking.", "image": "https://m.media-amazon.com/images/I/81bKX7EA4cL._AC_UF1000,1000_QL80_.jpg"},
    # Add more books...
]
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, '/css/favicon/'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('landing2.html')

@app.route("/app", methods=['GET', 'POST'])
def app_page():
    return render_template('app.html', books=books)

@app.route("/about-us", methods=['GET', 'POST'])
def about_us():
    return render_template('about-us.html')

@app.route("/buy", methods=["POST"])
def buy():
    name = request.form.get("name")
    grade = request.form.get("grade")
    section = request.form.get("section")
    book_id = request.form.get("book_id")
    book_title = request.form.get("book_title")

    # Here you can process the data, e.g., add it to a list or save it to a database.
    # For simplicity, we'll just print it.
    print(f"Received order from {name} ({grade}): book {book_id}, shipping to {section}")

    event_name = 'User - Purchase Order'

    event_properties = {
        'User ID': name,
        'Order': {"Student_Name":name, "Student_Grade":grade, "Book_ID":book_id, "Section":section, "Book_Title":book_title}
    }

    # Send the event to Mixpanel
    mp.track(name, event_name, event_properties)
    return render_template("thank_you.html")

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if book is None:
        return "Book not found", 404
    return render_template('book_detail.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)

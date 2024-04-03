import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bolt",
    database="pro"
)

cursor = db.cursor()

# Function to handle user login
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the user exists in the database
    cursor.execute("SELECT * FROM User WHERE Username=%s AND Password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        open_main_window(user)  # Pass the 'user' information to open_main_window
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


# Function to handle user signup
def signup():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    # Check if the username already exists
    cursor.execute("SELECT * FROM User WHERE Username=%s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Signup Failed", "Username already exists. Please choose another username.")
    else:
        # Insert the new user into the database
        cursor.execute("INSERT INTO User (Username, Password, Email) VALUES (%s, %s, %s)", (username, password, email))
        db.commit()
        messagebox.showinfo("Signup Successful", "Account created successfully. You can now log in.")
        clear_entries()

# Function to open the main window after login/signup
def open_main_window(user):
    main_window = tk.Toplevel(root)
    main_window.title("Event Booking Platform")

    # Create buttons for main window
    your_bookings_btn = tk.Button(main_window, text="Your Bookings", command=lambda: show_bookings(user))
    your_bookings_btn.pack(pady=10)

    your_events_btn = tk.Button(main_window, text="Your Events", command=lambda: show_user_events(user))
    your_events_btn.pack(pady=10)

    create_event_btn = tk.Button(main_window, text="Create Your Event", command=lambda: create_event(user))
    create_event_btn.pack(pady=10)

    book_events_btn = tk.Button(main_window, text="Book Available Events", command=lambda: book_available_events(user))
    book_events_btn.pack(pady=10)

# Function to show user's bookings
def show_bookings(user):
    # Fetch user's bookings from the database
    cursor.execute("SELECT Event.EventName, Event.Date, Event.Time, Venue.VenueName, Booking.TicketCount, Booking.TotalAmount FROM Booking "
                   "JOIN Event ON Booking.EventID = Event.EventID "
                   "JOIN Venue ON Event.VenueID = Venue.VenueID "
                   "WHERE Booking.UserID = %s", (user[0],))
    bookings = cursor.fetchall()

    # Display bookings in a new window
    bookings_window = tk.Toplevel(root)
    bookings_window.title("Your Bookings")

    for booking in bookings:
        booking_label = tk.Label(bookings_window, text=f"Event: {booking[0]}, Date: {booking[1]}, Time: {booking[2]}, Venue: {booking[3]}, Ticket Count: {booking[4]}, Total Amount: ₹{booking[5]:.2f}")
        booking_label.pack(pady=5)

# Function to show events created by the user, including ticket price
def show_user_events(user):
    # Fetch user's events from the database
    cursor.execute("SELECT EventName, Date, Time, Venue.VenueName, CategoryName, Description, Price FROM Event "
                   "JOIN Venue ON Event.VenueID = Venue.VenueID "
                   "WHERE OrganizerUserID = %s", (user[0],))
    user_events = cursor.fetchall()

    # Display user's events in a new window
    user_events_window = tk.Toplevel(root)
    user_events_window.title("Your Events")

    for event in user_events:
        event_label = tk.Label(user_events_window, text=f"Event: {event[0]}, Date: {event[1]}, Time: {event[2]}, Venue: {event[3]}, Category: {event[4]}, Description: {event[5]}, Price: ₹{event[6]}")
        event_label.pack(pady=5)

# Function to create a new event, including ticket price
def create_event(user):
    create_event_window = tk.Toplevel(root)
    create_event_window.title("Create Your Event")

    # Create entry widgets for event details
    event_name_label = tk.Label(create_event_window, text="Event Name:")
    event_name_label.grid(row=0, column=0, pady=10)
    event_name_entry = tk.Entry(create_event_window)
    event_name_entry.grid(row=0, column=1, pady=10)

    date_label = tk.Label(create_event_window, text="Date (YYYY-MM-DD):")
    date_label.grid(row=1, column=0, pady=10)
    date_entry = tk.Entry(create_event_window)
    date_entry.grid(row=1, column=1, pady=10)

    time_label = tk.Label(create_event_window, text="Time (HH:MM:SS):")
    time_label.grid(row=2, column=0, pady=10)
    time_entry = tk.Entry(create_event_window)
    time_entry.grid(row=2, column=1, pady=10)

    venue_label = tk.Label(create_event_window, text="Venue:")
    venue_label.grid(row=3, column=0, pady=10)
    venue_entry = tk.Entry(create_event_window)
    venue_entry.grid(row=3, column=1, pady=10)

    category_label = tk.Label(create_event_window, text="Category:")
    category_label.grid(row=4, column=0, pady=10)
    category_entry = tk.Entry(create_event_window)
    category_entry.grid(row=4, column=1, pady=10)

    description_label = tk.Label(create_event_window, text="Description:")
    description_label.grid(row=5, column=0, pady=10)
    description_entry = tk.Entry(create_event_window)
    description_entry.grid(row=5, column=1, pady=10)

    price_label = tk.Label(create_event_window, text="Ticket Price:")
    price_label.grid(row=6, column=0, pady=10)
    price_entry = tk.Entry(create_event_window)
    price_entry.grid(row=6, column=1, pady=10)

    # Function to save the new event to the database
    def save_event():
        event_name = event_name_entry.get()
        date = date_entry.get()
        time = time_entry.get()
        venue_name = venue_entry.get()
        category = category_entry.get()
        description = description_entry.get()
        price = price_entry.get()  # Get the ticket price

        # Check if the venue exists
        cursor.execute("SELECT * FROM Venue WHERE VenueName=%s", (venue_name,))
        venue = cursor.fetchone()

        if venue:
            # Check for overlapping events in the same venue and time
            cursor.execute("SELECT * FROM Event WHERE VenueID=%s AND Date=%s AND Time=%s", (venue[0], date, time))
            overlapping_event = cursor.fetchone()

            if overlapping_event:
                messagebox.showerror("Time Conflict", "There is already an event scheduled at the same time in this venue. Please choose another time.")
            else:
                # Insert the new event into the database
                cursor.execute("INSERT INTO Event (EventName, Date, Time, VenueID, OrganizerUserID, CategoryName, Description, Price) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                               (event_name, date, time, venue[0], user[0], category, description, price))
                db.commit()
                messagebox.showinfo("Event Created", "Your event has been created successfully.")
                create_event_window.destroy()
        else:
            messagebox.showerror("Venue not found", "Please enter a valid venue.")

    save_btn = tk.Button(create_event_window, text="Save Event", command=save_event)
    save_btn.grid(row=7, column=0, columnspan=2, pady=10)

# Function to book available events, including ticket price and total amount calculation
def book_available_events(user):
    book_events_window = tk.Toplevel(root)
    book_events_window.title("Book Available Events")

    # Fetch available events from the database
    cursor.execute("SELECT Event.EventID, Event.EventName, Event.Date, Event.Time, Venue.VenueName, Event.Price "
                   "FROM Event "
                   "JOIN Venue ON Event.VenueID = Venue.VenueID "
                   "WHERE Event.Date >= CURRENT_DATE()")
    available_events = cursor.fetchall()

    # Display available events in a new window
    for event in available_events:
        event_label = tk.Label(book_events_window, text=f"Event: {event[1]}, Date: {event[2]}, Time: {event[3]}, Venue: {event[4]}, Price: ₹{event[5]}")
        event_label.pack(pady=5)

    # Function to book the selected event, including ticket count and total amount
    def book_event():
        selected_event_index = available_events_listbox.curselection()

        if selected_event_index:
            selected_event_id = available_events[selected_event_index[0]][0]

            # Check if the user has already booked this event
            cursor.execute("SELECT * FROM Booking WHERE UserID=%s AND EventID=%s", (user[0], selected_event_id))
            existing_booking = cursor.fetchone()

            if existing_booking:
                messagebox.showerror("Booking Failed", "You have already booked this event.")
            else:
                # Get the ticket count from the user
                ticket_count = simpledialog.askinteger("Ticket Count", "Enter the number of tickets you want to book:", parent=book_events_window)

                if ticket_count is not None and ticket_count > 0:
                    # Calculate the total amount based on ticket count and ticket price
                    total_amount = ticket_count * available_events[selected_event_index[0]][5]

                    # Insert the booking record into the database
                    cursor.execute("INSERT INTO Booking (UserID, EventID, BookingDate, TicketCount, TotalAmount) "
                                   "VALUES (%s, %s, CURRENT_DATE(), %s, %s)", (user[0], selected_event_id, ticket_count, total_amount))
                    db.commit()
                    messagebox.showinfo("Booking Successful", "Your booking has been confirmed.")
                    book_events_window.destroy()
                else:
                    messagebox.showerror("Invalid Ticket Count", "Please enter a valid number of tickets.")
        else:
            messagebox.showerror("Selection Error", "Please select an event to book.")

    available_events_listbox = tk.Listbox(book_events_window)
    for event in available_events:
        available_events_listbox.insert(tk.END, event[1])  # Display event names in the listbox
    available_events_listbox.pack(pady=10)

    book_btn = tk.Button(book_events_window, text="Book Event", command=book_event)
    book_btn.pack(pady=10)

# Function to clear entry widgets
def clear_entries():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Main login/signup window
root = tk.Tk()
root.title("Event Booking Platform")

# Create entry widgets for login/signup
username_label = tk.Label(root, text="Username:")
username_label.pack(pady=10)
username_entry = tk.Entry(root)
username_entry.pack(pady=10)

password_label = tk.Label(root, text="Password:")
password_label.pack(pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=10)

email_label = tk.Label(root, text="Email:")
email_label.pack(pady=10)
email_entry = tk.Entry(root)
email_entry.pack(pady=10)

login_btn = tk.Button(root, text="Login", command=login)
login_btn.pack(pady=10)

signup_btn = tk.Button(root, text="Signup", command=signup)
signup_btn.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()

dynamic Ticket Booking Platform using Python (Tkinter) and MySQL

-The platform allows users to register, log in, and seamlessly book tickets for various events, including concerts, movies, sports, and user-created events.
-Users can also create, manage, and delete their own events, ensuring a personalized experience.
-The project showcases proficiency in full-stack development, database management, and user-centric design.

The data used is stored in the mysql database in the following tables :
User: UserID, Username, Password, Email 
Event: EventID, EventName, Date, Time, VenueID, OrganizerUserID, CategoryName,Description,price
Booking: BookingID, UserID, EventID, BookingDate, TicketCount, TotalAmount
Venue: VenueID, VenueName, Location, Capacity

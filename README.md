# liveclass-app

## Liveclass backend for math-materate

### requirements
* Django - `pip install django`
* Django Rest Framework - `pip install djangorestframework`

### Current apps
* authentication - **for authentication purposes**
* liveclass_api - **for all api related works**

### models 
* LiveClass - **It currently stores the standard and may be other things that will be specific to the standard**
* User_details - **It contains the current login user details like email and mobile number**
* Mentors - **Contains list of all the mentors that are available**
* LiveClass_details - **Details about the liveclasses like time, duration, mentor, standard, chapter and other details relevant to the live class**
* SavedClass - **contains all the saved classes by the users**
* RegisteredClass - **contains details of users that are registered for the class**

### Api endpoints
* `/register` - **To register a new user**
* `/login` - **To login the currently registered user**
* `/logout` - *To logout currently logined user**
* `/liveclass` - **It is a get request to list all the details of live classes**
* `/liveclass/id` - **It is post, update and delete request relevant to the liveclass and can only be done by the superuser**
* `/saved` - **This endpoints enables the current user to see his/her saved classes and add more class to the saved database**
* `/saved/id` - **This endpoints enables the current user to delete a particular saved classes**
* `/registerclass` - **To see current registered classes for the user**
* `/registerclass/id` - **To register or deregister for a liveclass by the user**
s
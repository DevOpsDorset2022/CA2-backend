# CA1-backend
CA1-backend
For this project we were asked to create a polls app in Django using MySQL as a database. 
The template we used it's from Django tutorial and it's a webapp where the user can vote answers for different questions.
We used the same template and data types, but instead of questions we used names of movies, 
and instead of answers the user can vote to give a score.
We added a delete button on the app to make use of some other method as delete

We tried in some ways to populate the database with a script, we approach the problem in 
2 different ways but the script was not working.

- **First method:** we retrieved data from an external API (title and score of movies), 
following the method on Django website we tried to populate the database, but we could not import the models, 
we tried to create a second data class with the same fields, but it did not work. 

- **Second method:** We tried to create a Json file with the data to use loaddata method, but when we were running the command, we were having an error

- We decided to pass the script manually on the shell, but it did not work.

- Finally, we added some data manually and continue working, after refactoring some datatypes in the model and adding some fields we generate and the migration again, 
without dumping the data, so we deleted the DB, and we created one more time, yet with all the refactoring we could not retrieve the choices for every movie,
at some point we decided to drop the whole project and start over, this time with little changes from the tutorial.

---
[Old repo that I broke](https://github.com/23643studentdorset/CAs-Backend)

---

- [x] All CRUD operations are working as intended (e.g. the right data is retrieved while using an index, data is being deleted by a criteria, retrieve one or multiple records). 
- [x] The application is connecting to the right database. 
- [ ] The data is complex: it contains at least one index (unique entry); has at least 3 types of variables and there are sufficient entries already in the database; 
- [x] Code is readable: consistency, right indentation, comments. 
- [x] The application is accompanied by a short report (max. 500 words) or a ReadMe file. The report should explain the developing process of the application. 
- [ ] Creativity: Do your own research and add any other functionality to your application. 

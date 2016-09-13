# tellmeallaboutit #


 ### Udacity full stack nanodegree (FSND) multi user blog project ###

This is a multi user blog project written in Python 2.7 for Google App Engine

You can view it live here:
http://fsnd-mub-project.appspot.com/

### Requirements for local deployment ###

* Google App Engine Launcher (>= 1.9.37)
* Python 2.7
* Web Browser

---

### Quickstart ###

1. Clone or download this repository from https://github.com/Kyushi/mub.git
* Install Google App Engine Launcher
* Select File -> Add Existing Application
* Find downloaded repository and add containing folder to Google App Engine Launcher
* Select project in list and click 'Run'
* Click 'Browse' in GAE

---

### Explanation ###

This is a blog project. A visitor to the page can create a user account. As a registered user, the visitor can login/logout, write a blog post, comment on others' or own blog posts, edit/delete their own posts or comments, and like others' posts.
When a user deletes their own post, all comments about the post get deleted as well.
The project is based on Google's App Engine with Python 2.7. The front-end uses Bootstrap's grid layout with a mobile-first approach (due to the current simplicity of the project, it is actually mobile-only non-responsive, i.e. there are no breakpoints to change the layout).
Liking and commenting is handled via AJAX, so that the user is not taken out of the flow when using those parts of the page.

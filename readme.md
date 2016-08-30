*This is a work in progress and not fully funcitonal yet.*

# tellmeallaboutit #


 ###### Udacity full stack nanodegree (FSND) multi user blog project ######


This is a multi user blog project written in Python 2.7 for Google App Engine

### Requirements for local deployment ###

* Google App Engine Launcher (>= 1.9.37)
* Python 2.7
* Web Browser

---

### Quickstart ###

1. Clone or download this repository from https://github.com/Kyushi/mub.git
* Install Google App Engine Launcher
* Select File -> Add Existing Application
* Find downloaded repository and add containing folder to Google Ap Engine Launcher
* Select project in list and click 'Run' (you may have to allow incoming traffic to the app)
* Click 'Browse'

---
### Test functionality ###

1. Click 'Signup', enter username, password (+verification), add e-mail (optional). The username can be 3-20 characters long and include letters, digits, underscores and dashes.
2. Username, Logout option and option to write a blog post should appear in the menu, cookie with user id and hash will be set.
3. Try logging out and in again
4. Write a blog post
5. After submission, you will be redirected to the single blog entry on its permalinked page
6. Try liking the blog post (error message appears)
7. Comment on the blog post
8. Edit blog post ("Edited + datetime" should appear in the bottom left corner of the post)
9. Sign out and create another user
10. Write blog post with other user.
11. Try liking others' blog posts (like and unlike). Like count should go up/down, 'You like this' should appear/disappear
12. Comment on blog posts, edit comments.
13. Sign out and grade ;)

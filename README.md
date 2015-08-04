# ostproject
NYU OST Final Project
Quora Q&A App Made with Python and Google Apps Engine

Project Outline:
ndex: - A greeting to the user and the option to sign in or out. - If the user is signed in, the username will display with the option to -sign out -add a question - A search box to search for tags for questions. The search will only return an exact matching tag. I.E. if 'dev' is searched for, 'development' will not return as a result. - A link to the upload page for adding images. - The 10 newest questions. Each question has a link showing the question id and text for 500 characters or any links and images in the question text, followed by the votes the question received. - At the bottom of the page, there is a pagination link to see older questions.

Login: - Login is handled with Federated Login with google as the only option. If there is an error, try refreshing to going back to the home page. Sometimes an error message shows up even when the login was successful.

Upload: - Choose a file and upload. It will be added to the list of available files. Each file has a link to the url.

Question Detail: - Shows login information with option to log out or log in. - If the user is logged in, there is an option to - add an answer. Any logged in user can add an answer. - edit the question. If the user is not the author, the clicking the link results in a notice that only the author can edit the question. - vote on the question or answer. Only one vote per question or answer per question counts, but the user can change the vote. - Shows full text of the question followed by the votes. - Shows image upload associated with the question. - Shows Answers associated with the question and images associated with the answers. - To vote on the question, select the radio button above the question text and select up or down. - To vote on an answer, select the radio button next to the answer text and select up or down. - Voting sends the user to the results page.

Results: - The results page shows the updated votes. - The links to add an answer or vote are not available on the results page. - Click vote again? at the bottom to return to question detail.

Add a Question: - Only a signed in user can add a question. - Shows text boxes for question text, optional tags and an optional image from the uploaded images. - Adding html such as an anchor tag will display as a link in the question. If an image url is added as an anchor tag it will be replaced with an img tag and display inline.

Add an Answer: - Only a signed in user can add an answer. - Shows text boxes for question text and optional image from the uploaded images. - Adding html such as an anchor tag will display as a link in the question. If an image url is added as an anchor tag it will be replaced with an img tag and display inline.

Edit a Question: - Only a signed in author of the original question can edit a question. - Shows text boxes for question text, optional tags and an optional image from the uploaded images. They are populated with the question text, tags and image. - Adding html such as an anchor tag will display as a link in the question. If an image url is added as an anchor tag it will be replaced with an img tag and display inline. -The publication date will be updated to the time that the edit to the question was submitted.

Edit an Answer: - Only a signed in author of the original question can edit a question. - Shows text boxes for question text, optional tags and an optional image from the uploaded images. They are populated with the question text, tags and image. - Adding html such as an anchor tag will display as a link in the question. If an image url is added as an anchor tag it will be replaced with an img tag and display inline. -The publication date will be updated to the time that the edit to the question was submitted.

Feed: -There is no link to feed for a question, but the feed can be viewed by adding /feed to the url of a question. -ie if the question detail url is -

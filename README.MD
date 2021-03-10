# Capstone Project: Food-finder

Hello, this is the repository for my Capstone project that I worked on as a fellow at [The Data Incubator](https://www.thedataincubator.com/).
<br>
You can check out the app here: [Food-finder](https://food-finder-vegas-app.herokuapp.com/)



### Objective:
* To build an interface for single and multi-user recommendation engine.
* **Single-user:** Hybrid recommendation interface.
* **Multi-user:** Knowledge-based recommendation interface for a group of two people.
* Address **cold-start** problem.


### Project genesis:
How often does it happen with you that you've got friends over and you all take forever to decide which place to go to? What are the plausible factors that prevent us from reaching a consensus? There could be several reasons: 
1. Every person has a **unique** taste.
2. People may have constraints like **proximity**, or a craving for a certain food like **Chicken tikka** or a **steak**.
 


#### Beneficiary: Who is it for?
This product is a useful tool for pretty much every single person who likes to go out to eat either by himself/herself or in a group.
You could be in a new city or in your own neighborhood and it will recommend restaurants to you based off the reviews left by thousands of users.

### Key details:

1. To build the system, the data is taken from the [Yelp dataset](https://www.yelp.com/dataset).
3. Restaurants are selected from the city of Las Vegas.
4. More cities could be added in the future to get the top recommendations in any of the major cities all over the US. 


## Project details:

### Data: Retreival, Filtering and Cleaning:

**Retrieval:**
1. Yelp dataset is a huge collection of user reviews in the form of *reviews.json*.
2. In addition to the user reviews, it contains two more datasets: *users.json* and *business.json*.

**Data filtering:**
1. Businesses related to the key category **Restaurants** are selected.
2. Most users either don't post too many reviews: one or two or none at all.
3. Yelp calls the users who frequently post reviews an **elite** user.
4. For our analysis, I have filtered either all the elite users who have been 'yelping' for a while or the ones who are not elite but fall in the top 25 percentile range or the users who have left at least 10 reviews.



### Under the hood:
**Knowledge-based system:**
* Each restaurant is provided with its **categories**. These categories are typically represent the cuisines they serve.
* **Text Reviews Analysis:** Using the unsupervised learning method of **Topic Modeling** and the natural language processing tools, a new set of **miscellaneous** categories, *e.g.* ambiance, dinner/breakfast choice is created. 
* The cleaning, processing of the reviews is done using [spaCy](https://spacy.io/) and for topic modeling, [Gensim](https://pypi.org/project/gensim/) is used.
* Together, these form a feature-set which, the users can choose to look for the ideal place. 
* The restaurant ratings are weighted-averaged and sorted in order to produce a list of **popular** restaurants.
* These **popular** restaurants are then suggested to the user(s) along with their geographical locations for them to make an informed choice.
* **Note:** This is a *cold-start* problem. The users are asked details about their preferences which helps the knowledge-based engine recommend the best possible options in the neighborhood. 

**Hybrid system:**
* This system is composed of two engines working in parallel: **Collaborative-based** and **Content-based**.
* **Collaborative-based:** The model-based collaborative filtering method is used to predict the rating a user would give to a restaurant he/she has never visited. Collaborative-filtering method looks for the set of people whose ratings are similar to the user and suggests the restaurants which those people have liked. Based on the predicted ratings, the top choices are recommended. The engine is built using [Scikit-Surprise](http://surpriselib.com/).
* It uses matrix factorization method, in particular, Singular Value ecomposition(SVD) to perform the predictions.
* **Content-based:** Unlike collaborative filtering, a content-based method looks for the places a user has liked in the past and suggests similar places. 
* In order to find the restaurants suggestions, the same feature-set is used for finding the cosine-similarities between the restaurants and the ones with the highest similarities are suggested. 










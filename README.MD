# Capstone Project: Food-finder

Hello, this is the repository for my Capstone project that I worked on as a fellow at [The Data Incubator](https://www.thedataincubator.com/).



### Objective:
* To build a knowledge-based recommendation interface for a group of two people.
* To build a hybrid recommendation interface for existing single-user accounts.
* Address a **cold-start** problem in the form of a **popularity-based** engine.


### Project genesis:
How often does it happen with you that you've got friends over and you all take forever to decide which place to go to? What are the plausible factors that prevent us from reaching a consensus? There could be several reasons: 
1. Every person has a **unique** taste.
2. People like specific things like **proximity**, **ambiance** and so on..
3. People have a craving for a certain food like **Chicken tikka** or a **steak**.

#### Solution:
Having gone through this trouble with my roommates about a million times, here is a solution in the form of **Food-finder**. 

#### Beneficiary: Who is it for?
This product is a useful tool for pretty much every single person who likes to go out to eat either by himself/herself or in a group.
You could be in a new city or in your own neighborhood and it will recommend restaurants to you based off the reviews left by thousands of users.

### Key assumptions and details:
1. They can select the cuisine from a wide variety of options available.
2. To build the system, data is taken from the [Yelp dataset](https://www.yelp.com/dataset)
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









**Data cleaning:**

The data is in the form of user reviews which is essentially, *text data*. In order to extract key information out of it, the data is cleaned off all the punctuation marks, stop words and other non-text characters to be fed to the natural language processing(NLP) methods.

### Under the hood:
The key steps behind the project are:
* Each restaurant is provided with its **categories**. First step is to vectorize the categories column and build a vector for each restaurant in the n-dimensional category space where n is the number of unique categories.
* **Methods:** Using advanced NLP toolkits like [NLTK](https://www.nltk.org/) and [spaCy](https://spacy.io/), the reviews data is analyzed and each review is given a user sentiment analyzed polarity score(VADER).
* Based off the polarity scores for each cuisine category grouped by restaurants, a mean polarity score is generated.
* The restaurants are then ranked based off these polarity ratings.
* These **popular** restaurants are then suggested to the user(s) along with their geographical locations for them to make an informed choice.
* **Note:** This is a *cold-start* problem. The users are asked details about their preferences which helps the popularity-based engine recommend the best possible options in the neighborhood. 











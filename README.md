# 🎥 MoodyTube v1.0.1 - Documentation

*"Tune Into The Feelings Of Your Audience"*

⚠️ Note this application is only extracting, cleaning and storing data, the machine learning model is still in development.

________________________________________________________________________

##  ℹ️ Introduction:

**MoodyTube** is an open-source sentiment analysis tool designed to help creators and businesses gauge audience reactions by analysing data from channels and individual videos. Ever heard the phrase, "You should just focus on content"? That's exactly why MoodyTube was created. By leveraging this tool, users can gain valuable insights into the emotional impact of their content—whether positive or negative. With this understanding, they can refine their messaging and better plan future content to ensure they’re delivering the right material. Let’s explore an example to see just how valuable MoodyTube can be:

💡 **Usage  Example 1:**

- You've released 100+ videos and now want to gauge whether users are responding positively to your content in order to plan effectively for future video releases. Use **MoodyTube** to analyse the video with the highest number of likes and the most positive sentiment. By leveraging machine learning, **MoodyTube** scrapes and analyses comments and likes, providing a detailed report on audience reactions.

💡 **Usage  Example 2:**

- You're noticing a video is receiving a surge of comments and dislikes. Use MoodyTube's machine learning capabilities to assess the negative impact on your audience by scraping and analysing the sentiment of the comments. This will give you a clear understanding of how your video is being received. 

**There are two main ways to use MoodyTube:

1. Use this to understand the sentiment of your own videos and the analyse the performance of your own channel. Gain valuable data to plan your future content releases .✅

2. Use this to understand the sentiment of multiple competitors, all it takes it's their channel ID which be found publicly in the channel URL, it's all completely legal. By understanding your competitors sentiment you can adopt new effective content creation and delivery strategies. ✅

________________________________________________________________________

##  ⚙️ Installation:

In order to use **MoodyTube** on your machine, you need to follow these steps in order.
#### First Steps - Setup Google Cloud & Activate API

1. Setup a Google Cloud account (if you don't have one).
2. Activate the YouTube Data API v3 service
3. Generate an API Key (OAuth is not necessary for this)
4. Create an `.env` file in the directory with fields for `API_KEY`
5. Add your generated API Key in the `.env` file in the field `API_KEY`

#### Second Steps - Setup PostgreSQL Database

1. Install PostgreSQL 16.3 (If not already installed)
2. Create Database using pgAdmin4 (recommended )or other database management platform
3. Tables are already created in the `db.py`, they will be automatically created once the `main.py` file is running.
4. Once the database is created, add the `.env` file database fields with your credentials.

#### Third Steps - Install  Dependencies

Dependencies used in this project:
 - **Pandas** - Used to create dataframes and create .csv files using the dataframe.
 - **Isodate** - To convert average video duration from ISO format to a more readable format.
 - **Psycopg2** - To create the postgresql database connection.
 - **Sqlalchemy** - To perform database queries to insert, update, delete data.
 - **Python-dotenv** - For the environmental variables.

1. Install the Python Google API Client with the following code in your terminal:

	`pip install --upgrade google-api-python-client`

2. Install all the modules required for this system to work by running this code in your terminal:

	`pip install -r requirements.txt`
	

________________________________________________________________________

##  💻 How To Use MoodyTube:

This tool is simple to use once the installation in your local machine is completed. You simply run the `main.py` file and you will be getting the `.csv` files generated in their dedicated directory folders and your data stored in the database.

#  ⚠️ Note this software only retrieves data, the machine learning model is still in development

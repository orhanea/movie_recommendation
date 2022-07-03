import streamlit as st
import pandas as pd
import datetime
import os
import sqlite3
from PIL import Image
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

# Database
conn = sqlite3.connect('cwt.db')
c = conn.cursor()

# Images
image = Image.open('C:\\Users\\linae\\PycharmProjects\\bitirme\\resim\\Canwatchthis.png')
st.image(image)
path = "C:\\Users\\linae\\PycharmProjects\\bitirme\\Resimler\\"  # resim klasörünü ekle
resim_list = os.listdir(path)

# Time
time = datetime.datetime.now()

c.execute('SELECT RatingID from rating Order by RatingID desc limit 1')
data = c.fetchall()
last_rating = data[0][0]

c.execute('SELECT * from rating limit 10000')
rating_data = c.fetchall()

c.execute('SELECT * from movie')
movie_data = c.fetchall()

c.execute('SELECT UserID from user Order by UserID desc limit 1')
data1 = c.fetchall()
last_userid = data1[0][0]


def update_userdata(user_id, firstname, lastname, username, password, email, age):
    c.execute('UPDATE User SET FirstName=?, LastName= ?, UserName= ?, Password=?, Email=? AND Age=? WHERE UserID=?',
              (user_id, firstname, lastname, username, password, email, age))
    conn.commit()


def add_friends(username,password,friendUsername):
    c.execute('INSERT INTO User(Friendlist) VALUES (?) WHERE username =? AND password = ?',
              (username, password,friendUsername)),
    conn.commit()


def add_userdata(last_user_id, firstname, lastname, username, password, email, age):
    c.execute('INSERT INTO User(UserID,FirstName,LastName,UserName,Password,Email,Age) VALUES (?,?,?,?,?,?,?)',
              (last_user_id+1, firstname, lastname, username, password, email, age))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM User WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM User')
    data = c.fetchall()
    return data


def view_user_infos(username):
     c.execute('SELECT username FROM User WHERE username =? ', (username,))
     data1 = c.fetchall()
     return data1[0][0]


def give_rating4(last_rating, last_userid, movie_id, u_rating):

    c.execute('INSERT INTO rating(RatingID, userID, movieID, rating, timestamp) VALUES (?,?,?,?,?)',
                  (last_rating + 1, int(last_userid), str(movie_id), float(u_rating), time))
    conn.commit()


def view_user_id(username, password):
    c.execute('SELECT UserID FROM User WHERE username =? AND password = ?', (username, password))
    data1 = c.fetchall()
    return data1[0][0]


def view_username(username, password):
    c.execute('SELECT username FROM User WHERE username =? AND password = ?', (username, password))
    data2 = c.fetchall()
    return data2[0][0]


def view_email(username, password):
    c.execute('SELECT email FROM User WHERE username =? AND password = ?', (username, password))
    data2 = c.fetchall()
    return data2[0][0]


def view_password(username, password):
    c.execute('SELECT password FROM User WHERE username =? AND password = ?', (username, password))
    data2 = c.fetchall()
    return data2[0][0]


def view_firstname(username, password):
    c.execute('SELECT firstname FROM User WHERE username =? AND password = ?', (username, password))
    data2 = c.fetchall()
    return data2[0][0]


def view_lastname(username, password):
    c.execute('SELECT lastname FROM User WHERE username =? AND password = ?', (username, password))
    data2 = c.fetchall()
    return data2[0][0]


def view_age(username, password):
    c.execute('SELECT age FROM User WHERE username =? AND password = ?', (username, password))
    data2 = c.fetchall()
    return data2[0][0]


def get_movie_name(title):
    c.execute('SELECT Title FROM movie WHERE title = ? ', (title,))
    data_m = c.fetchall()

    return data_m


def get_movie_id(title):
    c.execute('SELECT MovieID FROM movie WHERE title = ? ', (title,))
    data_m = c.fetchall()
    return data_m


def get_movie_name_for_movie_id(userID):
   c.execute('SELECT movie.Title, rating.rating, rating.timestamp FROM movie INNER JOIN rating ON movie.MovieID = rating.movieId WHERE UserID = ? ', (userID,) )
   data_m = c.fetchall()
   return data_m


def main():
    global create_user_movie_df
    st.title("Can Watch This")
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
    elif choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.checkbox("Login"):
            result = login_user(username, password)
            if result:
                st.sidebar.success("Logged In as {}".format(username))
                logged_user_id = result[0][0]
                logged_user_name = result[0][3]
                task = st.selectbox("Task", ["Choose an action", "Find Movie to Give Rating", "Give Rating", "Get Recommendation", "User Profiles"])
                if task == "Choose an action":
                    st.write('Welcome,' + logged_user_name + ':sunglasses:')
                    st.write('Please choose an action!')
                elif task == "Find Movie to Give Rating":
                    movie_name = st.text_input("Write Movie Name")
                    movie_name = movie_name + ' '
                    movie_name = movie_name.title()
                    click = st.button("Find")
                    if click:
                        movie = get_movie_name(movie_name)
                        st.write(movie)
                        rating = st.slider("Rating", min_value=1.0, max_value=5.0, step=0.5)
                        click_2 = st.button("Save your rating")
                        last_user_id_for_rating = view_user_id(username, password)
                        if click_2:
                            give_rating4(last_rating, last_userid=last_user_id_for_rating, u_rating=rating)
                elif task == "Give Rating":
                    st.subheader("Give Rating")
                    # rating verdikten sonra database göndermesi gerekiyor insert
                    movie_list = []
                    movie_id_for_last_rating = []
                    col1, col2 = st.columns(2)
                    with col1:
                        for i in range(10):
                            image = Image.open(path + resim_list[i])
                            new_image = image.resize((150, 250))
                            st.image(new_image, caption=resim_list[i][:-4])
                            movie_list.append(resim_list[i][:-4].title())

                            rating = st.slider("Rating", min_value=1.0, max_value=5.0, step=0.5, key=i)
                            click = st.button("Save your rating", key=i)

                            last_user_id_for_rating = view_user_id(username, password)
                            movie_id_for_last_rating.append(get_movie_id(movie_list[i]))

                            if click:
                                give_rating4(last_rating, last_user_id_for_rating, movie_id_for_last_rating[i][0][0], u_rating=rating)
                    with col2:
                        for i in range(10,20):
                            image = Image.open(path + resim_list[i])
                            new_image = image.resize((150, 250))
                            st.image(new_image, caption=resim_list[i][:-4])
                            movie_list.append(resim_list[i][:-4].title())

                            rating = st.slider("Rating", min_value=1.0, max_value=5.0, step=0.5, key=i)
                            click = st.button("Save your rating", key=i)

                            last_user_id_for_rating = view_user_id(username, password)
                            movie_id_for_last_rating.append(get_movie_id(movie_list[i]))

                            if click:
                                give_rating4(last_rating, last_user_id_for_rating, movie_id_for_last_rating[i][0][0], u_rating=rating)

                elif task == "Get Recommendation":
                    st.subheader("Get Recommendation")

                    def create_user_movie_df():
                        import pandas as pd
                        movie = pd.read_csv('movie_lens_dataset/movies.csv')
                        rating = pd.read_csv('movie_lens_dataset/rating.csv')
                        df = movie.merge(rating, how="left", on="movieId")
                        comment_counts = pd.DataFrame(df["title"].value_counts())
                        rare_movies = comment_counts[comment_counts["title"] <= 1400].index
                        common_movies = df[~df["title"].isin(rare_movies)]
                        user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
                        return user_movie_df

                    user_movie_df = create_user_movie_df()

                    # perc = len(movies_watched) * 60 / 100
                    # users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]

                    def user_based_recommender(random_user, user_movie_df, ratio=80, cor_th=0.75, score=3.5):
                        import pandas as pd
                        random_user_df = user_movie_df[user_movie_df.index == random_user]
                        movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()
                        movies_watched_df = user_movie_df[movies_watched]
                        user_movie_count = movies_watched_df.T.notnull().sum()
                        user_movie_count = user_movie_count.reset_index()
                        user_movie_count.columns = ["userId", "movie_count"]
                        perc = len(movies_watched) * ratio / 100
                        users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]

                        final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies)],
                                              random_user_df[movies_watched]])

                        corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()
                        corr_df = pd.DataFrame(corr_df, columns=["corr"])
                        corr_df.index.names = ['user_id_1', 'user_id_2']
                        corr_df = corr_df.reset_index()

                        top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= cor_th)][
                            ["user_id_2", "corr"]].reset_index(drop=True)

                        top_users = top_users.sort_values(by='corr', ascending=False)
                        top_users.rename(columns={"user_id_2": "userId"}, inplace=True)
                        rating = pd.read_csv('movie_lens_dataset/rating.csv')
                        top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')
                        top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']

                        recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})
                        recommendation_df = recommendation_df.reset_index()

                        movies_to_be_recommend = recommendation_df[
                            recommendation_df["weighted_rating"] > score].sort_values("weighted_rating",
                                                                                      ascending=False)
                        movie = pd.read_csv('movie_lens_dataset/movies.csv')

                        return movies_to_be_recommend.merge(movie[["movieId", "title"]])

                    random_user = view_user_id(username, password)
                    recommended_movies = user_based_recommender(random_user, user_movie_df, cor_th=0.70, score=3.5)
                    recommended_movies = recommended_movies[:10]
                    final_liste = recommended_movies["title"].to_list()
                    st.write("You Should watch these movies!")
                    st.balloons()
                    st.dataframe(data=recommended_movies)

                elif task == "User Profiles":
                    st.subheader("User Profiles")

                    bio = st.radio('Jump to', ['Your Profile', 'Add friends', 'Rated movies'])
                    if bio == 'Your Profile':
                        st.subheader("Update your user profile")
                        user_profile_id = view_user_id(username, password)
                        update_name = st.text_input("Name", view_firstname(username, password))
                        update_surname = st.text_input("Surname", view_lastname(username, password))
                        update_username = st.text_input("Username", view_username(username, password))
                        update_password = st.text_input("Password", view_password(username, password), type='password', key=2)
                        update_mail = st.text_input("Mail", view_email(username, password))
                        update_age = st.number_input("Age", view_age(username, password), step=1)

                        if st.button("Update"):
                            update_userdata(user_profile_id, update_name, update_surname, update_username,
                                            update_password, update_mail, update_age)
                    elif bio == 'Add friends':
                        st.write('Add friend.')
                        find_user = st.text_input("Enter the username of the user that you want to find.")
                        click = st.button("Find")
                        if click:
                            st.success("The user exists.")
                            st.text_input(" ", view_user_infos(find_user))
                            click2 = st.button("Add as Friend")
                            if click2:
                                add_friends(username, password, view_user_infos(find_user))
                    elif bio == 'Rated movies':
                        st.subheader("Rated Movies")
                        userprofile_id = view_user_id(username, password)
                        st.text_input("Movie Title, Rating , Time ", get_movie_name_for_movie_id(userprofile_id))
            else:
                st.warning("Incorrect Username/Password")
    elif choice == "SignUp":

        st.subheader("Create New Account")
        new_name = st.text_input("Name")
        new_surname = st.text_input("Surname")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        new_mail = st.text_input("Mail")
        new_age = st.number_input("Age", step=1)

        if st.button("Signup"):
            add_userdata(last_userid, new_name, new_surname, new_user, new_password, new_mail, new_age)
            st.success("You have successfully created a valid account.")
            st.balloons()
            st.info("Go to the Login Menu to login.")


if __name__ == '__main__':
    main()
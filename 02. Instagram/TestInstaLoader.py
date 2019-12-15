import instaloader

def main():
    # Info
    userName = "quang_quoc"
    passWord = "quoc@12345"
    # Get instance
    L = instaloader.Instaloader()

    # Optionally, login or load session
    #L.login(userName, passWord)        # (login)
    #L.interactive_login(userName)      # (ask password on terminal)
    #L.load_session_from_file(userName) # (load session created w/
                                #  `instaloader -l USERNAME`
    for post in L.get_hashtag_posts('cat'):
        likes = post.get_likes()
        for like in likes:
            print(like.username)
                            
if __name__ == '__main__':
    main()

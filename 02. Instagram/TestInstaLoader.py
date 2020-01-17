import instaloader

def main():
    userName = "quang_quoc"
    passWord = "quoc@12345"

    # Id post
    SHORTCODE = 'B5Z61Z6pgAC'

    # user scan
    userNameScan = "ngot.store.dn"
    
    # Get instance
    L = instaloader.Instaloader()

    # Optionally, login or load session
    L.login(userName, passWord)        # (login)
    #L.interactive_login(userName)      # (ask password on terminal)
    #L.load_session_from_file(userName) # (load session created w/
                                    #  `instaloader -l USERNAME`
    # get data from a post
    post =  instaloader.Post.from_shortcode(L.context, SHORTCODE)
    data_like = [like.username for like in post.get_likes()]
    print(data_like)

    # get data from a user
    profile = instaloader.Profile.from_username(L.context, userNameScan)
    # followees
    data_followees = [fl.username for fl in profile.get_followees()]
    #followers
    data_followers = [fl.username for fl in profile.get_followers()]

    print(data_followers)

    
                            
if __name__ == '__main__':
    main()

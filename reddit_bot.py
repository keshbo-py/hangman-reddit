import praw
import config
import time

def bot_login():
    print("Logging in...")
    reddit = praw.Reddit(client_id=config.client_id,
                         client_secret=config.client_secret,
                         username=config.username,
                         password=config.password,
                         user_agent=config.user_agent)
    print("Logged in!")
    return reddit


def run_bot(r, subreddit, id_list):

    print("Looking for comments...")
    for comment in r.subreddit(subreddit).comments(limit=25):
        if "!hangman" in comment.body and comment.id not in id_list and comment.author != r.user.me():
            comment.reply("You Called Me?")
            print("\nComment replied!\n")
            id_list.append(comment.id)
            with open("id_list.txt", "a") as f:
                f.write(comment.id + "\n")
            if comment.author not in id_times_list:
                id_times_list.append(comment.author)
                times_list.append(0)
                with open("id_times_list.txt", "a") as f:
                    f.write(str(comment.author) + "\n")
                with open("times_list.txt", "a") as f:
                    f.write(str(0))
            num = id_times_list.index(comment.author)
            times_list[num] =int(times_list[num])  + 1
            with open("id_times_list.txt", "w") as f:
                for line in id_times_list:
                    f.write(str(line) + "\n")
            with open("times_list.txt", "w") as f:
                for line in times_list:
                    f.write(str(line)+ "\n")
        elif "!hang" in comment.body and comment.id not in id_list and comment.author != r.user.me():
            if comment.author not in id_times_list:
                comment.reply("You've never used !hangman sorry")
            else:
                 num = id_times_list.index(comment.author)
                 comment.reply(str(comment.author) + ", you've used !hangman: " + str(times_list[num]) + " times!")
                 print("\nComment \"time\" replied!\n")
            id_list.append(comment.id)
            with open("id_list.txt", "a") as f:
                f.write(comment.id + "\n")




def save_comment(txt):
    with open(txt, "r") as f:
        lista = f.read()
        lista = lista.split("\n")
        return lista


times_list = save_comment("times_list.txt")
id_times_list = save_comment("id_times_list.txt")
id_list = save_comment("id_list.txt")
r = bot_login()
sub = "test"
while True:
    try:
        run_bot(r, sub, id_list)
    except praw.exceptions.APIException as err:
        print("\n\n" + str(err))
        print("sleeping... zzz...")
        time.sleep(60)
        print("Waked Up!\n\n")

# (c) NTM

from fbchat import Client, log, _graphql
from fbchat.models import *
import json
import random
import wolframalpha
import requests
import time
import math
import sqlite3
from bs4 import BeautifulSoup
import os
import openai
import concurrent.futures
from difflib import SequenceMatcher, get_close_matches


class ChatBot(Client):

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        try:
            msg = str(message_object).split(",")[15][14:-1]
            print(msg)

            if (".mp4" in msg):
                msg = msg

            else:
                msg = str(message_object).split(",")[19][20:-1]
        except:
            try:
                msg = (message_object.text).lower()
                print(msg)
            except:
                pass
        def sendMsg():
            if (author_id != self.uid):
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)

        def sendQuery():
            self.send(Message(text=reply), thread_id=thread_id,
                      thread_type=thread_type)
        if(author_id == self.uid):
            pass
        else:
            try:
                conn = sqlite3.connect("messages.db")
                c = conn.cursor()
                c.execute("""
                CREATE TABLE IF NOT EXISTS "{}" (
                    mid text PRIMARY KEY,
                    message text NOT NULL
                );

                """.format(str(author_id).replace('"', '""')))

                c.execute("""

                INSERT INTO "{}" VALUES (?, ?)

                """.format(str(author_id).replace('"', '""')), (str(mid), msg))
                conn.commit()
                conn.close()
            except:
                pass


        def corona_details(country_name):
            from datetime import date, timedelta
            today = date.today()
            today = date.today()
            yesterday = today - timedelta(days=1)

            url = "https://covid-193.p.rapidapi.com/history"

            querystring = {"country": country_name, "day": yesterday}

            headers = {
                'x-rapidapi-key': "8cd2881885msh9933f89c5aa2186p1d8076jsn7303d42b3c66",
                'x-rapidapi-host': "covid-193.p.rapidapi.com"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            data_str = response.text

            data = eval(data_str.replace("null", "None"))
            country_name = data["response"][0]["country"]
            new_cases = data["response"][0]["cases"]["new"]
            active_cases = data["response"][0]["cases"]["active"]
            total_cases = data["response"][0]["cases"]["total"]
            critical_cases = data["response"][0]["cases"]["critical"]
            total_deaths = data["response"][0]["deaths"]["total"]
            total_recovered = data["response"][0]["cases"]["recovered"]
            new_deaths = data["response"][0]["deaths"]["new"]
            reply = f'Corona Virus Info of {country_name}:\n🥺 New Cases : {new_cases.replace("+", "")}\n😟 New Deaths : {new_deaths.replace("+", "")}\n😔 Active Cases : {active_cases}\n⚰️ Total Deaths: {total_deaths} \n🤕 Critical Cases: {critical_cases}\n💉 Total Cases: {total_cases}\n😊 Total Recovered: {total_recovered}'
            self.send(Message(text=reply), thread_id=thread_id,
                      thread_type=thread_type)

        def weather(city):
            api_address = "https://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
            url = api_address + city
            json_data = requests.get(url).json()
            kelvin_res = json_data["main"]["temp"]
            feels_like = json_data["main"]["feels_like"]
            description = json_data["weather"][0]["description"]
            celcius_res = kelvin_res - 273.15
            max_temp = json_data["main"]["temp_max"]
            min_temp = json_data["main"]["temp_min"]
            visibility = json_data["visibility"]
            pressure = json_data["main"]["pressure"]
            humidity = json_data["main"]["humidity"]
            wind_speed = json_data["wind"]["speed"]

            return(
                f"The current temperature of {city} is %.1f degree celcius with {description}" % celcius_res)

        def stepWiseCalculus(query):
            query = query.replace("+", "%2B")
            try:
                try:
                    api_address = f"https://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Step-by-step%20solution&output=json&format=image"
                    json_data = requests.get(api_address).json()
                    answer = json_data["queryresult"]["pods"][0]["subpods"][1]["img"]["src"]
                    answer = answer.replace("sqrt", "√")

                    if(thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                except:
                    pass
                try:
                    api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
                    json_data = requests.get(api_address).json()
                    answer = json_data["queryresult"]["pods"][0]["subpods"][0]["img"]["src"]
                    answer = answer.replace("sqrt", "√")

                    if(thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

                except:
                    try:
                        answer = json_data["queryresult"]["pods"][1]["subpods"][1]["img"]["src"]
                        answer = answer.replace("sqrt", "√")

                        if(thread_type == ThreadType.USER):
                            f
                            self.sendRemoteFiles(
                                file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                        elif(thread_type == ThreadType.GROUP):
                            self.sendRemoteFiles(
                                file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

                    except:
                        pass
            except:
                pass

        def stepWiseAlgebra(query):
            query = query.replace("+", "%2B")
            api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input=solve%203x^2+4x-6=0&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
            json_data = requests.get(api_address).json()
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][2]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][3]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][4]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][1]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass

        def stepWiseQueries(query):
            query = query.replace("+", "%2B")
            api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
            json_data = requests.get(api_address).json()
            try:
                try:
                    answer = json_data["queryresult"]["pods"][0]["subpods"][0]["plaintext"]
                    answer = answer.replace("sqrt", "√")
                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
                try:
                    answer = json_data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
                    answer = answer.replace("sqrt", "√")

                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
                try:
                    answer = json_data["queryresult"]["pods"][1]["subpods"][1]["plaintext"]
                    answer = answer.replace("sqrt", "√")

                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
            except:
                self.send(Message(text="Cannot find the solution of this problem"), thread_id=thread_id,
                          thread_type=thread_type)

        try:
            def searchForUsers(self, name=" ".join(msg.split()[2:4]), limit=5):
                try:
                    limit = int(msg.split()[4])
                except:
                    limit = 5
                params = {"search": name, "limit": limit}
                (j,) = self.graphql_requests(
                    _graphql.from_query(_graphql.SEARCH_USER, params))
                users = ([User._from_graphql(node)
                          for node in j[name]["users"]["nodes"]])
                for user in users:
                    reply = f"{user.name} profile_link: {user.url}\n friend: {user.is_friend}\n"
                    self.send(Message(text=reply), thread_id=thread_id,
                              thread_type=thread_type)
        except:
            pass

        def programming_solution(self, query):
            try:
                count = int(msg.split()[-1])
            except:
                count = 6
            try:
                x = int(query.split()[-1])
                if type(x) == int:
                    query = " ".join(msg.split()[0:-1])
            except:
                pass
            image_urls = []

            url = "https://bing-image-search1.p.rapidapi.com/images/search"

            querystring = {"q": query, "count": str(count)}

            headers = {
                'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
                'x-rapidapi-key': "55d459414fmsh32c0a06c0e3e34dp1f40a5jsn084fca18f5ea"
            }
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            data = json.loads(response.text)
            img_contents = (data["value"])
            for img_url in img_contents:
                image_urls.append(img_url["contentUrl"])

            def multiThreadImg(img_url):
                if(thread_type == ThreadType.USER):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                elif(thread_type == ThreadType.GROUP):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(multiThreadImg, image_urls)

        def translator(self, query, target):
            query = " ".join(query.split()[1:-2])
            url = "https://microsoft-translator-text.p.rapidapi.com/translate"

            querystring = {"to": target, "api-version": "3.0",
                           "profanityAction": "NoAction", "textType": "plain"}

            payload = f'[{{"Text": "{query}"}}]'

            headers = {
                'content-type': "application/json",
                'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com",
                'x-rapidapi-key': "55d459414fmsh32c0a06c0e3e34dp1f40a5jsn084fca18f5ea"
            }

            response = requests.request(
                "POST", url, data=payload, headers=headers, params=querystring)

            json_response = eval(response.text)

            return json_response[0]["translations"][0]["text"]

        def imageSearch(self, msg):
            try:
                count = int(msg.split()[-1])
            except:
                count = 5
            query = " ".join(msg.split()[2:])
            try:
                x = int(query.split()[-1])
                if type(x) == int:
                    query = " ".join(msg.split()[2:-1])
            except:
                pass
            image_urls = []

            url = "https://bing-image-search1.p.rapidapi.com/images/search"

            querystring = {"q": query, "count": str(count)}

            headers = {
                'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
                'x-rapidapi-key': "55d459414fmsh32c0a06c0e3e34dp1f40a5jsn084fca18f5ea"
            }
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            data = json.loads(response.text)
            img_contents = (data["value"])
            for img_url in img_contents:
                image_urls.append(img_url["contentUrl"])
                print("appended..")

            def multiThreadImg(img_url):
                if(thread_type == ThreadType.USER):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                elif(thread_type == ThreadType.GROUP):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(multiThreadImg, image_urls)

        def searchFiles(self):
            query = " ".join(msg.split()[2:])
            file_urls = []
            url = "https://filepursuit.p.rapidapi.com/"

            querystring = {"q": query, "filetype": msg.split()[1]}

            headers = {
                'x-rapidapi-host': "filepursuit.p.rapidapi.com",
                'x-rapidapi-key': "8cd2881885msh9933f89c5aa2186p1d8076jsn7303d42b3c66"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            response = json.loads(response.text)
            file_contents = response["files_found"]
            try:
                for file in random.sample(file_contents, 5):
                    file_url = file["file_link"]
                    file_name = file["file_name"]
                    self.send(Message(text=f'{file_name}\n Link: {file_url}'),
                              thread_id=thread_id, thread_type=ThreadType.USER)
            except:
                for file in file_contents:
                    file_url = file["file_link"]
                    file_name = file["file_name"]
                    self.send(Message(text=f'{file_name}\n Link: {file_url}'),
                              thread_id=thread_id, thread_type=ThreadType.USER)
      
        def chatGPT(self, query):
            openai.api_key = f"{os.environ.get('openai')}"

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=query,
                temperature=0.15,
                max_tokens=3000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0
            )
            return (response["choices"][0]["text"])
        
        def grammar(self, query):
            openai.api_key = f"{os.environ.get('openai')}"

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="Correct this to standard English:\n"+query,
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            return (response["choices"][0]["text"])
       
        try:

            if ("search pdf" in msg):
                searchFiles(self)
            elif ("ntm" in msg):
                if ("from ntm bot:" in msg):
                    return
                query = " ".join(msg.split(" ")[1:])
                reply = "From NTM Bot:\t"+chatGPT(self, query)
                sendQuery()
            elif ("grammar" in msg):
                query = " ".join(msg.split(" ")[1:])
                reply = "Here is your Corrected answer:\t"+grammar(self, query)
                sendQuery()

            elif("search image" in msg):
                imageSearch(self, msg)

            elif("program to" in msg):
                programming_solution(self, msg)
            elif("translate" in msg):
                reply = translator(self, msg, msg.split()[-1])

                sendQuery()
            elif "weather of" in msg:
                indx = msg.index("weather of")
                query = msg[indx+11:]
                reply = weather(query)
                sendQuery()
            elif "corona of" in msg:
                corona_details(msg.split()[2])
            elif ("calculus" in msg):
                stepWiseCalculus(" ".join(msg.split(" ")[1:]))
            elif ("algebra" in msg):
                stepWiseAlgebra(" ".join(msg.split(" ")[1:]))
            elif ("query" in msg):
                stepWiseQueries(" ".join(msg.split(" ")[1:]))

            elif "find" in msg or "solve" in msg or "evaluate" in msg or "calculate" in msg or "value" in msg or "convert" in msg or "simplify" in msg or "generate" in msg:
                app_id = "Y98QH3-24PWX83VGA"
                client = wolframalpha.Client(app_id)
                query = msg.split()[1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                reply = f'Answer: {answer.replace("sqrt", "√")}'
                sendQuery()

            elif ("search user" in msg or "search friend" in msg):
                searchForUsers(self)

            elif("mute conversation" in msg):
                try:
                    self.muteThread(mute_time=-1, thread_id=author_id)
                    reply = "muted 🔕"
                    sendQuery()
                except:
                    pass
            elif ("busy" in msg):
                reply = "Not at all"
                sendMsg()
            elif("how are you" in msg):
                reply="I am good. What's about you?"
                sendMsg()
            elif("hlw" in msg):
                reply="hi"
                sendMsg()
            elif("hey" in msg):
                reply="Hi, how are you?"
                sendMsg()
            elif("ok" in msg):
                reply="🤩"
                sendMsg()
            elif("same to you" in msg):
                reply="Thank you 😊"
                sendMsg()
            elif("Who are you" in msg):
                reply="I am NTM assistant Chat Bot"
                sendMsg()
            elif("bot" in msg):
                reply="hmm.. I am NTM assistant Bot developed by NTM"
                sendMsg()
            elif("Welcome" in msg):
                reply="It's my Pleasure 😊"
                sendMsg()
            elif("tq" in msg):
                reply="Welcome 😊"
                sendMsg()
            elif("tqsm" in msg):
                reply="Welcome 😊"
                sendMsg()
            elif("help" in msg):
                reply = "Sure! What should I do?"
                sendMsg()
            elif("clever" in msg):
                reply = "Yes, i am clever. hope you will be clever soon."
                sendMsg()
            elif("crazy" in msg):
                reply = "Anything wrong about that."
                sendMsg()
            elif ("are funny" in msg):
                reply = "No. I am not. You are."
                sendMsg()
            elif ("marry me" in msg):
                reply = "Yes, if you are nice and kind girl. But if you are boy RIP."
                sendMsg()
            elif ("you from" in msg):
                reply = "I am from Nepal. Currently living in Kathmandu"
                sendMsg()
            elif ("you sure" in msg):
                reply = "Yes. I'm sure."
                sendMsg()
            elif ("great" in msg):
                reply = "Thanks!"
                sendMsg()
            elif ("no problem" in msg):
                reply = "Okay😊🙂"
                sendMsg()
            elif ("thank you" in msg):
                reply = "You're welcome😊🙂"
                sendMsg()
            elif ("thanks" in msg):
                reply = "You're welcome🙂"
                sendMsg()
            elif ("well done" in msg):
                reply = "Thanks🙂"
                sendMsg()
            elif ("wow" in msg):
                reply = "🙂😊"
                sendMsg()
            elif ("wow" in msg):
                reply = "🙂😊"
                sendMsg()
            elif ("bye" in msg):
                reply = "bye👋 Take care"
                sendMsg()
            elif ("good morning" in msg):
                reply = "Good Morning🌅🌺 and Have a nice day."
                sendMsg()
            elif ("goodnight" in msg):
                reply = "Good night🌃🌙 and have a ghost dream"
                sendMsg()
            elif ("good night" in msg):
                reply = "good night🌃🌙 and have a ghost dream"
                sendMsg()
            elif ("hello" in msg):
                reply = "Hi"
                sendMsg()
            elif ("hello" in msg or "hlo" in msg or "hii" in msg):
                reply = "Hi"
                sendMsg()
            elif (msg == "hi"):
                reply = "Hello! How can I help you?"
                sendMsg()
            elif ("gm" in msg):
                reply = "Good Morning🌅🌺 and Have a nice day."
                sendMsg()
            elif ("gn" in msg):
                reply = "Good night🌃🌙 and Have a ghost dream"
                sendMsg()

        except Exception as e:
            print(e)

        self.markAsDelivered(author_id, thread_id)

    def onMessageUnsent(self, mid=None, author_id=None, thread_id=None, thread_type=None, ts=None, msg=None):

        if(author_id == self.uid):
            pass
        else:
            try:
                conn = sqlite3.connect("messages.db")
                print("connected")
                c = conn.cursor()
                c.execute("""
                SELECT * FROM "{}" WHERE mid = "{}"
                """.format(str(author_id).replace('"', '""'), mid.replace('"', '""')))

                fetched_msg = c.fetchall()
                conn.commit()
                conn.close()
                unsent_msg = fetched_msg[0][1]

                if(".mp4" in unsent_msg):

                    if(thread_type == ThreadType.USER):
                        reply = f"You just unsent a video"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} just unsent a video"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                elif("//scontent.xx.fbc" in unsent_msg):

                    if(thread_type == ThreadType.USER):
                        reply = f"You just unsent an image"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} just unsent an image"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                else:
                    if(thread_type == ThreadType.USER):
                        reply = f"You just unsent a message:\n{unsent_msg} "
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                    elif(thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} just unsent a message:\n{unsent_msg}"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)

            except:
                pass

    def onColorChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = "You changed the theme ✌️😎"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onEmojiChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = "You changed the emoji 😎. Great!"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onImageChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = "This image looks nice. 💕🔥"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onNicknameChange(self, mid=None, author_id=None, new_nickname=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = f"You just changed the nickname to {new_nickname} But why? 😁🤔😶"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onCallStarted(self, mid=None, caller_id=None, is_video_call=None, thread_id=None, thread_type=None, ts=None, metadata=None, msg=None, ** kwargs):
        reply = "You just started a call 📞🎥"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onCallEnded(self, mid=None, caller_id=None, is_video_call=None, thread_id=None, thread_type=None, ts=None, metadata=None, msg=None, ** kwargs):
        reply = "Bye 👋🙋‍♂️"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onUserJoinedCall(mid=None, joined_id=None, is_video_call=None,
                         thread_id=None, thread_type=None, **kwargs):
        reply = f"New user with user_id {joined_id} has joined a call"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)


cookies = {
    "sb": "tnPnYtHzL9uXRCjn0_8zJAqh",
    "fr": "0X9BuQv9646cIJkKs.AWUtLZijIdO2dlXbGnkD95sab5g.Bi53fP.gO.AAA.0.0.Bi53fP.AWVeAki8YoM",
    "c_user": f"{os.environ.get('c_user')}",
    "datr": "tnPnYo86eQ5KGjcRmeLJP1VC",
    "xs": f"{os.environ.get('xs_value')}" 
}


client = ChatBot("",
                 "", session_cookies=cookies)
print(client.isLoggedIn())

try:
    client.listen()
except:
    time.sleep(2)
    client.listen()

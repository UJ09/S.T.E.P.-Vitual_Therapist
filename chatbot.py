from flask import Flask, request
#from flask_ngrok import run_with_ngrok
import text2emotion as te
import random

# global level
cur_emotion = []
level = 0

def get_happy_message_1():
    happy_sentences = [
        "You've made great progress!",
        "You are surrounded by people who care about you!",
        "Your hard work is paying off!",
        "You bring joy to those around you!",
        "You have a bright future ahead!",
        "You should be proud of yourself!",
        "You have a lot of amazing qualities!",
        "You have the power to create your own happiness!",
        "You are making a positive impact in the world!",
        "You are important and valued!",
        "You have so much to look forward to!"
    ]
    return "That's great to hear! " + random.choice(happy_sentences)

def get_angry_message():
    angey_sentences = [
    "I understand how you feel,and I'm sorry that any action caused you to become angry.",
    "Let's take a step back and try to calmly discuss the issue with your close ones.",
    "I apologize for any hurtful things that happens with you.",
    "I understand that you're upset, but getting angry and yelling won't solve the problem.",
    "I value your input, you should talk to your close ones to address your concerns."
    ]

    return random.choice(angey_sentences)

def get_surprise_message():
    surprise_sentences=[
    "I'm speechless! This is such a pleasent thing to hear!",
    "Wow,Oh my goodness, I can't believe it!",
    "This is amazing! Thank you so much!",
    "I'm blown away! This is such a thoughtful gesture.",
    "Wow great! I feel happy for you.",
    "This is wonderful to hear!"
    ]
    return random.choice(surprise_sentences)


def get_sad_message_1():
    sad_sentences = [
        "I'm sorry you're feeling down.",
        "It's okay to not be okay.",
        "Remember that things will get better.",
        "You are not alone in how you feel.",
        "You are stronger than you realize.",
        "Take care of yourself and be kind to yourself.",
        "It's okay to ask for help.",
        "You are loved and valued.",
        "You can get through this.",
        "Take things one step at a time.",
        "Remember that it's okay to take a break.",
    ]
    return "I'm sorry to hear that." + random.choice(sad_sentences)


def get_sad_message_2():
    sad_sentences = [
    "I'm sorry you're going through a tough time. Is there anything I can do to help?",
    "Remember that you're not alone. Would you like to talk about some ways to cope with your sadness?",
    "It's understandable to feel sad right now. Let's work together to find some ways to lift your mood.",
]

    return random.choice(sad_sentences)


def get_sad_message_3():
    sad_Sentences = [
    "I'm sorry you're feeling so low. Have you considered speaking with a therapist or counselor?",
    "It sounds like your sadness is affecting your daily life. Let's discuss some options for professional help.",
    "It's important to take care of your mental health. Let's work together to find a qualified mental health professional.",
]
    return random.choice(sad_Sentences)

def get_fear_message_1():
    fear_sentences = [
        "It's normal to feel scared sometimes.",
        "You are stronger than your fears!",
        "Remember that you can overcome this!",
        "Take deep breaths and try to stay calm.",
        "Fear is just a feeling, it can't control you!",
        "You have faced your fears before, you can do it again!",
        "It's okay to ask for help if you need it.",
        "You can take small steps to face your fears.",
        "Remember that you are not alone in feeling scared.",
        "Courage is not the absence of fear, but the ability to face it.",
        "You are capable of handling whatever comes your way!"
    ]
    return "It's okay to feel scared. " + random.choice(fear_sentences)

def get_fear_sad_message():
    fear_sad_sentences = [
    "It's okay to be afraid of what's coming next, but remember that you have the strength to face it.",
    "You might feel like the darkness is closing in, but I promise you that the light is always there, waiting for you to reach for it.",
    "It's okay to feel scared and sad at the same time. Take your time to process your emotions and remember that you have the power to overcome them.",
    "You are not alone in feeling this way. There are people who care about you and want to help you through this.",
    "It's normal to feel overwhelmed by fear and sadness, but remember that you are stronger than both of those emotions.",
    "You might feel like you're drowning in your fears and sadness, but I'm here to remind you that you have the power to swim to the surface.",
    "It's okay to feel like you're not okay. Just remember that you don't have to face your fears and sadness alone.",
    "I know that fear and sadness can be overwhelming, but I believe in you. You have the power to overcome them.",
    "It's okay to be scared of the unknown, but remember that there are also opportunities and possibilities waiting for you.",
    "You might feel like you're trapped in a maze of fear and sadness, but I promise you that there's a way out. You just have to keep going."
]
    return "It's okay to feel scared. " + random.choice(fear_sad_sentences)

def get_res(user_emotion):
    bot_message = ''
    global cur_emotion
    global level 
    if user_emotion == "Sad":
        if len(cur_emotion) > 0 and cur_emotion[-1] == "Sad":
            level += 1
        else:
            level = 1

        if level == 1:
            bot_message =  get_sad_message_1()
        elif level == 2:
            bot_message =  get_sad_message_2()
        else :
            bot_message =  get_sad_message_3()

    elif user_emotion == "Happy":
        bot_message =  get_happy_message_1()
    elif user_emotion == "Fear":
        bot_message = get_fear_message_1()
    elif user_emotion == "sad and scared":
        bot_message = get_fear_message_1()
    elif user_emotion == "Angry":
        bot_message = get_angry_message()
    elif user_emotion == "Surprise":
        bot_message = get_surprise_message()
    else:
        bot_message = "I'm not sure what you mean. Can you please rephrase your message?"
    
    cur_emotion.append(user_emotion)
    return bot_message

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        return "We are not connected to Dialogflow"


@app.route("/", methods=["POST"])
def webhook():
    payload = request.json
    user_response = (payload['queryResult']['queryText'])

    print("User: "+user_response)
    text = user_response
    result = te.get_emotion(text)
    tot = 0
    for r in result:
        if result[r] > 0:
            tot += result[r]
            print(r)
    fulfillmentText = "No text I guess"
    if tot == 0:
        fulfillmentText = "The feeling is neutral"
    else :
        print(fulfillmentText)
        print(type(result))
        res = {key: val for key, val in sorted(
            result.items(), key=lambda ele: ele[1], reverse=True)}
        print(type(res))
        l = list(res.keys())
        print(type(l),type(get_res))
        print(l[0])
        fulfillmentText = get_res(l[0])
        print(fulfillmentText)
    print("User: "+user_response)
    return {'fulfillmentText': fulfillmentText
            }


if __name__ == "__main__":
    app.run()

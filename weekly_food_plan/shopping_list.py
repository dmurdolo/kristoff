#!/usr/bin/python3

import yaml
import random
import smtplib
from email.message import EmailMessage

meals = []
shopping_list = {}
recipes = yaml.safe_load(open("recipes.yaml"))
regulars = open("regulars.txt")
recipients = ["luke.blakey@gmail.com", "hmjstath@gmail.com"]
kristoff_open = "Bonjour, Kristoff here. Here's your shopping plan for this week:\n"


def create_meal_plan():
    while len(meals) != 5:
        random_meal = random.choice(list(recipes))
        if random_meal not in meals:
            meals.append(random_meal)
    schedule = "\nMonday: " +  meals[0] + "\nTuesday: " + meals[1] + "\nWednesday: " + meals[2] + "\nThursday: " + meals[3] + "\nFriday: " + meals[4] + "\n"

    return schedule


def create_shopping_list(meals):
    for meal in meals:
        for ingredient, quantity in recipes[meal].items():
            if ingredient in shopping_list and shopping_list[ingredient][1] == quantity[1]:
                shopping_list[ingredient][0] = shopping_list[ingredient][0] + quantity[0]
            else:
                shopping_list[ingredient] = []
                shopping_list[ingredient].append(quantity[0])
                shopping_list[ingredient].append(quantity[1])

    # convert to readable string
    shopping_list_string = ""
    for k, v in sorted(shopping_list.items()):
        shopping_list_string = shopping_list_string + k + " (" + str(v[0]) + " " + v[1] + ")\n"

    return shopping_list_string


def email(content):
    for address in recipients:
        msg = EmailMessage()
        msg.set_content(content)
        msg["Subject"] = "Weekly Shop"
        msg["From"] = "Kristoff"
        msg["To"] = address
        mail = smtplib.SMTP("localhost")
        mail.send_message(msg)
        mail.quit


content = kristoff_open + create_meal_plan() + "\nBuy these things:\n" + create_shopping_list(meals) + "\nDon't forget the regulars!\n" + regulars.read() + "\nKristoff out."
email(content)

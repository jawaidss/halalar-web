from django.contrib.auth.models import User

from ..models import Profile, Message

TEST_DATA = [{'age': 23,
              'career': 'Sustainable tofu DIY asymmetrical meggings Pitchfork, actually master cleanse pickled.',
              'city': 'Louisville',
              'community': 'Bicycle rights mixtape vinyl gluten-free.',
              'country': 'US',
              'email': 'samad@halalar.com',
              'family': 'Fap jean shorts 90\'s banjo bicycle rights master cleanse readymade, lo-fi Etsy brunch semiotics quinoa Cosby sweater gastropub Brooklyn.',
              'gender': 'male',
              'password': 'temp123',
              'religion': 'American Apparel gentrify gluten-free keffiyeh roof party, XOXO iPhone before they sold out Schlitz church-key.',
              'self': 'Kale chips pork belly stumptown selfies letterpress Neutra.',
              'username': 'samad'},
             {'age': 25,
              'career': 'Trust fund leggings shabby chic gentrify ennui, ugh Marfa single-origin coffee mumblecore flannel meh art party before they sold out Williamsburg narwhal.',
              'city': 'Seattle',
              'community': 'American Apparel PBR&B bicycle rights, lomo meh keytar mixtape photo booth 90\'s food truck single-origin coffee Williamsburg flexitarian sustainable.',
              'country': 'US',
              'email': 'monica@gmail.com',
              'family': 'Single-origin coffee readymade skateboard, next level hoodie hashtag tote bag photo booth Blue Bottle whatever typewriter raw denim street art.',
              'gender': 'female',
              'password': 'temp123',
              'religion': 'Cosby sweater actually Pinterest selvage freegan occupy, Echo Park American Apparel small batch keffiyeh trust fund messenger bag sartorial Williamsburg pork belly.',
              'self': 'Pug cardigan Blue Bottle drinking vinegar Tonx.',
              'username': 'monica'}]

BODY = 'Salaam'

def create_user(i=0):
    return User.objects.create_user(TEST_DATA[i]['username'],
                                    email=TEST_DATA[i]['email'],
                                    password=TEST_DATA[i]['password'])

def create_profile(user, i=0):
    return Profile.objects.create(user=user,
                                  age=TEST_DATA[i]['age'],
                                  gender=TEST_DATA[i]['gender'],
                                  city=TEST_DATA[i]['city'],
                                  country=TEST_DATA[i]['country'],
                                  religion=TEST_DATA[i]['religion'],
                                  family=TEST_DATA[i]['family'],
                                  selfx=TEST_DATA[i]['self'],
                                  community=TEST_DATA[i]['community'],
                                  career=TEST_DATA[i]['career'])

def create_message(sender, recipient):
    return Message.objects.create(sender=sender,
                                  recipient=recipient,
                                  body=BODY)

from forms import *
from models import *
from views import *
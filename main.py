import json
import tweepy
import pygame
import random
import instaloader
import urllib.request
from settings import *

def makeRectText(x, y, message, size):
    FONT = pygame.font.Font(VIEW_FONT, size)
    text_Title = FONT.render('{:,}'.format(int(message)), True, WHITE)
    text_Rect = text_Title.get_rect()
    text_Rect.centerx = round(SCREEN_WIDTH / 4.4)
    text_Rect.x = x
    text_Rect.y = y
    screen.blit(text_Title, text_Rect)

def request_Youtube_API():
    channel_data = urllib.request.urlopen(YOUTUBE_CHANNEL_URL.format(YOUTUBE_ID, YOUTUBE_KEY)).read()
    subs = json.loads(channel_data)['items'][0]['statistics']['subscriberCount']
    return subs


pygame.init()
pygame.display.set_caption(TITLE)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
background_image = pygame.image.load(BACKGROUND)

start_ticks = pygame.time.get_ticks()
prv_seconds = 0

insta = instaloader.Instaloader()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

bp_subs = request_Youtube_API()
bp_prior_subs = str(int(bp_subs) + 69336)
cnt = 1

while True:
    seconds = (pygame.time.get_ticks()-start_ticks)/1000

    screen.blit(background_image, (0, 0))

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break


    # 인스타 데이터 가져오기
    if int(seconds) % 600 == 0:
        profile = instaloader.Profile.from_username(insta.context, INSTA_ID)
        insta_follower_cnt = profile.followers
        print("insta followers: ", insta_follower_cnt)

    # 유튜브 데이터 가져오기
    if int(seconds) % 300 == 0:
        bp_subs = request_Youtube_API()
        cnt = 1

        if int(bp_prior_subs) > int(bp_subs) + 100000:
            bp_prior_subs = str(int(bp_prior_subs) - random.randint(20000, 40000))
            print('blackpink down')

    # 트위터 데이터 가져오기 
    if int(seconds) % 120 == 0:
        user = api.get_user(TWITTER_ACCOUNT)
        twit_follower_cnt = user.followers_count


    makeRectText(POSITIONS[0][0], POSITIONS[0][1], insta_follower_cnt, 48)
    makeRectText(POSITIONS[1][0], POSITIONS[1][1], bp_prior_subs, 48)
    makeRectText(POSITIONS[2][0], POSITIONS[2][1], twit_follower_cnt, 48)

    if int(prv_seconds * 5) != int(seconds * 5):
        insta_follower_cnt += random.choice([0]*5 + list(range(0, 2)))

    if int(prv_seconds * 5) != int(seconds * 5):
        twit_follower_cnt += random.choice([0]*50 + list(range(0, 2)))
    
    if bp_prior_subs < bp_subs:
        bp_prior_subs = bp_subs

    if int(prv_seconds * 5) != int(seconds * 5):
        bp_prior_subs = str(random.randint(int(bp_prior_subs), int(bp_prior_subs)+random.choice([0]*9 + list(range(0, 2)))))

    if int(prv_seconds) != int(seconds):
        cnt += 1
    
    if cnt > 10:
        bp_prior_subs = str(random.randint(int(bp_prior_subs) - 1, int(bp_prior_subs)))
        cnt = 1

    pygame.display.update()
    clock.tick(10)

    
    prv_seconds = seconds

pygame.quit()

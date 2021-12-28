# Usage:
# - Specify discord user IDs within the id_whitelist [] or within config.json
# - Add discord API token by reassigning the alt_token variable or adding the token to config.json 
#
# Commands: 
#   .banimg <ID> 
# Whitelisted users can use the command in the Discord server `.banimg <message ID containing the image>`. This image will be downloaded and saved to the banned_images directory.
# Subsequent discord events (messages) will be checked for all images within the ban_images directory
#
# 

# @TODO: Implement a decerator/wrapper for the blocking functions to avoid heartbeat timeouts 


from skimage.metrics import structural_similarity
from skimage.transform import resize
import cv2
import uuid
import os
import discord
import json
import sys
import logging
import warnings
from colorama import Fore, Style, init
init(autoreset=True)
warnings.filterwarnings("ignore")


logger = logging.getLogger(__name__)
logging.basicConfig(filename="imgdelete.logs", filemode='a',level=logging.WARNING, format='%(asctime)s: %(message)s')
img_path = ""
id_whitelist = [] # Who can run .banimg
alt_token = ""
client = discord.Client()

with open("config.json", "r") as config:

    configs = json.load(config)
    if configs.get("discord_token") and not alt_token:
        alt_token = configs.get("discord_token")
    else:
        logger.warning(Fore.RED + "Token not found")
        sys.exit(1)
    if configs.get("cmd_whitelist") or id_whitelist:
        if len(id_whitelist) < len(configs.get("cmd_whitelist")):
            id_whitelist = configs.get("cmd_whitelist")
    else:
         logger.warning(Fore.RED + "You must create a whitelist, else nobody will be able to run commands")
    if configs.get("image_directory") and not img_path:
        img_path = configs.get("image_directory")
    if not configs.get("image_directory") and not img_path:
        logger.warning(Fore.RED + "You must specify a directory for the banned images to be saved to.")
        sys.exit(1)




def directory_handler():
    pass

def orb_sim(banned_img, sus_img):

  orb = cv2.ORB_create()
  banned_keypoint, banned_descriptor = orb.detectAndCompute(banned_img, None)
  sus_keypoint, sus_descriptor = orb.detectAndCompute(sus_img, None)

  bruteforce = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
  matches = bruteforce.match(banned_descriptor, sus_descriptor)
  matching_regions = [i for i in matches if i.distance < 50]
  if len(matches) == 0:
    return 0
  return len(matching_regions) / len(matches)


def structural_sim(banned_img, sus_img):

    resized_img = resize(banned_img, (sus_img.shape[0], sus_img.shape[1]), anti_aliasing=True, preserve_range=True)
    sim, diff = structural_similarity(resized_img, sus_img, full=True, multichannel=True)
    return sim


def rotate_image(img):

    rotated_images = []
    for degrees in range(30, 300, 30):
        img_center = (img.shape[0] / 2,  img.shape[1] / 2)
        M = cv2.getRotationMatrix2D(img_center, degrees, 1.0)
        rotated_images.append(cv2.warpAffine(img, M, (img.shape[0], img.shape[1])))
    return rotated_images

def make_ban_decision(orb, ssim): # Return true if ban

    if ssim >= 0.70:
        logger.warning(Style.BRIGHT + "Similarity detected using SSIM is: {}".format(ssim))
        return True
    if orb >= 0.70:
        logger.warning(Style.BRIGHT + "Similarity detected using orb is: {}".format(orb))
        return True
    return False




@client.event
async def on_ready():  # method expected by client. This runs once when connected
    logger.warning("Began monitoring as the user {}".format(client.user))  # notification of login.')

# Listening for "events", Discord messages
# Two events we are looking for:
# 1. A message containing ".banimg", a way of adding images to the banned list on the fly
# 2. A message containing a banned image

@client.event
async def on_message(message):

    # each message has a bunch of attributes. Here are a few.
    # check out more by print(dir(message)) for example.
    if message.content.startswith(".banimg") and message.author.id in id_whitelist:
        msg_id = message.content.split()[1]
        msg_target = await message.channel.fetch_message(msg_id)
        author = msg_target.author.id
        for attachment in msg_target.attachments:
            fname = str(uuid.uuid4())
            await attachment.save("{}{}".format(img_path,fname))
        await msg_target.delete()
        logger.warning(Style.BRIGHT + "{} has banned the image {} from {}".format(message.author, fname, msg_target.author))
    else:
        if message.attachments:
            for attachment in message.attachments:
                tmp_fname = "/tmp/{}".format(str(uuid.uuid4()))
                await attachment.save(tmp_fname)
                suspect_img = cv2.imread(tmp_fname)
                os.remove(tmp_fname)
                for x in os.listdir(img_path):
                    banned_img = cv2.imread(img_path + x)
                    if make_ban_decision(orb_sim(banned_img, suspect_img), structural_sim(banned_img, suspect_img)):
                        logger.warning(Fore.RED + "Deleting image with message ID {}".format(message.id))
                        await message.delete()
                        break
                    else:
                        for rotated_img in rotate_image(suspect_img):
                            if make_ban_decision(orb_sim(banned_img, rotated_img), structural_sim(banned_img, rotated_img)):
                                logger.warning(Fore.RED + "Deleting image with message ID {}".format(message.id))
                                await message.delete()
                                break
try:
    client.run(alt_token)
except discord.errors.HTTPException and discord.errors.LoginFailure as e:
    logger.warnings(Sytle.RED + "Failed to authenticate to Discord. Check the token within config.json. It will overwrite hardcoded values.")

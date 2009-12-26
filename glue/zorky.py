from waveapi import events
from waveapi import model
from waveapi import robot

import zorkyconn

NAME = "playzorky"
ROOT = "http://%s.appspot.com" % NAME

title = ""

def send_cmd (wave_id, command):
    "Make zorkyconn.send_cmd()'s output nice"

    response = zorkyconn.send_cmd (wave_id, command)

    return response['content']

def start (wave_id, game_name):
    "Make zorkyconn.start()'s output nice"

    response = zorkyconn.start (wave_id, game_name)

    return response['content']

def game_list ():
    "Make zorkyconn.game_list()'s output nice"

    return ("Possible games (choose one by starting a blip with \"/game " +
            "<name>\"):\n" + '\n'.join (map (lambda s: s.strip(".z5"),
                                             zorkyconn.game_list()['names'])))

def struck (annos):
    struck_out = False
    for a in annos:
        if a.name == "style/textDecoration" and a.value == "line-through" \
               and a.range.start == 0:
            struck_out = True
    return struck_out

def add_blip (context, string):
    new_blip = context.GetRootWavelet().CreateBlip()
    new_blip.GetDocument().SetText (str(string))

def self_added (properties, context):
    root_text = context.GetBlipById(context.GetRootWavelet().GetRootBlipId()).GetDocument().GetText()
    game = "list"
    for line in root_text.split("\n"):
        if line.lower().find ("/game") != -1:
            game = line[5:].strip()
            break
        elif line.lower().find ("/list") != -1:
            game = "list"
            break

    if game == "list":
        add_blip (context, game_list())
    else:
        initial_string = start (context.GetRootWavelet().GetWaveId(), game)
        add_blip (context, "Playing %s\n\n%s" % (game, initial_string))

def blip_submitted (properties, context):
    blip = context.GetBlipById (properties["blipId"])
#    all_blips = context.GetBlipById(context.GetRootWavelet().GetRootBlipId()).GetChildBlipIds()
    text = blip.GetDocument().GetText()
    annos = blip.GetAnnotations()
    if text[0] == ">":
        if not struck (annos):
            command = (text.split ("\n")[0])[1:].strip()
            response = send_cmd (context.GetRootWavelet().GetWaveId(), command)
            add_blip (context, "> %s\n%s" % (command, response))
    elif text[0] == "/":
        if not struck (annos):
            command = (text.split ("\n")[0])[1:].strip()
            if command[:4] == "game":
                game = command[5:].strip()
                initial_string = start (context.GetRootWavelet().GetWaveId(),
                                        game)
                add_blip (context, "Playing %s\n\n%s" % (game, initial_string))
            
if __name__ == "__main__":

    self_robot = robot.Robot (NAME,
                           image_url="%s/assets/icon.png" % ROOT,
                           version="1",
                           profile_url=ROOT)

    self_robot.RegisterHandler (events.WAVELET_SELF_ADDED, self_added)
    self_robot.RegisterHandler (events.BLIP_SUBMITTED, blip_submitted)

    self_robot.Run ()

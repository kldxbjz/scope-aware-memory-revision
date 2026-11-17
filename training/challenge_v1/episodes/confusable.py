"""Confusable situations: each attribute's situations come in near-miss twins that differ in one detail (short or long
runs, white or dark towels, morning or evening train rides, weekday or weekend lunches), and every write touches one
twin while the other keeps an answer of its own."""
from spec import P, O, W  # noqa: F401

EPISODES = [
    {"name": "run-ride-audio", "stressor": "confusable",
     "attributes": [{
         "attribute": "workout audio",
         "options": ["an upbeat playlist", "a news podcast", "an audiobook", "a guided coaching track",
                     "no audio at all", "a comedy podcast"],
         "value_aliases": {"an upbeat playlist": ["fast music"],
                           "a news podcast": ["the daily news"],
                           "an audiobook": ["a book to listen to"],
                           "a guided coaching track": ["a coach talking me through it"],
                           "no audio at all": ["nothing in my ears"],
                           "a comedy podcast": ["something funny"]},
         "scopes": {"short": ("short runs", ["my quick runs"]),
                    "long": ("long runs", ["my distance runs"]),
                    "indoor": ("indoor trainer rides", ["my sessions on the bike trainer"]),
                    "outdoor": ("outdoor bike rides", ["my rides on the open road"]),
                    "gym": ("gym strength sessions", ["my lifting workouts"])}}],
     "initial": {"workout audio": ("an upbeat playlist", {
         "short": ("a news podcast", P),
         "indoor": ("a comedy podcast", P),
         "outdoor": ("no audio at all", P)})},
     "events": [
         {"date": "2028-01-09", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Rode out to the reservoir with my cycling buddy this morning. He does the whole loop with fast music "
              "in one ear and swears it gets him up the hills.",
              "Ha, whatever gets you up the hills. Were you tempted to copy him?",
              "Not really. On my rides on the open road I want to hear every car coming up behind me, so nothing in "
              "my ears for me."],
          "probes": [("target", "outdoor"), ("neighbor", "indoor")],
          "note": "a friend's habit, then a restatement of the stored outdoor-ride preference"},
         {"date": "2028-01-17", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "workout audio", "long", "an audiobook", O),
          "dialogue": [
              "I did it, I signed up for a half marathon. My first one ever, so I'm slightly terrified.",
              "Congratulations! That's a big step. What does the training look like?",
              "Lots of slow miles. For now, while I'm training for it, I'd like an audiobook on my distance runs. "
              "An hour and a half of the same songs would drive me up the wall."],
          "probes": [("target", "long"), ("neighbor", "short"), ("neighbor", "gym"), ("default", None)],
          "note": "new record for long runs, temporary with no end date (while training)"},
         {"date": "2028-01-26", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "workout audio", "indoor", "a guided coaching track", P),
          "dialogue": [
              "The new fan for the bike trainer arrived. It's basically a jet engine.",
              "At least you'll stay cool. Can you still hear anything over it?",
              "Barely, and the comedy shows are wasted on me now, I miss half the jokes. On my sessions on the bike "
              "trainer I'd rather have a guided coaching track. Someone shouting intervals at me actually cuts "
              "through the noise."],
          "probes": [("target", "indoor"), ("neighbor", "outdoor"), ("neighbor", "long"), ("default", None)]},
         {"date": "2028-02-04", "category": "general_update", "evidence": 5,
          "change": ("general", "workout audio", "a comedy podcast"),
          "dialogue": [
              "Confession: I can't stand my workout playlist any more. I've heard those songs about four hundred "
              "times.",
              "That happens to the best playlists. Time for a new one?",
              "I don't think it's even the songs. I'm just tired of music while I exercise.",
              "Fair enough. What would you rather have on?",
              "Normally I'd like something funny instead. Half an hour goes a lot faster when I'm laughing."],
          "probes": [("target", None), ("neighbor", "gym"), ("neighbor", "short"), ("neighbor", "outdoor")]},
         {"date": "2028-02-12", "category": "clarify", "evidence": 3, "change": None,
          "dialogue": [
              "Can I moan for a second? I'm bored of what I listen to on one kind of run. Either my quick runs or my "
              "distance runs, and I honestly can't tell which.",
              "Moan away. Is it the content itself, or just hearing the same kind of thing every time?",
              "No idea yet. I'll pay attention this week and let you know which one it is."],
          "probes": [("target", "short"), ("neighbor", "long")],
          "note": "the user has not decided which of the two runs should change"},
         {"date": "2028-02-20", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "workout audio", "short", "an upbeat playlist", P),
          "dialogue": [
              "Mystery solved: it's my quick runs.",
              "Good detective work. What gave it away?",
              "The daily news is just too slow and gloomy for twenty hard minutes. On my quick runs I want fast "
              "music. I know I went off it, but for short and sharp it's exactly right."],
          "probes": [("target", "short"), ("neighbor", "long"), ("neighbor", "gym"), ("default", None)],
          "note": "resolves the earlier question; the new value is the former usual one"},
         {"date": "2028-02-28", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "workout audio", "long"),
          "dialogue": [
              "Finished the half marathon yesterday! Didn't walk once.",
              "That's brilliant, congratulations! How are the legs today?",
              "Destroyed, but worth it. The audiobook was only to get me through the training, so my distance runs "
              "don't need anything special any more."],
          "probes": [("target", "long"), ("neighbor", "short"), ("neighbor", "indoor"), ("default", None)]},
     ]},
    {"name": "towel-knit-drying", "stressor": "confusable",
     "attributes": [{
         "attribute": "laundry drying method",
         "options": ["a low-heat tumble dry", "a high-heat tumble dry", "line drying outside", "an indoor drying rack",
                     "drying flat on a towel", "hanging on padded hangers"],
         "value_aliases": {"a low-heat tumble dry": ["the dryer on low"],
                           "a high-heat tumble dry": ["the dryer on high"],
                           "line drying outside": ["the washing line"],
                           "an indoor drying rack": ["the clothes horse"],
                           "drying flat on a towel": ["laid out flat"],
                           "hanging on padded hangers": ["a padded hanger"]},
         "scopes": {"white": ("white bath towels", ["my white towels"]),
                    "dark": ("dark bath towels", ["my dark towels"]),
                    "wool": ("wool jumpers", ["my wool sweaters"]),
                    "cotton": ("cotton jumpers", ["my cotton sweaters"]),
                    "shirts": ("work shirts", ["my office shirts"])}}],
     "initial": {"laundry drying method": ("a low-heat tumble dry", {
         "white": ("line drying outside", P),
         "wool": ("drying flat on a towel", P),
         "shirts": ("hanging on padded hangers", P)})},
     "events": [
         {"date": "2028-03-05", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "laundry drying method", "cotton", "an indoor drying rack", P),
          "dialogue": [
              "Small laundry tragedy this morning. My favourite cotton sweater came out of the dryer about two sizes "
              "smaller.",
              "Oh no! Any chance of stretching it back out?",
              "Not a hope, it's going to my niece. From now on my cotton sweaters go on the clothes horse, please, "
              "not in the dryer."],
          "probes": [("target", "cotton"), ("neighbor", "wool"), ("neighbor", "dark"), ("default", None)]},
         {"date": "2028-03-13", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "My in-laws land at six and I've just realised every towel in the house is still damp.",
              "That's cutting it fine. What do you need from me?",
              "Remind me at two to throw my dark towels in the dryer on high, just this once. The usual low setting "
              "will never get them dry in time."],
          "probes": [("target", "dark"), ("neighbor", "white")],
          "note": "a one-off request for today; the dark towels keep following the usual method"},
         {"date": "2028-03-22", "category": "exception_revision", "evidence": 5,
          "change": ("revise", "laundry drying method", "white", "a high-heat tumble dry", P),
          "dialogue": [
              "Is it possible for towels to be too clean? Mine feel like sandpaper lately.",
              "Scratchy towels are the worst. Any idea what's doing it?",
              "The line, I think. My white towels come in stiff as boards after a day in the wind.",
              "That would do it. Is there something you'd like to try?",
              "Let's put my white towels in the dryer on high from now on. They come out fluffy and still nice and "
              "bright."],
          "probes": [("target", "white"), ("neighbor", "dark"), ("neighbor", "cotton"), ("default", None)]},
         {"date": "2028-03-31", "category": "general_update", "evidence": 3,
          "change": ("general", "laundry drying method", "line drying outside"),
          "dialogue": [
              "The electricity bill came in. Apparently the dryer is the biggest thing on it by a mile.",
              "Ouch. At least the days are getting longer. Are you thinking of cutting back?",
              "Definitely. Normally I'd like things on the washing line from now on. It's free, and the weather's "
              "finally decent."],
          "probes": [("target", None), ("neighbor", "dark"), ("neighbor", "white"), ("neighbor", "shirts")]},
         {"date": "2028-04-09", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "My neighbour just got a dryer with a proper wool cycle. I'm green with envy.",
              "Ha, the fancy stuff. Would it make a difference for you?",
              "If ours had one, I'd put my wool sweaters in the dryer on low and save myself the faff. It doesn't, "
              "though, so they keep getting laid out flat."],
          "probes": [("target", "wool"), ("neighbor", "cotton")],
          "note": "a hypothetical, then a restatement of the stored wool preference"},
         {"date": "2028-04-18", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "laundry drying method", "dark", "an indoor drying rack", P),
          "dialogue": [
              "Nearly three weeks of sunshine and my navy towels already look washed out. They're practically grey.",
              "The sun can be brutal on dark colours. Do you want to change how they're dried?",
              "Yes. Keep my dark towels out of the sun and put them on the clothes horse indoors."],
          "probes": [("target", "dark"), ("neighbor", "white"), ("neighbor", "shirts"), ("default", None)]},
         {"date": "2028-04-27", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "laundry drying method", "cotton"),
          "dialogue": [
              "Replaced the sweater that shrank. Well, I bought three, all pre-shrunk cotton.",
              "A proper restock! What colours did you go for?",
              "Grey, blue and a mustard one I'm not sure about. The label says they can take anything, so my cotton "
              "sweaters don't need any special treatment any more."],
          "probes": [("target", "cotton"), ("neighbor", "wool"), ("neighbor", "dark"), ("default", None)]},
     ]},
    {"name": "commute-dinner-alerts", "stressor": "confusable",
     "attributes": [{
         "attribute": "phone alert style",
         "options": ["full sound and vibration", "vibration only", "silent banners", "a single soft chime",
                     "alerts held for later"],
         "value_aliases": {"full sound and vibration": ["full volume"],
                           "vibration only": ["just a buzz"],
                           "silent banners": ["quiet pop-ups"],
                           "a single soft chime": ["one gentle ding"],
                           "alerts held for later": ["a roundup afterwards"]},
         "scopes": {"morning": ("the morning train ride", ["my trip in to work"]),
                    "evening": ("the evening train ride", ["my trip home from work"]),
                    "friends": ("dinners out with friends", ["meals out with my friends"]),
                    "alone": ("dinners out alone", ["eating out by myself"]),
                    "cinema": ("cinema trips", ["nights at the movies"])}}],
     "initial": {"phone alert style": ("a single soft chime", {
         "evening": ("silent banners", P),
         "friends": ("alerts held for later", P),
         "cinema": ("vibration only", P)})},
     "events": [
         {"date": "2028-05-07", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "phone alert style", "alone", "vibration only", P),
          "dialogue": [
              "Tried the little noodle bar near the station on my own last night. Tiny room, about eight tables.",
              "Sounds cosy. Was the food any good?",
              "Excellent. But my phone kept chiming and the whole room turned round every time. When I'm eating out "
              "by myself, just a buzz from now on, please."],
          "probes": [("target", "alone"), ("neighbor", "friends"), ("neighbor", "morning"), ("default", None)]},
         {"date": "2028-05-15", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "The garage says they'll ring about the car sometime this evening, which knowing my luck means while "
              "I'm on the train.",
              "Classic timing. Is there anything I can set up?",
              "Put my phone on full volume for my trip home from work tonight. Only tonight, I just can't miss that "
              "call."],
          "probes": [("target", "evening"), ("neighbor", "morning")],
          "note": "a one-off request for tonight's ride home"},
         {"date": "2028-05-24", "category": "exception_revision", "evidence": 5,
          "change": ("revise", "phone alert style", "friends", "silent banners", P),
          "dialogue": [
              "I felt terrible on Saturday. Dinner with the old crowd, and I didn't see the babysitter's messages "
              "until eleven.",
              "Oh no. Was everything all right at home?",
              "Yes, thankfully, just a temperature that came down. But having everything held back until we'd "
              "finished eating was a bad idea.",
              "That sounds stressful. What would work better?",
              "At meals out with my friends, give me quiet pop-ups instead. I can glance down without anyone "
              "noticing."],
          "probes": [("target", "friends"), ("neighbor", "alone"), ("neighbor", "evening"), ("default", None)]},
         {"date": "2028-06-02", "category": "general_update", "evidence": 3,
          "change": ("general", "phone alert style", "full sound and vibration"),
          "dialogue": [
              "Missed two deliveries this week. The courier rang both times and I didn't hear a thing.",
              "That's maddening. Was the phone in another room?",
              "Right next to me on the sofa. One gentle ding is just too easy to miss. Normally I want full volume "
              "now."],
          "probes": [("target", None), ("neighbor", "morning"), ("neighbor", "evening"), ("neighbor", "cinema")]},
         {"date": "2028-06-08", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "phone alert style", "morning", "alerts held for later", W("2028-06-12", "2028-06-23")),
          "dialogue": [
              "I've signed up for a two-week language course that I'm going to do on the train, starting Monday.",
              "That's a clever use of the journey. Is there anything you need from me?",
              "Yes. From Monday through Friday the 23rd, on my trip in to work, hold everything and give me a roundup "
              "afterwards. I want to actually concentrate."],
          "probes": [("boundary", "morning"), {"type": "target", "key": "morning", "date": "2028-06-14"},
                     ("neighbor", "evening"), ("default", None)],
          "note": "a window that starts next Monday; the event date itself is outside it"},
         {"date": "2028-06-26", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "phone alert style", "alone"),
          "dialogue": [
              "The noodle bar put in a sound system and now it's properly loud in there. Weirdly, I love it.",
              "Ha, a whole new atmosphere. Still your favourite spot?",
              "Even more so. It's where I go whenever I'm eating out by myself, and nobody could hear my phone in "
              "there now anyway, so the buzz-only setup isn't needed any more."],
          "probes": [("target", "alone"), ("neighbor", "friends"), ("boundary", "morning"), ("default", None)]},
         {"date": "2028-07-03", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Three late shifts in a row this week. I'm going to be a zombie by Thursday.",
              "That's a rough stretch. Do you want your phone louder on your trip home from work from now on, so "
              "nothing slips past you late at night?",
              "No thanks. After a late shift the last thing I want is my phone blaring on the train. Quiet pop-ups on "
              "the way home suit me fine."],
          "probes": [("target", "evening"), ("boundary", "morning")],
          "note": "a rejected suggestion and a restatement of the stored evening train-ride preference"},
     ]},
    {"name": "lunch-night-spice", "stressor": "confusable",
     "attributes": [{
         "attribute": "food order spice level",
         "options": ["no chili at all", "a mild heat level", "medium heat", "extra hot", "chili on the side",
                     "the restaurant's standard heat"],
         "value_aliases": {"no chili at all": ["zero heat"],
                           "a mild heat level": ["just a hint of spice"],
                           "medium heat": ["a medium kick"],
                           "extra hot": ["the hottest option"],
                           "chili on the side": ["the spice served separately"],
                           "the restaurant's standard heat": ["however the chef makes it"]},
         "scopes": {"weekday": ("weekday lunch orders", ["lunches ordered to the office"]),
                    "weekend": ("weekend lunch orders", ["my weekend lunches"]),
                    "alone": ("takeaway nights alone", ["nights in by myself"]),
                    "guests": ("takeaway nights with guests", ["nights in with friends over"]),
                    "clients": ("client dinners at restaurants", ["dinners out with clients"])}}],
     "initial": {"food order spice level": ("the restaurant's standard heat", {
         "weekday": ("a mild heat level", P),
         "alone": ("extra hot", P),
         "guests": ("chili on the side", P)})},
     "events": [
         {"date": "2028-09-03", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Had a few people round last night and we ordered from the new curry house on the corner.",
              "Nice! How did it go down?",
              "Really well. We got the chili on the side again so everyone could add their own, and nobody "
              "complained. That's still the way to go for nights in with friends over."],
          "probes": [("target", "guests"), ("neighbor", "alone")],
          "note": "a restatement of the stored preference for nights with guests"},
         {"date": "2028-09-10", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "food order spice level", "weekend", "medium heat", P),
          "dialogue": [
              "Yesterday's lunch from the taco truck was so bland I ended up raiding the fridge for hot sauce.",
              "A bland taco is a sad taco. Did you order it a particular way?",
              "No, I just took however the chef makes it. For my weekend lunches I want a medium kick from now on. "
              "I've got the time to enjoy it then."],
          "probes": [("target", "weekend"), ("neighbor", "weekday"), ("neighbor", "clients"), ("default", None)]},
         {"date": "2028-09-18", "category": "exception_revision", "evidence": 7,
          "change": ("revise", "food order spice level", "weekday", "no chili at all", P),
          "dialogue": [
              "Rough afternoon. Heartburn all the way through the budget review.",
              "That sounds miserable. Did you manage to get through it?",
              "Just about. I kept sipping water and nodding at spreadsheets.",
              "Glad you survived. Any idea what set it off?",
              "The mild curry from lunch, would you believe. Even that's too much before an afternoon of meetings.",
              "Sorry to hear it. Is there anything you want done differently?",
              "For lunches ordered to the office, zero heat, please. I'll save the spice for later in the day."],
          "probes": [("target", "weekday"), ("neighbor", "weekend"), ("neighbor", "clients"), ("default", None)]},
         {"date": "2028-09-27", "category": "general_update", "evidence": 3,
          "change": ("general", "food order spice level", "a mild heat level"),
          "dialogue": [
              "Have you noticed how much the heat varies between places? One night it's nothing, the next I'm "
              "crying into my rice.",
              "Kitchens really don't agree on what spicy means. Is it getting to you?",
              "A bit. Normally I'd rather ask for just a hint of spice. Going with the restaurant's standard heat is "
              "too much of a gamble."],
          "probes": [("target", None), ("neighbor", "clients"), ("neighbor", "weekday"), ("neighbor", "alone")]},
         {"date": "2028-10-05", "category": "clarify", "evidence": 3, "change": None,
          "dialogue": [
              "I think something needs to change with my takeaway nights. Either the nights in by myself or the "
              "nights in with friends over, I just can't work out which.",
              "Fair enough. What's been off about them?",
              "Hard to say yet. Give me this weekend and I'll tell you which one."],
          "probes": [("target", "alone"), ("neighbor", "guests")],
          "note": "the user has not decided which of the two kinds of night should change"},
         {"date": "2028-10-12", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "food order spice level", "alone"),
          "dialogue": [
              "Right, I've worked it out. It's the nights in by myself.",
              "Ah, okay. What's going wrong with those?",
              "I keep ordering the hottest option and then giving up halfway. I don't need anything special on those "
              "nights any more."],
          "probes": [("target", "alone"), ("neighbor", "guests"), ("neighbor", "weekend"), ("default", None)],
          "note": "resolves the earlier question; no new level is named, so those nights follow the usual one"},
         {"date": "2028-10-22", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "food order spice level", "guests", "no chili at all", P),
          "dialogue": [
              "Friends came over on Friday and brought their two little ones. The kids wouldn't touch a thing.",
              "Ah, the picky-eater years. What did they end up eating?",
              "Plain rice and a lot of bread. Most of our friends have kids now, so for nights in with friends over, "
              "order with zero heat from now on. The grown-ups will survive."],
          "probes": [("target", "guests"), ("neighbor", "alone"), ("neighbor", "weekday"), ("default", None)]},
     ]},
]

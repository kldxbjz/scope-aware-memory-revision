"""Chain: the right answer for a situation depends on the order of earlier changes (a record retired after a general
update, a temporary record made lasting and then changed, a situation added again after its retirement, general
updates around a revised record), so a memory that keeps a stale record or copies a value at the wrong moment answers
wrongly later."""
from spec import P, O, W  # noqa: F401

EPISODES = [
    # (a) the obedience-class record is retired after the first general update, then a second general update follows
    {"name": "dog-treats", "stressor": "chain",
     "attributes": [{
         "attribute": "reward treat for the dog",
         "options": ["small cubes of cheese", "carrot sticks", "apple slices", "freeze-dried liver bites",
                     "peanut butter biscuits", "chicken jerky strips"],
         "value_aliases": {"small cubes of cheese": ["cheese cubes"],
                           "carrot sticks": ["carrot batons"],
                           "apple slices": ["slices of apple"],
                           "freeze-dried liver bites": ["liver bites"],
                           "chicken jerky strips": ["chicken jerky"]},
         "scopes": {"class": ("obedience classes", ["training class"]),
                    "vet": ("trips to the vet", ["vet appointments"]),
                    "hike": ("long hikes", ["all-day hikes"]),
                    "groomer": ("visits to the groomer", ["grooming appointments"])}}],
     "initial": {"reward treat for the dog": ("small cubes of cheese", {
         "class": ("freeze-dried liver bites", P),
         "vet": ("peanut butter biscuits", P)})},
     "events": [
         {"date": "2028-01-08", "category": "general_update", "evidence": 3,
          "change": ("general", "reward treat for the dog", "carrot sticks"),
          "dialogue": [
              "She was sick on the rug again last night. Third time this month, and it's always after she's had "
              "cheese.",
              "Oh no, poor thing. Is she alright now?",
              "Bouncing off the walls as if nothing happened. But the cheese has to go. From now on her regular "
              "treats are carrot sticks. She loves the crunch anyway."],
          "probes": [("target", None), ("neighbor", "class"), ("neighbor", "vet")]},
         {"date": "2028-01-15", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Guess who finally nailed the long down-stay at training class last night?",
              "No way! That's a tough one. What do you think made it click?",
              "The liver bites, honestly. She would sell her soul for them. Keep them coming for class, they're "
              "clearly doing the job."],
          "probes": [("target", "class"), ("default", None), ("neighbor", "groomer")],
          "note": "a restatement of the stored obedience-class treat"},
         {"date": "2028-01-26", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "reward treat for the dog", "class"),
          "dialogue": [
              "New term at training class, and the trainer's homework is to phase out the fancy rewards so the "
              "dogs learn to work for ordinary stuff.",
              "That's a big step for her. How do you feel about it?",
              "Relieved, if I'm honest. Those liver things cost a fortune. So no special treats for obedience "
              "classes any more, she can have whatever she normally gets."],
          "probes": [("target", "class"), ("default", None), ("neighbor", "vet")],
          "note": "the class record is dropped after the switch to carrot sticks, so classes now follow them"},
         {"date": "2028-02-02", "category": "stable_preference", "evidence": 5, "change": None,
          "dialogue": [
              "Saturday is the off-lead test at training class and I'm more nervous than she is.",
              "You've both put so much work in. Is there anything you want ready for the day?",
              "Could you remind me on Friday night to cut up some cheese cubes?",
              "Of course. Is her stomach up to it?",
              "One day won't hurt her. It's just for the test, I want the big guns on Saturday."],
          "probes": [("target", "class"), ("default", None), ("neighbor", "hike")],
          "note": "a one-off request for the class test; classes still follow the usual treat"},
         {"date": "2028-02-14", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "reward treat for the dog", "vet", "freeze-dried liver bites", P),
          "dialogue": [
              "Vet trip this morning for her booster. She shook the whole time and wouldn't even sniff the peanut "
              "butter biscuits.",
              "Poor girl, that sounds stressful for both of you. Would something else help next time?",
              "The nurse had a pocket full of liver bites and she perked right up. So for trips to the vet, liver "
              "bites from now on."],
          "probes": [("target", "vet"), ("neighbor", "class"), ("default", None), ("neighbor", "groomer")]},
         {"date": "2028-02-25", "category": "general_update", "evidence": 3,
          "change": ("general", "reward treat for the dog", "apple slices"),
          "dialogue": [
              "News from the fussy department: she's gone off carrots. Picks them up, spits them out, gives me a "
              "look.",
              "A dog with opinions! Has anything else caught her interest lately?",
              "Apple, of all things. She pinched a slice off my plate and did a little dance. Let's make apple "
              "slices her usual treat now."],
          "probes": [("target", None), ("neighbor", "class"), ("neighbor", "vet"), ("neighbor", "groomer")],
          "note": "a second general change; the retired class situation follows it too"},
         {"date": "2028-03-07", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "reward treat for the dog", "hike", "chicken jerky strips", P),
          "dialogue": [
              "We did a six-hour loop on Sunday and she was flagging badly by the end.",
              "That's a long day for anyone, four legs or two. Did she have enough to keep her going?",
              "Clearly not. Fruit isn't enough fuel for that. On long hikes she should get chicken jerky strips from "
              "now on, something with a bit of protein in it."],
          "probes": [("target", "hike"), ("neighbor", "class"), ("default", None), ("neighbor", "vet")]},
     ]},

    # (b) a temporary bedtime speed with no end is made lasting, then gets a new value, then is retired
    {"name": "listening-speed", "stressor": "chain",
     "attributes": [{
         "attribute": "audiobook playback speed",
         "options": ["normal speed", "1.25x speed", "1.5x speed", "double speed", "0.75x speed"],
         "value_aliases": {"normal speed": ["1x"],
                           "1.25x speed": ["one and a quarter times"],
                           "1.5x speed": ["one and a half times"],
                           "double speed": ["2x"],
                           "0.75x speed": ["three-quarter speed"]},
         "scopes": {"commute": ("the morning commute", ["my drive to work"]),
                    "bed": ("bedtime listening", ["listening in bed"]),
                    "gym": ("gym sessions", ["workouts at the gym"]),
                    "chores": ("household chores", ["doing the housework"])}}],
     "initial": {"audiobook playback speed": ("1.25x speed", {"commute": ("1.5x speed", P)})},
     "events": [
         {"date": "2028-04-03", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "audiobook playback speed", "bed", "0.75x speed", O),
          "dialogue": [
              "I've been sleeping terribly. Most nights I'm still staring at the ceiling at two.",
              "That sounds exhausting. Has anything helped at all?",
              "Audiobooks, if the narrator is slow and droney enough. So for now, can bedtime listening go at "
              "0.75x speed? Just while I'm going through this rough patch."],
          "probes": [("target", "bed"), ("default", None), ("neighbor", "commute")],
          "note": "stated as temporary with no end: open validity"},
         {"date": "2028-04-11", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Book club is tomorrow evening and I'm still four chapters from the end. Rookie mistake.",
              "Oh no! Do you think you'll make it?",
              "Only if I cheat. Tonight in bed, play it at double speed, just this once. I'll sleep when I know "
              "who did it."],
          "probes": [("target", "bed"), ("default", None), ("neighbor", "gym")],
          "note": "a one-off request for tonight; bedtime keeps its slow speed"},
         {"date": "2028-04-20", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "audiobook playback speed", "bed", "0.75x speed", P),
          "dialogue": [
              "Small victory: I slept right through the night five times this week.",
              "That's great news! Any idea what's made the difference?",
              "Partly the slower speed at bedtime, I think. I know I said it was only for a while, but I'd like to "
              "keep it for good. It's become part of how I fall asleep."],
          "probes": [("target", "bed"), ("default", None), ("neighbor", "commute")],
          "note": "the temporary bedtime speed becomes lasting: same value, validity only"},
         {"date": "2028-05-02", "category": "general_update", "evidence": 5,
          "change": ("general", "audiobook playback speed", "double speed"),
          "dialogue": [
              "I've been doing that ear-training trick where you nudge the speed up a notch each week.",
              "Oh, interesting. How far have you got?",
              "Far enough that 1.25x sounds like slow motion now. It's honestly a bit unsettling.",
              "Ha, that happens. Do you want me to change anything?",
              "Yes, let's make double speed my usual from here on."],
          "probes": [("target", None), ("neighbor", "bed"), ("neighbor", "commute"), ("neighbor", "chores")]},
         {"date": "2028-05-13", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "audiobook playback speed", "bed", "normal speed", P),
          "dialogue": [
              "The slow bedtime audiobooks have started backfiring. I nod off so fast I wake up having missed half "
              "the book.",
              "Too effective! What would you like to do about it?",
              "Bump bedtime listening up to normal speed. Still gentle, but I might actually remember the plot."],
          "probes": [("target", "bed"), ("default", None), ("neighbor", "gym")]},
         {"date": "2028-05-24", "category": "clarify", "evidence": 3, "change": None,
          "dialogue": [
              "Something about my listening setup feels off this week.",
              "Off how? Is something bugging you?",
              "One of the speeds is wrong, either for bedtime listening or for doing the housework, but I can't pin "
              "down which. Let me pay attention for a few days and get back to you."],
          "probes": [("target", "bed"), ("neighbor", "chores"), ("default", None)],
          "note": "the user has not settled which situation should change"},
         {"date": "2028-06-05", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "audiobook playback speed", "bed"),
          "dialogue": [
              "Mystery solved, it was bedtime. I've been sleeping like a log for weeks, so the gentle setting has "
              "no point any more.",
              "That's lovely to hear. What would you like at bedtime from here on?",
              "Bedtime listening doesn't need its own speed now. Just play it the way I usually listen."],
          "probes": [("target", "bed"), ("default", None), ("neighbor", "commute"), ("neighbor", "chores")],
          "note": "the bedtime record is dropped, so bedtime follows the usual double speed"},
     ]},

    # (c) the strawberry record is retired, the patch gets a new record with another value later, then it is revised
    {"name": "garden-mulch", "stressor": "chain",
     "attributes": [{
         "attribute": "mulch material",
         "options": ["shredded bark", "barley straw", "leaf mould", "grass clippings", "pine needles",
                     "pea gravel"],
         "value_aliases": {"shredded bark": ["bark chips"],
                           "barley straw": ["straw"],
                           "leaf mould": ["rotted leaves"],
                           "grass clippings": ["lawn clippings"],
                           "pea gravel": ["fine gravel"]},
         "scopes": {"berry": ("the strawberry patch", ["my strawberry bed"]),
                    "herbs": ("the herb garden", ["my herb bed"]),
                    "veg": ("the vegetable beds", ["my veg plot"]),
                    "roses": ("the rose border", ["the roses along the fence"])}}],
     "initial": {"mulch material": ("shredded bark", {"berry": ("barley straw", P), "herbs": ("pea gravel", P)})},
     "events": [
         {"date": "2028-07-04", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "mulch material", "berry"),
          "dialogue": [
              "Slug carnage on the strawberries this year. I lifted the straw yesterday and there were dozens of "
              "them living underneath.",
              "Ugh, that must have been grim to find.",
              "Grim is the word. The strawberry patch doesn't get its own special mulch any more. It can have the "
              "same as the rest of the garden."],
          "probes": [("target", "berry"), ("default", None), ("neighbor", "herbs")],
          "note": "the strawberry record is dropped; the patch follows the usual mulch"},
         {"date": "2028-07-12", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Had a long chat over the fence this morning. The neighbour swears pine needles are the secret to "
              "sweet strawberries.",
              "Would you want to try that on the strawberry patch?",
              "Not this year. After the slug disaster I'd rather leave that bed alone and see how it does with the "
              "usual stuff."],
          "probes": [("target", "berry"), ("default", None), ("neighbor", "roses")],
          "note": "someone else's suggestion, declined; the patch keeps following the usual mulch"},
         {"date": "2028-07-25", "category": "general_update", "evidence": 3,
          "change": ("general", "mulch material", "leaf mould"),
          "dialogue": [
              "I finally emptied the leaf cage. Three autumns' worth, dark and crumbly, it's gorgeous stuff.",
              "Gardener's gold! What are you planning to do with it all?",
              "Use it. Leaf mould is my standard mulch from now on. It's free, and the worms go mad for it."],
          "probes": [("target", None), ("neighbor", "berry"), ("neighbor", "herbs")]},
         {"date": "2028-08-08", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "mulch material", "berry", "grass clippings", P),
          "dialogue": [
              "The new strawberry runners have rooted, so that bed is back in business.",
              "Lovely. Are you planning anything different this time round?",
              "Yes. For the strawberry patch I want grass clippings from now on. A thin layer keeps the berries off "
              "the soil, and the slugs can't hide in it the way they did in the straw."],
          "probes": [("target", "berry"), ("default", None), ("neighbor", "veg")],
          "note": "a new record for the patch, with a value different from the retired one"},
         {"date": "2028-08-19", "category": "scoped_exception", "evidence": 5,
          "change": ("add", "mulch material", "veg", "barley straw", P),
          "dialogue": [
              "The squash are sprawling all over the vegetable beds and the fruit keeps sitting on wet soil.",
              "That can lead to rot, can't it?",
              "It already has, I lost two last week.",
              "Oh no. Is there anything you'd like to do about it?",
              "For the vegetable beds, let's go with barley straw from now on. The squash love sitting on it, and "
              "slugs have never been a problem out there."],
          "probes": [("target", "veg"), ("neighbor", "berry"), ("default", None), ("neighbor", "herbs")]},
         {"date": "2028-09-01", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "mulch material", "berry", "pine needles", P),
          "dialogue": [
              "The grass clippings around the strawberries have turned into a slimy, smelly mat. Not my finest "
              "idea.",
              "Oh dear. How are the plants coping?",
              "They're fine, it's my nose that's suffering. I'm giving in to the neighbour: pine needles on the "
              "strawberry patch from now on."],
          "probes": [("target", "berry"), ("default", None), ("neighbor", "herbs")]},
         {"date": "2028-09-14", "category": "general_update", "evidence": 3,
          "change": ("general", "mulch material", "shredded bark"),
          "dialogue": [
              "The leaf mould's all gone already. I clearly underestimated how much I'd get through.",
              "It goes fast, doesn't it? What do you want to do now?",
              "I've ordered a delivery of bark chips. That's my standard again from now on, the leaf cage needs a "
              "couple of years to fill back up."],
          "probes": [("target", None), ("neighbor", "berry"), ("neighbor", "veg"), ("neighbor", "roses")]},
     ]},

    # (d) two general updates keep the situation records; the birthday record is revised between them
    {"name": "cake-toppings", "stressor": "chain",
     "attributes": [{
         "attribute": "topping for home-baked cakes",
         "options": ["cream cheese frosting", "chocolate ganache", "a simple lemon glaze", "whipped cream",
                     "a dusting of icing sugar", "salted caramel drizzle"],
         "value_aliases": {"cream cheese frosting": ["cream cheese icing"],
                           "chocolate ganache": ["ganache"],
                           "a simple lemon glaze": ["lemon glaze"],
                           "whipped cream": ["whipped double cream"],
                           "a dusting of icing sugar": ["powdered sugar"],
                           "salted caramel drizzle": ["caramel drizzle"]},
         "scopes": {"bday": ("birthday parties", ["the kids' birthdays"]),
                    "office": ("bake sales at work", ["the office bake sale"]),
                    "tea": ("afternoon tea with the neighbours", ["tea with my neighbours"]),
                    "picnic": ("summer picnics", ["picnics in the park"])}}],
     "initial": {"topping for home-baked cakes": ("cream cheese frosting", {
         "bday": ("chocolate ganache", P),
         "office": ("salted caramel drizzle", P)})},
     "events": [
         {"date": "2028-10-02", "category": "general_update", "evidence": 3,
          "change": ("general", "topping for home-baked cakes", "a simple lemon glaze"),
          "dialogue": [
              "I made a carrot cake at the weekend and couldn't even finish a slice. The frosting sat in my stomach "
              "like a brick.",
              "Too rich these days?",
              "Way too rich for me. Normally I'd rather have a simple lemon glaze on top now, something lighter."],
          "probes": [("target", None), ("neighbor", "bday"), ("neighbor", "office")]},
         {"date": "2028-10-11", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "There's a bake sale at work next Friday. A colleague says the ganache cakes always sell out first.",
              "Are you tempted to switch things up?",
              "Nope. People queue for my caramel drizzle, I'm not messing with a winning formula. Same as ever for "
              "the office bake sale."],
          "probes": [("target", "office"), ("neighbor", "bday"), ("default", None), ("neighbor", "picnic")],
          "note": "a colleague's view, then a restatement of the stored bake-sale topping"},
         {"date": "2028-10-20", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "topping for home-baked cakes", "bday", "whipped cream", P),
          "dialogue": [
              "The twins' birthday party was chaos. Half the kids scraped the ganache off and left it on their "
              "plates.",
              "Kids can be tough critics. Would you do anything differently next time?",
              "Definitely. For birthday parties, whipped cream from now on. They'll eat anything that's white and "
              "fluffy."],
          "probes": [("target", "bday"), ("default", None), ("neighbor", "office")]},
         {"date": "2028-10-31", "category": "stable_preference", "evidence": 5, "change": None,
          "dialogue": [
              "My niece turns twelve on Saturday and she's asked me for a chocolate cake with ganache for her "
              "birthday party.",
              "She knows what she wants! Shall I put the ingredients on the shopping list?",
              "Yes please, dark chocolate and a pot of cream.",
              "Added. Anything else for the party?",
              "No, that's it. The ganache is just for her party though, she's the only kid I know who likes the "
              "bitter stuff."],
          "probes": [("target", "bday"), ("default", None), ("neighbor", "tea")],
          "note": "a one-off request for one party; birthday parties keep the whipped cream"},
         {"date": "2028-11-12", "category": "general_update", "evidence": 3,
          "change": ("general", "topping for home-baked cakes", "a dusting of icing sugar"),
          "dialogue": [
              "I've gone right off glazes. The lemon ones keep going sticky and weepy by the second day.",
              "That's annoying. Could it be the damp weather?",
              "Maybe. Either way, my usual from now on is just a dusting of icing sugar. Less fuss, and it still "
              "looks pretty."],
          "probes": [("target", None), ("neighbor", "bday"), ("neighbor", "office"), ("neighbor", "tea")],
          "note": "a second general change; the revised birthday record and the bake-sale record stay"},
         {"date": "2028-11-24", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "topping for home-baked cakes", "tea", "cream cheese frosting", P),
          "dialogue": [
              "The neighbours came round for tea yesterday and asked, very politely, where my carrot cake had gone.",
              "Sounds like it's been missed! Do you want to bring it back for them?",
              "Looks like I have to. For afternoon tea with the neighbours, it's cream cheese frosting from now on. "
              "They're not the ones complaining about rich food."],
          "probes": [("target", "tea"), ("neighbor", "bday"), ("default", None), ("neighbor", "office")]},
     ]},
]

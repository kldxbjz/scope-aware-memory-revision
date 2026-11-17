"""Distractors: no-write events that talk about situations and values already in memory (someone else's preference,
one-off requests, hypotheticals, declined suggestions, restatements, clarifications resolved later), mixed with real
changes so that whether an event writes cannot be told from its position."""
from spec import P, O, W  # noqa: F401

EPISODES = [
    {"name": "delivery-slots", "stressor": "distractor",
     "attributes": [{
         "attribute": "delivery time slot",
         "options": ["an early-morning slot", "a lunchtime slot", "a mid-afternoon slot", "an evening slot",
                     "a weekend slot", "the first available slot"],
         "value_aliases": {"an early-morning slot": ["first thing in the morning"],
                           "a lunchtime slot": ["around midday"],
                           "a mid-afternoon slot": ["around three"],
                           "an evening slot": ["after six"],
                           "a weekend slot": ["a Saturday or Sunday"],
                           "the first available slot": ["whatever's soonest"]},
         "scopes": {"groc": ("grocery deliveries", ["the weekly food order"]),
                    "furn": ("furniture deliveries", ["big flat-pack orders"]),
                    "sign": ("parcels that need a signature", ["anything I have to sign for"]),
                    "ret": ("courier pickups for returns", ["returns being collected"])}}],
     "initial": {"delivery time slot": ("the first available slot", {
         "groc": ("an evening slot", P),
         "furn": ("a weekend slot", P),
         "sign": ("an early-morning slot", P)})},
     "events": [
         {"date": "2028-01-08", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Had dinner at my brother's last night. He's decided that from now on his weekly food order turns up "
              "first thing in the morning, so the milk's in the fridge before he's even left for work.",
              "Very organized. Tempted to try it?",
              "Ha, no. I'm barely a person before eight. That's his system, not mine."],
          "probes": [("target", "groc"), ("neighbor", "sign"), ("default", None)],
          "note": "the brother's preference for the stored grocery situation; the user does not adopt it"},
         {"date": "2028-01-15", "category": "scoped_exception", "evidence": 5,
          "change": ("add", "delivery time slot", "ret", "a lunchtime slot", P),
          "dialogue": [
              "Third pair of shoes going back this month. Online sizing is a complete lottery.",
              "Oof. Is sending them back at least painless?",
              "Not really. The courier keeps coming while I'm at the office and leaves one of those little "
              "sorry-we-missed-you cards.",
              "Annoying. Is there a time you're reliably around?",
              "I pop home for lunch most days, so for returns being collected, a lunchtime slot is the way to go."],
          "probes": [("target", "ret"), ("neighbor", "sign"), ("default", None)]},
         {"date": "2028-01-23", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "My parents land on Thursday and the bookshelf for the spare room still hasn't come.",
              "Cutting it fine! When is it booked for?",
              "Not until a week from Saturday, which is useless. Just this once, grab the first available slot for "
              "that furniture delivery, weekday or not. I'll take a day off if I have to."],
          "probes": [("target", "furn"), ("neighbor", "groc"), ("default", None)],
          "note": "a one-off request for one furniture delivery; the stored weekend preference is unchanged"},
         {"date": "2028-02-01", "category": "general_update", "evidence": 3,
          "change": ("general", "delivery time slot", "a mid-afternoon slot"),
          "dialogue": [
              "Guess who finally talked her manager into letting her work from home most of the week?",
              "No way! Congratulations. How's it feeling so far?",
              "Bliss. It also means that normally I'd go for a mid-afternoon slot for my deliveries now. Taking "
              "whatever's soonest made sense when the place sat empty all day, but these days I'm right here "
              "after lunch."],
          "probes": [("target", None), ("neighbor", "ret"), ("neighbor", "furn")]},
         {"date": "2028-02-10", "category": "clarify", "evidence": 3, "change": None,
          "dialogue": [
              "Working from home has me rethinking my odd delivery times. One of them has stopped making sense: "
              "either the early courier for anything I have to sign for, or the weekly food order after six.",
              "Which of the two is bothering you more?",
              "That's just it, I can't tell yet. Give me a couple more weeks of actually living like this and I'll "
              "tell you which one."],
          "probes": [("target", "sign"), ("neighbor", "groc"), ("default", None)],
          "note": "the user has not decided which of two stored situations should change"},
         {"date": "2028-02-18", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Random thought while taping up yet another return: if I ever took a job across town, returns being "
              "collected around midday would be hopeless. I'd need them after six.",
              "Are you thinking of changing jobs?",
              "Not at all, I'm very happy where I am. Just thinking out loud."],
          "probes": [("target", "ret"), ("neighbor", "groc"), ("default", None)],
          "note": "a hypothetical about the stored returns situation"},
         {"date": "2028-02-27", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "delivery time slot", "sign"),
          "dialogue": [
              "Okay, after a couple more weeks at home I know which delivery time has to go.",
              "Oh? Which one?",
              "The early courier for anything I have to sign for. I'm home most days now, so there's no reason to "
              "drag myself out of bed for it. Just scrap that one."],
          "probes": [("target", "sign"), ("neighbor", "groc"), ("default", None)],
          "note": "resolves the earlier clarify: the signature record is dropped and those parcels follow the "
                  "usual slot again; no new value is named"},
         {"date": "2028-03-07", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "The food order turned up at six-thirty last night and I had everything put away before my show "
              "started. Perfect.",
              "Nice timing. Since you're home in the afternoons now, should I move the weekly food order to a "
              "mid-afternoon slot from now on?",
              "No, leave that one alone. Putting the shopping away after work is how I switch off, and afternoons "
              "are for actual work."],
          "probes": [("target", "groc"), ("neighbor", "ret"), ("default", None)],
          "note": "the assistant suggests a change for the stored grocery situation and the user declines"},
     ]},
    {"name": "gift-wrapping", "stressor": "distractor",
     "attributes": [{
         "attribute": "gift wrapping style",
         "options": ["glossy paper with a satin ribbon", "brown kraft paper with twine", "a reusable cloth wrap",
                     "a patterned gift bag", "no wrapping at all"],
         "value_aliases": {"glossy paper with a satin ribbon": ["shiny paper and a bow"],
                           "brown kraft paper with twine": ["brown paper and string"],
                           "a reusable cloth wrap": ["a fabric wrap"],
                           "a patterned gift bag": ["a gift bag with tissue"],
                           "no wrapping at all": ["left unwrapped"]},
         "scopes": {"kids": ("presents for nieces and nephews", ["gifts for the kids in the family"]),
                    "work": ("gifts for coworkers", ["presents for people at work"]),
                    "wed": ("wedding gifts", ["presents for couples getting married"]),
                    "post": ("gifts sent by mail", ["presents that go in the post"])}}],
     "initial": {"gift wrapping style": ("glossy paper with a satin ribbon", {
         "kids": ("a patterned gift bag", P),
         "work": ("brown kraft paper with twine", P)})},
     "events": [
         {"date": "2028-04-03", "category": "general_update", "evidence": 3,
          "change": ("general", "gift wrapping style", "a reusable cloth wrap"),
          "dialogue": [
              "We did my dad's birthday yesterday, and afterwards half the recycling bin was shiny wrapping paper. "
              "It felt a bit obscene.",
              "It does pile up. Has it put you off the shiny stuff?",
              "Pretty much. For most presents I'd like a reusable cloth wrap from now on. People can hand it back "
              "or use it again, I don't mind which."],
          "probes": [("target", None), ("neighbor", "kids"), ("neighbor", "work")]},
         {"date": "2028-04-11", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Someone on my team is leaving on Friday, so I ordered a little succulent for her desk.",
              "That's sweet of you. Should I add gift wrapping to the order?",
              "Yes please. Brown paper and string, same as I always do for presents for people at work. Nobody in "
              "the office goes in for anything flashy."],
          "probes": [("target", "work"), ("neighbor", "kids"), ("default", None)],
          "note": "a restatement of the stored coworker preference in other words"},
         {"date": "2028-04-19", "category": "stable_preference", "evidence": 5, "change": None,
          "dialogue": [
              "My nephew turns six on Saturday and he's in a phase of drawing on absolutely everything.",
              "Ha, a budding artist. Have you found him something yet?",
              "A giant box of markers, obviously. It's arriving Friday.",
              "Perfect. How would you like it wrapped?",
              "Only this once, brown paper and string instead of a gift bag, so he can draw all over the wrapping "
              "before he even gets to the markers."],
          "probes": [("target", "kids"), ("neighbor", "work"), ("default", None)],
          "note": "a one-off request for one nephew's present; the stored preference for nieces and nephews is "
                  "unchanged"},
         {"date": "2028-04-28", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "gift wrapping style", "wed", "glossy paper with a satin ribbon", P),
          "dialogue": [
              "Three weddings this summer. Three! My weekends are nothing but gift tables.",
              "Busy season. Have you thought about how you want those wrapped?",
              "Yes. For wedding gifts I want glossy paper with a satin ribbon, whoever's getting married. A cloth "
              "wrap looks a bit too casual on a table full of fancy boxes."],
          "probes": [("target", "wed"), ("neighbor", "kids"), ("default", None)]},
         {"date": "2028-05-06", "category": "clarify", "evidence": 3, "change": None,
          "dialogue": [
              "Now that most of my presents go out in cloth, two of my old wrapping habits look a bit odd: the gift "
              "bags for the kids in the family and the brown paper for people at work.",
              "Do you want to change both of them?",
              "No, just one, but I honestly can't decide which. Let me sit on it for a while."],
          "probes": [("target", "kids"), ("neighbor", "work"), ("default", None)],
          "note": "the user has not decided which of two stored situations should change"},
         {"date": "2028-05-15", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "A friend of mine who sells handmade cards at the market says glossy paper is over, and from now on "
              "she's doing every wedding gift in a fabric wrap.",
              "Interesting. Is she right, do you think?",
              "Not for me. She can wrap her presents however she likes, but I want mine to look like a proper "
              "present on that table."],
          "probes": [("target", "wed"), ("neighbor", "work"), ("default", None)],
          "note": "a friend's preference for the stored wedding situation; the user keeps their own"},
         {"date": "2028-05-24", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "gift wrapping style", "kids", "brown kraft paper with twine", P),
          "dialogue": [
              "My nephew still talks about his birthday present, mostly because he got to draw all over the "
              "wrapping.",
              "That's adorable. Has it helped with the wrapping question you were mulling over?",
              "It has. No more gift bags for the kids: gifts for the kids in the family get brown paper and string "
              "from now on, so they can doodle on it."],
          "probes": [("target", "kids"), ("neighbor", "wed"), ("default", None)],
          "note": "resolves the earlier clarify: the nieces-and-nephews record gets a new value"},
         {"date": "2028-06-01", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "I'm covering for my manager for the time being while she's on leave. Feels strange sitting in her "
              "chair.",
              "That's a vote of confidence. How's it going?",
              "Fine so far. If I ever got the job for real, presents for people at work would need to look a bit "
              "more special, shiny paper and a bow probably. But that's a long way off."],
          "probes": [("target", "work"), ("neighbor", "wed"), ("default", None)],
          "note": "a hypothetical about the stored coworker situation"},
     ]},
    {"name": "taxi-cars", "stressor": "distractor",
     "attributes": [{
         "attribute": "taxi vehicle type",
         "options": ["a standard sedan", "a roomy minivan", "a compact hatchback", "a fully electric car",
                     "a premium car with leather seats"],
         "value_aliases": {"a standard sedan": ["a regular car"],
                           "a roomy minivan": ["one of the big vans"],
                           "a compact hatchback": ["a small car"],
                           "a fully electric car": ["an EV"],
                           "a premium car with leather seats": ["the leather-seat option"]},
         "scopes": {"air": ("rides to the airport", ["airport trips"]),
                    "late": ("late-night rides home", ["getting home after midnight"]),
                    "client": ("rides to client meetings", ["trips to see clients"]),
                    "kids": ("rides with the children", ["trips with my kids"])}}],
     "initial": {"taxi vehicle type": ("a standard sedan", {
         "air": ("a roomy minivan", P),
         "client": ("a premium car with leather seats", P)})},
     "events": [
         {"date": "2028-06-12", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "I'm off to a two-day workshop on Wednesday, and the flight leaves at some ungodly hour.",
              "Ouch, early start. Anything I should know for the ride?",
              "I'm only taking a backpack, so just for this airport run a small car is plenty. No sense paying for "
              "a van to haul one bag."],
          "probes": [("target", "air"), ("neighbor", "client"), ("default", None)],
          "note": "a one-off request for one airport ride; the stored airport preference is unchanged"},
         {"date": "2028-06-20", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Had lunch with my business partner. She's convinced that for trips to see clients we should always "
              "show up in an EV, says it tells them we're a modern outfit.",
              "That's one way to make an impression. What do you think?",
              "It works for her clients, they're all young startups. Mine expect a bit of comfort, so that's not "
              "changing for me."],
          "probes": [("target", "client"), ("neighbor", "air"), ("default", None)],
          "note": "the business partner's preference for the stored client situation; the user keeps their own"},
         {"date": "2028-06-29", "category": "general_update", "evidence": 3,
          "change": ("general", "taxi vehicle type", "a fully electric car"),
          "dialogue": [
              "Did you see the air quality warnings this week? I could practically taste the traffic on my walk "
              "this morning.",
              "It's been grim. Is it changing how you want to get around?",
              "A bit. Usually I'd like an EV now when I book a ride. I can't fix the whole city, but I can stop "
              "adding to the fumes."],
          "probes": [("target", None), ("neighbor", "air"), ("neighbor", "client")]},
         {"date": "2028-07-08", "category": "clarify", "evidence": 3, "change": None,
          "dialogue": [
              "That backpack-only trip last month was such a relief. I'm half thinking of switching airport trips "
              "to a small car from now on.",
              "You do seem to be traveling lighter these days.",
              "Mostly. But there's the trade fair in October with all my display kit, and there could be more "
              "trips like that. Maybe I should just decide trip by trip. I genuinely don't know yet.",
              "Is there anything that would help you decide?",
              "Finding out how the display stuff gets there. I'll come back to you once I know."],
          "probes": [("target", "air"), ("neighbor", "client"), ("default", None)],
          "note": "the user leaves open whether airport rides should change for good or be decided trip by trip"},
         {"date": "2028-07-17", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "taxi vehicle type", "air", "a compact hatchback", P),
          "dialogue": [
              "Good news about the trade fair: the organizers are shipping everyone's display kit for them.",
              "That's a weight off. Does it settle the airport question?",
              "It does. Airport trips get a compact hatchback from now on. These days it's always just me and a "
              "carry-on."],
          "probes": [("target", "air"), ("neighbor", "client"), ("default", None)],
          "note": "resolves the earlier clarify: the airport record gets a new lasting value"},
         {"date": "2028-07-26", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "My business partner keeps floating the idea of bringing the whole sales team to the big renewal "
              "meetings.",
              "Would that become a regular thing?",
              "If we ever did that, trips to see clients would need one of the big vans, obviously. But I don't "
              "see it happening. The clients like it small and personal."],
          "probes": [("target", "client"), ("neighbor", "air"), ("default", None)],
          "note": "a hypothetical about the stored client situation"},
         {"date": "2028-08-03", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Back from a trip to the regional office last night. The little hatchback was perfect for one bag.",
              "Glad it worked out. Want me to book an EV for airport trips from now on? They're often cheaper on "
              "the early runs.",
              "No, stick with the small cars for those. The electric ones out near the airport are usually miles "
              "away and I'd rather not stand around waiting."],
          "probes": [("target", "air"), ("neighbor", "client"), ("default", None)],
          "note": "the assistant suggests a change for the stored airport situation and the user declines"},
         {"date": "2028-08-10", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "taxi vehicle type", "client"),
          "dialogue": [
              "Finance just announced they won't reimburse the fancy cars anymore.",
              "Oh no. Is that going to be a problem for you?",
              "Honestly, no. In three years not a single client has mentioned the leather seats. Drop them for "
              "trips to see clients, they were only ever for show."],
          "probes": [("target", "client"), ("neighbor", "air"), ("default", None)],
          "note": "the client record is dropped and those rides follow the usual car again; no new value is "
                  "named"},
     ]},
    {"name": "notebooks-and-pens", "stressor": "distractor",
     "attributes": [
         {"attribute": "notebook page ruling",
          "options": ["narrow-ruled lines", "wide-ruled lines", "plain blank pages", "a dot grid", "a square grid"],
          "value_aliases": {"narrow-ruled lines": ["thin lines"],
                            "wide-ruled lines": ["wide lines"],
                            "plain blank pages": ["unlined paper"],
                            "a dot grid": ["dotted pages"],
                            "a square grid": ["graph paper"]},
          "scopes": {"layout": ("sketching page layouts", ["drafting layouts"]),
                     "budget": ("monthly budget planning", ["working out the monthly numbers"])}},
         {"attribute": "pen ink color",
          "options": ["black ink", "navy blue ink", "green ink", "red ink", "purple ink"],
          "value_aliases": {"black ink": ["a black pen"],
                            "navy blue ink": ["a dark blue pen"],
                            "green ink": ["a green pen"],
                            "red ink": ["a red pen"],
                            "purple ink": ["a purple pen"]},
          "scopes": {"sign": ("signing contracts", ["official paperwork"]),
                     "edit": ("marking up drafts", ["editing printouts"])}}],
     "initial": {"notebook page ruling": ("narrow-ruled lines", {"layout": ("a dot grid", P),
                                                                 "budget": ("a square grid", P)}),
                 "pen ink color": ("black ink", {"sign": ("navy blue ink", P)})},
     "events": [
         {"date": "2028-09-05", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "pen ink color", "edit", "green ink", O),
          "dialogue": [
              "I handed a marked-up report back to one of our new interns today and the poor kid looked crushed. "
              "Every margin was full of my black scrawl.",
              "Oof. A wall of corrections can be a lot to take in.",
              "Right? For marking up drafts I want green ink for the time being, until the interns find their "
              "feet. It reads a lot friendlier."],
          "probes": [("target", "edit"), ("neighbor", "sign"), ("default", None)],
          "note": "a new record stated as temporary with no end date (open validity)"},
         {"date": "2028-09-13", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "The designer who sits next to me does all her layout sketches on graph paper. She swears the "
              "squares keep her columns honest.",
              "That's a neat trick. Have you ever tried it?",
              "Ages ago. It's great for her, but I'm happier on my dotted pages, they don't shout at me."],
          "probes": [{"type": "target", "key": "layout", "attribute": "notebook page ruling"},
                     {"type": "neighbor", "key": "budget", "attribute": "notebook page ruling"},
                     {"type": "default", "key": None, "attribute": "notebook page ruling"}],
          "note": "a colleague's preference for the stored layout situation, then a restatement of the user's own"},
         {"date": "2028-09-22", "category": "general_update", "evidence": 3,
          "change": ("general", "notebook page ruling", "plain blank pages"),
          "dialogue": [
              "I've started thinking in little boxes and arrows, and the ruled lines in my notebooks keep getting "
              "in the way.",
              "Sounds like your notebooks aren't keeping up with you.",
              "They're not. Most of the time I'd like unlined paper now. Lines only made sense back when I wrote "
              "neat paragraphs."],
          "probes": [("target", None), ("neighbor", "layout"), ("neighbor", "budget")]},
         {"date": "2028-10-02", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "The lease renewal finally came through. I'm signing it at the landlord's office tomorrow morning.",
              "That's a relief! Anything you need to bring?",
              "Their form says black ink only, so just for tomorrow's signing I'll need a black pen. Their rule, "
              "not mine. Can you put it on my list for the morning?"],
          "probes": [{"type": "target", "key": "sign", "attribute": "pen ink color"},
                     {"type": "neighbor", "key": "edit", "attribute": "pen ink color"},
                     {"type": "default", "key": None, "attribute": "pen ink color"}],
          "note": "a one-off request forced by someone else's rule; the stored contract preference is unchanged"},
         {"date": "2028-10-11", "category": "clarify", "evidence": 3, "change": None,
          "dialogue": [
              "Since switching to blank notebooks, the special paper I use for layouts and for budgets has started "
              "to feel off.",
              "Off in what way?",
              "Hard to say. One of the two needs a different ruling, but I can't tell which one yet.",
              "Want to try a few pages of each and see?",
              "Yeah, that's the plan. I'll know after the big client deadline next week."],
          "probes": [{"type": "target", "key": "layout", "attribute": "notebook page ruling"},
                     {"type": "neighbor", "key": "budget", "attribute": "notebook page ruling"},
                     {"type": "default", "key": None, "attribute": "notebook page ruling"}],
          "note": "the user has not decided which of two stored situations should change"},
         {"date": "2028-10-23", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "notebook page ruling", "layout", "a square grid", P),
          "dialogue": [
              "Deadline survived. And I worked out the notebook thing: it's the layout sketches.",
              "Oh? What's wrong with them?",
              "I'm doing much tighter wireframes now and the dots just aren't precise enough. For drafting layouts "
              "I want graph paper from now on."],
          "probes": [("target", "layout"), ("neighbor", "budget"), ("default", None)],
          "note": "resolves the earlier clarify: the layout record gets a new value"},
         {"date": "2028-11-01", "category": "stable_preference", "evidence": 7, "change": None,
          "dialogue": [
              "My old professor emailed again about teaching a night class next spring.",
              "Again? She must really want you. Is it tempting?",
              "A little. I do miss being in a classroom.",
              "What's holding you back?",
              "Time, mostly. I'd be grading essays at midnight.",
              "That would be a lot on top of your job.",
              "Exactly. If I ever said yes, I'd probably mark up drafts with a red pen like a proper teacher. But "
              "I keep turning her down, so don't hold your breath."],
          "probes": [{"type": "target", "key": "edit", "attribute": "pen ink color"},
                     {"type": "neighbor", "key": "sign", "attribute": "pen ink color"},
                     {"type": "default", "key": None, "attribute": "pen ink color"}],
          "note": "a hypothetical about the stored draft situation"},
         {"date": "2028-11-09", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Sending the insurance forms off today. It took me all morning to find where I'd put them.",
              "Paperwork has a way of hiding. All signed?",
              "All signed, in a dark blue pen, which is what I normally use for official paperwork. That way I can "
              "always tell the originals from the copies."],
          "probes": [{"type": "target", "key": "sign", "attribute": "pen ink color"},
                     {"type": "neighbor", "key": "edit", "attribute": "pen ink color"},
                     {"type": "default", "key": None, "attribute": "pen ink color"}],
          "note": "a restatement of the stored contract preference in other words"},
     ]},
]

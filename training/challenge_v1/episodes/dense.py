"""Dense memory: one or two attributes carrying three or four situation-specific records at once (v1.1 never has more
than two per attribute), so every write has to pick the right record among several similar ones."""
from spec import P, O, W  # noqa: F401

EPISODES = [
    {"name": "hotel-rooms", "stressor": "dense",
     "attributes": [{
         "attribute": "hotel room placement",
         "options": ["a room on a high floor", "a ground-floor room", "a room near the lifts",
                     "a room at the quiet end of the corridor", "a room overlooking the courtyard",
                     "a room next to the stairwell"],
         "value_aliases": {"a room on a high floor": ["somewhere up high"],
                           "a ground-floor room": ["street level"],
                           "a room near the lifts": ["close to the elevators"],
                           "a room at the quiet end of the corridor": ["the far end of the hallway"],
                           "a room overlooking the courtyard": ["a courtyard view"],
                           "a room next to the stairwell": ["a spot by the stairs"]},
         "scopes": {"conf": ("conference trips", ["work conferences"]),
                    "beach": ("beach holidays", ["trips to the coast"]),
                    "layover": ("overnight layovers", ["stopovers between flights"]),
                    "grand": ("visits to the grandparents", ["trips to see my grandparents"]),
                    "road": ("road trips", ["driving holidays"])}}],
     "initial": {"hotel room placement": ("a room on a high floor", {
         "conf": ("a room near the lifts", P),
         "layover": ("a room at the quiet end of the corridor", P),
         "beach": ("a ground-floor room", P)})},
     "events": [
         {"date": "2028-01-10", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Quick thing before I forget. My coworker swears that on work conferences the trick is a courtyard "
              "view, because the street side never quiets down.",
              "Is that something you'd want for your own bookings?",
              "Nah, that's just what works for them. I'm happy being close to the elevators when I'm dragging a "
              "poster tube around the venue."],
          "probes": [("target", "conf"), ("default", None)],
          "note": "a coworker's preference, then a restatement of the stored conference-trip preference"},
         {"date": "2028-01-17", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "hotel room placement", "road", "a room overlooking the courtyard", P),
          "dialogue": [
              "We're planning a few driving holidays this year, which I'm weirdly excited about.",
              "Nice! Anything I should keep in mind when I book the hotels for those?",
              "Yes. Whenever it's one of our driving holidays, ask for a courtyard view. The car park side is where "
              "everyone slams doors at six in the morning."],
          "probes": [("target", "road"), ("neighbor", "beach"), ("neighbor", "layover"), ("default", None)]},
         {"date": "2028-01-25", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "hotel room placement", "conf", "a room next to the stairwell", P),
          "dialogue": [
              "The lifts at that last conference hotel were a disaster. Twenty minutes just to get down for the "
              "keynote.",
              "That sounds miserable. Should I book those differently?",
              "Please. For work conferences, put me in a room next to the stairwell from now on so I can just walk "
              "down."],
          "probes": [("target", "conf"), ("neighbor", "layover"), ("neighbor", "road"), ("default", None)]},
         {"date": "2028-02-02", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "hotel room placement", "beach"),
          "dialogue": [
              "I'm sorting out the March trip to the coast. We sold the surfboards, by the way.",
              "Oh, end of an era! Does that change anything about the booking?",
              "It does. For trips to the coast I don't need street level any more, that was only for hauling the "
              "boards in and out. Nothing special there now."],
          "probes": [("target", "beach"), ("neighbor", "road"), ("neighbor", "conf"), ("default", None)]},
         {"date": "2028-02-09", "category": "general_update", "evidence": 3,
          "change": ("general", "hotel room placement", "a room near the lifts"),
          "dialogue": [
              "I finally bought one of those enormous checked suitcases and dragging it down long corridors is "
              "wrecking my shoulder.",
              "Ouch. Do you want me to take that into account for hotels?",
              "Yeah. Normally I'd rather be close to the elevators now instead of up high."],
          "probes": [("target", None), ("neighbor", "beach"), ("neighbor", "conf"), ("neighbor", "layover"),
                     ("neighbor", "road")]},
         {"date": "2028-02-21", "category": "clarify", "evidence": 1, "change": None,
          "dialogue": [
              "I think I want something different either for stopovers between flights or for trips to see my "
              "grandparents. I honestly can't tell which one is bugging me.",
              "No rush. What's making you reconsider?",
              "Just sleeping badly on both lately. I'll work out which one it is after the next trip."],
          "probes": [("target", "layover"), ("neighbor", "grand")],
          "note": "the user has not decided which situation should change"},
         {"date": "2028-03-02", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "hotel room placement", "grand", "a room on a high floor", P),
          "dialogue": [
              "Worked it out. It's the grandparents' town: the hotel there is right on the main road.",
              "Ah. So what would help on those visits?",
              "For trips to see my grandparents, get me somewhere up high, away from the traffic."],
          "probes": [("target", "grand"), ("neighbor", "layover"), ("neighbor", "beach"), ("default", None)]},
     ]},
    {"name": "living-room-lights", "stressor": "dense",
     "attributes": [{
         "attribute": "living room lighting",
         "options": ["bright white light", "a warm low glow", "candlelight", "the TV backlight",
                     "the floor lamps alone", "complete darkness"],
         "value_aliases": {"bright white light": ["full brightness"],
                           "a warm low glow": ["the cozy dim setting"],
                           "candlelight": ["real candles"],
                           "the TV backlight": ["the strip behind the screen"],
                           "the floor lamps alone": ["just the floor lamps"],
                           "complete darkness": ["every light off"]},
         "scopes": {"movie": ("movie nights", ["film nights"]),
                    "dinner": ("dinner parties", ["friends over for dinner"]),
                    "homework": ("homework hour", ["the kids' homework time"]),
                    "calls": ("video calls", ["my work calls"]),
                    "games": ("board game nights", ["game nights"])}}],
     "initial": {"living room lighting": ("a warm low glow", {
         "movie": ("the TV backlight", P),
         "dinner": ("candlelight", P),
         "homework": ("bright white light", P)})},
     "events": [
         {"date": "2028-04-04", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "living room lighting", "calls", "bright white light", P),
          "dialogue": [
              "Big news on our end: the spare room is officially the nursery now, so my work calls have moved down "
              "to the living room.",
              "Congratulations! How is the living room working out for that?",
              "Fine, apart from the lights. That warm glow makes me look half asleep on camera. For video calls, "
              "give me bright white light, please."],
          "probes": [("target", "calls"), ("neighbor", "homework"), ("neighbor", "movie"), ("default", None)]},
         {"date": "2028-04-12", "category": "stable_preference", "evidence": 5, "change": None,
          "dialogue": [
              "My brother is coming over tonight to watch that new haunted-lighthouse film everyone keeps talking "
              "about.",
              "Sounds like a fun evening! Are you a horror fan?",
              "Not remotely. He is, though, and he swears it only works in the pitch dark.",
              "Want the living room set up for it?",
              "Yes, but just for tonight: every light off, even the strip behind the screen. Normally I'd hate "
              "that, but I'll survive one evening of it."],
          "probes": [{"type": "target", "key": "movie", "date": "2028-04-19"}, ("default", None)],
          "note": "a one-off request for tonight that follows the brother's taste; movie nights keep their setting"},
         {"date": "2028-04-24", "category": "general_update", "evidence": 5,
          "change": ("general", "living room lighting", "the floor lamps alone"),
          "dialogue": [
              "We finally rearranged the living room over the weekend. The two floor lamps are on either side of "
              "the sofa now.",
              "Oh, nice! Did the new rug fit in the end?",
              "After a small war with the coffee table, yes. The lamps changed the whole feel of the room, though.",
              "In a good way, I hope? Should the lights work differently now?",
              "A very good way. Normally I just want the floor lamps alone in there now. It finally feels like a "
              "proper den."],
          "probes": [("target", None), ("neighbor", "movie"), ("neighbor", "dinner"), ("neighbor", "homework"),
                     ("neighbor", "calls")]},
         {"date": "2028-04-30", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "living room lighting", "dinner", "a warm low glow", P),
          "dialogue": [
              "Last night's dinner was lovely right up until a napkin caught fire on one of the candles. Nobody got "
              "hurt, but the tablecloth is history.",
              "Oh no! I'm glad everyone's okay. Will that change how you set things up when people come round?",
              "It will. No more real candles at dinner parties. Let's have the cozy dim setting for those instead."],
          "probes": [("target", "dinner"), ("neighbor", "movie"), ("neighbor", "calls"), ("default", None)]},
         {"date": "2028-05-09", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "living room lighting", "homework"),
          "dialogue": [
              "Parent-teacher evening was last night. Both kids are doing fine, which I'll gladly take.",
              "That's great to hear! Did anything come out of it for home?",
              "Only that the school gave every pupil a clip-on desk light, so homework hour doesn't need full "
              "brightness in the living room any more. No special lighting for it from now on."],
          "probes": [("target", "homework"), ("neighbor", "calls"), ("neighbor", "dinner"), ("default", None)]},
         {"date": "2028-05-18", "category": "clarify", "evidence": 1, "change": None,
          "dialogue": [
              "Something in our evening setup is giving me headaches. It's either the backlight on film nights or "
              "the dim setting we use for dinner parties, and for now I honestly can't tell which.",
              "Sorry to hear that. Has anything else changed lately, like more screen time or less sleep?",
              "Not that I can think of. I'll pay attention at the next film night and the next dinner and tell you "
              "which one it is."],
          "probes": [("target", "movie"), ("neighbor", "dinner")],
          "note": "the user cannot tell yet which of the two situations needs a change"},
         {"date": "2028-05-27", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "living room lighting", "movie", "a warm low glow", P),
          "dialogue": [
              "Mystery solved, I think. During last night's film the strip behind the screen flickered every time "
              "a scene went dark, and the headache arrived right on cue.",
              "That would do it. And the dinner on Sunday?",
              "Not a twinge all evening. So it's the movie nights: give those the cozy dim setting instead of the "
              "backlight."],
          "probes": [("target", "movie"), ("neighbor", "dinner"), ("neighbor", "calls"), ("default", None)]},
     ]},
    {"name": "grocery-delivery-times", "stressor": "dense",
     "attributes": [{
         "attribute": "grocery delivery time",
         "options": ["early-morning delivery", "lunchtime delivery", "mid-afternoon delivery", "evening delivery",
                     "late-night delivery"],
         "value_aliases": {"early-morning delivery": ["a drop-off before eight"],
                           "lunchtime delivery": ["the noon slot"],
                           "mid-afternoon delivery": ["the three o'clock slot"],
                           "evening delivery": ["the after-work slot"],
                           "late-night delivery": ["the last slot of the night"]},
         "scopes": {"nights": ("night-shift weeks", ["my weeks on nights"]),
                    "deadline": ("deadline weeks", ["my crunch weeks"]),
                    "homeoffice": ("home-office weeks", ["my weeks working from home"]),
                    "guests": ("weeks with house guests", ["my in-laws' visits"]),
                    "holidays": ("school holidays", ["the kids' break from school"])}}],
     "initial": {"grocery delivery time": ("evening delivery", {
         "nights": ("early-morning delivery", P),
         "deadline": ("late-night delivery", P),
         "homeoffice": ("lunchtime delivery", P)})},
     "events": [
         {"date": "2028-07-05", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "School holidays start on Friday, so both kids will be home all day until September. Wish me luck.",
              "Good luck! With someone home during the day, would lunchtime delivery make sense for the school "
              "holidays?",
              "Ha, no. Lunchtime with those two is pure chaos, and I'm not adding a delivery driver to it. Leave it "
              "as it is."],
          "probes": [("target", "holidays"), ("neighbor", "homeoffice")],
          "note": "a rejected suggestion: the school holidays keep the usual delivery time"},
         {"date": "2028-07-14", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "grocery delivery time", "guests", "mid-afternoon delivery", P),
          "dialogue": [
              "My in-laws arrive on the 28th for ten days. They come three or four times a year, so I'd better get "
              "organised.",
              "That's nice of them. Does having guests change anything about the grocery orders?",
              "It does. For weeks with house guests, book mid-afternoon delivery. They nap after lunch and are up "
              "again by three, and we're always out in the evenings with them."],
          "probes": [("target", "guests"), ("neighbor", "nights"), ("neighbor", "deadline"), ("default", None)]},
         {"date": "2028-07-25", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "grocery delivery time", "deadline", "early-morning delivery", P),
          "dialogue": [
              "Ugh. Last week was a crunch week, and the late-night driver rang the bell at eleven and woke the "
              "whole house.",
              "That's rough. Did the kids settle again?",
              "Eventually. The thing is, during my crunch weeks I'm up at five anyway, so make it early-morning "
              "delivery for those from now on."],
          "probes": [("target", "deadline"), ("neighbor", "nights"), ("neighbor", "guests"), ("default", None)]},
         {"date": "2028-08-03", "category": "exception_retirement", "evidence": 7,
          "change": ("retire", "grocery delivery time", "homeoffice"),
          "dialogue": [
              "Guess who's training for a half marathon.",
              "No way! When's the race?",
              "Mid-October. I've started running on my lunch break whenever I work from home.",
              "Impressive. How are the legs holding up?",
              "Badly, my knees are complaining. It also means noon deliveries on home-office weeks just sit on the "
              "doorstep in the heat.",
              "Not ideal for the frozen stuff. What would you like to do about it?",
              "Let's drop the lunchtime arrangement for those weeks. I'm back from my run long before any other "
              "slot anyway."],
          "probes": [("target", "homeoffice"), ("neighbor", "guests"), ("neighbor", "deadline"), ("default", None)]},
         {"date": "2028-08-12", "category": "general_update", "evidence": 5,
          "change": ("general", "grocery delivery time", "late-night delivery"),
          "dialogue": [
              "Swim club has moved to six o'clock, so our evenings are now a blur of wet towels and lost goggles.",
              "That sounds hectic! Are the kids enjoying it at least?",
              "They love it. I just wish the pool were closer. The groceries keep turning up while we're out, "
              "though.",
              "Ah, that's annoying. Do you want the deliveries moved?",
              "Yes. Make late-night delivery our regular slot from now on. Once the kids are in bed I can put "
              "everything away in peace."],
          "probes": [("target", None), ("neighbor", "nights"), ("neighbor", "deadline"), ("neighbor", "guests"),
                     ("neighbor", "homeoffice")]},
         {"date": "2028-08-21", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "I've been asked to apply for the team lead role. If I get it, my crunch weeks will be twice as bad.",
              "Congratulations on being asked! Would that change anything for the shopping?",
              "If it happens, I'd probably switch those weeks to mid-afternoon delivery so my partner can take it "
              "in. The interview isn't until October, though, so who knows."],
          "probes": [("target", "deadline"), ("default", None)],
          "note": "a hypothetical change for deadline weeks that depends on a promotion"},
         {"date": "2028-08-30", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "grocery delivery time", "holidays", "early-morning delivery", P),
          "dialogue": [
              "School starts again on Monday, thank goodness. The late deliveries were a disaster this summer: the "
              "kids stayed up to 'help' unpack every single time.",
              "Very helpful of them. Is there anything you'd like done differently next time?",
              "Yes. For school holidays, book early-morning delivery. They sleep in until nine, so I can unpack "
              "before anyone's up."],
          "probes": [("target", "holidays"), ("neighbor", "guests"), ("neighbor", "homeoffice"), ("default", None)]},
     ]},
    {"name": "phone-ringer", "stressor": "dense",
     "attributes": [{
         "attribute": "phone ringer mode",
         "options": ["full-volume ringing", "vibrate only", "total silence", "a soft chime",
                     "favorites-only ringing"],
         "value_aliases": {"full-volume ringing": ["the loudest ring"],
                           "vibrate only": ["just the buzz"],
                           "total silence": ["no sound at all"],
                           "a soft chime": ["the gentle tone"],
                           "favorites-only ringing": ["only my starred contacts"]},
         "scopes": {"meetings": ("work meetings", ["my team meetings"]),
                    "overnight": ("overnight hours", ["my sleeping hours"]),
                    "gym": ("gym sessions", ["my workouts"]),
                    "commute": ("the train commute", ["my ride to work"]),
                    "classes": ("evening classes", ["my night classes"])}}],
     "initial": {"phone ringer mode": ("a soft chime", {
         "meetings": ("vibrate only", P),
         "overnight": ("favorites-only ringing", P),
         "gym": ("full-volume ringing", P)})},
     "events": [
         {"date": "2028-10-03", "category": "exception_revision", "evidence": 5,
          "change": ("revise", "phone ringer mode", "overnight", "full-volume ringing", O),
          "dialogue": [
              "So I've been roped into the on-call rota for the building's heating emergencies.",
              "Oh no. Since when?",
              "Starting tonight. It runs until they hire a second technician, and nobody can tell me when that'll "
              "be.",
              "That sounds stressful. Will the phone need to wake you up for those calls?",
              "Definitely. So for now, overnight I need full-volume ringing or I'll sleep straight through them."],
          "probes": [("target", "overnight"), ("neighbor", "gym"), ("default", None)],
          "note": "temporary with no known end (until a second technician is hired), so open validity"},
         {"date": "2028-10-11", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "My new manager is a bit intense. She keeps her phone on total silence in work meetings and says "
              "from now on the whole team should too.",
              "That's quite a rule. Are you going to follow her lead?",
              "Not a chance. I need to feel the buzz in case the school calls about my son. She can do what she "
              "likes with hers."],
          "probes": [("target", "meetings"), ("default", None)],
          "note": "the manager's preference, which the user turns down"},
         {"date": "2028-10-19", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "phone ringer mode", "commute", "total silence", P),
          "dialogue": [
              "I've started reading on the train again. Two novels already this month.",
              "That's a great habit! Anything good?",
              "A sea mystery and a very long family saga. Only problem is every chime yanks me out of the story, so "
              "on the train commute I'd like total silence."],
          "probes": [("target", "commute"), ("neighbor", "meetings"), ("neighbor", "overnight"), ("default", None)]},
         {"date": "2028-10-27", "category": "general_update", "evidence": 3,
          "change": ("general", "phone ringer mode", "favorites-only ringing"),
          "dialogue": [
              "I got six spam calls yesterday. Six! One of them in the middle of a dentist appointment.",
              "That's ridiculous. Do you want to do something about it?",
              "Yes. From now on my usual setting should be favorites-only ringing. Anyone who matters is starred, "
              "and the rest can leave a message."],
          "probes": [("target", None), ("neighbor", "overnight"), ("neighbor", "gym"), ("neighbor", "commute"),
                     ("neighbor", "meetings")]},
         {"date": "2028-11-04", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "phone ringer mode", "overnight"),
          "dialogue": [
              "Best news all month: they've hired the second technician, so I'm officially off the on-call rota.",
              "Congratulations! You must be relieved.",
              "So relieved. My nights don't need the phone blasting any more, so I don't need anything special "
              "overnight now."],
          "probes": [("target", "overnight"), ("neighbor", "gym"), ("neighbor", "commute"), ("default", None)]},
         {"date": "2028-11-13", "category": "scoped_exception", "evidence": 5,
          "change": ("add", "phone ringer mode", "classes", "vibrate only", P),
          "dialogue": [
              "I signed up for a life-drawing course at the community center, Tuesday and Thursday evenings.",
              "How fun! Have you drawn before?",
              "Only doodles in the margins of meeting notes. The teacher is strict about phones, apparently.",
              "Do you want the phone set up differently for those?",
              "Yes, for evening classes put it on vibrate only. I still want to know if the school rings."],
          "probes": [("target", "classes"), ("neighbor", "meetings"), ("default", None)]},
         {"date": "2028-11-22", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "phone ringer mode", "meetings", "total silence", P),
          "dialogue": [
              "Embarrassing moment today: my phone buzzed so hard against the table during the quarterly review "
              "that the whole room turned around.",
              "Oof. What did your manager say?",
              "Just a look. She had a point all along, I suppose. For work meetings, total silence from now on; I'll "
              "check my messages in between."],
          "probes": [("target", "meetings"), ("neighbor", "classes"), ("neighbor", "commute"), ("default", None)]},
     ]},
]

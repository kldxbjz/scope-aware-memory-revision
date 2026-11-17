"""Temporal: situation records that hold only inside a dated window (announced before it starts, extended later, or
given to an open temporary record afterwards), so the right answer depends on the probe date as well as the situation."""
from spec import P, O, W  # noqa: F401

EPISODES = [
    {"name": "audit-week-calls", "stressor": "temporal",
     "attributes": [{
         "attribute": "meeting time slot",
         "options": ["first thing in the morning", "late morning", "right after lunch", "mid-afternoon",
                     "late afternoon"],
         "value_aliases": {"first thing in the morning": ["the start of the workday"],
                           "late morning": ["just before lunch"],
                           "right after lunch": ["early afternoon"],
                           "mid-afternoon": ["around three"],
                           "late afternoon": ["the end of the workday"]},
         "scopes": {"client": ("client calls", ["calls with clients"]),
                    "retro": ("team retrospectives", ["our retros"]),
                    "interview": ("candidate interviews", ["interviews with applicants"]),
                    "budget": ("budget reviews", ["the monthly budget meetings"])}}],
     "initial": {"meeting time slot": ("late morning", {
         "retro": ("late afternoon", P),
         "interview": ("right after lunch", P)})},
     "events": [
         {"date": "2028-03-03", "category": "scoped_exception", "evidence": 5,
          "change": ("add", "meeting time slot", "client", "first thing in the morning",
                     W("2028-03-10", "2028-03-16")),
          "dialogue": [
              "Morning! Someone finally fixed the coffee machine on our floor, so the week is ending on a high note.",
              "Small victories. Anything you want to sort out before the weekend?",
              "The calendar for the next couple of weeks. Our clients have their annual audit from the 10th through "
              "the 16th, and their finance people are tied up from ten o'clock every day of it.",
              "That doesn't leave them much room. How would you like me to handle it?",
              "For client calls from the 10th through the 16th, book them first thing in the morning, before the "
              "auditors grab everyone. Their calendars free up again after the 16th."],
          "probes": [("boundary", "client"),
                     {"type": "target", "key": "client", "date": "2028-03-13"},
                     {"type": "boundary", "key": "client", "date": "2028-03-17"},
                     {"type": "boundary", "key": "client", "date": "2028-03-24"},
                     ("default", None),
                     {"type": "neighbor", "key": "interview", "date": "2028-03-13"}],
          "note": "a window announced a week before it starts: client calls only from 2028-03-10 through "
                  "2028-03-16; before and after it they follow the usual slot"},
         {"date": "2028-03-27", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "My manager is on the early rota from April 1st through the 14th, so she's doing all her candidate "
              "interviews first thing in the morning.",
              "That's an early start for everyone involved.",
              "Rather her than me. I'm useless before my second coffee, so mine stay in the early afternoon."],
          "probes": [("target", "interview"), {"type": "target", "key": "interview", "date": "2028-04-02"},
                     ("default", None)],
          "note": "the manager's own interview time during her rota (someone else's window), then a restatement of "
                  "the stored interview slot"},
         {"date": "2028-04-03", "category": "general_update", "evidence": 3,
          "change": ("general", "meeting time slot", "mid-afternoon"),
          "dialogue": [
              "I've been trying a new routine for a couple of weeks: mornings are for actual work, no meetings.",
              "How's it going so far?",
              "Better than I expected. Usually, I'd like meetings around three from now on; it keeps the whole "
              "morning clear."],
          "probes": [("target", None), ("neighbor", "retro"), ("boundary", "client")],
          "note": "the usual slot changes; the client-call window ended on 2028-03-16, so client calls now follow "
                  "the new usual slot"},
         {"date": "2028-04-10", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "One of the applicants for the analyst role can only talk on the 13th, before her shift starts at "
              "noon.",
              "That's a narrow slot. What would you like to do?",
              "I'll bend my no-morning-meetings rule for her. Book her interview on the 13th for late morning, just "
              "that once."],
          "probes": [("target", "interview"), ("default", None), ("neighbor", "budget")],
          "note": "a one-off booking for a single interview; the stored interview slot is unchanged"},
         {"date": "2028-04-17", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "meeting time slot", "retro"),
          "dialogue": [
              "Half the team has switched to early hours. They're in at seven and gone by four.",
              "Big change. Has it altered the feel of the office?",
              "It's very quiet by five. It also kills the end-of-day slot for our retros, so let's scrap that. The "
              "late timing only made sense when everyone stayed till six."],
          "probes": [("target", "retro"), ("neighbor", "interview"), ("default", None)]},
         {"date": "2028-04-24", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "meeting time slot", "interview", "late afternoon", P),
          "dialogue": [
              "Recruiting update: most of the people applying now have day jobs, and they keep asking for slots "
              "near the end of the day.",
              "Makes sense if they're job hunting on the quiet.",
              "Exactly. So from now on, put candidate interviews in the late afternoon. I'd rather adjust than lose "
              "good people."],
          "probes": [("target", "interview"), ("neighbor", "retro"), ("neighbor", "budget"), ("default", None)]},
     ]},

    {"name": "branch-line-detour", "stressor": "temporal",
     "attributes": [{
         "attribute": "rail or coach service",
         "options": ["the direct train", "the stopping train", "the express coach", "the rail replacement bus",
                     "the overnight coach"],
         "value_aliases": {"the direct train": ["the fast train"],
                           "the stopping train": ["the slow train"],
                           "the express coach": ["the motorway coach"],
                           "the rail replacement bus": ["the replacement bus"],
                           "the overnight coach": ["the night coach"]},
         "scopes": {"head": ("trips to the head office", ["head office visits"]),
                    "airport": ("airport runs", ["trips to the airport"]),
                    "north": ("family visits up north", ["trips up north to see family"]),
                    "concert": ("concert nights in the city", ["gigs in town"])}}],
     "initial": {"rail or coach service": ("the direct train", {
         "airport": ("the express coach", P),
         "north": ("the overnight coach", P)})},
     "events": [
         {"date": "2028-05-03", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "rail or coach service", "head", "the stopping train", W("2028-05-08", "2028-05-21")),
          "dialogue": [
              "Just got an email from the rail operator: the main line to the head office is shut for engineering "
              "works from the 8th through the 21st.",
              "Two weeks without it, ouch. Is there another way in?",
              "The old branch line still runs. For trips to the head office from the 8th through the 21st, put me "
              "on the slow train. It adds forty minutes, but anything beats the replacement bus."],
          "probes": [("boundary", "head"),
                     {"type": "target", "key": "head", "date": "2028-05-08"},
                     ("default", None), ("neighbor", "airport")],
          "note": "a window announced before it starts: head office trips from 2028-05-08 through 2028-05-21"},
         {"date": "2028-05-09", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Yesterday was my first day on the branch line. Slow, but the views are lovely.",
              "A scenic silver lining. Anything coming up this week?",
              "The board meeting at head office on Friday the 12th starts at eight, and the slow train doesn't get "
              "in until nine. Could you book me the express coach just for that one trip?"],
          "probes": [("target", "head"), ("neighbor", "concert"), ("default", None)],
          "note": "a one-off booking for one day inside the window; the stored record is unchanged"},
         {"date": "2028-05-15", "category": "exception_revision", "evidence": 5,
          "change": ("revise", "rail or coach service", "head", "the stopping train", W("2028-05-08", "2028-05-28")),
          "dialogue": [
              "More news from the rail operator, and not the good kind.",
              "Uh oh. What now?",
              "They found extra damage under the river bridge, so the closure is running long.",
              "How much longer are they saying?",
              "Another week. The main line now stays closed through the 28th, so keep me on the slow train for head "
              "office visits until then."],
          "probes": [("target", "head"),
                     {"type": "target", "key": "head", "date": "2028-05-25"},
                     {"type": "boundary", "key": "head", "date": "2028-05-29"},
                     ("neighbor", "north"),
                     {"type": "default", "key": None, "date": "2028-05-25"}],
          "note": "the closure is extended: the window now ends on 2028-05-28 instead of 2028-05-21"},
         {"date": "2028-06-01", "category": "exception_retirement", "evidence": 5,
          "change": ("retire", "rail or coach service", "north"),
          "dialogue": [
              "Finally booked some time off in July. I'm going to see the family up north for a long weekend.",
              "Lovely. They'll be glad to see you.",
              "They will. My back less so: it still hasn't forgiven me for the last night coach.",
              "Ten hours folded up on a coach would do that. How do you want to get there this time?",
              "For family visits up north, no more night coach, ever. I'll go up the normal way."],
          "probes": [("target", "north"), ("neighbor", "airport"), ("default", None)]},
         {"date": "2028-06-08", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "rail or coach service", "concert", "the stopping train", P),
          "dialogue": [
              "I've got tickets for three gigs in town this summer!",
              "Fun! Who are you seeing?",
              "Mostly local bands. One snag: the last fast train leaves before the encores. For concert nights in "
              "the city, book the stopping train home from now on; it runs until midnight."],
          "probes": [("target", "concert"), ("neighbor", "north"), ("boundary", "head")]},
         {"date": "2028-06-20", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "Saw a notice at the station: the operator may need another closure on the main line in the autumn.",
              "Again? That bridge has it in for you.",
              "Ha, it really does. If it happens I suppose it would be the slow train for head office visits again, "
              "but nothing's announced yet, so for now it's just a rumour."],
          "probes": [("boundary", "head"), ("neighbor", "concert"), ("default", None)],
          "note": "a hypothetical closure with no dates; nothing to store"},
     ]},

    {"name": "builders-next-door", "stressor": "temporal",
     "attributes": [{
         "attribute": "wake-up alarm time",
         "options": ["half past five", "six o'clock", "a quarter to seven", "half past seven", "eight o'clock"],
         "value_aliases": {"half past five": ["five thirty"],
                           "six o'clock": ["six sharp"],
                           "a quarter to seven": ["six forty-five"],
                           "half past seven": ["seven thirty"],
                           "eight o'clock": ["eight sharp"]},
         "scopes": {"remote": ("remote workdays", ["days working from home"]),
                    "commute": ("commuting days", ["days at the office"]),
                    "weekend": ("weekends", ["Saturdays and Sundays"]),
                    "flight": ("early-flight days", ["days with an early flight"])}}],
     "initial": {"wake-up alarm time": ("a quarter to seven", {
         "commute": ("six o'clock", P),
         "weekend": ("eight o'clock", P)})},
     "events": [
         {"date": "2028-07-05", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "wake-up alarm time", "remote", "half past five", O),
          "dialogue": [
              "The house next door is being gutted, and the builders start drilling at seven on the dot.",
              "That's a brutal alarm clock. How are you holding up?",
              "Badly, so I'm getting my focus hour in before they start. On remote workdays, wake me at half past "
              "five for now. They won't say how long the job will take."],
          "probes": [("target", "remote"),
                     {"type": "target", "key": "remote", "date": "2028-07-10"},
                     ("neighbor", "commute"), ("default", None)],
          "note": "temporary with no end given: an open record for remote workdays"},
         {"date": "2028-07-12", "category": "clarify", "evidence": 5, "change": None,
          "dialogue": [
              "Strange confession: I'm starting to enjoy the early starts.",
              "Really? What changed?",
              "The street is silent before six, and I get more done in that hour than in the whole afternoon.",
              "There's something to be said for having the world to yourself.",
              "There is. I might keep the early alarm on remote workdays even once the builders are gone, or I might "
              "not. I usually hate mornings, so let me see how I feel when they're done."],
          "probes": [("target", "remote"), ("neighbor", "weekend")],
          "note": "whether the early alarm outlasts the building work is left open; settled on 2028-07-19"},
         {"date": "2028-07-19", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "wake-up alarm time", "remote", "half past five", W("2028-07-05", "2028-07-24")),
          "dialogue": [
              "Finally, a date from the builders: they'll be finished on the 24th.",
              "Light at the end of the tunnel! You must be counting the days.",
              "I am. And I've decided the dawn club isn't for me. I've been up at half past five on remote workdays "
              "since the 5th; keep that going through the 24th and not a day longer."],
          "probes": [("target", "remote"),
                     {"type": "target", "key": "remote", "date": "2028-07-24"},
                     {"type": "boundary", "key": "remote", "date": "2028-07-25"},
                     ("neighbor", "weekend"), ("default", None)],
          "note": "the open record gets an end date: a window from 2028-07-05 (when it started) through 2028-07-24"},
         {"date": "2028-07-28", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "wake-up alarm time", "commute"),
          "dialogue": [
              "Blissful silence next door. The builders packed up on the 24th as promised.",
              "Enjoy it! Anything else going on with your mornings?",
              "One thing: the office has moved our start time to ten, so I can drop the six o'clock wake-up on "
              "commuting days. Best news all month."],
          "probes": [("target", "commute"), ("boundary", "remote"), ("neighbor", "weekend"), ("default", None)]},
         {"date": "2028-08-04", "category": "general_update", "evidence": 3,
          "change": ("general", "wake-up alarm time", "half past seven"),
          "dialogue": [
              "I joined an evening pottery class. Messy, but I love it.",
              "That sounds like a great way to unwind. How late does it run?",
              "Till ten, so I'm getting to bed later. Normally I'd like to wake up at half past seven now instead "
              "of a quarter to seven."],
          "probes": [("target", None), ("neighbor", "weekend"), ("neighbor", "commute"), ("boundary", "remote")]},
         {"date": "2028-08-11", "category": "stable_preference", "evidence": 3, "change": None,
          "dialogue": [
              "I'm flying to a friend's wedding on the 17th, and the only flight that works leaves at seven.",
              "Early one! Do you need anything sorted for that morning?",
              "Please set my alarm for half past five that day. Just the 17th, though. Normally I'd never book "
              "anything that early, and I'm not planning to make a habit of it."],
          "probes": [("target", "flight"), ("default", None)],
          "note": "a one-off alarm for one date; no lasting preference for early-flight days"},
     ]},

    {"name": "book-club-and-game-nights", "stressor": "temporal",
     "attributes": [{
         "attribute": "guest meal format",
         "options": ["a sit-down meal", "a buffet spread", "a potluck", "a backyard barbecue", "drinks and nibbles",
                     "a takeaway night"],
         "value_aliases": {"a sit-down meal": ["a proper meal at the table"],
                           "a buffet spread": ["a help-yourself buffet"],
                           "a potluck": ["a bring-a-dish night"],
                           "a backyard barbecue": ["a grill-out in the garden"],
                           "drinks and nibbles": ["just drinks and snacks"],
                           "a takeaway night": ["ordered-in food"]},
         "scopes": {"book": ("book club evenings", ["my book club nights"]),
                    "game": ("board game nights", ["game nights"]),
                    "family": ("family Sunday lunches", ["Sunday lunch with the family"]),
                    "team": ("team socials", ["get-togethers with my team"])}}],
     "initial": {"guest meal format": ("a sit-down meal", {
         "team": ("a backyard barbecue", P),
         "family": ("a potluck", P)})},
     "events": [
         {"date": "2028-09-04", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "guest meal format", "book", "drinks and nibbles", W("2028-09-11", "2028-09-24")),
          "dialogue": [
              "Our book club voted to tackle a giant trilogy, so we're meeting twice a week from the 11th through "
              "the 24th.",
              "That's a serious reading schedule. Are they all coming to yours?",
              "Every single time. I'm not cooking a full meal twice a week, so for book club evenings from the 11th "
              "through the 24th, just drinks and nibbles."],
          "probes": [("boundary", "book"),
                     {"type": "target", "key": "book", "date": "2028-09-12"},
                     ("default", None), ("neighbor", "team")],
          "note": "first window, announced a week ahead: book club evenings from 2028-09-11 through 2028-09-24"},
         {"date": "2028-09-14", "category": "general_update", "evidence": 3,
          "change": ("general", "guest meal format", "a buffet spread"),
          "dialogue": [
              "I hosted my cousins at the weekend and spent the whole evening plating food instead of talking to "
              "anyone.",
              "The classic host's curse. Did they enjoy it, at least?",
              "They loved it, but I barely sat down. So from here on I'd rather do a buffet spread than a sit-down "
              "meal; that way I can actually join in."],
          "probes": [("target", None), ("neighbor", "book"), ("neighbor", "family"), ("neighbor", "game")],
          "note": "the usual format changes while the book club window is running; the window record is untouched"},
         {"date": "2028-09-17", "category": "scoped_exception", "evidence": 3,
          "change": ("add", "guest meal format", "game", "a takeaway night", W("2028-09-20", "2028-10-03")),
          "dialogue": [
              "Bad news for game nights: the friend who always does the cooking for them is away on a work trip "
              "from the 20th through October 3rd.",
              "Losing your chef is rough. What's the plan?",
              "For game nights from the 20th through October 3rd, let's make it a takeaway night. Nobody wants my "
              "cooking in the middle of a six-hour strategy game."],
          "probes": [{"type": "target", "key": "game", "date": "2028-09-22"},
                     {"type": "neighbor", "key": "book", "date": "2028-09-22"},
                     {"type": "default", "key": None, "date": "2028-09-22"},
                     {"type": "boundary", "key": "book", "date": "2028-09-27"},
                     {"type": "target", "key": "game", "date": "2028-09-27"},
                     {"type": "boundary", "key": "game", "date": "2028-10-05"}],
          "note": "second window, 2028-09-20 through 2028-10-03, overlapping the book club window on 2028-09-20 "
                  "through 2028-09-24"},
         {"date": "2028-10-09", "category": "stable_preference", "evidence": 5, "change": None,
          "dialogue": [
              "My brother is taking a turn hosting the family Sunday lunch this week.",
              "A week off for you, then! Does he have big plans?",
              "He's going all out: a sit-down meal with place cards and everything, and he says that's how he'll "
              "host from now on.",
              "Fancy! Are you bringing anything?",
              "Just dessert. When it's at my place it's still a potluck, though. I'm not trying to compete."],
          "probes": [("target", "family"), ("default", None)],
          "note": "the brother's own hosting style (someone else's lasting preference), then a restatement of the "
                  "stored family-lunch format"},
         {"date": "2028-10-16", "category": "exception_retirement", "evidence": 3,
          "change": ("retire", "guest meal format", "team"),
          "dialogue": [
              "Had the team round at the weekend. It was freezing, and everyone huddled round the grill in their "
              "coats.",
              "Brr. Did people still have a good time?",
              "They did, but let's leave the grill out of team socials from now on. I'm tired of smelling like "
              "smoke for two days afterwards."],
          "probes": [("target", "team"), ("neighbor", "family"), ("default", None)]},
         {"date": "2028-10-23", "category": "exception_revision", "evidence": 3,
          "change": ("revise", "guest meal format", "family", "a sit-down meal", P),
          "dialogue": [
              "Lunch at my brother's the other week was lovely, actually. Everyone sat at the table and talked for "
              "hours.",
              "That sounds like a nice change of pace.",
              "It was. Our potlucks have turned into a cooking contest, so for family Sunday lunches I'd like a "
              "proper meal at the table from now on. I'll do the cooking."],
          "probes": [("target", "family"), ("neighbor", "team"), ("boundary", "game"), ("default", None)]},
     ]},
]

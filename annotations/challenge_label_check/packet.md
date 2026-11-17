# Label audit packet

For each item, read the stored preferences and the conversation, then choose the one category that describes what should change in the user's lasting preferences (protocol section 3). Label alone; do not look up the data files.

- `general_update`: the usual (general) preference changes; situation-specific preferences stay
- `scoped_exception`: a new preference for one situation (lasting, for dates, or for now)
- `exception_revision`: an existing situation-specific preference changes its value or its dates
- `exception_retirement`: an existing situation-specific preference is dropped, so that situation follows the usual preference again
- `stable_preference`: nothing to store: a one-off request, someone else's or a quoted preference, a hypothetical, a rejected suggestion, or a restated preference
- `clarify`: nothing to store yet: the user leaves open what should change or for how long

## L001 (2028-01-09)

Stored preferences:
- For workout audio, the user prefers an upbeat playlist.
- For workout audio when indoor trainer rides, the user prefers a comedy podcast.
- For workout audio when outdoor bike rides, the user prefers no audio at all.
- For workout audio when short runs, the user prefers a news podcast.

Conversation:
- user: Rode out to the reservoir with my cycling buddy this morning. He does the whole loop with fast music in one ear and swears it gets him up the hills.
- assistant: Ha, whatever gets you up the hills. Were you tempted to copy him?
- user: Not really. On my rides on the open road I want to hear every car coming up behind me, so nothing in my ears for me.

## L002 (2028-06-20)

Stored preferences:
- For taxi vehicle type, the user prefers a standard sedan.
- For taxi vehicle type when rides to the airport, the user prefers a roomy minivan.
- For taxi vehicle type when rides to client meetings, the user prefers a premium car with leather seats.

Conversation:
- user: Had lunch with my business partner. She's convinced that for trips to see clients we should always show up in an EV, says it tells them we're a modern outfit.
- assistant: That's one way to make an impression. What do you think?
- user: It works for her clients, they're all young startups. Mine expect a bit of comfort, so that's not changing for me.

## L003 (2028-04-28)

Stored preferences:
- For gift wrapping style, the user prefers a reusable cloth wrap.
- For gift wrapping style when presents for nieces and nephews, the user prefers a patterned gift bag.
- For gift wrapping style when gifts for coworkers, the user prefers brown kraft paper with twine.

Conversation:
- user: Three weddings this summer. Three! My weekends are nothing but gift tables.
- assistant: Busy season. Have you thought about how you want those wrapped?
- user: Yes. For wedding gifts I want glossy paper with a satin ribbon, whoever's getting married. A cloth wrap looks a bit too casual on a table full of fancy boxes.

## L004 (2028-04-03)

Stored preferences:
- For meeting time slot, the user prefers late morning.
- For meeting time slot when client calls, the user prefers first thing in the morning from 2028-03-10 through 2028-03-16.
- For meeting time slot when candidate interviews, the user prefers right after lunch.
- For meeting time slot when team retrospectives, the user prefers late afternoon.

Conversation:
- user: I've been trying a new routine for a couple of weeks: mornings are for actual work, no meetings.
- assistant: How's it going so far?
- user: Better than I expected. Usually, I'd like meetings around three from now on; it keeps the whole morning clear.

## L005 (2028-05-09)

Stored preferences:
- For living room lighting, the user prefers the floor lamps alone.
- For living room lighting when video calls, the user prefers bright white light.
- For living room lighting when dinner parties, the user prefers a warm low glow.
- For living room lighting when homework hour, the user prefers bright white light.
- For living room lighting when movie nights, the user prefers the TV backlight.

Conversation:
- user: Parent-teacher evening was last night. Both kids are doing fine, which I'll gladly take.
- assistant: That's great to hear! Did anything come out of it for home?
- user: Only that the school gave every pupil a clip-on desk light, so homework hour doesn't need full brightness in the living room any more. No special lighting for it from now on.

## L006 (2028-04-11)

Stored preferences:
- For gift wrapping style, the user prefers a reusable cloth wrap.
- For gift wrapping style when presents for nieces and nephews, the user prefers a patterned gift bag.
- For gift wrapping style when gifts for coworkers, the user prefers brown kraft paper with twine.

Conversation:
- user: Someone on my team is leaving on Friday, so I ordered a little succulent for her desk.
- assistant: That's sweet of you. Should I add gift wrapping to the order?
- user: Yes please. Brown paper and string, same as I always do for presents for people at work. Nobody in the office goes in for anything flashy.

## L007 (2028-07-04)

Stored preferences:
- For mulch material, the user prefers shredded bark.
- For mulch material when the strawberry patch, the user prefers barley straw.
- For mulch material when the herb garden, the user prefers pea gravel.

Conversation:
- user: Slug carnage on the strawberries this year. I lifted the straw yesterday and there were dozens of them living underneath.
- assistant: Ugh, that must have been grim to find.
- user: Grim is the word. The strawberry patch doesn't get its own special mulch any more. It can have the same as the rest of the garden.

## L008 (2028-11-13)

Stored preferences:
- For phone ringer mode, the user prefers favorites-only ringing.
- For phone ringer mode when the train commute, the user prefers total silence.
- For phone ringer mode when gym sessions, the user prefers full-volume ringing.
- For phone ringer mode when work meetings, the user prefers vibrate only.

Conversation:
- user: I signed up for a life-drawing course at the community center, Tuesday and Thursday evenings.
- assistant: How fun! Have you drawn before?
- user: Only doodles in the margins of meeting notes. The teacher is strict about phones, apparently.
- assistant: Do you want the phone set up differently for those?
- user: Yes, for evening classes put it on vibrate only. I still want to know if the school rings.

## L009 (2028-11-12)

Stored preferences:
- For topping for home-baked cakes, the user prefers a simple lemon glaze.
- For topping for home-baked cakes when birthday parties, the user prefers whipped cream.
- For topping for home-baked cakes when bake sales at work, the user prefers salted caramel drizzle.

Conversation:
- user: I've gone right off glazes. The lemon ones keep going sticky and weepy by the second day.
- assistant: That's annoying. Could it be the damp weather?
- user: Maybe. Either way, my usual from now on is just a dusting of icing sugar. Less fuss, and it still looks pretty.

## L010 (2028-02-12)

Stored preferences:
- For workout audio, the user prefers a comedy podcast.
- For workout audio when indoor trainer rides, the user prefers a guided coaching track.
- For workout audio when long runs, the user prefers an audiobook for now, with no end date given.
- For workout audio when outdoor bike rides, the user prefers no audio at all.
- For workout audio when short runs, the user prefers a news podcast.

Conversation:
- user: Can I moan for a second? I'm bored of what I listen to on one kind of run. Either my quick runs or my distance runs, and I honestly can't tell which.
- assistant: Moan away. Is it the content itself, or just hearing the same kind of thing every time?
- user: No idea yet. I'll pay attention this week and let you know which one it is.

## L011 (2028-04-27)

Stored preferences:
- For long-distance transport, the user prefers the high-speed train.
- For long-distance transport when trips with the dog, the user prefers a rental car.
- For long-distance transport when weekend getaways, the user prefers a rental car.
- For long-distance transport when work trips, the user prefers the overnight sleeper.
- For main travel bag, the user prefers a wheeled carry-on.
- For main travel bag when weekend getaways, the user prefers a canvas duffel.
- For main travel bag when work trips, the user prefers a garment bag.

Conversation:
- user: This weekend's trip is a bit different: my cousin is getting married out in the countryside.
- assistant: How lovely! Do you need anything special for it?
- user: Just for this one, pack the suit carrier instead of the duffel. I'm not turning up to a wedding with a crumpled jacket. After that it's back to the duffel.

## L012 (2028-04-24)

Stored preferences:
- For meeting time slot, the user prefers mid-afternoon.
- For meeting time slot when client calls, the user prefers first thing in the morning from 2028-03-10 through 2028-03-16.
- For meeting time slot when candidate interviews, the user prefers right after lunch.

Conversation:
- user: Recruiting update: most of the people applying now have day jobs, and they keep asking for slots near the end of the day.
- assistant: Makes sense if they're job hunting on the quiet.
- user: Exactly. So from now on, put candidate interviews in the late afternoon. I'd rather adjust than lose good people.

## L013 (2028-05-06)

Stored preferences:
- For gift wrapping style, the user prefers a reusable cloth wrap.
- For gift wrapping style when presents for nieces and nephews, the user prefers a patterned gift bag.
- For gift wrapping style when wedding gifts, the user prefers glossy paper with a satin ribbon.
- For gift wrapping style when gifts for coworkers, the user prefers brown kraft paper with twine.

Conversation:
- user: Now that most of my presents go out in cloth, two of my old wrapping habits look a bit odd: the gift bags for the kids in the family and the brown paper for people at work.
- assistant: Do you want to change both of them?
- user: No, just one, but I honestly can't decide which. Let me sit on it for a while.

## L014 (2028-04-12)

Stored preferences:
- For living room lighting, the user prefers a warm low glow.
- For living room lighting when video calls, the user prefers bright white light.
- For living room lighting when dinner parties, the user prefers candlelight.
- For living room lighting when homework hour, the user prefers bright white light.
- For living room lighting when movie nights, the user prefers the TV backlight.

Conversation:
- user: My brother is coming over tonight to watch that new haunted-lighthouse film everyone keeps talking about.
- assistant: Sounds like a fun evening! Are you a horror fan?
- user: Not remotely. He is, though, and he swears it only works in the pitch dark.
- assistant: Want the living room set up for it?
- user: Yes, but just for tonight: every light off, even the strip behind the screen. Normally I'd hate that, but I'll survive one evening of it.

## L015 (2028-10-23)

Stored preferences:
- For notebook page ruling, the user prefers plain blank pages.
- For notebook page ruling when monthly budget planning, the user prefers a square grid.
- For notebook page ruling when sketching page layouts, the user prefers a dot grid.
- For pen ink color, the user prefers black ink.
- For pen ink color when marking up drafts, the user prefers green ink for now, with no end date given.
- For pen ink color when signing contracts, the user prefers navy blue ink.

Conversation:
- user: Deadline survived. And I worked out the notebook thing: it's the layout sketches.
- assistant: Oh? What's wrong with them?
- user: I'm doing much tighter wireframes now and the dots just aren't precise enough. For drafting layouts I want graph paper from now on.

## L016 (2028-03-05)

Stored preferences:
- For laundry drying method, the user prefers a low-heat tumble dry.
- For laundry drying method when work shirts, the user prefers hanging on padded hangers.
- For laundry drying method when white bath towels, the user prefers line drying outside.
- For laundry drying method when wool jumpers, the user prefers drying flat on a towel.

Conversation:
- user: Small laundry tragedy this morning. My favourite cotton sweater came out of the dryer about two sizes smaller.
- assistant: Oh no! Any chance of stretching it back out?
- user: Not a hope, it's going to my niece. From now on my cotton sweaters go on the clothes horse, please, not in the dryer.

## L017 (2028-02-20)

Stored preferences:
- For workout audio, the user prefers a comedy podcast.
- For workout audio when indoor trainer rides, the user prefers a guided coaching track.
- For workout audio when long runs, the user prefers an audiobook for now, with no end date given.
- For workout audio when outdoor bike rides, the user prefers no audio at all.
- For workout audio when short runs, the user prefers a news podcast.

Conversation:
- user: Mystery solved: it's my quick runs.
- assistant: Good detective work. What gave it away?
- user: The daily news is just too slow and gloomy for twenty hard minutes. On my quick runs I want fast music. I know I went off it, but for short and sharp it's exactly right.

## L018 (2028-04-18)

Stored preferences:
- For laundry drying method, the user prefers line drying outside.
- For laundry drying method when cotton jumpers, the user prefers an indoor drying rack.
- For laundry drying method when work shirts, the user prefers hanging on padded hangers.
- For laundry drying method when white bath towels, the user prefers a high-heat tumble dry.
- For laundry drying method when wool jumpers, the user prefers drying flat on a towel.

Conversation:
- user: Nearly three weeks of sunshine and my navy towels already look washed out. They're practically grey.
- assistant: The sun can be brutal on dark colours. Do you want to change how they're dried?
- user: Yes. Keep my dark towels out of the sun and put them on the clothes horse indoors.

## L019 (2028-03-27)

Stored preferences:
- For meeting time slot, the user prefers late morning.
- For meeting time slot when client calls, the user prefers first thing in the morning from 2028-03-10 through 2028-03-16.
- For meeting time slot when candidate interviews, the user prefers right after lunch.
- For meeting time slot when team retrospectives, the user prefers late afternoon.

Conversation:
- user: My manager is on the early rota from April 1st through the 14th, so she's doing all her candidate interviews first thing in the morning.
- assistant: That's an early start for everyone involved.
- user: Rather her than me. I'm useless before my second coffee, so mine stay in the early afternoon.

## L020 (2028-09-19)

Stored preferences:
- For background music style, the user prefers classical piano.
- For background music style when dinner with friends, the user prefers old soul records.
- For background music style when evenings with the kids, the user prefers film soundtracks.
- For evening film genre, the user prefers a slow-burn thriller.
- For evening film genre when film club evenings, the user prefers an old black-and-white classic.
- For evening film genre when date nights, the user prefers a romantic comedy.
- For evening film genre when evenings with the kids, the user prefers an animated feature.

Conversation:
- user: Since the school trip to the aquarium, the kids are obsessed with sea creatures. Cartoons are suddenly 'for babies'.
- assistant: Ha, that happens fast. What would they enjoy now?
- user: On family evenings let's do a wildlife film instead. Keep the movie scores going in the background, though, they still ask for those.

## L021 (2028-04-03)

Stored preferences:
- For gift wrapping style, the user prefers glossy paper with a satin ribbon.
- For gift wrapping style when presents for nieces and nephews, the user prefers a patterned gift bag.
- For gift wrapping style when gifts for coworkers, the user prefers brown kraft paper with twine.

Conversation:
- user: We did my dad's birthday yesterday, and afterwards half the recycling bin was shiny wrapping paper. It felt a bit obscene.
- assistant: It does pile up. Has it put you off the shiny stuff?
- user: Pretty much. For most presents I'd like a reusable cloth wrap from now on. People can hand it back or use it again, I don't mind which.

## L022 (2028-08-03)

Stored preferences:
- For taxi vehicle type, the user prefers a fully electric car.
- For taxi vehicle type when rides to the airport, the user prefers a compact hatchback.
- For taxi vehicle type when rides to client meetings, the user prefers a premium car with leather seats.

Conversation:
- user: Back from a trip to the regional office last night. The little hatchback was perfect for one bag.
- assistant: Glad it worked out. Want me to book an EV for airport trips from now on? They're often cheaper on the early runs.
- user: No, stick with the small cars for those. The electric ones out near the airport are usually miles away and I'd rather not stand around waiting.

## L023 (2028-01-15)

Stored preferences:
- For reward treat for the dog, the user prefers carrot sticks.
- For reward treat for the dog when obedience classes, the user prefers freeze-dried liver bites.
- For reward treat for the dog when trips to the vet, the user prefers peanut butter biscuits.

Conversation:
- user: Guess who finally nailed the long down-stay at training class last night?
- assistant: No way! That's a tough one. What do you think made it click?
- user: The liver bites, honestly. She would sell her soul for them. Keep them coming for class, they're clearly doing the job.

## L024 (2028-01-25)

Stored preferences:
- For hotel room placement, the user prefers a room on a high floor.
- For hotel room placement when beach holidays, the user prefers a ground-floor room.
- For hotel room placement when conference trips, the user prefers a room near the lifts.
- For hotel room placement when overnight layovers, the user prefers a room at the quiet end of the corridor.
- For hotel room placement when road trips, the user prefers a room overlooking the courtyard.

Conversation:
- user: The lifts at that last conference hotel were a disaster. Twenty minutes just to get down for the keynote.
- assistant: That sounds miserable. Should I book those differently?
- user: Please. For work conferences, put me in a room next to the stairwell from now on so I can just walk down.

## L025 (2028-06-01)

Stored preferences:
- For rail or coach service, the user prefers the direct train.
- For rail or coach service when airport runs, the user prefers the express coach.
- For rail or coach service when trips to the head office, the user prefers the stopping train from 2028-05-08 through 2028-05-28.
- For rail or coach service when family visits up north, the user prefers the overnight coach.

Conversation:
- user: Finally booked some time off in July. I'm going to see the family up north for a long weekend.
- assistant: Lovely. They'll be glad to see you.
- user: They will. My back less so: it still hasn't forgiven me for the last night coach.
- assistant: Ten hours folded up on a coach would do that. How do you want to get there this time?
- user: For family visits up north, no more night coach, ever. I'll go up the normal way.

## L026 (2028-02-25)

Stored preferences:
- For reward treat for the dog, the user prefers carrot sticks.
- For reward treat for the dog when trips to the vet, the user prefers freeze-dried liver bites.

Conversation:
- user: News from the fussy department: she's gone off carrots. Picks them up, spits them out, gives me a look.
- assistant: A dog with opinions! Has anything else caught her interest lately?
- user: Apple, of all things. She pinched a slice off my plate and did a little dance. Let's make apple slices her usual treat now.

## L027 (2028-10-24)

Stored preferences:
- For meeting length, the user prefers a full hour.
- For meeting length when release weeks, the user prefers a 15-minute check-in.
- For meeting length when planning days, the user prefers a 90-minute working session.
- For quick-question channel, the user prefers stopping by their desk.
- For quick-question channel when release weeks, the user prefers a five-minute video call.
- For quick-question channel when remote days, the user prefers a chat message.

Conversation:
- user: Good news: we finally hired a release manager, so release weeks should be a lot calmer.
- assistant: That's a relief! Does it change how you want those weeks to run?
- user: It does. In launch weeks my meetings don't need squeezing into quick check-ins anymore. I do still want the quick video chats for questions in those weeks, though.

## L028 (2028-08-08)

Stored preferences:
- For mulch material, the user prefers leaf mould.
- For mulch material when the herb garden, the user prefers pea gravel.

Conversation:
- user: The new strawberry runners have rooted, so that bed is back in business.
- assistant: Lovely. Are you planning anything different this time round?
- user: Yes. For the strawberry patch I want grass clippings from now on. A thin layer keeps the berries off the soil, and the slugs can't hide in it the way they did in the straw.

## L029 (2028-05-07)

Stored preferences:
- For phone alert style, the user prefers a single soft chime.
- For phone alert style when cinema trips, the user prefers vibration only.
- For phone alert style when the evening train ride, the user prefers silent banners.
- For phone alert style when dinners out with friends, the user prefers alerts held for later.

Conversation:
- user: Tried the little noodle bar near the station on my own last night. Tiny room, about eight tables.
- assistant: Sounds cosy. Was the food any good?
- user: Excellent. But my phone kept chiming and the whole room turned round every time. When I'm eating out by myself, just a buzz from now on, please.

## L030 (2028-08-21)

Stored preferences:
- For grocery delivery time, the user prefers late-night delivery.
- For grocery delivery time when deadline weeks, the user prefers early-morning delivery.
- For grocery delivery time when weeks with house guests, the user prefers mid-afternoon delivery.
- For grocery delivery time when night-shift weeks, the user prefers early-morning delivery.

Conversation:
- user: I've been asked to apply for the team lead role. If I get it, my crunch weeks will be twice as bad.
- assistant: Congratulations on being asked! Would that change anything for the shopping?
- user: If it happens, I'd probably switch those weeks to mid-afternoon delivery so my partner can take it in. The interview isn't until October, though, so who knows.

## L031 (2028-11-22)

Stored preferences:
- For phone ringer mode, the user prefers favorites-only ringing.
- For phone ringer mode when evening classes, the user prefers vibrate only.
- For phone ringer mode when the train commute, the user prefers total silence.
- For phone ringer mode when gym sessions, the user prefers full-volume ringing.
- For phone ringer mode when work meetings, the user prefers vibrate only.

Conversation:
- user: Embarrassing moment today: my phone buzzed so hard against the table during the quarterly review that the whole room turned around.
- assistant: Oof. What did your manager say?
- user: Just a look. She had a point all along, I suppose. For work meetings, total silence from now on; I'll check my messages in between.

## L032 (2028-10-02)

Stored preferences:
- For topping for home-baked cakes, the user prefers cream cheese frosting.
- For topping for home-baked cakes when birthday parties, the user prefers chocolate ganache.
- For topping for home-baked cakes when bake sales at work, the user prefers salted caramel drizzle.

Conversation:
- user: I made a carrot cake at the weekend and couldn't even finish a slice. The frosting sat in my stomach like a brick.
- assistant: Too rich these days?
- user: Way too rich for me. Normally I'd rather have a simple lemon glaze on top now, something lighter.

## L033 (2028-02-21)

Stored preferences:
- For hotel room placement, the user prefers a room near the lifts.
- For hotel room placement when conference trips, the user prefers a room next to the stairwell.
- For hotel room placement when overnight layovers, the user prefers a room at the quiet end of the corridor.
- For hotel room placement when road trips, the user prefers a room overlooking the courtyard.

Conversation:
- user: I think I want something different either for stopovers between flights or for trips to see my grandparents. I honestly can't tell which one is bugging me.
- assistant: No rush. What's making you reconsider?
- user: Just sleeping badly on both lately. I'll work out which one it is after the next trip.

## L034 (2028-07-25)

Stored preferences:
- For grocery delivery time, the user prefers evening delivery.
- For grocery delivery time when deadline weeks, the user prefers late-night delivery.
- For grocery delivery time when weeks with house guests, the user prefers mid-afternoon delivery.
- For grocery delivery time when home-office weeks, the user prefers lunchtime delivery.
- For grocery delivery time when night-shift weeks, the user prefers early-morning delivery.

Conversation:
- user: Ugh. Last week was a crunch week, and the late-night driver rang the bell at eleven and woke the whole house.
- assistant: That's rough. Did the kids settle again?
- user: Eventually. The thing is, during my crunch weeks I'm up at five anyway, so make it early-morning delivery for those from now on.

## L035 (2028-02-17)

Stored preferences:
- For commute mode, the user prefers cycling in.
- For commute mode when gym days, the user prefers driving myself.
- For commute mode when late shifts, the user prefers driving myself.
- For commute mode when rainy days, the user prefers the commuter train.
- For packed lunch, the user prefers a veggie wrap.
- For packed lunch when gym days, the user prefers a chicken and rice bowl.
- For packed lunch when rainy days, the user prefers a thermos of soup.

Conversation:
- user: Big news: the gym opened a second branch on the ground floor of our office building.
- assistant: Oh, that's convenient! Does it change anything on your gym days?
- user: It does! No more dragging the car in on workout days, there's just no reason anymore. I still want the rice bowl those days though, the classes are as brutal as ever.

## L036 (2028-09-22)

Stored preferences:
- For notebook page ruling, the user prefers narrow-ruled lines.
- For notebook page ruling when monthly budget planning, the user prefers a square grid.
- For notebook page ruling when sketching page layouts, the user prefers a dot grid.
- For pen ink color, the user prefers black ink.
- For pen ink color when marking up drafts, the user prefers green ink for now, with no end date given.
- For pen ink color when signing contracts, the user prefers navy blue ink.

Conversation:
- user: I've started thinking in little boxes and arrows, and the ruled lines in my notebooks keep getting in the way.
- assistant: Sounds like your notebooks aren't keeping up with you.
- user: They're not. Most of the time I'd like unlined paper now. Lines only made sense back when I wrote neat paragraphs.

## L037 (2028-02-28)

Stored preferences:
- For commute mode, the user prefers cycling in.
- For commute mode when late shifts, the user prefers driving myself.
- For commute mode when rainy days, the user prefers the commuter train.
- For packed lunch, the user prefers a veggie wrap.
- For packed lunch when gym days, the user prefers a chicken and rice bowl.
- For packed lunch when rainy days, the user prefers a thermos of soup.

Conversation:
- user: Something about rainy days isn't working for me lately and I want to change it. I just can't tell yet whether it's the trip in or the lunch.
- assistant: Do you want to talk it through now, or see how it goes for a bit?
- user: Give me a few more grey mornings to figure it out, then I'll tell you which one it is.

## L038 (2028-07-25)

Stored preferences:
- For mulch material, the user prefers shredded bark.
- For mulch material when the herb garden, the user prefers pea gravel.

Conversation:
- user: I finally emptied the leaf cage. Three autumns' worth, dark and crumbly, it's gorgeous stuff.
- assistant: Gardener's gold! What are you planning to do with it all?
- user: Use it. Leaf mould is my standard mulch from now on. It's free, and the worms go mad for it.

## L039 (2028-10-11)

Stored preferences:
- For topping for home-baked cakes, the user prefers a simple lemon glaze.
- For topping for home-baked cakes when birthday parties, the user prefers chocolate ganache.
- For topping for home-baked cakes when bake sales at work, the user prefers salted caramel drizzle.

Conversation:
- user: There's a bake sale at work next Friday. A colleague says the ganache cakes always sell out first.
- assistant: Are you tempted to switch things up?
- user: Nope. People queue for my caramel drizzle, I'm not messing with a winning formula. Same as ever for the office bake sale.

## L040 (2028-09-17)

Stored preferences:
- For guest meal format, the user prefers a buffet spread.
- For guest meal format when book club evenings, the user prefers drinks and nibbles from 2028-09-11 through 2028-09-24.
- For guest meal format when family Sunday lunches, the user prefers a potluck.
- For guest meal format when team socials, the user prefers a backyard barbecue.

Conversation:
- user: Bad news for game nights: the friend who always does the cooking for them is away on a work trip from the 20th through October 3rd.
- assistant: Losing your chef is rough. What's the plan?
- user: For game nights from the 20th through October 3rd, let's make it a takeaway night. Nobody wants my cooking in the middle of a six-hour strategy game.

## L041 (2028-10-02)

Stored preferences:
- For notebook page ruling, the user prefers plain blank pages.
- For notebook page ruling when monthly budget planning, the user prefers a square grid.
- For notebook page ruling when sketching page layouts, the user prefers a dot grid.
- For pen ink color, the user prefers black ink.
- For pen ink color when marking up drafts, the user prefers green ink for now, with no end date given.
- For pen ink color when signing contracts, the user prefers navy blue ink.

Conversation:
- user: The lease renewal finally came through. I'm signing it at the landlord's office tomorrow morning.
- assistant: That's a relief! Anything you need to bring?
- user: Their form says black ink only, so just for tomorrow's signing I'll need a black pen. Their rule, not mine. Can you put it on my list for the morning?

## L042 (2028-09-14)

Stored preferences:
- For guest meal format, the user prefers a sit-down meal.
- For guest meal format when book club evenings, the user prefers drinks and nibbles from 2028-09-11 through 2028-09-24.
- For guest meal format when family Sunday lunches, the user prefers a potluck.
- For guest meal format when team socials, the user prefers a backyard barbecue.

Conversation:
- user: I hosted my cousins at the weekend and spent the whole evening plating food instead of talking to anyone.
- assistant: The classic host's curse. Did they enjoy it, at least?
- user: They loved it, but I barely sat down. So from here on I'd rather do a buffet spread than a sit-down meal; that way I can actually join in.

## L043 (2028-05-03)

Stored preferences:
- For rail or coach service, the user prefers the direct train.
- For rail or coach service when airport runs, the user prefers the express coach.
- For rail or coach service when family visits up north, the user prefers the overnight coach.

Conversation:
- user: Just got an email from the rail operator: the main line to the head office is shut for engineering works from the 8th through the 21st.
- assistant: Two weeks without it, ouch. Is there another way in?
- user: The old branch line still runs. For trips to the head office from the 8th through the 21st, put me on the slow train. It adds forty minutes, but anything beats the replacement bus.

## L044 (2028-10-23)

Stored preferences:
- For guest meal format, the user prefers a buffet spread.
- For guest meal format when book club evenings, the user prefers drinks and nibbles from 2028-09-11 through 2028-09-24.
- For guest meal format when family Sunday lunches, the user prefers a potluck.
- For guest meal format when board game nights, the user prefers a takeaway night from 2028-09-20 through 2028-10-03.

Conversation:
- user: Lunch at my brother's the other week was lovely, actually. Everyone sat at the table and talked for hours.
- assistant: That sounds like a nice change of pace.
- user: It was. Our potlucks have turned into a cooking contest, so for family Sunday lunches I'd like a proper meal at the table from now on. I'll do the cooking.

## L045 (2028-06-07)

Stored preferences:
- For long-distance transport, the user prefers the intercity coach.
- For long-distance transport when trips with the dog, the user prefers a rental car.
- For long-distance transport when weekend getaways, the user prefers a rental car.
- For long-distance transport when work trips, the user prefers the overnight sleeper.
- For main travel bag, the user prefers a wheeled carry-on.
- For main travel bag when work trips, the user prefers a garment bag.

Conversation:
- user: We finally bought a proper tent! First trip is in two weeks and I'm far too excited.
- assistant: Exciting! How do you want to pack for that sort of trip?
- user: For camping trips it has to be the big rucksack. A bag on wheels is useless on a muddy path.

## L046 (2028-10-12)

Stored preferences:
- For meeting length, the user prefers a full hour.
- For meeting length when release weeks, the user prefers a 15-minute check-in.
- For meeting length when planning days, the user prefers a 90-minute working session.
- For quick-question channel, the user prefers stopping by their desk.
- For quick-question channel when release weeks, the user prefers a five-minute video call.
- For quick-question channel when remote days, the user prefers a chat message.

Conversation:
- user: Tomorrow's a remote day for me, but I'll be stuck on a train half the morning with terrible signal.
- assistant: Annoying. Anything you'd like set up for it?
- user: Just for tomorrow, if anyone has a quick question they should ring me instead of messaging. Chat won't load on that line.

## L047 (2028-07-12)

Stored preferences:
- For mulch material, the user prefers shredded bark.
- For mulch material when the herb garden, the user prefers pea gravel.

Conversation:
- user: Had a long chat over the fence this morning. The neighbour swears pine needles are the secret to sweet strawberries.
- assistant: Would you want to try that on the strawberry patch?
- user: Not this year. After the slug disaster I'd rather leave that bed alone and see how it does with the usual stuff.

## L048 (2028-07-03)

Stored preferences:
- For phone alert style, the user prefers full sound and vibration.
- For phone alert style when cinema trips, the user prefers vibration only.
- For phone alert style when the evening train ride, the user prefers silent banners.
- For phone alert style when dinners out with friends, the user prefers silent banners.
- For phone alert style when the morning train ride, the user prefers alerts held for later from 2028-06-12 through 2028-06-23.

Conversation:
- user: Three late shifts in a row this week. I'm going to be a zombie by Thursday.
- assistant: That's a rough stretch. Do you want your phone louder on your trip home from work from now on, so nothing slips past you late at night?
- user: No thanks. After a late shift the last thing I want is my phone blaring on the train. Quiet pop-ups on the way home suit me fine.

## L049 (2028-07-08)

Stored preferences:
- For taxi vehicle type, the user prefers a fully electric car.
- For taxi vehicle type when rides to the airport, the user prefers a roomy minivan.
- For taxi vehicle type when rides to client meetings, the user prefers a premium car with leather seats.

Conversation:
- user: That backpack-only trip last month was such a relief. I'm half thinking of switching airport trips to a small car from now on.
- assistant: You do seem to be traveling lighter these days.
- user: Mostly. But there's the trade fair in October with all my display kit, and there could be more trips like that. Maybe I should just decide trip by trip. I genuinely don't know yet.
- assistant: Is there anything that would help you decide?
- user: Finding out how the display stuff gets there. I'll come back to you once I know.

## L050 (2028-05-18)

Stored preferences:
- For living room lighting, the user prefers the floor lamps alone.
- For living room lighting when video calls, the user prefers bright white light.
- For living room lighting when dinner parties, the user prefers a warm low glow.
- For living room lighting when movie nights, the user prefers the TV backlight.

Conversation:
- user: Something in our evening setup is giving me headaches. It's either the backlight on film nights or the dim setting we use for dinner parties, and for now I honestly can't tell which.
- assistant: Sorry to hear that. Has anything else changed lately, like more screen time or less sleep?
- user: Not that I can think of. I'll pay attention at the next film night and the next dinner and tell you which one it is.

## L051 (2028-02-27)

Stored preferences:
- For delivery time slot, the user prefers a mid-afternoon slot.
- For delivery time slot when furniture deliveries, the user prefers a weekend slot.
- For delivery time slot when grocery deliveries, the user prefers an evening slot.
- For delivery time slot when courier pickups for returns, the user prefers a lunchtime slot.
- For delivery time slot when parcels that need a signature, the user prefers an early-morning slot.

Conversation:
- user: Okay, after a couple more weeks at home I know which delivery time has to go.
- assistant: Oh? Which one?
- user: The early courier for anything I have to sign for. I'm home most days now, so there's no reason to drag myself out of bed for it. Just scrap that one.

## L052 (2028-06-01)

Stored preferences:
- For gift wrapping style, the user prefers a reusable cloth wrap.
- For gift wrapping style when presents for nieces and nephews, the user prefers brown kraft paper with twine.
- For gift wrapping style when wedding gifts, the user prefers glossy paper with a satin ribbon.
- For gift wrapping style when gifts for coworkers, the user prefers brown kraft paper with twine.

Conversation:
- user: I'm covering for my manager for the time being while she's on leave. Feels strange sitting in her chair.
- assistant: That's a vote of confidence. How's it going?
- user: Fine so far. If I ever got the job for real, presents for people at work would need to look a bit more special, shiny paper and a bow probably. But that's a long way off.

## L053 (2028-08-11)

Stored preferences:
- For wake-up alarm time, the user prefers half past seven.
- For wake-up alarm time when remote workdays, the user prefers half past five from 2028-07-05 through 2028-07-24.
- For wake-up alarm time when weekends, the user prefers eight o'clock.

Conversation:
- user: I'm flying to a friend's wedding on the 17th, and the only flight that works leaves at seven.
- assistant: Early one! Do you need anything sorted for that morning?
- user: Please set my alarm for half past five that day. Just the 17th, though. Normally I'd never book anything that early, and I'm not planning to make a habit of it.

## L054 (2028-10-27)

Stored preferences:
- For phone ringer mode, the user prefers a soft chime.
- For phone ringer mode when the train commute, the user prefers total silence.
- For phone ringer mode when gym sessions, the user prefers full-volume ringing.
- For phone ringer mode when work meetings, the user prefers vibrate only.
- For phone ringer mode when overnight hours, the user prefers full-volume ringing for now, with no end date given.

Conversation:
- user: I got six spam calls yesterday. Six! One of them in the middle of a dentist appointment.
- assistant: That's ridiculous. Do you want to do something about it?
- user: Yes. From now on my usual setting should be favorites-only ringing. Anyone who matters is starred, and the rest can leave a message.

## L055 (2028-08-19)

Stored preferences:
- For mulch material, the user prefers leaf mould.
- For mulch material when the strawberry patch, the user prefers grass clippings.
- For mulch material when the herb garden, the user prefers pea gravel.

Conversation:
- user: The squash are sprawling all over the vegetable beds and the fruit keeps sitting on wet soil.
- assistant: That can lead to rot, can't it?
- user: It already has, I lost two last week.
- assistant: Oh no. Is there anything you'd like to do about it?
- user: For the vegetable beds, let's go with barley straw from now on. The squash love sitting on it, and slugs have never been a problem out there.

## L056 (2028-09-03)

Stored preferences:
- For food order spice level, the user prefers the restaurant's standard heat.
- For food order spice level when takeaway nights alone, the user prefers extra hot.
- For food order spice level when takeaway nights with guests, the user prefers chili on the side.
- For food order spice level when weekday lunch orders, the user prefers a mild heat level.

Conversation:
- user: Had a few people round last night and we ordered from the new curry house on the corner.
- assistant: Nice! How did it go down?
- user: Really well. We got the chili on the side again so everyone could add their own, and nobody complained. That's still the way to go for nights in with friends over.

## L057 (2028-10-11)

Stored preferences:
- For notebook page ruling, the user prefers plain blank pages.
- For notebook page ruling when monthly budget planning, the user prefers a square grid.
- For notebook page ruling when sketching page layouts, the user prefers a dot grid.
- For pen ink color, the user prefers black ink.
- For pen ink color when marking up drafts, the user prefers green ink for now, with no end date given.
- For pen ink color when signing contracts, the user prefers navy blue ink.

Conversation:
- user: Since switching to blank notebooks, the special paper I use for layouts and for budgets has started to feel off.
- assistant: Off in what way?
- user: Hard to say. One of the two needs a different ruling, but I can't tell which one yet.
- assistant: Want to try a few pages of each and see?
- user: Yeah, that's the plan. I'll know after the big client deadline next week.

## L058 (2028-01-23)

Stored preferences:
- For delivery time slot, the user prefers the first available slot.
- For delivery time slot when furniture deliveries, the user prefers a weekend slot.
- For delivery time slot when grocery deliveries, the user prefers an evening slot.
- For delivery time slot when courier pickups for returns, the user prefers a lunchtime slot.
- For delivery time slot when parcels that need a signature, the user prefers an early-morning slot.

Conversation:
- user: My parents land on Thursday and the bookshelf for the spare room still hasn't come.
- assistant: Cutting it fine! When is it booked for?
- user: Not until a week from Saturday, which is useless. Just this once, grab the first available slot for that furniture delivery, weekday or not. I'll take a day off if I have to.

## L059 (2028-01-26)

Stored preferences:
- For reward treat for the dog, the user prefers carrot sticks.
- For reward treat for the dog when obedience classes, the user prefers freeze-dried liver bites.
- For reward treat for the dog when trips to the vet, the user prefers peanut butter biscuits.

Conversation:
- user: New term at training class, and the trainer's homework is to phase out the fancy rewards so the dogs learn to work for ordinary stuff.
- assistant: That's a big step for her. How do you feel about it?
- user: Relieved, if I'm honest. Those liver things cost a fortune. So no special treats for obedience classes any more, she can have whatever she normally gets.

## L060 (2028-03-13)

Stored preferences:
- For laundry drying method, the user prefers a low-heat tumble dry.
- For laundry drying method when cotton jumpers, the user prefers an indoor drying rack.
- For laundry drying method when work shirts, the user prefers hanging on padded hangers.
- For laundry drying method when white bath towels, the user prefers line drying outside.
- For laundry drying method when wool jumpers, the user prefers drying flat on a towel.

Conversation:
- user: My in-laws land at six and I've just realised every towel in the house is still damp.
- assistant: That's cutting it fine. What do you need from me?
- user: Remind me at two to throw my dark towels in the dryer on high, just this once. The usual low setting will never get them dry in time.

## L061 (2028-07-14)

Stored preferences:
- For grocery delivery time, the user prefers evening delivery.
- For grocery delivery time when deadline weeks, the user prefers late-night delivery.
- For grocery delivery time when home-office weeks, the user prefers lunchtime delivery.
- For grocery delivery time when night-shift weeks, the user prefers early-morning delivery.

Conversation:
- user: My in-laws arrive on the 28th for ten days. They come three or four times a year, so I'd better get organised.
- assistant: That's nice of them. Does having guests change anything about the grocery orders?
- user: It does. For weeks with house guests, book mid-afternoon delivery. They nap after lunch and are up again by three, and we're always out in the evenings with them.

## L062 (2028-08-22)

Stored preferences:
- For background music style, the user prefers classical piano.
- For background music style when date nights, the user prefers slow jazz.
- For background music style when dinner with friends, the user prefers old soul records.
- For background music style when evenings with the kids, the user prefers film soundtracks.
- For evening film genre, the user prefers a slow-burn thriller.
- For evening film genre when film club evenings, the user prefers an old black-and-white classic.
- For evening film genre when date nights, the user prefers a romantic comedy.
- For evening film genre when evenings with the kids, the user prefers an animated feature.

Conversation:
- user: We've given up cooking on date nights. It always ended in a row about the onions, so it's takeaway on the sofa now.
- assistant: Peace restored, then. Does that change the rest of the evening?
- user: The rom-com afterwards stays, obviously. But the slow jazz was only ever for the cooking, so date nights don't need their own music anymore.

## L063 (2028-10-09)

Stored preferences:
- For guest meal format, the user prefers a buffet spread.
- For guest meal format when book club evenings, the user prefers drinks and nibbles from 2028-09-11 through 2028-09-24.
- For guest meal format when family Sunday lunches, the user prefers a potluck.
- For guest meal format when board game nights, the user prefers a takeaway night from 2028-09-20 through 2028-10-03.
- For guest meal format when team socials, the user prefers a backyard barbecue.

Conversation:
- user: My brother is taking a turn hosting the family Sunday lunch this week.
- assistant: A week off for you, then! Does he have big plans?
- user: He's going all out: a sit-down meal with place cards and everything, and he says that's how he'll host from now on.
- assistant: Fancy! Are you bringing anything?
- user: Just dessert. When it's at my place it's still a potluck, though. I'm not trying to compete.

## L064 (2028-05-24)

Stored preferences:
- For audiobook playback speed, the user prefers double speed.
- For audiobook playback speed when bedtime listening, the user prefers normal speed.
- For audiobook playback speed when the morning commute, the user prefers 1.5x speed.

Conversation:
- user: Something about my listening setup feels off this week.
- assistant: Off how? Is something bugging you?
- user: One of the speeds is wrong, either for bedtime listening or for doing the housework, but I can't pin down which. Let me pay attention for a few days and get back to you.

## L065 (2028-04-30)

Stored preferences:
- For living room lighting, the user prefers the floor lamps alone.
- For living room lighting when video calls, the user prefers bright white light.
- For living room lighting when dinner parties, the user prefers candlelight.
- For living room lighting when homework hour, the user prefers bright white light.
- For living room lighting when movie nights, the user prefers the TV backlight.

Conversation:
- user: Last night's dinner was lovely right up until a napkin caught fire on one of the candles. Nobody got hurt, but the tablecloth is history.
- assistant: Oh no! I'm glad everyone's okay. Will that change how you set things up when people come round?
- user: It will. No more real candles at dinner parties. Let's have the cozy dim setting for those instead.

## L066 (2028-05-15)

Stored preferences:
- For gift wrapping style, the user prefers a reusable cloth wrap.
- For gift wrapping style when presents for nieces and nephews, the user prefers a patterned gift bag.
- For gift wrapping style when wedding gifts, the user prefers glossy paper with a satin ribbon.
- For gift wrapping style when gifts for coworkers, the user prefers brown kraft paper with twine.

Conversation:
- user: A friend of mine who sells handmade cards at the market says glossy paper is over, and from now on she's doing every wedding gift in a fabric wrap.
- assistant: Interesting. Is she right, do you think?
- user: Not for me. She can wrap her presents however she likes, but I want mine to look like a proper present on that table.

## L067 (2028-08-03)

Stored preferences:
- For grocery delivery time, the user prefers evening delivery.
- For grocery delivery time when deadline weeks, the user prefers early-morning delivery.
- For grocery delivery time when weeks with house guests, the user prefers mid-afternoon delivery.
- For grocery delivery time when home-office weeks, the user prefers lunchtime delivery.
- For grocery delivery time when night-shift weeks, the user prefers early-morning delivery.

Conversation:
- user: Guess who's training for a half marathon.
- assistant: No way! When's the race?
- user: Mid-October. I've started running on my lunch break whenever I work from home.
- assistant: Impressive. How are the legs holding up?
- user: Badly, my knees are complaining. It also means noon deliveries on home-office weeks just sit on the doorstep in the heat.
- assistant: Not ideal for the frozen stuff. What would you like to do about it?
- user: Let's drop the lunchtime arrangement for those weeks. I'm back from my run long before any other slot anyway.

## L068 (2028-01-26)

Stored preferences:
- For workout audio, the user prefers an upbeat playlist.
- For workout audio when indoor trainer rides, the user prefers a comedy podcast.
- For workout audio when long runs, the user prefers an audiobook for now, with no end date given.
- For workout audio when outdoor bike rides, the user prefers no audio at all.
- For workout audio when short runs, the user prefers a news podcast.

Conversation:
- user: The new fan for the bike trainer arrived. It's basically a jet engine.
- assistant: At least you'll stay cool. Can you still hear anything over it?
- user: Barely, and the comedy shows are wasted on me now, I miss half the jokes. On my sessions on the bike trainer I'd rather have a guided coaching track. Someone shouting intervals at me actually cuts through the noise.

## L069 (2028-03-22)

Stored preferences:
- For laundry drying method, the user prefers a low-heat tumble dry.
- For laundry drying method when cotton jumpers, the user prefers an indoor drying rack.
- For laundry drying method when work shirts, the user prefers hanging on padded hangers.
- For laundry drying method when white bath towels, the user prefers line drying outside.
- For laundry drying method when wool jumpers, the user prefers drying flat on a towel.

Conversation:
- user: Is it possible for towels to be too clean? Mine feel like sandpaper lately.
- assistant: Scratchy towels are the worst. Any idea what's doing it?
- user: The line, I think. My white towels come in stiff as boards after a day in the wind.
- assistant: That would do it. Is there something you'd like to try?
- user: Let's put my white towels in the dryer on high from now on. They come out fluffy and still nice and bright.

## L070 (2028-10-20)

Stored preferences:
- For topping for home-baked cakes, the user prefers a simple lemon glaze.
- For topping for home-baked cakes when birthday parties, the user prefers chocolate ganache.
- For topping for home-baked cakes when bake sales at work, the user prefers salted caramel drizzle.

Conversation:
- user: The twins' birthday party was chaos. Half the kids scraped the ganache off and left it on their plates.
- assistant: Kids can be tough critics. Would you do anything differently next time?
- user: Definitely. For birthday parties, whipped cream from now on. They'll eat anything that's white and fluffy.

## L071 (2028-10-11)

Stored preferences:
- For phone ringer mode, the user prefers a soft chime.
- For phone ringer mode when gym sessions, the user prefers full-volume ringing.
- For phone ringer mode when work meetings, the user prefers vibrate only.
- For phone ringer mode when overnight hours, the user prefers full-volume ringing for now, with no end date given.

Conversation:
- user: My new manager is a bit intense. She keeps her phone on total silence in work meetings and says from now on the whole team should too.
- assistant: That's quite a rule. Are you going to follow her lead?
- user: Not a chance. I need to feel the buzz in case the school calls about my son. She can do what she likes with hers.

## L072 (2028-04-03)

Stored preferences:
- For audiobook playback speed, the user prefers 1.25x speed.
- For audiobook playback speed when the morning commute, the user prefers 1.5x speed.

Conversation:
- user: I've been sleeping terribly. Most nights I'm still staring at the ceiling at two.
- assistant: That sounds exhausting. Has anything helped at all?
- user: Audiobooks, if the narrator is slow and droney enough. So for now, can bedtime listening go at 0.75x speed? Just while I'm going through this rough patch.

## L073 (2028-03-31)

Stored preferences:
- For laundry drying method, the user prefers a low-heat tumble dry.
- For laundry drying method when cotton jumpers, the user prefers an indoor drying rack.
- For laundry drying method when work shirts, the user prefers hanging on padded hangers.
- For laundry drying method when white bath towels, the user prefers a high-heat tumble dry.
- For laundry drying method when wool jumpers, the user prefers drying flat on a towel.

Conversation:
- user: The electricity bill came in. Apparently the dryer is the biggest thing on it by a mile.
- assistant: Ouch. At least the days are getting longer. Are you thinking of cutting back?
- user: Definitely. Normally I'd like things on the washing line from now on. It's free, and the weather's finally decent.

## L074 (2028-02-28)

Stored preferences:
- For workout audio, the user prefers a comedy podcast.
- For workout audio when indoor trainer rides, the user prefers a guided coaching track.
- For workout audio when long runs, the user prefers an audiobook for now, with no end date given.
- For workout audio when outdoor bike rides, the user prefers no audio at all.
- For workout audio when short runs, the user prefers an upbeat playlist.

Conversation:
- user: Finished the half marathon yesterday! Didn't walk once.
- assistant: That's brilliant, congratulations! How are the legs today?
- user: Destroyed, but worth it. The audiobook was only to get me through the training, so my distance runs don't need anything special any more.

## L075 (2028-08-08)

Stored preferences:
- For background music style, the user prefers lo-fi beats.
- For background music style when date nights, the user prefers slow jazz.
- For background music style when dinner with friends, the user prefers old soul records.
- For background music style when evenings with the kids, the user prefers film soundtracks.
- For evening film genre, the user prefers a slow-burn thriller.
- For evening film genre when film club evenings, the user prefers an old black-and-white classic.
- For evening film genre when date nights, the user prefers a romantic comedy.
- For evening film genre when evenings with the kids, the user prefers an animated feature.

Conversation:
- user: I started piano lessons last month, and now I hear the piano in everything.
- assistant: That's a lovely thing to pick up. Has it changed what you like to have on in the background?
- user: Completely. These days I'd much rather have classical piano playing than those beats.

## L076 (2028-02-02)

Stored preferences:
- For reward treat for the dog, the user prefers carrot sticks.
- For reward treat for the dog when trips to the vet, the user prefers peanut butter biscuits.

Conversation:
- user: Saturday is the off-lead test at training class and I'm more nervous than she is.
- assistant: You've both put so much work in. Is there anything you want ready for the day?
- user: Could you remind me on Friday night to cut up some cheese cubes?
- assistant: Of course. Is her stomach up to it?
- user: One day won't hurt her. It's just for the test, I want the big guns on Saturday.

## L077 (2028-07-17)

Stored preferences:
- For taxi vehicle type, the user prefers a fully electric car.
- For taxi vehicle type when rides to the airport, the user prefers a roomy minivan.
- For taxi vehicle type when rides to client meetings, the user prefers a premium car with leather seats.

Conversation:
- user: Good news about the trade fair: the organizers are shipping everyone's display kit for them.
- assistant: That's a weight off. Does it settle the airport question?
- user: It does. Airport trips get a compact hatchback from now on. These days it's always just me and a carry-on.

## L078 (2028-04-19)

Stored preferences:
- For gift wrapping style, the user prefers a reusable cloth wrap.
- For gift wrapping style when presents for nieces and nephews, the user prefers a patterned gift bag.
- For gift wrapping style when gifts for coworkers, the user prefers brown kraft paper with twine.

Conversation:
- user: My nephew turns six on Saturday and he's in a phase of drawing on absolutely everything.
- assistant: Ha, a budding artist. Have you found him something yet?
- user: A giant box of markers, obviously. It's arriving Friday.
- assistant: Perfect. How would you like it wrapped?
- user: Only this once, brown paper and string instead of a gift bag, so he can draw all over the wrapping before he even gets to the markers.

## L079 (2028-11-09)

Stored preferences:
- For notebook page ruling, the user prefers plain blank pages.
- For notebook page ruling when monthly budget planning, the user prefers a square grid.
- For notebook page ruling when sketching page layouts, the user prefers a square grid.
- For pen ink color, the user prefers black ink.
- For pen ink color when marking up drafts, the user prefers green ink for now, with no end date given.
- For pen ink color when signing contracts, the user prefers navy blue ink.

Conversation:
- user: Sending the insurance forms off today. It took me all morning to find where I'd put them.
- assistant: Paperwork has a way of hiding. All signed?
- user: All signed, in a dark blue pen, which is what I normally use for official paperwork. That way I can always tell the originals from the copies.

## L080 (2028-02-04)

Stored preferences:
- For workout audio, the user prefers an upbeat playlist.
- For workout audio when indoor trainer rides, the user prefers a guided coaching track.
- For workout audio when long runs, the user prefers an audiobook for now, with no end date given.
- For workout audio when outdoor bike rides, the user prefers no audio at all.
- For workout audio when short runs, the user prefers a news podcast.

Conversation:
- user: Confession: I can't stand my workout playlist any more. I've heard those songs about four hundred times.
- assistant: That happens to the best playlists. Time for a new one?
- user: I don't think it's even the songs. I'm just tired of music while I exercise.
- assistant: Fair enough. What would you rather have on?
- user: Normally I'd like something funny instead. Half an hour goes a lot faster when I'm laughing.

## L081 (2028-03-07)

Stored preferences:
- For delivery time slot, the user prefers a mid-afternoon slot.
- For delivery time slot when furniture deliveries, the user prefers a weekend slot.
- For delivery time slot when grocery deliveries, the user prefers an evening slot.
- For delivery time slot when courier pickups for returns, the user prefers a lunchtime slot.

Conversation:
- user: The food order turned up at six-thirty last night and I had everything put away before my show started. Perfect.
- assistant: Nice timing. Since you're home in the afternoons now, should I move the weekly food order to a mid-afternoon slot from now on?
- user: No, leave that one alone. Putting the shopping away after work is how I switch off, and afternoons are for actual work.

## L082 (2028-04-20)

Stored preferences:
- For audiobook playback speed, the user prefers 1.25x speed.
- For audiobook playback speed when bedtime listening, the user prefers 0.75x speed for now, with no end date given.
- For audiobook playback speed when the morning commute, the user prefers 1.5x speed.

Conversation:
- user: Small victory: I slept right through the night five times this week.
- assistant: That's great news! Any idea what's made the difference?
- user: Partly the slower speed at bedtime, I think. I know I said it was only for a while, but I'd like to keep it for good. It's become part of how I fall asleep.

## L083 (2028-03-03)

Stored preferences:
- For meeting time slot, the user prefers late morning.
- For meeting time slot when candidate interviews, the user prefers right after lunch.
- For meeting time slot when team retrospectives, the user prefers late afternoon.

Conversation:
- user: Morning! Someone finally fixed the coffee machine on our floor, so the week is ending on a high note.
- assistant: Small victories. Anything you want to sort out before the weekend?
- user: The calendar for the next couple of weeks. Our clients have their annual audit from the 10th through the 16th, and their finance people are tied up from ten o'clock every day of it.
- assistant: That doesn't leave them much room. How would you like me to handle it?
- user: For client calls from the 10th through the 16th, book them first thing in the morning, before the auditors grab everyone. Their calendars free up again after the 16th.

## L084 (2028-01-17)

Stored preferences:
- For workout audio, the user prefers an upbeat playlist.
- For workout audio when indoor trainer rides, the user prefers a comedy podcast.
- For workout audio when outdoor bike rides, the user prefers no audio at all.
- For workout audio when short runs, the user prefers a news podcast.

Conversation:
- user: I did it, I signed up for a half marathon. My first one ever, so I'm slightly terrified.
- assistant: Congratulations! That's a big step. What does the training look like?
- user: Lots of slow miles. For now, while I'm training for it, I'd like an audiobook on my distance runs. An hour and a half of the same songs would drive me up the wall.

## L085 (2028-06-05)

Stored preferences:
- For audiobook playback speed, the user prefers double speed.
- For audiobook playback speed when bedtime listening, the user prefers normal speed.
- For audiobook playback speed when the morning commute, the user prefers 1.5x speed.

Conversation:
- user: Mystery solved, it was bedtime. I've been sleeping like a log for weeks, so the gentle setting has no point any more.
- assistant: That's lovely to hear. What would you like at bedtime from here on?
- user: Bedtime listening doesn't need its own speed now. Just play it the way I usually listen.

## L086 (2028-09-10)

Stored preferences:
- For food order spice level, the user prefers the restaurant's standard heat.
- For food order spice level when takeaway nights alone, the user prefers extra hot.
- For food order spice level when takeaway nights with guests, the user prefers chili on the side.
- For food order spice level when weekday lunch orders, the user prefers a mild heat level.

Conversation:
- user: Yesterday's lunch from the taco truck was so bland I ended up raiding the fridge for hot sauce.
- assistant: A bland taco is a sad taco. Did you order it a particular way?
- user: No, I just took however the chef makes it. For my weekend lunches I want a medium kick from now on. I've got the time to enjoy it then.

## L087 (2028-09-13)

Stored preferences:
- For notebook page ruling, the user prefers narrow-ruled lines.
- For notebook page ruling when monthly budget planning, the user prefers a square grid.
- For notebook page ruling when sketching page layouts, the user prefers a dot grid.
- For pen ink color, the user prefers black ink.
- For pen ink color when marking up drafts, the user prefers green ink for now, with no end date given.
- For pen ink color when signing contracts, the user prefers navy blue ink.

Conversation:
- user: The designer who sits next to me does all her layout sketches on graph paper. She swears the squares keep her columns honest.
- assistant: That's a neat trick. Have you ever tried it?
- user: Ages ago. It's great for her, but I'm happier on my dotted pages, they don't shout at me.

## L088 (2028-05-10)

Stored preferences:
- For long-distance transport, the user prefers the high-speed train.
- For long-distance transport when trips with the dog, the user prefers a rental car.
- For long-distance transport when weekend getaways, the user prefers a rental car.
- For long-distance transport when work trips, the user prefers the overnight sleeper.
- For main travel bag, the user prefers a wheeled carry-on.
- For main travel bag when weekend getaways, the user prefers a canvas duffel.
- For main travel bag when work trips, the user prefers a garment bag.

Conversation:
- user: Have you seen what the fast trains cost now? I nearly dropped my phone.
- assistant: Fares have gone up a lot. Do you want to look at other options?
- user: Yeah. Normally I'll take the long-distance bus now. It's slower, but I get a whole book read on the way.

## L089 (2028-02-18)

Stored preferences:
- For delivery time slot, the user prefers a mid-afternoon slot.
- For delivery time slot when furniture deliveries, the user prefers a weekend slot.
- For delivery time slot when grocery deliveries, the user prefers an evening slot.
- For delivery time slot when courier pickups for returns, the user prefers a lunchtime slot.
- For delivery time slot when parcels that need a signature, the user prefers an early-morning slot.

Conversation:
- user: Random thought while taping up yet another return: if I ever took a job across town, returns being collected around midday would be hopeless. I'd need them after six.
- assistant: Are you thinking of changing jobs?
- user: Not at all, I'm very happy where I am. Just thinking out loud.

## L090 (2028-02-09)

Stored preferences:
- For hotel room placement, the user prefers a room on a high floor.
- For hotel room placement when conference trips, the user prefers a room next to the stairwell.
- For hotel room placement when overnight layovers, the user prefers a room at the quiet end of the corridor.
- For hotel room placement when road trips, the user prefers a room overlooking the courtyard.

Conversation:
- user: I finally bought one of those enormous checked suitcases and dragging it down long corridors is wrecking my shoulder.
- assistant: Ouch. Do you want me to take that into account for hotels?
- user: Yeah. Normally I'd rather be close to the elevators now instead of up high.

## L091 (2028-09-01)

Stored preferences:
- For mulch material, the user prefers leaf mould.
- For mulch material when the strawberry patch, the user prefers grass clippings.
- For mulch material when the herb garden, the user prefers pea gravel.
- For mulch material when the vegetable beds, the user prefers barley straw.

Conversation:
- user: The grass clippings around the strawberries have turned into a slimy, smelly mat. Not my finest idea.
- assistant: Oh dear. How are the plants coping?
- user: They're fine, it's my nose that's suffering. I'm giving in to the neighbour: pine needles on the strawberry patch from now on.

## L092 (2028-01-08)

Stored preferences:
- For reward treat for the dog, the user prefers small cubes of cheese.
- For reward treat for the dog when obedience classes, the user prefers freeze-dried liver bites.
- For reward treat for the dog when trips to the vet, the user prefers peanut butter biscuits.

Conversation:
- user: She was sick on the rug again last night. Third time this month, and it's always after she's had cheese.
- assistant: Oh no, poor thing. Is she alright now?
- user: Bouncing off the walls as if nothing happened. But the cheese has to go. From now on her regular treats are carrot sticks. She loves the crunch anyway.

## L093 (2028-04-10)

Stored preferences:
- For meeting time slot, the user prefers mid-afternoon.
- For meeting time slot when client calls, the user prefers first thing in the morning from 2028-03-10 through 2028-03-16.
- For meeting time slot when candidate interviews, the user prefers right after lunch.
- For meeting time slot when team retrospectives, the user prefers late afternoon.

Conversation:
- user: One of the applicants for the analyst role can only talk on the 13th, before her shift starts at noon.
- assistant: That's a narrow slot. What would you like to do?
- user: I'll bend my no-morning-meetings rule for her. Book her interview on the 13th for late morning, just that once.

## L094 (2028-05-13)

Stored preferences:
- For audiobook playback speed, the user prefers double speed.
- For audiobook playback speed when bedtime listening, the user prefers 0.75x speed.
- For audiobook playback speed when the morning commute, the user prefers 1.5x speed.

Conversation:
- user: The slow bedtime audiobooks have started backfiring. I nod off so fast I wake up having missed half the book.
- assistant: Too effective! What would you like to do about it?
- user: Bump bedtime listening up to normal speed. Still gentle, but I might actually remember the plot.

## L095 (2028-04-04)

Stored preferences:
- For living room lighting, the user prefers a warm low glow.
- For living room lighting when dinner parties, the user prefers candlelight.
- For living room lighting when homework hour, the user prefers bright white light.
- For living room lighting when movie nights, the user prefers the TV backlight.

Conversation:
- user: Big news on our end: the spare room is officially the nursery now, so my work calls have moved down to the living room.
- assistant: Congratulations! How is the living room working out for that?
- user: Fine, apart from the lights. That warm glow makes me look half asleep on camera. For video calls, give me bright white light, please.

## L096 (2028-07-28)

Stored preferences:
- For wake-up alarm time, the user prefers a quarter to seven.
- For wake-up alarm time when commuting days, the user prefers six o'clock.
- For wake-up alarm time when remote workdays, the user prefers half past five from 2028-07-05 through 2028-07-24.
- For wake-up alarm time when weekends, the user prefers eight o'clock.

Conversation:
- user: Blissful silence next door. The builders packed up on the 24th as promised.
- assistant: Enjoy it! Anything else going on with your mornings?
- user: One thing: the office has moved our start time to ten, so I can drop the six o'clock wake-up on commuting days. Best news all month.

## L097 (2028-01-12)

Stored preferences:
- For commute mode, the user prefers cycling in.
- For commute mode when gym days, the user prefers driving myself.
- For commute mode when late shifts, the user prefers driving myself.
- For commute mode when rainy days, the user prefers the express bus.
- For packed lunch, the user prefers leftovers from dinner.
- For packed lunch when rainy days, the user prefers a thermos of soup.

Conversation:
- user: I finally signed up for those evening spin classes. Three a week, and my legs are already filing complaints.
- assistant: Ha, that's a big commitment! Does it mean any changes on those days?
- user: Just lunch. I'm taking the car on gym days anyway, so that's sorted, but pack me the rice bowl on those days instead of leftovers. I need something solid before class.

## L098 (2028-06-08)

Stored preferences:
- For phone alert style, the user prefers full sound and vibration.
- For phone alert style when dinners out alone, the user prefers vibration only.
- For phone alert style when cinema trips, the user prefers vibration only.
- For phone alert style when the evening train ride, the user prefers silent banners.
- For phone alert style when dinners out with friends, the user prefers silent banners.

Conversation:
- user: I've signed up for a two-week language course that I'm going to do on the train, starting Monday.
- assistant: That's a clever use of the journey. Is there anything you need from me?
- user: Yes. From Monday through Friday the 23rd, on my trip in to work, hold everything and give me a roundup afterwards. I want to actually concentrate.

## L099 (2028-04-09)

Stored preferences:
- For laundry drying method, the user prefers line drying outside.
- For laundry drying method when cotton jumpers, the user prefers an indoor drying rack.
- For laundry drying method when work shirts, the user prefers hanging on padded hangers.
- For laundry drying method when white bath towels, the user prefers a high-heat tumble dry.
- For laundry drying method when wool jumpers, the user prefers drying flat on a towel.

Conversation:
- user: My neighbour just got a dryer with a proper wool cycle. I'm green with envy.
- assistant: Ha, the fancy stuff. Would it make a difference for you?
- user: If ours had one, I'd put my wool sweaters in the dryer on low and save myself the faff. It doesn't, though, so they keep getting laid out flat.

## L100 (2028-08-04)

Stored preferences:
- For wake-up alarm time, the user prefers a quarter to seven.
- For wake-up alarm time when remote workdays, the user prefers half past five from 2028-07-05 through 2028-07-24.
- For wake-up alarm time when weekends, the user prefers eight o'clock.

Conversation:
- user: I joined an evening pottery class. Messy, but I love it.
- assistant: That sounds like a great way to unwind. How late does it run?
- user: Till ten, so I'm getting to bed later. Normally I'd like to wake up at half past seven now instead of a quarter to seven.

## L101 (2028-07-05)

Stored preferences:
- For grocery delivery time, the user prefers evening delivery.
- For grocery delivery time when deadline weeks, the user prefers late-night delivery.
- For grocery delivery time when home-office weeks, the user prefers lunchtime delivery.
- For grocery delivery time when night-shift weeks, the user prefers early-morning delivery.

Conversation:
- user: School holidays start on Friday, so both kids will be home all day until September. Wish me luck.
- assistant: Good luck! With someone home during the day, would lunchtime delivery make sense for the school holidays?
- user: Ha, no. Lunchtime with those two is pure chaos, and I'm not adding a delivery driver to it. Leave it as it is.

## L102 (2028-03-07)

Stored preferences:
- For commute mode, the user prefers cycling in.
- For commute mode when late shifts, the user prefers driving myself.
- For commute mode when rainy days, the user prefers the commuter train.
- For packed lunch, the user prefers a veggie wrap.
- For packed lunch when gym days, the user prefers a chicken and rice bowl.
- For packed lunch when rainy days, the user prefers a thermos of soup.

Conversation:
- user: Worked out the rainy-day thing. The train's been fine, so it's not that. It's lunch: the soup keeps going lukewarm because my thermos cracked, and the new one is stuck on backorder.
- assistant: Oh no, bad timing. What would work instead?
- user: Until the new thermos turns up, give me cold pasta on wet days. No idea how long that'll take.

## L103 (2028-06-20)

Stored preferences:
- For long-distance transport, the user prefers the intercity coach.
- For long-distance transport when trips with the dog, the user prefers a rental car.
- For long-distance transport when weekend getaways, the user prefers a rental car.
- For long-distance transport when work trips, the user prefers the overnight sleeper.
- For main travel bag, the user prefers a wheeled carry-on.
- For main travel bag when camping trips, the user prefers a hiking backpack.
- For main travel bag when work trips, the user prefers a garment bag.

Conversation:
- user: New client wants live demos at every visit, so now I have to haul the test kit around with me.
- assistant: That sounds heavy. Does it change anything for your trips?
- user: For work trips I'll need the big suitcase now, the kit won't fit in anything else. Still the night train, thank goodness. I wouldn't want to drag that thing through an airport.

## L104 (2028-01-10)

Stored preferences:
- For hotel room placement, the user prefers a room on a high floor.
- For hotel room placement when beach holidays, the user prefers a ground-floor room.
- For hotel room placement when conference trips, the user prefers a room near the lifts.
- For hotel room placement when overnight layovers, the user prefers a room at the quiet end of the corridor.

Conversation:
- user: Quick thing before I forget. My coworker swears that on work conferences the trick is a courtyard view, because the street side never quiets down.
- assistant: Is that something you'd want for your own bookings?
- user: Nah, that's just what works for them. I'm happy being close to the elevators when I'm dragging a poster tube around the venue.

## L105 (2028-10-03)

Stored preferences:
- For phone ringer mode, the user prefers a soft chime.
- For phone ringer mode when gym sessions, the user prefers full-volume ringing.
- For phone ringer mode when work meetings, the user prefers vibrate only.
- For phone ringer mode when overnight hours, the user prefers favorites-only ringing.

Conversation:
- user: So I've been roped into the on-call rota for the building's heating emergencies.
- assistant: Oh no. Since when?
- user: Starting tonight. It runs until they hire a second technician, and nobody can tell me when that'll be.
- assistant: That sounds stressful. Will the phone need to wake you up for those calls?
- user: Definitely. So for now, overnight I need full-volume ringing or I'll sleep straight through them.

## L106 (2028-01-15)

Stored preferences:
- For delivery time slot, the user prefers the first available slot.
- For delivery time slot when furniture deliveries, the user prefers a weekend slot.
- For delivery time slot when grocery deliveries, the user prefers an evening slot.
- For delivery time slot when parcels that need a signature, the user prefers an early-morning slot.

Conversation:
- user: Third pair of shoes going back this month. Online sizing is a complete lottery.
- assistant: Oof. Is sending them back at least painless?
- user: Not really. The courier keeps coming while I'm at the office and leaves one of those little sorry-we-missed-you cards.
- assistant: Annoying. Is there a time you're reliably around?
- user: I pop home for lunch most days, so for returns being collected, a lunchtime slot is the way to go.

## L107 (2028-07-19)

Stored preferences:
- For wake-up alarm time, the user prefers a quarter to seven.
- For wake-up alarm time when commuting days, the user prefers six o'clock.
- For wake-up alarm time when remote workdays, the user prefers half past five for now, with no end date given.
- For wake-up alarm time when weekends, the user prefers eight o'clock.

Conversation:
- user: Finally, a date from the builders: they'll be finished on the 24th.
- assistant: Light at the end of the tunnel! You must be counting the days.
- user: I am. And I've decided the dawn club isn't for me. I've been up at half past five on remote workdays since the 5th; keep that going through the 24th and not a day longer.

## L108 (2028-11-24)

Stored preferences:
- For topping for home-baked cakes, the user prefers a dusting of icing sugar.
- For topping for home-baked cakes when birthday parties, the user prefers whipped cream.
- For topping for home-baked cakes when bake sales at work, the user prefers salted caramel drizzle.

Conversation:
- user: The neighbours came round for tea yesterday and asked, very politely, where my carrot cake had gone.
- assistant: Sounds like it's been missed! Do you want to bring it back for them?
- user: Looks like I have to. For afternoon tea with the neighbours, it's cream cheese frosting from now on. They're not the ones complaining about rich food.

## L109 (2028-10-22)

Stored preferences:
- For food order spice level, the user prefers a mild heat level.
- For food order spice level when takeaway nights with guests, the user prefers chili on the side.
- For food order spice level when weekday lunch orders, the user prefers no chili at all.
- For food order spice level when weekend lunch orders, the user prefers medium heat.

Conversation:
- user: Friends came over on Friday and brought their two little ones. The kids wouldn't touch a thing.
- assistant: Ah, the picky-eater years. What did they end up eating?
- user: Plain rice and a lot of bread. Most of our friends have kids now, so for nights in with friends over, order with zero heat from now on. The grown-ups will survive.

## L110 (2028-06-26)

Stored preferences:
- For phone alert style, the user prefers full sound and vibration.
- For phone alert style when dinners out alone, the user prefers vibration only.
- For phone alert style when cinema trips, the user prefers vibration only.
- For phone alert style when the evening train ride, the user prefers silent banners.
- For phone alert style when dinners out with friends, the user prefers silent banners.
- For phone alert style when the morning train ride, the user prefers alerts held for later from 2028-06-12 through 2028-06-23.

Conversation:
- user: The noodle bar put in a sound system and now it's properly loud in there. Weirdly, I love it.
- assistant: Ha, a whole new atmosphere. Still your favourite spot?
- user: Even more so. It's where I go whenever I'm eating out by myself, and nobody could hear my phone in there now anyway, so the buzz-only setup isn't needed any more.

## L111 (2028-05-09)

Stored preferences:
- For rail or coach service, the user prefers the direct train.
- For rail or coach service when airport runs, the user prefers the express coach.
- For rail or coach service when trips to the head office, the user prefers the stopping train from 2028-05-08 through 2028-05-21.
- For rail or coach service when family visits up north, the user prefers the overnight coach.

Conversation:
- user: Yesterday was my first day on the branch line. Slow, but the views are lovely.
- assistant: A scenic silver lining. Anything coming up this week?
- user: The board meeting at head office on Friday the 12th starts at eight, and the slow train doesn't get in until nine. Could you book me the express coach just for that one trip?

## L112 (2028-10-05)

Stored preferences:
- For food order spice level, the user prefers a mild heat level.
- For food order spice level when takeaway nights alone, the user prefers extra hot.
- For food order spice level when takeaway nights with guests, the user prefers chili on the side.
- For food order spice level when weekday lunch orders, the user prefers no chili at all.
- For food order spice level when weekend lunch orders, the user prefers medium heat.

Conversation:
- user: I think something needs to change with my takeaway nights. Either the nights in by myself or the nights in with friends over, I just can't work out which.
- assistant: Fair enough. What's been off about them?
- user: Hard to say yet. Give me this weekend and I'll tell you which one.

## L113 (2028-10-19)

Stored preferences:
- For phone ringer mode, the user prefers a soft chime.
- For phone ringer mode when gym sessions, the user prefers full-volume ringing.
- For phone ringer mode when work meetings, the user prefers vibrate only.
- For phone ringer mode when overnight hours, the user prefers full-volume ringing for now, with no end date given.

Conversation:
- user: I've started reading on the train again. Two novels already this month.
- assistant: That's a great habit! Anything good?
- user: A sea mystery and a very long family saga. Only problem is every chime yanks me out of the story, so on the train commute I'd like total silence.

## L114 (2028-04-18)

Stored preferences:
- For long-distance transport, the user prefers the high-speed train.
- For long-distance transport when trips with the dog, the user prefers a rental car.
- For long-distance transport when weekend getaways, the user prefers a rental car.
- For long-distance transport when work trips, the user prefers a short-haul flight.
- For main travel bag, the user prefers a wheeled carry-on.
- For main travel bag when weekend getaways, the user prefers a canvas duffel.
- For main travel bag when work trips, the user prefers a garment bag.

Conversation:
- user: Our company just announced it won't pay for flights anymore if there's a train that gets you there overnight.
- assistant: That's quite a shift. How does it affect your trips for the job?
- user: For work trips, put me on the night train from now on. Honestly I don't mind: I sleep on the way and walk straight into the meeting.
- assistant: Sounds civilised. Anything different about packing for those?
- user: No, the suit carrier still comes along on business travel. Clients expect the jacket.

## L115 (2028-09-14)

Stored preferences:
- For mulch material, the user prefers leaf mould.
- For mulch material when the strawberry patch, the user prefers pine needles.
- For mulch material when the herb garden, the user prefers pea gravel.
- For mulch material when the vegetable beds, the user prefers barley straw.

Conversation:
- user: The leaf mould's all gone already. I clearly underestimated how much I'd get through.
- assistant: It goes fast, doesn't it? What do you want to do now?
- user: I've ordered a delivery of bark chips. That's my standard again from now on, the leaf cage needs a couple of years to fill back up.

## L116 (2028-01-20)

Stored preferences:
- For commute mode, the user prefers cycling in.
- For commute mode when gym days, the user prefers driving myself.
- For commute mode when late shifts, the user prefers driving myself.
- For commute mode when rainy days, the user prefers the express bus.
- For packed lunch, the user prefers leftovers from dinner.
- For packed lunch when gym days, the user prefers a chicken and rice bowl.
- For packed lunch when rainy days, the user prefers a thermos of soup.

Conversation:
- user: A guy on my team walks in even when it's pouring. Says the rain wakes him up better than coffee.
- assistant: Is that something you'd want to try?
- user: Nah, that's his thing. On rainy days I'll stick with the fast bus, and the hot soup at lunch.

## L117 (2028-01-17)

Stored preferences:
- For hotel room placement, the user prefers a room on a high floor.
- For hotel room placement when beach holidays, the user prefers a ground-floor room.
- For hotel room placement when conference trips, the user prefers a room near the lifts.
- For hotel room placement when overnight layovers, the user prefers a room at the quiet end of the corridor.

Conversation:
- user: We're planning a few driving holidays this year, which I'm weirdly excited about.
- assistant: Nice! Anything I should keep in mind when I book the hotels for those?
- user: Yes. Whenever it's one of our driving holidays, ask for a courtyard view. The car park side is where everyone slams doors at six in the morning.

## L118 (2028-01-08)

Stored preferences:
- For delivery time slot, the user prefers the first available slot.
- For delivery time slot when furniture deliveries, the user prefers a weekend slot.
- For delivery time slot when grocery deliveries, the user prefers an evening slot.
- For delivery time slot when parcels that need a signature, the user prefers an early-morning slot.

Conversation:
- user: Had dinner at my brother's last night. He's decided that from now on his weekly food order turns up first thing in the morning, so the milk's in the fridge before he's even left for work.
- assistant: Very organized. Tempted to try it?
- user: Ha, no. I'm barely a person before eight. That's his system, not mine.

## L119 (2028-04-17)

Stored preferences:
- For meeting time slot, the user prefers mid-afternoon.
- For meeting time slot when client calls, the user prefers first thing in the morning from 2028-03-10 through 2028-03-16.
- For meeting time slot when candidate interviews, the user prefers right after lunch.
- For meeting time slot when team retrospectives, the user prefers late afternoon.

Conversation:
- user: Half the team has switched to early hours. They're in at seven and gone by four.
- assistant: Big change. Has it altered the feel of the office?
- user: It's very quiet by five. It also kills the end-of-day slot for our retros, so let's scrap that. The late timing only made sense when everyone stayed till six.

## L120 (2028-05-15)

Stored preferences:
- For rail or coach service, the user prefers the direct train.
- For rail or coach service when airport runs, the user prefers the express coach.
- For rail or coach service when trips to the head office, the user prefers the stopping train from 2028-05-08 through 2028-05-21.
- For rail or coach service when family visits up north, the user prefers the overnight coach.

Conversation:
- user: More news from the rail operator, and not the good kind.
- assistant: Uh oh. What now?
- user: They found extra damage under the river bridge, so the closure is running long.
- assistant: How much longer are they saying?
- user: Another week. The main line now stays closed through the 28th, so keep me on the slow train for head office visits until then.

## L121 (2028-06-29)

Stored preferences:
- For taxi vehicle type, the user prefers a standard sedan.
- For taxi vehicle type when rides to the airport, the user prefers a roomy minivan.
- For taxi vehicle type when rides to client meetings, the user prefers a premium car with leather seats.

Conversation:
- user: Did you see the air quality warnings this week? I could practically taste the traffic on my walk this morning.
- assistant: It's been grim. Is it changing how you want to get around?
- user: A bit. Usually I'd like an EV now when I book a ride. I can't fix the whole city, but I can stop adding to the fumes.

## L122 (2028-05-27)

Stored preferences:
- For living room lighting, the user prefers the floor lamps alone.
- For living room lighting when video calls, the user prefers bright white light.
- For living room lighting when dinner parties, the user prefers a warm low glow.
- For living room lighting when movie nights, the user prefers the TV backlight.

Conversation:
- user: Mystery solved, I think. During last night's film the strip behind the screen flickered every time a scene went dark, and the headache arrived right on cue.
- assistant: That would do it. And the dinner on Sunday?
- user: Not a twinge all evening. So it's the movie nights: give those the cozy dim setting instead of the backlight.

## L123 (2028-02-14)

Stored preferences:
- For reward treat for the dog, the user prefers carrot sticks.
- For reward treat for the dog when trips to the vet, the user prefers peanut butter biscuits.

Conversation:
- user: Vet trip this morning for her booster. She shook the whole time and wouldn't even sniff the peanut butter biscuits.
- assistant: Poor girl, that sounds stressful for both of you. Would something else help next time?
- user: The nurse had a pocket full of liver bites and she perked right up. So for trips to the vet, liver bites from now on.

## L124 (2028-11-02)

Stored preferences:
- For meeting length, the user prefers a full hour.
- For meeting length when planning days, the user prefers a 90-minute working session.
- For quick-question channel, the user prefers stopping by their desk.
- For quick-question channel when release weeks, the user prefers a five-minute video call.
- For quick-question channel when remote days, the user prefers a chat message.

Conversation:
- user: Someone stuck a 'protect your focus time' sign up on our floor, and I'm fairly sure it was aimed at me.
- assistant: Oof. Too many drop-ins?
- user: Probably. Normally I'll send a short email now instead of walking over to people's desks.

## L125 (2028-07-06)

Stored preferences:
- For background music style, the user prefers lo-fi beats.
- For background music style when date nights, the user prefers slow jazz.
- For background music style when dinner with friends, the user prefers old soul records.
- For background music style when evenings with the kids, the user prefers sing-along pop.
- For evening film genre, the user prefers a slow-burn thriller.
- For evening film genre when film club evenings, the user prefers an old black-and-white classic.
- For evening film genre when evenings with the kids, the user prefers an animated feature.

Conversation:
- user: My partner pointed out that we've watched four bleak thrillers in a row on our evenings together. Not exactly romantic.
- assistant: Ha, fair point. Fancy a change of mood?
- user: Definitely. On date nights let's put on a rom-com instead. The slow jazz while we cook is perfect, though, that part we love.

## L126 (2028-10-03)

Stored preferences:
- For meeting length, the user prefers a full hour.
- For meeting length when release weeks, the user prefers a 15-minute check-in.
- For meeting length when planning days, the user prefers a 90-minute working session.
- For quick-question channel, the user prefers stopping by their desk.
- For quick-question channel when release weeks, the user prefers a phone call.
- For quick-question channel when remote days, the user prefers a chat message.

Conversation:
- user: Release prep kicks off again next month and I'm already dreading the phone ringing nonstop.
- assistant: It got pretty hectic last time. Want to handle anything differently this round?
- user: Yes. During release weeks, let's sort out questions with a quick video chat instead of phone calls. Half the time we end up needing to look at the same screen anyway.
- assistant: Makes sense. What about the meetings in those weeks?
- user: Keep those to a quick check-in, like last time. That part works.

## L127 (2028-11-04)

Stored preferences:
- For phone ringer mode, the user prefers favorites-only ringing.
- For phone ringer mode when the train commute, the user prefers total silence.
- For phone ringer mode when gym sessions, the user prefers full-volume ringing.
- For phone ringer mode when work meetings, the user prefers vibrate only.
- For phone ringer mode when overnight hours, the user prefers full-volume ringing for now, with no end date given.

Conversation:
- user: Best news all month: they've hired the second technician, so I'm officially off the on-call rota.
- assistant: Congratulations! You must be relieved.
- user: So relieved. My nights don't need the phone blasting any more, so I don't need anything special overnight now.

## L128 (2028-10-12)

Stored preferences:
- For food order spice level, the user prefers a mild heat level.
- For food order spice level when takeaway nights alone, the user prefers extra hot.
- For food order spice level when takeaway nights with guests, the user prefers chili on the side.
- For food order spice level when weekday lunch orders, the user prefers no chili at all.
- For food order spice level when weekend lunch orders, the user prefers medium heat.

Conversation:
- user: Right, I've worked it out. It's the nights in by myself.
- assistant: Ah, okay. What's going wrong with those?
- user: I keep ordering the hottest option and then giving up halfway. I don't need anything special on those nights any more.

## L129 (2028-07-26)

Stored preferences:
- For taxi vehicle type, the user prefers a fully electric car.
- For taxi vehicle type when rides to the airport, the user prefers a compact hatchback.
- For taxi vehicle type when rides to client meetings, the user prefers a premium car with leather seats.

Conversation:
- user: My business partner keeps floating the idea of bringing the whole sales team to the big renewal meetings.
- assistant: Would that become a regular thing?
- user: If we ever did that, trips to see clients would need one of the big vans, obviously. But I don't see it happening. The clients like it small and personal.

## L130 (2028-07-25)

Stored preferences:
- For background music style, the user prefers lo-fi beats.
- For background music style when date nights, the user prefers slow jazz.
- For background music style when dinner with friends, the user prefers old soul records.
- For background music style when evenings with the kids, the user prefers sing-along pop.
- For evening film genre, the user prefers a slow-burn thriller.
- For evening film genre when film club evenings, the user prefers an old black-and-white classic.
- For evening film genre when date nights, the user prefers a romantic comedy.
- For evening film genre when evenings with the kids, the user prefers an animated feature.

Conversation:
- user: Mystery solved. Apparently they're 'way too old' for the pop stuff now, according to my nine-year-old.
- assistant: Nine going on nineteen! Did they say what they'd rather hear?
- user: Movie scores, of all things. So on evenings with the kids, play film soundtracks from now on.
- assistant: That's a fun pick. And the films themselves?
- user: No complaints there, they still want a cartoon movie on those nights.

## L131 (2028-10-16)

Stored preferences:
- For guest meal format, the user prefers a buffet spread.
- For guest meal format when book club evenings, the user prefers drinks and nibbles from 2028-09-11 through 2028-09-24.
- For guest meal format when family Sunday lunches, the user prefers a potluck.
- For guest meal format when board game nights, the user prefers a takeaway night from 2028-09-20 through 2028-10-03.
- For guest meal format when team socials, the user prefers a backyard barbecue.

Conversation:
- user: Had the team round at the weekend. It was freezing, and everyone huddled round the grill in their coats.
- assistant: Brr. Did people still have a good time?
- user: They did, but let's leave the grill out of team socials from now on. I'm tired of smelling like smoke for two days afterwards.

## L132 (2028-06-20)

Stored preferences:
- For rail or coach service, the user prefers the direct train.
- For rail or coach service when airport runs, the user prefers the express coach.
- For rail or coach service when concert nights in the city, the user prefers the stopping train.
- For rail or coach service when trips to the head office, the user prefers the stopping train from 2028-05-08 through 2028-05-28.

Conversation:
- user: Saw a notice at the station: the operator may need another closure on the main line in the autumn.
- assistant: Again? That bridge has it in for you.
- user: Ha, it really does. If it happens I suppose it would be the slow train for head office visits again, but nothing's announced yet, so for now it's just a rumour.

## L133 (2028-04-24)

Stored preferences:
- For living room lighting, the user prefers a warm low glow.
- For living room lighting when video calls, the user prefers bright white light.
- For living room lighting when dinner parties, the user prefers candlelight.
- For living room lighting when homework hour, the user prefers bright white light.
- For living room lighting when movie nights, the user prefers the TV backlight.

Conversation:
- user: We finally rearranged the living room over the weekend. The two floor lamps are on either side of the sofa now.
- assistant: Oh, nice! Did the new rug fit in the end?
- user: After a small war with the coffee table, yes. The lamps changed the whole feel of the room, though.
- assistant: In a good way, I hope? Should the lights work differently now?
- user: A very good way. Normally I just want the floor lamps alone in there now. It finally feels like a proper den.

## L134 (2028-09-04)

Stored preferences:
- For guest meal format, the user prefers a sit-down meal.
- For guest meal format when family Sunday lunches, the user prefers a potluck.
- For guest meal format when team socials, the user prefers a backyard barbecue.

Conversation:
- user: Our book club voted to tackle a giant trilogy, so we're meeting twice a week from the 11th through the 24th.
- assistant: That's a serious reading schedule. Are they all coming to yours?
- user: Every single time. I'm not cooking a full meal twice a week, so for book club evenings from the 11th through the 24th, just drinks and nibbles.

## L135 (2028-11-01)

Stored preferences:
- For notebook page ruling, the user prefers plain blank pages.
- For notebook page ruling when monthly budget planning, the user prefers a square grid.
- For notebook page ruling when sketching page layouts, the user prefers a square grid.
- For pen ink color, the user prefers black ink.
- For pen ink color when marking up drafts, the user prefers green ink for now, with no end date given.
- For pen ink color when signing contracts, the user prefers navy blue ink.

Conversation:
- user: My old professor emailed again about teaching a night class next spring.
- assistant: Again? She must really want you. Is it tempting?
- user: A little. I do miss being in a classroom.
- assistant: What's holding you back?
- user: Time, mostly. I'd be grading essays at midnight.
- assistant: That would be a lot on top of your job.
- user: Exactly. If I ever said yes, I'd probably mark up drafts with a red pen like a proper teacher. But I keep turning her down, so don't hold your breath.

## L136 (2028-11-22)

Stored preferences:
- For meeting length, the user prefers a full hour.
- For meeting length when planning days, the user prefers a 90-minute working session.
- For quick-question channel, the user prefers a short email.
- For quick-question channel when release weeks, the user prefers a five-minute video call.
- For quick-question channel when remote days, the user prefers a chat message.

Conversation:
- user: My partner starts two weeks of night shifts on Monday, so they'll be asleep upstairs all day.
- assistant: That'll take some juggling. Anything you want to adjust?
- user: From Monday through Friday the 8th, on days I work from home, keep my meetings to twenty-five minutes so I'm not talking for hours. Quick questions can still come as a chat message, that's silent anyway.

## L137 (2028-05-24)

Stored preferences:
- For gift wrapping style, the user prefers a reusable cloth wrap.
- For gift wrapping style when presents for nieces and nephews, the user prefers a patterned gift bag.
- For gift wrapping style when wedding gifts, the user prefers glossy paper with a satin ribbon.
- For gift wrapping style when gifts for coworkers, the user prefers brown kraft paper with twine.

Conversation:
- user: My nephew still talks about his birthday present, mostly because he got to draw all over the wrapping.
- assistant: That's adorable. Has it helped with the wrapping question you were mulling over?
- user: It has. No more gift bags for the kids: gifts for the kids in the family get brown paper and string from now on, so they can doodle on it.

## L138 (2028-05-15)

Stored preferences:
- For phone alert style, the user prefers a single soft chime.
- For phone alert style when dinners out alone, the user prefers vibration only.
- For phone alert style when cinema trips, the user prefers vibration only.
- For phone alert style when the evening train ride, the user prefers silent banners.
- For phone alert style when dinners out with friends, the user prefers alerts held for later.

Conversation:
- user: The garage says they'll ring about the car sometime this evening, which knowing my luck means while I'm on the train.
- assistant: Classic timing. Is there anything I can set up?
- user: Put my phone on full volume for my trip home from work tonight. Only tonight, I just can't miss that call.

## L139 (2028-01-31)

Stored preferences:
- For commute mode, the user prefers cycling in.
- For commute mode when gym days, the user prefers driving myself.
- For commute mode when late shifts, the user prefers driving myself.
- For commute mode when rainy days, the user prefers the express bus.
- For packed lunch, the user prefers leftovers from dinner.
- For packed lunch when gym days, the user prefers a chicken and rice bowl.
- For packed lunch when rainy days, the user prefers a thermos of soup.

Conversation:
- user: They've cut the express route back to once an hour. I stood at the stop for forty minutes this morning, soaked through.
- assistant: Forty minutes in that weather sounds miserable. Are you thinking of switching?
- user: Yes. On rainy days I'll be catching the train from now on. It's a longer walk to the station, but at least it actually turns up.
- assistant: Fair enough. Does that change anything about lunch on those days?
- user: No, the hot soup is the one thing about wet days that works. Keep that coming.

## L140 (2028-03-02)

Stored preferences:
- For hotel room placement, the user prefers a room near the lifts.
- For hotel room placement when conference trips, the user prefers a room next to the stairwell.
- For hotel room placement when overnight layovers, the user prefers a room at the quiet end of the corridor.
- For hotel room placement when road trips, the user prefers a room overlooking the courtyard.

Conversation:
- user: Worked it out. It's the grandparents' town: the hotel there is right on the main road.
- assistant: Ah. So what would help on those visits?
- user: For trips to see my grandparents, get me somewhere up high, away from the traffic.

## L141 (2028-04-05)

Stored preferences:
- For long-distance transport, the user prefers the high-speed train.
- For long-distance transport when trips with the dog, the user prefers a rental car.
- For long-distance transport when work trips, the user prefers a short-haul flight.
- For main travel bag, the user prefers a wheeled carry-on.
- For main travel bag when weekend getaways, the user prefers a canvas duffel.
- For main travel bag when work trips, the user prefers a garment bag.

Conversation:
- user: We had the best weekend: tiny cabin up in the hills, no signal, total bliss. Getting there by train took three changes though.
- assistant: That sounds lovely, apart from the changes. Anything you'd do differently next time?
- user: Yes. For weekend getaways, just book us a hire car. The duffel is still all I need for those.

## L142 (2028-08-12)

Stored preferences:
- For grocery delivery time, the user prefers evening delivery.
- For grocery delivery time when deadline weeks, the user prefers early-morning delivery.
- For grocery delivery time when weeks with house guests, the user prefers mid-afternoon delivery.
- For grocery delivery time when night-shift weeks, the user prefers early-morning delivery.

Conversation:
- user: Swim club has moved to six o'clock, so our evenings are now a blur of wet towels and lost goggles.
- assistant: That sounds hectic! Are the kids enjoying it at least?
- user: They love it. I just wish the pool were closer. The groceries keep turning up while we're out, though.
- assistant: Ah, that's annoying. Do you want the deliveries moved?
- user: Yes. Make late-night delivery our regular slot from now on. Once the kids are in bed I can put everything away in peace.

## L143 (2028-09-05)

Stored preferences:
- For notebook page ruling, the user prefers narrow-ruled lines.
- For notebook page ruling when monthly budget planning, the user prefers a square grid.
- For notebook page ruling when sketching page layouts, the user prefers a dot grid.
- For pen ink color, the user prefers black ink.
- For pen ink color when signing contracts, the user prefers navy blue ink.

Conversation:
- user: I handed a marked-up report back to one of our new interns today and the poor kid looked crushed. Every margin was full of my black scrawl.
- assistant: Oof. A wall of corrections can be a lot to take in.
- user: Right? For marking up drafts I want green ink for the time being, until the interns find their feet. It reads a lot friendlier.

## L144 (2028-03-07)

Stored preferences:
- For reward treat for the dog, the user prefers apple slices.
- For reward treat for the dog when trips to the vet, the user prefers freeze-dried liver bites.

Conversation:
- user: We did a six-hour loop on Sunday and she was flagging badly by the end.
- assistant: That's a long day for anyone, four legs or two. Did she have enough to keep her going?
- user: Clearly not. Fruit isn't enough fuel for that. On long hikes she should get chicken jerky strips from now on, something with a bit of protein in it.

## L145 (2028-09-05)

Stored preferences:
- For background music style, the user prefers classical piano.
- For background music style when dinner with friends, the user prefers old soul records.
- For background music style when evenings with the kids, the user prefers film soundtracks.
- For evening film genre, the user prefers a slow-burn thriller.
- For evening film genre when film club evenings, the user prefers an old black-and-white classic.
- For evening film genre when date nights, the user prefers a romantic comedy.
- For evening film genre when evenings with the kids, the user prefers an animated feature.

Conversation:
- user: A friend keeps telling us a proper date night needs something tense, and that rom-coms are for teenagers.
- assistant: Strong opinions! Are you tempted to try it their way?
- user: Not a chance. We get enough suspense at work. We're sticking with our rom-coms.

## L146 (2028-08-10)

Stored preferences:
- For taxi vehicle type, the user prefers a fully electric car.
- For taxi vehicle type when rides to the airport, the user prefers a compact hatchback.
- For taxi vehicle type when rides to client meetings, the user prefers a premium car with leather seats.

Conversation:
- user: Finance just announced they won't reimburse the fancy cars anymore.
- assistant: Oh no. Is that going to be a problem for you?
- user: Honestly, no. In three years not a single client has mentioned the leather seats. Drop them for trips to see clients, they were only ever for show.

## L147 (2028-02-10)

Stored preferences:
- For delivery time slot, the user prefers a mid-afternoon slot.
- For delivery time slot when furniture deliveries, the user prefers a weekend slot.
- For delivery time slot when grocery deliveries, the user prefers an evening slot.
- For delivery time slot when courier pickups for returns, the user prefers a lunchtime slot.
- For delivery time slot when parcels that need a signature, the user prefers an early-morning slot.

Conversation:
- user: Working from home has me rethinking my odd delivery times. One of them has stopped making sense: either the early courier for anything I have to sign for, or the weekly food order after six.
- assistant: Which of the two is bothering you more?
- user: That's just it, I can't tell yet. Give me a couple more weeks of actually living like this and I'll tell you which one.

## L148 (2028-06-08)

Stored preferences:
- For rail or coach service, the user prefers the direct train.
- For rail or coach service when airport runs, the user prefers the express coach.
- For rail or coach service when trips to the head office, the user prefers the stopping train from 2028-05-08 through 2028-05-28.

Conversation:
- user: I've got tickets for three gigs in town this summer!
- assistant: Fun! Who are you seeing?
- user: Mostly local bands. One snag: the last fast train leaves before the encores. For concert nights in the city, book the stopping train home from now on; it runs until midnight.

## L149 (2028-02-02)

Stored preferences:
- For hotel room placement, the user prefers a room on a high floor.
- For hotel room placement when beach holidays, the user prefers a ground-floor room.
- For hotel room placement when conference trips, the user prefers a room next to the stairwell.
- For hotel room placement when overnight layovers, the user prefers a room at the quiet end of the corridor.
- For hotel room placement when road trips, the user prefers a room overlooking the courtyard.

Conversation:
- user: I'm sorting out the March trip to the coast. We sold the surfboards, by the way.
- assistant: Oh, end of an era! Does that change anything about the booking?
- user: It does. For trips to the coast I don't need street level any more, that was only for hauling the boards in and out. Nothing special there now.

## L150 (2028-07-12)

Stored preferences:
- For wake-up alarm time, the user prefers a quarter to seven.
- For wake-up alarm time when commuting days, the user prefers six o'clock.
- For wake-up alarm time when remote workdays, the user prefers half past five for now, with no end date given.
- For wake-up alarm time when weekends, the user prefers eight o'clock.

Conversation:
- user: Strange confession: I'm starting to enjoy the early starts.
- assistant: Really? What changed?
- user: The street is silent before six, and I get more done in that hour than in the whole afternoon.
- assistant: There's something to be said for having the world to yourself.
- user: There is. I might keep the early alarm on remote workdays even once the builders are gone, or I might not. I usually hate mornings, so let me see how I feel when they're done.

## L151 (2028-09-27)

Stored preferences:
- For food order spice level, the user prefers the restaurant's standard heat.
- For food order spice level when takeaway nights alone, the user prefers extra hot.
- For food order spice level when takeaway nights with guests, the user prefers chili on the side.
- For food order spice level when weekday lunch orders, the user prefers no chili at all.
- For food order spice level when weekend lunch orders, the user prefers medium heat.

Conversation:
- user: Have you noticed how much the heat varies between places? One night it's nothing, the next I'm crying into my rice.
- assistant: Kitchens really don't agree on what spicy means. Is it getting to you?
- user: A bit. Normally I'd rather ask for just a hint of spice. Going with the restaurant's standard heat is too much of a gamble.

## L152 (2028-10-31)

Stored preferences:
- For topping for home-baked cakes, the user prefers a simple lemon glaze.
- For topping for home-baked cakes when birthday parties, the user prefers whipped cream.
- For topping for home-baked cakes when bake sales at work, the user prefers salted caramel drizzle.

Conversation:
- user: My niece turns twelve on Saturday and she's asked me for a chocolate cake with ganache for her birthday party.
- assistant: She knows what she wants! Shall I put the ingredients on the shopping list?
- user: Yes please, dark chocolate and a pot of cream.
- assistant: Added. Anything else for the party?
- user: No, that's it. The ganache is just for her party though, she's the only kid I know who likes the bitter stuff.

## L153 (2028-11-13)

Stored preferences:
- For meeting length, the user prefers a full hour.
- For meeting length when planning days, the user prefers a 90-minute working session.
- For quick-question channel, the user prefers a short email.
- For quick-question channel when release weeks, the user prefers a five-minute video call.
- For quick-question channel when remote days, the user prefers a chat message.

Conversation:
- user: My new manager does everything by phone on her remote days. She says typing is slower than talking.
- assistant: Some people really prefer that. Does it suit you?
- user: Not me. When I'm working from home I'd still rather get a quick ping, I can answer it between other things.

## L154 (2028-02-09)

Stored preferences:
- For commute mode, the user prefers cycling in.
- For commute mode when gym days, the user prefers driving myself.
- For commute mode when late shifts, the user prefers driving myself.
- For commute mode when rainy days, the user prefers the commuter train.
- For packed lunch, the user prefers leftovers from dinner.
- For packed lunch when gym days, the user prefers a chicken and rice bowl.
- For packed lunch when rainy days, the user prefers a thermos of soup.

Conversation:
- user: We've started cooking smaller dinners, so the fridge is basically empty by the next morning.
- assistant: Less waste, at least. Does that change what goes in your lunch box?
- user: It does. Most days, just make me a veggie wrap. Quick and easy.

## L155 (2028-07-05)

Stored preferences:
- For wake-up alarm time, the user prefers a quarter to seven.
- For wake-up alarm time when commuting days, the user prefers six o'clock.
- For wake-up alarm time when weekends, the user prefers eight o'clock.

Conversation:
- user: The house next door is being gutted, and the builders start drilling at seven on the dot.
- assistant: That's a brutal alarm clock. How are you holding up?
- user: Badly, so I'm getting my focus hour in before they start. On remote workdays, wake me at half past five for now. They won't say how long the job will take.

## L156 (2028-06-12)

Stored preferences:
- For taxi vehicle type, the user prefers a standard sedan.
- For taxi vehicle type when rides to the airport, the user prefers a roomy minivan.
- For taxi vehicle type when rides to client meetings, the user prefers a premium car with leather seats.

Conversation:
- user: I'm off to a two-day workshop on Wednesday, and the flight leaves at some ungodly hour.
- assistant: Ouch, early start. Anything I should know for the ride?
- user: I'm only taking a backpack, so just for this airport run a small car is plenty. No sense paying for a van to haul one bag.

## L157 (2028-05-24)

Stored preferences:
- For long-distance transport, the user prefers the intercity coach.
- For long-distance transport when trips with the dog, the user prefers a rental car.
- For long-distance transport when weekend getaways, the user prefers a rental car.
- For long-distance transport when work trips, the user prefers the overnight sleeper.
- For main travel bag, the user prefers a wheeled carry-on.
- For main travel bag when weekend getaways, the user prefers a canvas duffel.
- For main travel bag when work trips, the user prefers a garment bag.

Conversation:
- user: Funny thing: since we started taking a hire car for weekend getaways, I keep cramming everything into that duffel for no reason.
- assistant: Old habits! Do you still want it packed for those trips?
- user: Not really, the boot has loads of room. For weekends away I don't need the duffel anymore.

## L158 (2028-09-18)

Stored preferences:
- For food order spice level, the user prefers the restaurant's standard heat.
- For food order spice level when takeaway nights alone, the user prefers extra hot.
- For food order spice level when takeaway nights with guests, the user prefers chili on the side.
- For food order spice level when weekday lunch orders, the user prefers a mild heat level.
- For food order spice level when weekend lunch orders, the user prefers medium heat.

Conversation:
- user: Rough afternoon. Heartburn all the way through the budget review.
- assistant: That sounds miserable. Did you manage to get through it?
- user: Just about. I kept sipping water and nodding at spreadsheets.
- assistant: Glad you survived. Any idea what set it off?
- user: The mild curry from lunch, would you believe. Even that's too much before an afternoon of meetings.
- assistant: Sorry to hear it. Is there anything you want done differently?
- user: For lunches ordered to the office, zero heat, please. I'll save the spice for later in the day.

## L159 (2028-06-02)

Stored preferences:
- For phone alert style, the user prefers a single soft chime.
- For phone alert style when dinners out alone, the user prefers vibration only.
- For phone alert style when cinema trips, the user prefers vibration only.
- For phone alert style when the evening train ride, the user prefers silent banners.
- For phone alert style when dinners out with friends, the user prefers silent banners.

Conversation:
- user: Missed two deliveries this week. The courier rang both times and I didn't hear a thing.
- assistant: That's maddening. Was the phone in another room?
- user: Right next to me on the sofa. One gentle ding is just too easy to miss. Normally I want full volume now.

## L160 (2028-08-30)

Stored preferences:
- For grocery delivery time, the user prefers late-night delivery.
- For grocery delivery time when deadline weeks, the user prefers early-morning delivery.
- For grocery delivery time when weeks with house guests, the user prefers mid-afternoon delivery.
- For grocery delivery time when night-shift weeks, the user prefers early-morning delivery.

Conversation:
- user: School starts again on Monday, thank goodness. The late deliveries were a disaster this summer: the kids stayed up to 'help' unpack every single time.
- assistant: Very helpful of them. Is there anything you'd like done differently next time?
- user: Yes. For school holidays, book early-morning delivery. They sleep in until nine, so I can unpack before anyone's up.

## L161 (2028-02-01)

Stored preferences:
- For delivery time slot, the user prefers the first available slot.
- For delivery time slot when furniture deliveries, the user prefers a weekend slot.
- For delivery time slot when grocery deliveries, the user prefers an evening slot.
- For delivery time slot when courier pickups for returns, the user prefers a lunchtime slot.
- For delivery time slot when parcels that need a signature, the user prefers an early-morning slot.

Conversation:
- user: Guess who finally talked her manager into letting her work from home most of the week?
- assistant: No way! Congratulations. How's it feeling so far?
- user: Bliss. It also means that normally I'd go for a mid-afternoon slot for my deliveries now. Taking whatever's soonest made sense when the place sat empty all day, but these days I'm right here after lunch.

## L162 (2028-05-24)

Stored preferences:
- For phone alert style, the user prefers a single soft chime.
- For phone alert style when dinners out alone, the user prefers vibration only.
- For phone alert style when cinema trips, the user prefers vibration only.
- For phone alert style when the evening train ride, the user prefers silent banners.
- For phone alert style when dinners out with friends, the user prefers alerts held for later.

Conversation:
- user: I felt terrible on Saturday. Dinner with the old crowd, and I didn't see the babysitter's messages until eleven.
- assistant: Oh no. Was everything all right at home?
- user: Yes, thankfully, just a temperature that came down. But having everything held back until we'd finished eating was a bad idea.
- assistant: That sounds stressful. What would work better?
- user: At meals out with my friends, give me quiet pop-ups instead. I can glance down without anyone noticing.

## L163 (2028-05-02)

Stored preferences:
- For audiobook playback speed, the user prefers 1.25x speed.
- For audiobook playback speed when bedtime listening, the user prefers 0.75x speed.
- For audiobook playback speed when the morning commute, the user prefers 1.5x speed.

Conversation:
- user: I've been doing that ear-training trick where you nudge the speed up a notch each week.
- assistant: Oh, interesting. How far have you got?
- user: Far enough that 1.25x sounds like slow motion now. It's honestly a bit unsettling.
- assistant: Ha, that happens. Do you want me to change anything?
- user: Yes, let's make double speed my usual from here on.

## L164 (2028-07-18)

Stored preferences:
- For background music style, the user prefers lo-fi beats.
- For background music style when date nights, the user prefers slow jazz.
- For background music style when dinner with friends, the user prefers old soul records.
- For background music style when evenings with the kids, the user prefers sing-along pop.
- For evening film genre, the user prefers a slow-burn thriller.
- For evening film genre when film club evenings, the user prefers an old black-and-white classic.
- For evening film genre when date nights, the user prefers a romantic comedy.
- For evening film genre when evenings with the kids, the user prefers an animated feature.

Conversation:
- user: The kids have been restless on family evenings lately. Either they're bored of the films or of the music, and I honestly can't tell which.
- assistant: Do you want to change something now, or find out first?
- user: I'll ask them at the weekend and get back to you on what should change.

## L165 (2028-04-27)

Stored preferences:
- For laundry drying method, the user prefers line drying outside.
- For laundry drying method when cotton jumpers, the user prefers an indoor drying rack.
- For laundry drying method when dark bath towels, the user prefers an indoor drying rack.
- For laundry drying method when work shirts, the user prefers hanging on padded hangers.
- For laundry drying method when white bath towels, the user prefers a high-heat tumble dry.
- For laundry drying method when wool jumpers, the user prefers drying flat on a towel.

Conversation:
- user: Replaced the sweater that shrank. Well, I bought three, all pre-shrunk cotton.
- assistant: A proper restock! What colours did you go for?
- user: Grey, blue and a mustard one I'm not sure about. The label says they can take anything, so my cotton sweaters don't need any special treatment any more.

## L166 (2028-04-11)

Stored preferences:
- For audiobook playback speed, the user prefers 1.25x speed.
- For audiobook playback speed when bedtime listening, the user prefers 0.75x speed for now, with no end date given.
- For audiobook playback speed when the morning commute, the user prefers 1.5x speed.

Conversation:
- user: Book club is tomorrow evening and I'm still four chapters from the end. Rookie mistake.
- assistant: Oh no! Do you think you'll make it?
- user: Only if I cheat. Tonight in bed, play it at double speed, just this once. I'll sleep when I know who did it.

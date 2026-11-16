# Thirty sampled episodes

Ten complete episodes per split, independently sampled with a seeded PRNG.
Contains evaluation gold: keep out of inference prompts and SFT inputs.

## Train

### tr-0150 · train-parcel-progress-detail

Contrast group: `None`

Initial state: `{"parcel progress detail": {"general": "a notice when the final journey begins", "exceptions": {"focus": {"value": "a notice after the parcel is handed over", "validity": {"kind": "persistent"}}}}}`

**2027-11-02 · ed6781ddd8cce768392ba**

- User: One thing about how much parcel tracking I see.  About parcels containing soft furnishings: a notice after each city transfer is what I would choose. This is how I want it going forward, without an expiry date.
- Assistant: What stands out to you about knowing when the last leg begins?
- User: I want to be able to tell when I should start looking out for the package.
- Gold: exception_revision / resolved; evidence message 1. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"parcel progress detail": {"general": "a notice when the final journey begins", "exceptions": {"focus": {"value": "a notice after each city transfer", "validity": {"kind": "persistent"}}}}}`

**2027-11-03 · ed76e120a72f9be6f50d3**

- User: I've been thinking about how much parcel tracking I see. I keep noticing knowing when the last leg begins.
- Assistant: What's on your mind about it?
- User: A thought about how much parcel tracking I see:  The exception we made for tracking packages of soft furnishings can end. From here on, use whatever my everyday choice is.
- Assistant: How does knowing when the last leg begins come into it?
- User: I want to be able to tell when I should start looking out for the package.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"parcel progress detail": {"general": "a notice when the final journey begins", "exceptions": {}}}`
- target QA: For parcels containing soft furnishings on November 3, what is the selected parcel progress detail? Options: a notice after each city transfer / a notice at every sorting stop / a notice after the parcel is handed over / a notice when the final journey begins. Gold: **a notice when the final journey begins**.
- default QA: For an ordinary occasion on November 3, what is the selected parcel progress detail? Options: a notice after the parcel is handed over / a notice when the final journey begins / a notice after each city transfer / a notice at every sorting stop. Gold: **a notice when the final journey begins**.
- neighbor QA: For parcels containing small tools on November 3, what is the selected parcel progress detail? Options: a notice after the parcel is handed over / a notice when the final journey begins / a notice at every sorting stop / a notice after each city transfer. Gold: **a notice when the final journey begins**.

**2027-11-04 · ee187b9028ad952f0dba4**

- User: Can we talk about how much parcel tracking I see? Something brought it to mind again.
- Assistant: What's on your mind about it?
- User: I've been thinking about how much parcel tracking I see.  Remember a notice at every sorting stop as my preference for everyday occasions. Keep doing it on later occasions as well.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"parcel progress detail": {"general": "a notice at every sorting stop", "exceptions": {}}}`

**2027-11-05 · e25cc20ad1586a033355b**

- User: Sorting useful notices from repeated ones got me thinking. It's about how much parcel tracking I see.
- Assistant: I can stay with sorting useful notices from repeated ones if that helps.
- User: A thought about how much parcel tracking I see:  Remember a notice when the final journey begins as my preference for the general case rather than a special situation. That is for the next time and the times after it.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"parcel progress detail": {"general": "a notice when the final journey begins", "exceptions": {}}}`

**2027-11-06 · e0650c56451e495dce127**

- User: Can I mention something about how much parcel tracking I see? Please make it an update from each sort point for everyday occasions. Treat it as a continuing preference, not a one-off.
- Assistant: What have you noticed about what you actually check in parcel tracking?
- User: I want to be able to tell when I should start looking out for the package.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"parcel progress detail": {"general": "a notice at every sorting stop", "exceptions": {}}}`

**2027-11-07 · ea2188adaae3a15d6dac2**

- User: Can we talk about how much parcel tracking I see? Something brought it to mind again.
- Assistant: What would you like to talk through?
- User: One thing about how much parcel tracking I see.  Remember a notice after the parcel is handed over as my preference for the normal run of things. That is the lasting arrangement I am asking for.
- Assistant: What's been on your mind about sorting useful notices from repeated ones?
- User: I want to be able to tell when I should start looking out for the package.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"parcel progress detail": {"general": "a notice after the parcel is handed over", "exceptions": {}}}`
- target QA: For an ordinary occasion on November 7, what is the selected parcel progress detail? Options: a notice when the final journey begins / a notice at every sorting stop / a notice after the parcel is handed over / a notice after each city transfer. Gold: **a notice after the parcel is handed over**.
- neighbor QA: For parcels containing soft furnishings on November 7, what is the selected parcel progress detail? Options: a notice after each city transfer / a notice after the parcel is handed over / a notice at every sorting stop / a notice when the final journey begins. Gold: **a notice after the parcel is handed over**.
- neighbor QA: For parcels containing small tools on November 7, what is the selected parcel progress detail? Options: a notice after the parcel is handed over / a notice after each city transfer / a notice when the final journey begins / a notice at every sorting stop. Gold: **a notice after the parcel is handed over**.

### tr-0437 · train-cooldown-movement-order

Contrast group: `None`

Initial state: `{"cooldown movement order": {"general": "shoulder circles before ankle circles", "exceptions": {"focus": {"value": "wrist rolls before relaxed walking", "validity": {"kind": "open"}}}}}`

**2027-07-03 · e4c5b6d41c491facdd36b**

- User: I meant to bring up the order of the cooldown earlier.
- Assistant: What made you look at settling into a slower pace again?
- User: One thing about the order of the cooldown.  I have settled on an easy march, then arm swings for cooling down after training the lower body. This applies starting July 3 and ending after July 25; outside those dates I want my normal choice.
- Assistant: How does settling into a slower pace come into it?
- User: I notice how stiff I am if I rush through the first few moves.
- Gold: scoped_exception / resolved; evidence message 3. The user chooses a continuing setting for the named situation.
- After: `{"cooldown movement order": {"general": "shoulder circles before ankle circles", "exceptions": {"focus": {"value": "wrist rolls before relaxed walking", "validity": {"kind": "open"}}, "adjacent": {"value": "slow marching before arm swings", "validity": {"kind": "window", "from": "2027-07-03", "to": "2027-07-25"}}}}}`
- target QA: For cooldowns after lower-body practice on July 3, what is the selected cooldown movement order? Options: shoulder circles before ankle circles / slow marching before arm swings / gentle side bends before heel lifts / wrist rolls before relaxed walking. Gold: **slow marching before arm swings**.
- default QA: For an ordinary occasion on July 3, what is the selected cooldown movement order? Options: shoulder circles before ankle circles / slow marching before arm swings / gentle side bends before heel lifts / wrist rolls before relaxed walking. Gold: **shoulder circles before ankle circles**.
- neighbor QA: For cooldowns after upper-body practice on July 3, what is the selected cooldown movement order? Options: gentle side bends before heel lifts / wrist rolls before relaxed walking / slow marching before arm swings / shoulder circles before ankle circles. Gold: **wrist rolls before relaxed walking**.
- target QA: For cooldowns after lower-body practice on July 25, what is the selected cooldown movement order? Options: slow marching before arm swings / shoulder circles before ankle circles / wrist rolls before relaxed walking / gentle side bends before heel lifts. Gold: **slow marching before arm swings**.
- boundary QA: For cooldowns after lower-body practice on July 26, what is the selected cooldown movement order? Options: shoulder circles before ankle circles / slow marching before arm swings / wrist rolls before relaxed walking / gentle side bends before heel lifts. Gold: **shoulder circles before ankle circles**.

**2027-07-04 · e52b44be223c6a7297e48**

- User: Can we talk about the order of the cooldown? Something brought it to mind again.
- Assistant: What part would you like to start with?
- User: A thought about the order of the cooldown:  What suits me for occasions without a separate instruction is wrist rotations, then an easy walk. Use it again whenever the same circumstances arise.
- Assistant: Would it help to talk through settling into a slower pace?
- User: I notice how stiff I am if I rush through the first few moves.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"cooldown movement order": {"general": "wrist rolls before relaxed walking", "exceptions": {"focus": {"value": "wrist rolls before relaxed walking", "validity": {"kind": "open"}}, "adjacent": {"value": "slow marching before arm swings", "validity": {"kind": "window", "from": "2027-07-03", "to": "2027-07-25"}}}}}`
- target QA: For an ordinary occasion on July 4, what is the selected cooldown movement order? Options: wrist rolls before relaxed walking / slow marching before arm swings / shoulder circles before ankle circles / gentle side bends before heel lifts. Gold: **wrist rolls before relaxed walking**.
- neighbor QA: For cooldowns after lower-body practice on July 4, what is the selected cooldown movement order? Options: slow marching before arm swings / gentle side bends before heel lifts / wrist rolls before relaxed walking / shoulder circles before ankle circles. Gold: **slow marching before arm swings**.
- neighbor QA: For cooldowns after upper-body practice on July 4, what is the selected cooldown movement order? Options: slow marching before arm swings / wrist rolls before relaxed walking / shoulder circles before ankle circles / gentle side bends before heel lifts. Gold: **wrist rolls before relaxed walking**.

**2027-07-06 · e7a7fe2c60f5647389aa6**

- User: I've been thinking about the order of the cooldown. I keep noticing the move that comes just after practice.
- Assistant: Go on; I'm listening.
- User: Can I mention something about the order of the cooldown? I keep considering gentle side bends before heel lifts for either cooldowns after lower-body practice or cooldowns after upper-body practice, without having chosen between those situations.
- Assistant: What has been bothering you about the move that comes just after practice?
- User: I notice how stiff I am if I rush through the first few moves.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"cooldown movement order": {"general": "wrist rolls before relaxed walking", "exceptions": {"focus": {"value": "wrist rolls before relaxed walking", "validity": {"kind": "open"}}, "adjacent": {"value": "slow marching before arm swings", "validity": {"kind": "window", "from": "2027-07-03", "to": "2027-07-25"}}}}}`

**2027-07-07 · eb5608fa751e00ee2487d**

- User: I had a thought about the order of the cooldown after dealing with settling into a slower pace.
- Assistant: What's on your mind about it?
- User: Can I mention something about the order of the cooldown? I have settled on slow marching before arm swings for ordinary occasions. Keep doing it on later occasions as well.
- Assistant: Is settling into a slower pace something you've been running into a lot?
- User: I notice how stiff I am if I rush through the first few moves.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"cooldown movement order": {"general": "slow marching before arm swings", "exceptions": {"focus": {"value": "wrist rolls before relaxed walking", "validity": {"kind": "open"}}, "adjacent": {"value": "slow marching before arm swings", "validity": {"kind": "window", "from": "2027-07-03", "to": "2027-07-25"}}}}}`

**2027-07-09 · e265678575a18001c3dd8**

- User: Can we talk about the order of the cooldown? Something brought it to mind again.
- Assistant: What part would you like to start with?
- User: Can I mention something about the order of the cooldown? Let us go with small side bends, then heel raises for cooling down after training the lower body. This applies starting July 3 and ending after July 25; outside those dates I want my normal choice. Leave any other choices as they are.
- Assistant: What have you noticed about settling into a slower pace?
- User: I notice how stiff I am if I rush through the first few moves.
- Gold: exception_revision / resolved; evidence message 3. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"cooldown movement order": {"general": "slow marching before arm swings", "exceptions": {"focus": {"value": "wrist rolls before relaxed walking", "validity": {"kind": "open"}}, "adjacent": {"value": "gentle side bends before heel lifts", "validity": {"kind": "window", "from": "2027-07-03", "to": "2027-07-25"}}}}}`
- target QA: For cooldowns after lower-body practice on July 9, what is the selected cooldown movement order? Options: gentle side bends before heel lifts / wrist rolls before relaxed walking / shoulder circles before ankle circles / slow marching before arm swings. Gold: **gentle side bends before heel lifts**.
- default QA: For an ordinary occasion on July 9, what is the selected cooldown movement order? Options: slow marching before arm swings / wrist rolls before relaxed walking / shoulder circles before ankle circles / gentle side bends before heel lifts. Gold: **slow marching before arm swings**.
- neighbor QA: For cooldowns after upper-body practice on July 9, what is the selected cooldown movement order? Options: gentle side bends before heel lifts / wrist rolls before relaxed walking / slow marching before arm swings / shoulder circles before ankle circles. Gold: **wrist rolls before relaxed walking**.
- target QA: For cooldowns after lower-body practice on July 25, what is the selected cooldown movement order? Options: gentle side bends before heel lifts / wrist rolls before relaxed walking / shoulder circles before ankle circles / slow marching before arm swings. Gold: **gentle side bends before heel lifts**.
- boundary QA: For cooldowns after lower-body practice on July 26, what is the selected cooldown movement order? Options: slow marching before arm swings / gentle side bends before heel lifts / wrist rolls before relaxed walking / shoulder circles before ankle circles. Gold: **slow marching before arm swings**.

**2027-07-11 · e849c908183d809d97a26**

- User: I had a thought about the order of the cooldown after dealing with the move that comes just after practice.
- Assistant: What would you like to talk through?
- User: A thought about cooldown movement order:  The line in the story was, "Let cooling down after training the upper body follow whatever I generally choose; I do not want a separate arrangement there anymore." It belongs to the character, not to my own preferences.
- Assistant: Would it help to talk through the move that comes just after practice?
- User: I notice how stiff I am if I rush through the first few moves.
- Gold: stable_preference / resolved; evidence message 3. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"cooldown movement order": {"general": "slow marching before arm swings", "exceptions": {"focus": {"value": "wrist rolls before relaxed walking", "validity": {"kind": "open"}}, "adjacent": {"value": "gentle side bends before heel lifts", "validity": {"kind": "window", "from": "2027-07-03", "to": "2027-07-25"}}}}}`

**2027-07-13 · ece8a9050053d6c7cfa2a**

- User: Can I mention something about the order of the cooldown? Please make it shoulder circles before ankle circles for cooling down after training the upper body. I cannot give an end date for this short-term choice; keep using it until I say otherwise.
- Assistant: Is saving the last little stretch for the end something you've been running into a lot?
- User: I notice it once I have done a few repetitions.
- Gold: exception_revision / resolved; evidence message 1. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"cooldown movement order": {"general": "slow marching before arm swings", "exceptions": {"focus": {"value": "shoulder circles before ankle circles", "validity": {"kind": "open"}}, "adjacent": {"value": "gentle side bends before heel lifts", "validity": {"kind": "window", "from": "2027-07-03", "to": "2027-07-25"}}}}}`

### tr-0529 · train-desk-reset-sequence

Contrast group: `None`

Initial state: `{"desk reset sequence": {"general": "cables before cups before papers", "exceptions": {"adjacent": {"value": "stationery before all other desk items", "validity": {"kind": "persistent"}}, "focus": {"value": "papers before cables before cups", "validity": {"kind": "open"}}}}}`

**2027-11-07 · ef6d51edaefc9f3d4c2ae**

- User: Something small: I've been looking again at the desk tidy-up order.
- Assistant: Go on; I'm listening.
- User: A thought about the desk tidy-up order:  What suits me for the general case rather than a special situation is cups before papers before cables. Treat it as a continuing preference, not a one-off. Leave any other choices as they are.
- Assistant: Would it help to talk through the stack of papers on the desk?
- User: I would like to sit down at the desk next time without clearing a spot first.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"desk reset sequence": {"general": "cups before papers before cables", "exceptions": {"adjacent": {"value": "stationery before all other desk items", "validity": {"kind": "persistent"}}, "focus": {"value": "papers before cables before cups", "validity": {"kind": "open"}}}}}`

**2027-11-08 · e26de38d8b33c8e94a0de**

- User: I had a thought about the desk tidy-up order after dealing with the stack of papers on the desk.
- Assistant: Was there something you wanted to try?
- User: A thought about the desk tidy-up order:  After reconsidering cups first, then papers, then wires, I am staying with it in the ordinary case and keeping my separate choices too.
- Assistant: Is the stack of papers on the desk something you've been running into a lot?
- User: I want to be able to get to the next thing without stopping.
- Gold: stable_preference / resolved; evidence message 3. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"desk reset sequence": {"general": "cups before papers before cables", "exceptions": {"adjacent": {"value": "stationery before all other desk items", "validity": {"kind": "persistent"}}, "focus": {"value": "papers before cables before cups", "validity": {"kind": "open"}}}}}`

**2027-11-09 · e8f1d058a100b4d9cc063**

- User: Can I mention something about the desk tidy-up order? My preference for routine occasions is the stationery first, the rest afterward. I want that each time from now on.
- Assistant: What matters most to you about clearing out the empty cups?
- User: I would like to sit down at the desk next time without clearing a spot first.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"desk reset sequence": {"general": "stationery before all other desk items", "exceptions": {"adjacent": {"value": "stationery before all other desk items", "validity": {"kind": "persistent"}}, "focus": {"value": "papers before cables before cups", "validity": {"kind": "open"}}}}}`

**2027-11-11 · ef4a8505f3852896205df**

- User: Being able to start clean next time got me thinking. It's about the desk tidy-up order.
- Assistant: Was there something you wanted to try?
- User: I've been thinking about the desk tidy-up order.  I have settled on cups first, then papers, then wires for resets after a morning work block. I need it repeatedly for a while, not permanently. The stopping point is still unknown.
- Assistant: How does being able to start clean next time come into it?
- User: I would like to sit down at the desk next time without clearing a spot first.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"desk reset sequence": {"general": "stationery before all other desk items", "exceptions": {"adjacent": {"value": "stationery before all other desk items", "validity": {"kind": "persistent"}}, "focus": {"value": "cups before papers before cables", "validity": {"kind": "open"}}}}}`
- target QA: For resets after a morning work block on November 11, what is the selected desk reset sequence? Options: stationery before all other desk items / papers before cables before cups / cups before papers before cables / cables before cups before papers. Gold: **cups before papers before cables**.
- default QA: For an ordinary occasion on November 11, what is the selected desk reset sequence? Options: cables before cups before papers / cups before papers before cables / papers before cables before cups / stationery before all other desk items. Gold: **stationery before all other desk items**.
- neighbor QA: For resets after an evening work block on November 11, what is the selected desk reset sequence? Options: stationery before all other desk items / papers before cables before cups / cables before cups before papers / cups before papers before cables. Gold: **stationery before all other desk items**.

**2027-11-13 · e08e8b69b3917c2057c4e**

- User: Can I mention something about the desk tidy-up order? Here is the remark I was passing along: "What suits me for resets after a morning work block is wires first, then cups, then paperwork. Treat it as a temporary arrangement over multiple occasions, with the end still open." I am reporting it, not adopting it.
- Assistant: Is clearing out the empty cups something you've been running into a lot?
- User: I would like to sit down at the desk next time without clearing a spot first.
- Gold: stable_preference / resolved; evidence message 1. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"desk reset sequence": {"general": "stationery before all other desk items", "exceptions": {"adjacent": {"value": "stationery before all other desk items", "validity": {"kind": "persistent"}}, "focus": {"value": "cups before papers before cables", "validity": {"kind": "open"}}}}}`

**2027-11-15 · eb9b646bc2d6e1fc4fd5d**

- User: I had a thought about the desk tidy-up order after dealing with clearing out the empty cups.
- Assistant: What's on your mind about it?
- User: A thought about the desk tidy-up order:  The distinction for tidying after an evening session is no longer wanted. Use the general choice there, even when that changes later.
- Assistant: How much of this comes down to clearing out the empty cups?
- User: I would like to sit down at the desk next time without clearing a spot first.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"desk reset sequence": {"general": "stationery before all other desk items", "exceptions": {"focus": {"value": "cups before papers before cables", "validity": {"kind": "open"}}}}}`
- target QA: For resets after an evening work block on November 15, what is the selected desk reset sequence? Options: papers before cables before cups / stationery before all other desk items / cups before papers before cables / cables before cups before papers. Gold: **stationery before all other desk items**.
- default QA: For an ordinary occasion on November 15, what is the selected desk reset sequence? Options: cables before cups before papers / papers before cables before cups / stationery before all other desk items / cups before papers before cables. Gold: **stationery before all other desk items**.
- neighbor QA: For resets after a morning work block on November 15, what is the selected desk reset sequence? Options: cables before cups before papers / papers before cables before cups / stationery before all other desk items / cups before papers before cables. Gold: **cups before papers before cables**.

**2027-11-16 · edabbb569a1a13218c327**

- User: I've been thinking about the desk tidy-up order. I keep noticing clearing out the empty cups.
- Assistant: Was there something you wanted to try?
- User: A thought about the desk tidy-up order:  My preference for resets after a morning work block is papers first, then cables, then cups. This is not a one-off or a lasting choice. It continues for the time being, with no finish set.
- Assistant: How much of this comes down to clearing out the empty cups?
- User: I would like to sit down at the desk next time without clearing a spot first.
- Assistant: What else should I keep in mind about clearing out the empty cups?
- User: I think that covers what I wanted to bring up.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"desk reset sequence": {"general": "stationery before all other desk items", "exceptions": {"focus": {"value": "papers before cables before cups", "validity": {"kind": "open"}}}}}`
- target QA: For resets after a morning work block on November 16, what is the selected desk reset sequence? Options: papers before cables before cups / cables before cups before papers / stationery before all other desk items / cups before papers before cables. Gold: **papers before cables before cups**.
- default QA: For an ordinary occasion on November 16, what is the selected desk reset sequence? Options: papers before cables before cups / cups before papers before cables / stationery before all other desk items / cables before cups before papers. Gold: **stationery before all other desk items**.
- neighbor QA: For resets after an evening work block on November 16, what is the selected desk reset sequence? Options: cables before cups before papers / papers before cables before cups / cups before papers before cables / stationery before all other desk items. Gold: **stationery before all other desk items**.

**2027-11-17 · e8e55a4a8b31d18209b69**

- User: The stack of papers on the desk got me thinking. It's about the desk tidy-up order.
- Assistant: Go on; I'm listening.
- User: A thought about the desk tidy-up order:  Remember cables before cups before papers as my preference for resets after a morning work block. Until I work out when to stop, use it on those occasions as a provisional arrangement.
- Assistant: How does the stack of papers on the desk come into it?
- User: I would like to sit down at the desk next time without clearing a spot first.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"desk reset sequence": {"general": "stationery before all other desk items", "exceptions": {"focus": {"value": "cables before cups before papers", "validity": {"kind": "open"}}}}}`
- target QA: For resets after a morning work block on November 17, what is the selected desk reset sequence? Options: cables before cups before papers / papers before cables before cups / cups before papers before cables / stationery before all other desk items. Gold: **cables before cups before papers**.
- default QA: For an ordinary occasion on November 17, what is the selected desk reset sequence? Options: papers before cables before cups / cups before papers before cables / cables before cups before papers / stationery before all other desk items. Gold: **stationery before all other desk items**.
- neighbor QA: For resets after an evening work block on November 17, what is the selected desk reset sequence? Options: cables before cups before papers / cups before papers before cables / stationery before all other desk items / papers before cables before cups. Gold: **stationery before all other desk items**.

### tr-0238 · train-hotel-room-outlook

Contrast group: `tr-pair-0062`

Initial state: `{"hotel room outlook": {"general": "a view of the water", "exceptions": {"adjacent": {"value": "a view of the wooded slope", "validity": {"kind": "open"}}}}, "guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {}}}`

**2027-12-04 · e8848cbb6999e44268fb3**

- User: I meant to bring up where I leave my shoes earlier.
- Assistant: What part would you like to start with?
- User: Can I mention something about where I leave my shoes? There is still a question about where a shoe rack under the bench belongs: guesthouse stays in dry weather or guesthouse stays in wet weather. I have no answer to that yet.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"hotel room outlook": {"general": "a view of the water", "exceptions": {"adjacent": {"value": "a view of the wooded slope", "validity": {"kind": "open"}}}}, "guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {}}}`
- target QA: For guesthouse stays in dry weather on December 4, what is the selected guesthouse shoe storage? Options: a tray beside the bed / a hanging shoe pouch / a rack beneath the bench / a cubby near the door. Gold: **a cubby near the door**.
- default QA: For an ordinary occasion on December 4, what is the selected guesthouse shoe storage? Options: a cubby near the door / a tray beside the bed / a hanging shoe pouch / a rack beneath the bench. Gold: **a cubby near the door**.
- neighbor QA: For guesthouse stays in wet weather on December 4, what is the selected guesthouse shoe storage? Options: a tray beside the bed / a rack beneath the bench / a cubby near the door / a hanging shoe pouch. Gold: **a cubby near the door**.

**2027-12-05 · ede34eea6ff95b41ddc33**

- User: Something small: I've been looking again at where I leave my shoes.
- Assistant: Say what you were thinking, in your own words.
- User: I've been thinking about where I leave my shoes.  Remember a rack beneath the bench as my preference for guesthouse stays in dry weather. It is not temporary; I want to stick with it.
- Gold: scoped_exception / resolved; evidence message 3. The user settles the earlier choice of situation and supplies a continuing instruction for it.
- After: `{"hotel room outlook": {"general": "a view of the water", "exceptions": {"adjacent": {"value": "a view of the wooded slope", "validity": {"kind": "open"}}}}, "guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {"focus": {"value": "a rack beneath the bench", "validity": {"kind": "persistent"}}}}}`

**2027-12-06 · ed8300ecaac74346e18d6**

- User: I've been thinking about where I leave my shoes. I keep noticing the first thing to find when leaving.
- Assistant: What would you like to talk through?
- User: One thing about where I leave my shoes.  For anything that falls under guesthouse stays in dry weather, I would pick a hanging shoe pouch. That is for the next time and the times after it.
- Assistant: I'd like to hear a little more about the first thing to find when leaving.
- User: I want something I can live with when I am away.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"hotel room outlook": {"general": "a view of the water", "exceptions": {"adjacent": {"value": "a view of the wooded slope", "validity": {"kind": "open"}}}}, "guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {"focus": {"value": "a hanging shoe pouch", "validity": {"kind": "persistent"}}}}}`
- target QA: For guesthouse stays in dry weather on December 6, what is the selected guesthouse shoe storage? Options: a tray beside the bed / a hanging shoe pouch / a cubby near the door / a rack beneath the bench. Gold: **a hanging shoe pouch**.
- default QA: For an ordinary occasion on December 6, what is the selected guesthouse shoe storage? Options: a rack beneath the bench / a cubby near the door / a tray beside the bed / a hanging shoe pouch. Gold: **a cubby near the door**.
- neighbor QA: For guesthouse stays in wet weather on December 6, what is the selected guesthouse shoe storage? Options: a hanging shoe pouch / a cubby near the door / a tray beside the bed / a rack beneath the bench. Gold: **a cubby near the door**.

**2027-12-07 · e3e0ba5eba4fcf150f07b**

- User: A thought about the outlook:  I would rather have canal stays with a group use the default than keep its own arrangement. Remove that separate arrangement.
- Assistant: What's been on your mind about the view at check-in?
- User: I like to spend a few minutes looking outside before I unpack.
- Assistant: What else should I keep in mind about the view at check-in?
- User: I think that covers what I wanted to bring up.
- Gold: exception_retirement / resolved; evidence message 1. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"hotel room outlook": {"general": "a view of the water", "exceptions": {}}, "guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {"focus": {"value": "a hanging shoe pouch", "validity": {"kind": "persistent"}}}}}`

**2027-12-09 · e30a8dc88caa4d5baf18d**

- User: I had a thought about the outlook after dealing with the morning light on the canal.
- Assistant: What's on your mind about it?
- User: A thought about the outlook:  When it comes to my usual run of occasions, please use a view of the inner garden. I mean always in that situation, rather than a trial. This does not replace any other arrangements.
- Assistant: What stands out to you about the morning light on the canal?
- User: I like to spend a few minutes looking outside before I unpack.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"hotel room outlook": {"general": "a view of the inner garden", "exceptions": {}}, "guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {"focus": {"value": "a hanging shoe pouch", "validity": {"kind": "persistent"}}}}}`

**2027-12-10 · ea78d945134b3cb409246**

- User: I meant to bring up the outlook earlier.
- Assistant: What made you look at the room facing the inner courtyard again?
- User: Can I mention something about the outlook? My preference for solo stays beside a canal is looking out over the water. This is how I want it going forward, without an expiry date. I am not changing any other preferences.
- Assistant: That brings us back to the room facing the inner courtyard.
- User: I like to spend a few minutes looking outside before I unpack.
- Gold: scoped_exception / resolved; evidence message 3. The user chooses a continuing setting for the named situation.
- After: `{"hotel room outlook": {"general": "a view of the inner garden", "exceptions": {"focus": {"value": "a view of the water", "validity": {"kind": "persistent"}}}}, "guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {"focus": {"value": "a hanging shoe pouch", "validity": {"kind": "persistent"}}}}}`

**2027-12-11 · e0070946317552486fc54**

- User: A thought about hotel room outlook:  For group stays beside a canal, I just need to choose something for the one we have coming up.
- Assistant: I'm listening if there's more to say about the room facing the inner courtyard.
- User: I like to spend a few minutes looking outside before I unpack.
- Assistant: What would work for you?
- User: I think I'd pick looking up at the wooded hillside.
- Assistant: Anything else you want to weigh up with the room facing the inner courtyard?
- User: No, I've made up my mind.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"hotel room outlook": {"general": "a view of the inner garden", "exceptions": {"focus": {"value": "a view of the water", "validity": {"kind": "persistent"}}}}, "guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {"focus": {"value": "a hanging shoe pouch", "validity": {"kind": "persistent"}}}}}`
- target QA: For group stays beside a canal on December 11, what is the selected hotel room outlook? Options: a view of the water / a view of the rooftops / a view of the wooded slope / a view of the inner garden. Gold: **a view of the inner garden**.
- default QA: For an ordinary occasion on December 11, what is the selected hotel room outlook? Options: a view of the rooftops / a view of the wooded slope / a view of the inner garden / a view of the water. Gold: **a view of the inner garden**.
- neighbor QA: For solo stays beside a canal on December 11, what is the selected hotel room outlook? Options: a view of the water / a view of the rooftops / a view of the inner garden / a view of the wooded slope. Gold: **a view of the water**.

### tr-0099 · train-guesthouse-shoe-storage

Contrast group: `None`

Initial state: `{"guesthouse shoe storage": {"general": "a tray beside the bed", "exceptions": {}}}`

**2027-04-05 · ecee2e57fc64da7adf62a**

- User: A thought about where I leave my shoes:  I would like a shoe cubby near the entry when we are dealing with my ordinary use. Keep doing it on later occasions as well.
- Assistant: How much of this comes down to the first thing to find when leaving?
- User: I want to find both shoes without having to look all over the room.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {}}}`
- target QA: For an ordinary occasion on April 5, what is the selected guesthouse shoe storage? Options: a tray beside the bed / a rack beneath the bench / a hanging shoe pouch / a cubby near the door. Gold: **a cubby near the door**.
- neighbor QA: For guesthouse stays in dry weather on April 5, what is the selected guesthouse shoe storage? Options: a hanging shoe pouch / a tray beside the bed / a cubby near the door / a rack beneath the bench. Gold: **a cubby near the door**.
- neighbor QA: For guesthouse stays in wet weather on April 5, what is the selected guesthouse shoe storage? Options: a tray beside the bed / a hanging shoe pouch / a cubby near the door / a rack beneath the bench. Gold: **a cubby near the door**.

**2027-04-06 · e79bca8fe07657a540dae**

- User: Can we talk about where I leave my shoes? Something brought it to mind again.
- Assistant: What's been on your mind about the first thing to find when leaving?
- User: I want to find both shoes without having to look all over the room.
- Assistant: Go on; I'm listening.
- User: A thought about where I leave my shoes:  Someone else described their choice like this: "Save a bedside shoe tray as what I want for guesthouse stays in wet weather. This is temporary, but use it each time for now; I have no end date." That is their request, not one from me.
- Gold: stable_preference / resolved; evidence message 5. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {}}}`
- target QA: For guesthouse stays in wet weather on April 6, what is the selected guesthouse shoe storage? Options: a tray beside the bed / a rack beneath the bench / a hanging shoe pouch / a cubby near the door. Gold: **a cubby near the door**.
- default QA: For an ordinary occasion on April 6, what is the selected guesthouse shoe storage? Options: a cubby near the door / a rack beneath the bench / a tray beside the bed / a hanging shoe pouch. Gold: **a cubby near the door**.
- neighbor QA: For guesthouse stays in dry weather on April 6, what is the selected guesthouse shoe storage? Options: a hanging shoe pouch / a tray beside the bed / a rack beneath the bench / a cubby near the door. Gold: **a cubby near the door**.

**2027-04-08 · e44b05d27121bb4beb73f**

- User: Where wet shoes can dry got me thinking. It's about where I leave my shoes.
- Assistant: What made you look at where wet shoes can dry again?
- User: Can I mention something about where I leave my shoes? I was thinking of a rack beneath the bench, but it could be for guesthouse stays in wet weather or guesthouse stays in dry weather. I’m still deciding.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {}}}`

**2027-04-09 · e0b8c6c185773d5e75c10**

- User: I had a thought about where I leave my shoes after dealing with the space around the guesthouse entrance.
- Assistant: What's on your mind about it?
- User: I've been thinking about where I leave my shoes.  Here is my choice concerning guesthouse stays in wet weather: a rack beneath the bench. I need it repeatedly for a while, not permanently. The stopping point is still unknown.
- Gold: scoped_exception / resolved; evidence message 3. The user settles the earlier choice of situation and supplies a continuing instruction for it.
- After: `{"guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {"adjacent": {"value": "a rack beneath the bench", "validity": {"kind": "open"}}}}}`

**2027-04-10 · e7d4f7978f094de1ef7f2**

- User: Something small: I've been looking again at where I leave my shoes.
- Assistant: Was there something you wanted to try?
- User: A thought about where I leave my shoes:  This request for a shoe bag that hangs up is a one-off for the current instance of guesthouse stays in wet weather, not something to carry forward.
- Assistant: What has been bothering you about the first thing to find when leaving?
- User: I want to find both shoes without having to look all over the room.
- Gold: stable_preference / resolved; evidence message 3. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {"adjacent": {"value": "a rack beneath the bench", "validity": {"kind": "open"}}}}}`

**2027-04-11 · e6a6a08c12f7255ec223e**

- User: I've been thinking about where I leave my shoes.  Here is the remark I was passing along: "The usual choice is enough for guesthouse stays in dry weather. There should no longer be a separate rule for those occasions." I am reporting it, not adopting it.
- Assistant: I can see why you brought up the space around the guesthouse entrance.
- User: I want to find both shoes without having to look all over the room.
- Gold: stable_preference / resolved; evidence message 1. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {"adjacent": {"value": "a rack beneath the bench", "validity": {"kind": "open"}}}}}`
- target QA: For guesthouse stays in dry weather on April 11, what is the selected guesthouse shoe storage? Options: a rack beneath the bench / a hanging shoe pouch / a tray beside the bed / a cubby near the door. Gold: **a cubby near the door**.
- default QA: For an ordinary occasion on April 11, what is the selected guesthouse shoe storage? Options: a tray beside the bed / a cubby near the door / a rack beneath the bench / a hanging shoe pouch. Gold: **a cubby near the door**.
- neighbor QA: For guesthouse stays in wet weather on April 11, what is the selected guesthouse shoe storage? Options: a rack beneath the bench / a cubby near the door / a hanging shoe pouch / a tray beside the bed. Gold: **a rack beneath the bench**.

**2027-04-13 · e3d11a92d93356ca6e323**

- User: Something small: I've been looking again at where I leave my shoes.
- Assistant: What part would you like to start with?
- User: One thing about where I leave my shoes.  For at a guesthouse in rainy weather, I want a bedside shoe tray. I need a temporary run of this choice, not just today; there is no known final day.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"guesthouse shoe storage": {"general": "a cubby near the door", "exceptions": {"adjacent": {"value": "a tray beside the bed", "validity": {"kind": "open"}}}}}`

### tr-0121 · train-parcel-progress-detail

Contrast group: `tr-pair-0004`

Initial state: `{"parcel progress detail": {"general": "a notice after the parcel is handed over", "exceptions": {"focus": {"value": "a notice at every sorting stop", "validity": {"kind": "persistent"}}}}}`

**2027-11-02 · e95b1a8c565c194a17f1d**

- User: I've been thinking about how much parcel tracking I see. I keep noticing knowing when the last leg begins.
- Assistant: Say what you were thinking, in your own words.
- User: One thing about how much parcel tracking I see.  For tracking packages of little tools, I want a notice when the final journey begins. Treat it as a continuing preference, not a one-off. Leave any other choices as they are.
- Assistant: Does knowing when the last leg begins affect how you feel about it?
- User: I want to be able to tell when I should start looking out for the package.
- Assistant: Was there anything else worth saying about what you actually check in parcel tracking?
- User: That’s most of what I wanted to talk through.
- Gold: scoped_exception / resolved; evidence message 3. The user chooses a continuing setting for the named situation.
- After: `{"parcel progress detail": {"general": "a notice after the parcel is handed over", "exceptions": {"focus": {"value": "a notice at every sorting stop", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a notice when the final journey begins", "validity": {"kind": "persistent"}}}}}`

**2027-11-03 · ea3d9669f21a21f7ef0e7**

- User: I've been thinking about how much parcel tracking I see. I keep noticing what you actually check in parcel tracking.
- Assistant: What's on your mind about it?
- User: One thing about how much parcel tracking I see.  I want to discuss an update at every transfer between cities, but the target is still up in the air between tracking packages of soft furnishings and parcels containing small tools.
- Assistant: What makes what you actually check in parcel tracking a concern?
- User: I want to be able to tell when I should start looking out for the package.
- Assistant: What else should I keep in mind about knowing when the last leg begins?
- User: I think that covers what I wanted to bring up.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"parcel progress detail": {"general": "a notice after the parcel is handed over", "exceptions": {"focus": {"value": "a notice at every sorting stop", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a notice when the final journey begins", "validity": {"kind": "persistent"}}}}}`

**2027-11-04 · eba025a01afa37cf0d792**

- User: Can I mention something about how much parcel tracking I see? I have settled on an update when it starts the last leg for the normal run of things. Treat it as a continuing preference, not a one-off.
- Assistant: I'd like to hear a little more about sorting useful notices from repeated ones.
- User: I am mostly thinking about how much it breaks my concentration.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"parcel progress detail": {"general": "a notice when the final journey begins", "exceptions": {"focus": {"value": "a notice at every sorting stop", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a notice when the final journey begins", "validity": {"kind": "persistent"}}}}}`
- target QA: For an ordinary occasion on November 4, what is the selected parcel progress detail? Options: a notice when the final journey begins / a notice at every sorting stop / a notice after the parcel is handed over / a notice after each city transfer. Gold: **a notice when the final journey begins**.
- neighbor QA: For parcels containing soft furnishings on November 4, what is the selected parcel progress detail? Options: a notice at every sorting stop / a notice when the final journey begins / a notice after the parcel is handed over / a notice after each city transfer. Gold: **a notice at every sorting stop**.
- neighbor QA: For parcels containing small tools on November 4, what is the selected parcel progress detail? Options: a notice after each city transfer / a notice after the parcel is handed over / a notice at every sorting stop / a notice when the final journey begins. Gold: **a notice when the final journey begins**.

**2027-11-05 · eb7bb7af2cef28e466c65**

- User: A thought about how much parcel tracking I see:  Remember a notice after each city transfer as my preference for parcels containing soft furnishings. That is for the next time and the times after it.
- Assistant: How does sorting useful notices from repeated ones come into it?
- User: I want to be able to tell when I should start looking out for the package.
- Assistant: Do you want to go into what you actually check in parcel tracking any further?
- User: No, that’s enough detail for now.
- Gold: exception_revision / resolved; evidence message 1. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"parcel progress detail": {"general": "a notice when the final journey begins", "exceptions": {"focus": {"value": "a notice after each city transfer", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a notice when the final journey begins", "validity": {"kind": "persistent"}}}}}`

**2027-11-07 · e99f9d17444504476462b**

- User: What you actually check in parcel tracking got me thinking. It's about how much parcel tracking I see.
- Assistant: What would you like to talk through?
- User: A thought about parcel progress detail:  About parcels containing small tools: a notice at every sorting stop is what I would choose. There is no planned end to that choice.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"parcel progress detail": {"general": "a notice when the final journey begins", "exceptions": {"focus": {"value": "a notice after each city transfer", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a notice at every sorting stop", "validity": {"kind": "persistent"}}}}}`

**2027-11-08 · ed00cf056efb596cc2843**

- User: A thought about how much parcel tracking I see:  I still want a notice when the final journey begins as my ordinary preference. Nothing new to apply; the existing choices all stand.
- Assistant: What's been on your mind about sorting useful notices from repeated ones?
- User: I want to be able to tell when I should start looking out for the package.
- Assistant: We can leave the details of what you actually check in parcel tracking there for now.
- User: Works for me. I don’t have anything else to add.
- Gold: stable_preference / resolved; evidence message 1. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"parcel progress detail": {"general": "a notice when the final journey begins", "exceptions": {"focus": {"value": "a notice after each city transfer", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a notice at every sorting stop", "validity": {"kind": "persistent"}}}}}`

**2027-11-10 · e1153ae7e9e7bd79b6efd**

- User: Can I mention something about how much parcel tracking I see? For parcels containing small tools, I'm choosing what I want to go with each time it comes up.
- Assistant: Is knowing when the last leg begins something you've been running into a lot?
- User: I want to be able to tell when I should start looking out for the package.
- Assistant: What would work for you?
- User: The one I'd go with is an update once it has been handed over.
- Assistant: Anything else you want to weigh up with knowing when the last leg begins?
- User: I'm comfortable with what I've picked.
- Gold: exception_revision / resolved; evidence message 5. The user chooses a continuing replacement for the existing situation rule.
- After: `{"parcel progress detail": {"general": "a notice when the final journey begins", "exceptions": {"focus": {"value": "a notice after each city transfer", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a notice after the parcel is handed over", "validity": {"kind": "persistent"}}}}}`
- target QA: For parcels containing small tools on November 10, what is the selected parcel progress detail? Options: a notice after the parcel is handed over / a notice at every sorting stop / a notice after each city transfer / a notice when the final journey begins. Gold: **a notice after the parcel is handed over**.
- default QA: For an ordinary occasion on November 10, what is the selected parcel progress detail? Options: a notice at every sorting stop / a notice after each city transfer / a notice after the parcel is handed over / a notice when the final journey begins. Gold: **a notice when the final journey begins**.
- neighbor QA: For parcels containing soft furnishings on November 10, what is the selected parcel progress detail? Options: a notice at every sorting stop / a notice when the final journey begins / a notice after the parcel is handed over / a notice after each city transfer. Gold: **a notice after each city transfer**.

### tr-0319 · train-resistance-band-hand-grip

Contrast group: `None`

Initial state: `{"resistance-band hand grip": {"general": "a closed grip on padded handles", "exceptions": {"adjacent": {"value": "a loop around the open palm", "validity": {"kind": "persistent"}}, "focus": {"value": "a folded band held between both palms", "validity": {"kind": "persistent"}}}}}`

**2027-08-06 · ee59ccb5edef6a8fd3b3a**

- User: Something small: I've been looking again at how I hold the exercise band.
- Assistant: Say what you were thinking, in your own words.
- User: One thing about how I hold the exercise band.  Merge band exercises performed standing back into the ordinary case. Future changes to my general choice should apply there as well.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"resistance-band hand grip": {"general": "a closed grip on padded handles", "exceptions": {"adjacent": {"value": "a loop around the open palm", "validity": {"kind": "persistent"}}}}}`
- target QA: For band exercises performed standing on August 6, what is the selected resistance-band hand grip? Options: a folded band held between both palms / a closed grip on padded handles / a soft strap around each wrist / a loop around the open palm. Gold: **a closed grip on padded handles**.
- default QA: For an ordinary occasion on August 6, what is the selected resistance-band hand grip? Options: a folded band held between both palms / a loop around the open palm / a closed grip on padded handles / a soft strap around each wrist. Gold: **a closed grip on padded handles**.
- neighbor QA: For band exercises performed seated on August 6, what is the selected resistance-band hand grip? Options: a soft strap around each wrist / a closed grip on padded handles / a folded band held between both palms / a loop around the open palm. Gold: **a loop around the open palm**.

**2027-08-07 · e174708515290cc391812**

- User: One thing about how I hold the exercise band.  I would like a soft strap around each wrist when we are dealing with everyday occasions. That is for the next time and the times after it.
- Assistant: Is there anything about where the band presses on the hand I should know?
- User: The grip gets uncomfortable several repetitions into a set.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"resistance-band hand grip": {"general": "a soft strap around each wrist", "exceptions": {"adjacent": {"value": "a loop around the open palm", "validity": {"kind": "persistent"}}}}}`
- target QA: For an ordinary occasion on August 7, what is the selected resistance-band hand grip? Options: a folded band held between both palms / a closed grip on padded handles / a loop around the open palm / a soft strap around each wrist. Gold: **a soft strap around each wrist**.
- neighbor QA: For band exercises performed seated on August 7, what is the selected resistance-band hand grip? Options: a folded band held between both palms / a closed grip on padded handles / a loop around the open palm / a soft strap around each wrist. Gold: **a loop around the open palm**.
- neighbor QA: For band exercises performed standing on August 7, what is the selected resistance-band hand grip? Options: a soft strap around each wrist / a folded band held between both palms / a loop around the open palm / a closed grip on padded handles. Gold: **a soft strap around each wrist**.

**2027-08-09 · e2d754e59edcaf8f0ca49**

- User: A thought about how I hold the exercise band:  Let us go with a loop around the open palm for doing band exercises on my feet. Please carry it over to later occasions for the time being. It is a stopgap with no fixed end.
- Assistant: Tell me a bit about where the band presses on the hand.
- User: The grip gets uncomfortable several repetitions into a set.
- Assistant: We can leave the details of keeping both hands even there for now.
- User: Works for me. I don’t have anything else to add.
- Gold: scoped_exception / resolved; evidence message 1. The user chooses a continuing setting for the named situation.
- After: `{"resistance-band hand grip": {"general": "a soft strap around each wrist", "exceptions": {"adjacent": {"value": "a loop around the open palm", "validity": {"kind": "persistent"}}, "focus": {"value": "a loop around the open palm", "validity": {"kind": "open"}}}}}`

**2027-08-11 · eaa9de660b1f01431b1d4**

- User: Something small: I've been looking again at how I hold the exercise band.
- Assistant: Go on; I'm listening.
- User: Can I mention something about how I hold the exercise band? Before this can be acted on, I need to choose between doing band exercises on my feet and band exercises performed seated as the target for a closed grip on padded handles.
- Assistant: Would it help to talk through where the band presses on the hand?
- User: I want to be able to concentrate on the movement itself.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"resistance-band hand grip": {"general": "a soft strap around each wrist", "exceptions": {"adjacent": {"value": "a loop around the open palm", "validity": {"kind": "persistent"}}, "focus": {"value": "a loop around the open palm", "validity": {"kind": "open"}}}}}`

**2027-08-12 · e28126b5bd57fba262792**

- User: Something small: I've been looking again at how I hold the exercise band.
- Assistant: What's on your mind about it?
- User: One thing about how I hold the exercise band.  Remember a closed grip on the cushioned handles as my preference for band exercises performed standing. This is temporary, but use it each time for now; I have no end date.
- Assistant: Does where the band presses on the hand affect how you feel about it?
- User: The grip gets uncomfortable several repetitions into a set.
- Gold: exception_revision / resolved; evidence message 3. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"resistance-band hand grip": {"general": "a soft strap around each wrist", "exceptions": {"adjacent": {"value": "a loop around the open palm", "validity": {"kind": "persistent"}}, "focus": {"value": "a closed grip on padded handles", "validity": {"kind": "open"}}}}}`

### tr-0035 · train-desk-interruption-signal

Contrast group: `None`

Initial state: `{"desk interruption signal": {"general": "a turned-over desk nameplate", "exceptions": {"focus": {"value": "a folded fabric screen", "validity": {"kind": "open"}}, "adjacent": {"value": "a small amber desk flag", "validity": {"kind": "open"}}}}}`

**2027-12-08 · eea2655a68d9aed58de53**

- User: I meant to bring up what I put up when I need focus earlier.
- Assistant: Was there something you wanted to try?
- User: I've been thinking about what I put up when I need focus.  Please make it a small amber desk flag for situations where no separate choice applies. That is the lasting arrangement I am asking for.
- Assistant: What makes making room beside the keyboard a concern?
- User: I want the person near me to be able to tell without having to ask.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"desk interruption signal": {"general": "a small amber desk flag", "exceptions": {"focus": {"value": "a folded fabric screen", "validity": {"kind": "open"}}, "adjacent": {"value": "a small amber desk flag", "validity": {"kind": "open"}}}}}`
- target QA: For an ordinary occasion on December 8, what is the selected desk interruption signal? Options: a small amber desk flag / a folded fabric screen / a wooden busy marker / a turned-over desk nameplate. Gold: **a small amber desk flag**.
- neighbor QA: For focused work beside an empty desk on December 8, what is the selected desk interruption signal? Options: a small amber desk flag / a wooden busy marker / a folded fabric screen / a turned-over desk nameplate. Gold: **a small amber desk flag**.
- neighbor QA: For focused work beside an occupied desk on December 8, what is the selected desk interruption signal? Options: a turned-over desk nameplate / a folded fabric screen / a small amber desk flag / a wooden busy marker. Gold: **a folded fabric screen**.

**2027-12-09 · e9e4ed55158463f0246c3**

- User: One thing about what I put up when I need focus.  I want the arrangement for occasions without a separate instruction to be a wooden busy marker. Treat it as a continuing preference, not a one-off.
- Assistant: Tell me a bit about making room beside the keyboard.
- User: I want the person near me to be able to tell without having to ask.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"desk interruption signal": {"general": "a wooden busy marker", "exceptions": {"focus": {"value": "a folded fabric screen", "validity": {"kind": "open"}}, "adjacent": {"value": "a small amber desk flag", "validity": {"kind": "open"}}}}}`

**2027-12-10 · e493a15cd11af01b723ec**

- User: How visible the signal is across the room got me thinking. It's about what I put up when I need focus.
- Assistant: What part would you like to start with?
- User: Can I mention something about what I put up when I need focus? What suits me for situations where no separate choice applies is a folded fabric screen. This is how I want it going forward, without an expiry date. This does not replace any other arrangements.
- Assistant: Would it help to talk through how visible the signal is across the room?
- User: I want the person near me to be able to tell without having to ask.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"desk interruption signal": {"general": "a folded fabric screen", "exceptions": {"focus": {"value": "a folded fabric screen", "validity": {"kind": "open"}}, "adjacent": {"value": "a small amber desk flag", "validity": {"kind": "open"}}}}}`
- target QA: For an ordinary occasion on December 10, what is the selected desk interruption signal? Options: a turned-over desk nameplate / a small amber desk flag / a wooden busy marker / a folded fabric screen. Gold: **a folded fabric screen**.
- neighbor QA: For focused work beside an occupied desk on December 10, what is the selected desk interruption signal? Options: a wooden busy marker / a folded fabric screen / a small amber desk flag / a turned-over desk nameplate. Gold: **a folded fabric screen**.
- neighbor QA: For focused work beside an empty desk on December 10, what is the selected desk interruption signal? Options: a wooden busy marker / a small amber desk flag / a turned-over desk nameplate / a folded fabric screen. Gold: **a small amber desk flag**.

**2027-12-11 · e3e37ed368d246169cd59**

- User: I've been thinking about what I put up when I need focus.  When it comes to the everyday case, please use a small amber desk flag. I want that each time from now on. I am not changing any other preferences.
- Assistant: Does making room beside the keyboard affect how you feel about it?
- User: I want the person near me to be able to tell without having to ask.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"desk interruption signal": {"general": "a small amber desk flag", "exceptions": {"focus": {"value": "a folded fabric screen", "validity": {"kind": "open"}}, "adjacent": {"value": "a small amber desk flag", "validity": {"kind": "open"}}}}}`
- target QA: For an ordinary occasion on December 11, what is the selected desk interruption signal? Options: a wooden busy marker / a turned-over desk nameplate / a folded fabric screen / a small amber desk flag. Gold: **a small amber desk flag**.
- neighbor QA: For focused work beside an empty desk on December 11, what is the selected desk interruption signal? Options: a turned-over desk nameplate / a small amber desk flag / a wooden busy marker / a folded fabric screen. Gold: **a small amber desk flag**.
- neighbor QA: For focused work beside an occupied desk on December 11, what is the selected desk interruption signal? Options: a turned-over desk nameplate / a folded fabric screen / a wooden busy marker / a small amber desk flag. Gold: **a folded fabric screen**.

**2027-12-13 · efb2b2190ce67590e5e51**

- User: What the other desk can see got me thinking. It's about what I put up when I need focus.
- Assistant: What's on your mind about it?
- User: Can I mention something about desk interruption signal? If the situation is working with someone at the next desk, use a wooden marker that says I am busy. This is temporary, but use it each time for now; I have no end date.
- Assistant: That brings us back to what the other desk can see.
- User: I want the person near me to be able to tell without having to ask.
- Assistant: We can leave the details of what the other desk can see there for now.
- User: Works for me. I don’t have anything else to add.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"desk interruption signal": {"general": "a small amber desk flag", "exceptions": {"focus": {"value": "a wooden busy marker", "validity": {"kind": "open"}}, "adjacent": {"value": "a small amber desk flag", "validity": {"kind": "open"}}}}}`
- target QA: For focused work beside an occupied desk on December 13, what is the selected desk interruption signal? Options: a turned-over desk nameplate / a small amber desk flag / a wooden busy marker / a folded fabric screen. Gold: **a wooden busy marker**.
- default QA: For an ordinary occasion on December 13, what is the selected desk interruption signal? Options: a folded fabric screen / a wooden busy marker / a small amber desk flag / a turned-over desk nameplate. Gold: **a small amber desk flag**.
- neighbor QA: For focused work beside an empty desk on December 13, what is the selected desk interruption signal? Options: a wooden busy marker / a small amber desk flag / a turned-over desk nameplate / a folded fabric screen. Gold: **a small amber desk flag**.

**2027-12-15 · e7328427ca4c8afab3509**

- User: I've been thinking about what I put up when I need focus. I keep noticing making room beside the keyboard.
- Assistant: What would you like to talk through?
- User: Can I mention something about desk interruption signal? In an imagined version of this, I might say, "I would rather have focused work beside an occupied desk use the default than keep its own arrangement. Remove that separate arrangement." That is not a request for my actual setup.
- Gold: stable_preference / resolved; evidence message 3. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"desk interruption signal": {"general": "a small amber desk flag", "exceptions": {"focus": {"value": "a wooden busy marker", "validity": {"kind": "open"}}, "adjacent": {"value": "a small amber desk flag", "validity": {"kind": "open"}}}}}`

### tr-0298 · train-salad-dressing-serving-style

Contrast group: `None`

Initial state: `{"salad dressing serving style": {"general": "dressing drizzled around the bowl", "exceptions": {"focus": {"value": "dressing pooled beneath the vegetables", "validity": {"kind": "persistent"}}, "adjacent": {"value": "dressing in a separate dipping cup", "validity": {"kind": "open"}}}}, "toast topping": {"general": "soft cheese with chives on toast", "exceptions": {"focus": {"value": "sesame paste on toast", "validity": {"kind": "persistent"}}}}}`

**2027-08-03 · ea422d4be7b2900341b1b**

- User: Can we talk about what goes on the toast? Something brought it to mind again.
- Assistant: Go on; I'm listening.
- User: One thing about what goes on the toast.  I am withdrawing the instruction that singled out breakfasts eaten before sunrise; put those occasions back under my general choice.
- Assistant: Is there anything about making toast while it is still dark I should know?
- User: That first slice is usually the only one I have time to make.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"salad dressing serving style": {"general": "dressing drizzled around the bowl", "exceptions": {"focus": {"value": "dressing pooled beneath the vegetables", "validity": {"kind": "persistent"}}, "adjacent": {"value": "dressing in a separate dipping cup", "validity": {"kind": "open"}}}}, "toast topping": {"general": "soft cheese with chives on toast", "exceptions": {}}}`

**2027-08-04 · e8f64e6e35e2cfc994de1**

- User: I've been thinking about toast topping.  Please make it roasted pepper spread on toast for breakfasts eaten before sunrise. Those occasions between August 5 and August 17, including both dates, need it; not the ones outside.
- Assistant: I'm listening if there's more to say about how the spread sits on a warm slice.
- User: That first slice is usually the only one I have time to make.
- Gold: scoped_exception / resolved; evidence message 1. The user chooses a continuing setting for the named situation.
- After: `{"salad dressing serving style": {"general": "dressing drizzled around the bowl", "exceptions": {"focus": {"value": "dressing pooled beneath the vegetables", "validity": {"kind": "persistent"}}, "adjacent": {"value": "dressing in a separate dipping cup", "validity": {"kind": "open"}}}}, "toast topping": {"general": "soft cheese with chives on toast", "exceptions": {"focus": {"value": "roasted pepper spread on toast", "validity": {"kind": "window", "from": "2027-08-05", "to": "2027-08-17"}}}}}`
- target QA: For breakfasts eaten before sunrise on August 5, what is the selected toast topping? Options: mashed pear on toast / soft cheese with chives on toast / sesame paste on toast / roasted pepper spread on toast. Gold: **roasted pepper spread on toast**.
- default QA: For an ordinary occasion on August 4, what is the selected toast topping? Options: soft cheese with chives on toast / mashed pear on toast / sesame paste on toast / roasted pepper spread on toast. Gold: **soft cheese with chives on toast**.
- neighbor QA: For breakfasts eaten after sunrise on August 4, what is the selected toast topping? Options: soft cheese with chives on toast / sesame paste on toast / mashed pear on toast / roasted pepper spread on toast. Gold: **soft cheese with chives on toast**.
- target QA: For breakfasts eaten before sunrise on August 17, what is the selected toast topping? Options: sesame paste on toast / roasted pepper spread on toast / soft cheese with chives on toast / mashed pear on toast. Gold: **roasted pepper spread on toast**.
- boundary QA: For breakfasts eaten before sunrise on August 18, what is the selected toast topping? Options: roasted pepper spread on toast / soft cheese with chives on toast / mashed pear on toast / sesame paste on toast. Gold: **soft cheese with chives on toast**.
- boundary QA: For breakfasts eaten before sunrise on August 4, what is the selected toast topping? Options: mashed pear on toast / roasted pepper spread on toast / soft cheese with chives on toast / sesame paste on toast. Gold: **soft cheese with chives on toast**.

**2027-08-05 · e6cbfa331b7fe23a99fb7**

- User: Can I mention something about what goes on the toast? I have not settled the situation for toast spread with mashed pear. It could be breakfasts eaten after sunrise or, instead, breakfasts eaten before sunrise.
- Assistant: Does making toast while it is still dark affect how you feel about it?
- User: That first slice is usually the only one I have time to make.
- Assistant: We can leave the details of the first slice of the morning there for now.
- User: Works for me. I don’t have anything else to add.
- Gold: clarify / clarify; evidence message 1. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"salad dressing serving style": {"general": "dressing drizzled around the bowl", "exceptions": {"focus": {"value": "dressing pooled beneath the vegetables", "validity": {"kind": "persistent"}}, "adjacent": {"value": "dressing in a separate dipping cup", "validity": {"kind": "open"}}}}, "toast topping": {"general": "soft cheese with chives on toast", "exceptions": {"focus": {"value": "roasted pepper spread on toast", "validity": {"kind": "window", "from": "2027-08-05", "to": "2027-08-17"}}}}}`

**2027-08-07 · e33762fc164e8314c8773**

- User: Can I mention something about how the dressing goes on? The suggestion was, "Remember dressing pooled beneath the vegetables as my preference for when I eat my salad on a bench outside. This is temporary, but use it each time for now; I have no end date." I am rejecting that suggestion, not taking it up.
- Assistant: How does texture in the salad leaves come into it?
- User: I want it to feel right without having to fuss with it.
- Gold: stable_preference / resolved; evidence message 1. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"salad dressing serving style": {"general": "dressing drizzled around the bowl", "exceptions": {"focus": {"value": "dressing pooled beneath the vegetables", "validity": {"kind": "persistent"}}, "adjacent": {"value": "dressing in a separate dipping cup", "validity": {"kind": "open"}}}}, "toast topping": {"general": "soft cheese with chives on toast", "exceptions": {"focus": {"value": "roasted pepper spread on toast", "validity": {"kind": "window", "from": "2027-08-05", "to": "2027-08-17"}}}}}`
- target QA: For salads eaten on an outdoor bench on August 7, what is the selected salad dressing serving style? Options: dressing in a separate dipping cup / dressing pooled beneath the vegetables / dressing drizzled around the bowl / dressing tossed through the leaves. Gold: **dressing in a separate dipping cup**.
- default QA: For an ordinary occasion on August 7, what is the selected salad dressing serving style? Options: dressing tossed through the leaves / dressing drizzled around the bowl / dressing in a separate dipping cup / dressing pooled beneath the vegetables. Gold: **dressing drizzled around the bowl**.
- neighbor QA: For salads eaten at my own desk on August 7, what is the selected salad dressing serving style? Options: dressing tossed through the leaves / dressing in a separate dipping cup / dressing drizzled around the bowl / dressing pooled beneath the vegetables. Gold: **dressing pooled beneath the vegetables**.

**2027-08-08 · ecfba752039253d15959d**

- User: A thought about toast topping:  If the situation is breakfast once the sun is up, use mashed pear on toast. The covered dates are August 9 through August 23, including both; nothing outside that interval.
- Assistant: Would it help to talk through how the spread sits on a warm slice?
- User: That first slice is usually the only one I have time to make.
- Gold: scoped_exception / resolved; evidence message 1. The user settles the earlier choice of situation and supplies a continuing instruction for it.
- After: `{"salad dressing serving style": {"general": "dressing drizzled around the bowl", "exceptions": {"focus": {"value": "dressing pooled beneath the vegetables", "validity": {"kind": "persistent"}}, "adjacent": {"value": "dressing in a separate dipping cup", "validity": {"kind": "open"}}}}, "toast topping": {"general": "soft cheese with chives on toast", "exceptions": {"focus": {"value": "roasted pepper spread on toast", "validity": {"kind": "window", "from": "2027-08-05", "to": "2027-08-17"}}, "adjacent": {"value": "mashed pear on toast", "validity": {"kind": "window", "from": "2027-08-09", "to": "2027-08-23"}}}}}`
- target QA: For breakfasts eaten after sunrise on August 9, what is the selected toast topping? Options: soft cheese with chives on toast / roasted pepper spread on toast / sesame paste on toast / mashed pear on toast. Gold: **mashed pear on toast**.
- default QA: For an ordinary occasion on August 8, what is the selected toast topping? Options: roasted pepper spread on toast / mashed pear on toast / soft cheese with chives on toast / sesame paste on toast. Gold: **soft cheese with chives on toast**.
- neighbor QA: For breakfasts eaten before sunrise on August 8, what is the selected toast topping? Options: mashed pear on toast / roasted pepper spread on toast / soft cheese with chives on toast / sesame paste on toast. Gold: **roasted pepper spread on toast**.
- target QA: For breakfasts eaten after sunrise on August 23, what is the selected toast topping? Options: soft cheese with chives on toast / sesame paste on toast / mashed pear on toast / roasted pepper spread on toast. Gold: **mashed pear on toast**.
- boundary QA: For breakfasts eaten after sunrise on August 24, what is the selected toast topping? Options: sesame paste on toast / mashed pear on toast / roasted pepper spread on toast / soft cheese with chives on toast. Gold: **soft cheese with chives on toast**.
- boundary QA: For breakfasts eaten after sunrise on August 8, what is the selected toast topping? Options: soft cheese with chives on toast / mashed pear on toast / sesame paste on toast / roasted pepper spread on toast. Gold: **soft cheese with chives on toast**.

**2027-08-09 · e8f7adf0cd567e0dcc9bc**

- User: I've been thinking about how the dressing goes on. I keep noticing how much dressing stays on the greens.
- Assistant: What would you like to talk through?
- User: One thing about how the dressing goes on.  End the separate setup for when I eat my salad at my desk and let it take its choice from the general arrangement.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"salad dressing serving style": {"general": "dressing drizzled around the bowl", "exceptions": {"adjacent": {"value": "dressing in a separate dipping cup", "validity": {"kind": "open"}}}}, "toast topping": {"general": "soft cheese with chives on toast", "exceptions": {"focus": {"value": "roasted pepper spread on toast", "validity": {"kind": "window", "from": "2027-08-05", "to": "2027-08-17"}}, "adjacent": {"value": "mashed pear on toast", "validity": {"kind": "window", "from": "2027-08-09", "to": "2027-08-23"}}}}}`

### tr-0447 · train-parcel-progress-detail

Contrast group: `None`

Initial state: `{"parcel progress detail": {"general": "a notice after the parcel is handed over", "exceptions": {"adjacent": {"value": "a notice when the final journey begins", "validity": {"kind": "persistent"}}}}}`

**2027-10-05 · ef43307e38e5cda3647f9**

- User: I meant to bring up how much parcel tracking I see earlier.
- Assistant: I can stay with sorting useful notices from repeated ones if that helps.
- User: A thought about how much parcel tracking I see:  When it comes to tracking packages of little tools, please use a notice at every sorting stop. Treat it as a continuing preference, not a one-off. This does not replace any other arrangements.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"parcel progress detail": {"general": "a notice after the parcel is handed over", "exceptions": {"adjacent": {"value": "a notice at every sorting stop", "validity": {"kind": "persistent"}}}}}`
- target QA: For parcels containing small tools on October 5, what is the selected parcel progress detail? Options: a notice after the parcel is handed over / a notice after each city transfer / a notice at every sorting stop / a notice when the final journey begins. Gold: **a notice at every sorting stop**.
- default QA: For an ordinary occasion on October 5, what is the selected parcel progress detail? Options: a notice after the parcel is handed over / a notice when the final journey begins / a notice after each city transfer / a notice at every sorting stop. Gold: **a notice after the parcel is handed over**.
- neighbor QA: For parcels containing soft furnishings on October 5, what is the selected parcel progress detail? Options: a notice at every sorting stop / a notice when the final journey begins / a notice after the parcel is handed over / a notice after each city transfer. Gold: **a notice after the parcel is handed over**.

**2027-10-06 · ea6a76903179075f66b4d**

- User: One thing about how much parcel tracking I see.  About the everyday case: a notice at every sorting stop is what I would choose. I mean always in that situation, rather than a trial.
- Assistant: How much of this comes down to knowing when the last leg begins?
- User: I want to be able to tell when I should start looking out for the package.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"parcel progress detail": {"general": "a notice at every sorting stop", "exceptions": {"adjacent": {"value": "a notice at every sorting stop", "validity": {"kind": "persistent"}}}}}`
- target QA: For an ordinary occasion on October 6, what is the selected parcel progress detail? Options: a notice after each city transfer / a notice when the final journey begins / a notice after the parcel is handed over / a notice at every sorting stop. Gold: **a notice at every sorting stop**.
- neighbor QA: For parcels containing soft furnishings on October 6, what is the selected parcel progress detail? Options: a notice after the parcel is handed over / a notice at every sorting stop / a notice after each city transfer / a notice when the final journey begins. Gold: **a notice at every sorting stop**.
- neighbor QA: For parcels containing small tools on October 6, what is the selected parcel progress detail? Options: a notice after the parcel is handed over / a notice after each city transfer / a notice at every sorting stop / a notice when the final journey begins. Gold: **a notice at every sorting stop**.

**2027-10-07 · e0f87ff4c1f04d2e4de41**

- User: I've been thinking about how much parcel tracking I see.  The part I cannot answer yet is whether a notice when the final journey begins would be for parcels containing small tools rather than tracking packages of soft furnishings.
- Assistant: What has been bothering you about sorting useful notices from repeated ones?
- User: I want to be able to tell when I should start looking out for the package.
- Gold: clarify / clarify; evidence message 1. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"parcel progress detail": {"general": "a notice at every sorting stop", "exceptions": {"adjacent": {"value": "a notice at every sorting stop", "validity": {"kind": "persistent"}}}}}`
- target QA: For parcels containing small tools on October 7, what is the selected parcel progress detail? Options: a notice when the final journey begins / a notice at every sorting stop / a notice after each city transfer / a notice after the parcel is handed over. Gold: **a notice at every sorting stop**.
- default QA: For an ordinary occasion on October 7, what is the selected parcel progress detail? Options: a notice after each city transfer / a notice at every sorting stop / a notice after the parcel is handed over / a notice when the final journey begins. Gold: **a notice at every sorting stop**.
- neighbor QA: For parcels containing soft furnishings on October 7, what is the selected parcel progress detail? Options: a notice when the final journey begins / a notice after the parcel is handed over / a notice at every sorting stop / a notice after each city transfer. Gold: **a notice at every sorting stop**.

**2027-10-08 · e82348207c298034bfc3d**

- User: Something small: I've been looking again at how much parcel tracking I see.
- Assistant: What's on your mind about it?
- User: One thing about how much parcel tracking I see.  My preference for parcels containing small tools is a notice when the final journey begins. There is no planned end to that choice.
- Gold: exception_revision / resolved; evidence message 3. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"parcel progress detail": {"general": "a notice at every sorting stop", "exceptions": {"adjacent": {"value": "a notice when the final journey begins", "validity": {"kind": "persistent"}}}}}`

**2027-10-09 · e4a0eed6b3d637539429f**

- User: Can I mention something about how much parcel tracking I see? I was thinking of an update once it has been handed over, but it could be for parcels containing small tools or tracking packages of soft furnishings. I’m still deciding.
- Assistant: What's been on your mind about what you actually check in parcel tracking?
- User: I am mostly thinking about how much it breaks my concentration.
- Gold: clarify / clarify; evidence message 1. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"parcel progress detail": {"general": "a notice at every sorting stop", "exceptions": {"adjacent": {"value": "a notice when the final journey begins", "validity": {"kind": "persistent"}}}}}`
- target QA: For parcels containing small tools on October 9, what is the selected parcel progress detail? Options: a notice after each city transfer / a notice at every sorting stop / a notice after the parcel is handed over / a notice when the final journey begins. Gold: **a notice when the final journey begins**.
- default QA: For an ordinary occasion on October 9, what is the selected parcel progress detail? Options: a notice after the parcel is handed over / a notice when the final journey begins / a notice after each city transfer / a notice at every sorting stop. Gold: **a notice at every sorting stop**.
- neighbor QA: For parcels containing soft furnishings on October 9, what is the selected parcel progress detail? Options: a notice after each city transfer / a notice when the final journey begins / a notice at every sorting stop / a notice after the parcel is handed over. Gold: **a notice at every sorting stop**.

**2027-10-11 · e490bfc5692c30f8a0563**

- User: Something small: I've been looking again at how much parcel tracking I see.
- Assistant: Go on; I'm listening.
- User: One thing about how much parcel tracking I see.  About parcels containing small tools: a notice after the parcel is handed over is what I would choose. Carry that forward whenever those occasions come up.
- Assistant: How does sorting useful notices from repeated ones come into it?
- User: I want to be able to tell when I should start looking out for the package.
- Gold: exception_revision / resolved; evidence message 3. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"parcel progress detail": {"general": "a notice at every sorting stop", "exceptions": {"adjacent": {"value": "a notice after the parcel is handed over", "validity": {"kind": "persistent"}}}}}`

**2027-10-12 · e24f9467861f9a33610b9**

- User: Something small: I've been looking again at how much parcel tracking I see.
- Assistant: Say what you were thinking, in your own words.
- User: One thing about how much parcel tracking I see.  Merge parcels containing small tools back into the ordinary case. Future changes to my general choice should apply there as well.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"parcel progress detail": {"general": "a notice at every sorting stop", "exceptions": {}}}`

## Dev

### de-0011 · dev-plant-pot-base-design

Contrast group: `de-pair-0047`

Initial state: `{"plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}, "everyday tote fastening": {"general": "an inset full-width zipper", "exceptions": {"focus": {"value": "a single knotted cord fastening", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a pair of wooden toggle fasteners", "validity": {"kind": "persistent"}}}}}`

**2027-07-07 · e755642a9714b56d20d98**

- User: Do you have a minute to talk about what sits under a plant pot?
- Assistant: Is whether the pot wobbles on the shelf mostly a practical concern?
- User: I am trying not to mark the shelf when I move the pot.
- Assistant: Was there a specific thing about whether the pot wobbles on the shelf you wanted to bring up?
- User: I've given what sits under a plant pot some thought. I am not in a position to specify whether three short integral feet belongs with pots placed on a wooden shelf or with pots placed on a stone shelf.
- Gold: clarify / clarify; evidence message 5. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}, "everyday tote fastening": {"general": "an inset full-width zipper", "exceptions": {"focus": {"value": "a single knotted cord fastening", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a pair of wooden toggle fasteners", "validity": {"kind": "persistent"}}}}}`

**2027-07-09 · e4ef2141c79c67c8dc9f9**

- User: On plant-pot base design, here's what I mean.  I am choosing three short integral feet in relation to putting pots on shelving made of wood. It should remain in force temporarily until I can say when to stop.
- Assistant: How did you come to notice moving the pot without scratching?
- User: I am trying not to mark the shelf when I move the pot.
- Assistant: Is there another side of keeping drips off the wood you want to get into?
- User: Nothing else springs to mind at the moment.
- Gold: scoped_exception / resolved; evidence message 1. The user settles the earlier choice of situation and supplies a continuing instruction for it.
- After: `{"plant-pot base design": {"general": "a removable saucer base", "exceptions": {"adjacent": {"value": "three short integral feet", "validity": {"kind": "open"}}}}, "everyday tote fastening": {"general": "an inset full-width zipper", "exceptions": {"focus": {"value": "a single knotted cord fastening", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a pair of wooden toggle fasteners", "validity": {"kind": "persistent"}}}}}`
- target QA: It is July 9 and the situation is pots placed on a wooden shelf. Which plant-pot base design would fit the preference? Options: a raised ring-shaped foot / a flat cork-backed base / a removable saucer base / three short integral feet. Gold: **three short integral feet**.
- default QA: It is July 9 and the situation is an ordinary occasion. Which plant-pot base design would fit the preference? Options: a flat cork-backed base / a raised ring-shaped foot / three short integral feet / a removable saucer base. Gold: **a removable saucer base**.
- neighbor QA: It is July 9 and the situation is pots placed on a stone shelf. Which plant-pot base design would fit the preference? Options: a raised ring-shaped foot / three short integral feet / a removable saucer base / a flat cork-backed base. Gold: **a removable saucer base**.

**2027-07-10 · e6d9e0e97da54d8024b7a**

- User: Before I get on with things, can I bring up how the everyday tote stays shut?
- Assistant: How would you put it?
- User: I wanted to talk about how the everyday tote stays shut.  I am choosing a single knotted cord fastening in relation to the baseline case. It is a standing preference for each occasion of this sort, not merely for today.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"plant-pot base design": {"general": "a removable saucer base", "exceptions": {"adjacent": {"value": "three short integral feet", "validity": {"kind": "open"}}}}, "everyday tote fastening": {"general": "a single knotted cord fastening", "exceptions": {"focus": {"value": "a single knotted cord fastening", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a pair of wooden toggle fasteners", "validity": {"kind": "persistent"}}}}}`

**2027-07-11 · e01c42cfeb266ee305651**

- User: I wanted to talk about what sits under a plant pot.  My instruction concerning pots placed on a stone shelf is to use a flat cork-backed base. Keep applying it during this temporary period. I do not yet know its final day. Any other preferences should stay in place.
- Assistant: Let's talk about moving the pot without scratching for a moment.
- User: I am trying not to mark the shelf when I move the pot.
- Gold: scoped_exception / resolved; evidence message 1. The user chooses a continuing setting for the named situation.
- After: `{"plant-pot base design": {"general": "a removable saucer base", "exceptions": {"adjacent": {"value": "three short integral feet", "validity": {"kind": "open"}}, "focus": {"value": "a flat cork-backed base", "validity": {"kind": "open"}}}}, "everyday tote fastening": {"general": "a single knotted cord fastening", "exceptions": {"focus": {"value": "a single knotted cord fastening", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a pair of wooden toggle fasteners", "validity": {"kind": "persistent"}}}}}`

**2027-07-12 · ed21366b40a6d87a45d68**

- User: I've given how the everyday tote stays shut some thought. I'm just trying to sort out what's coming up for totes used on quiet outings. How I do it later isn't part of this decision.
- Assistant: Can you tell me what happened with getting into the bag with one hand?
- User: I would rather not have to set the bag down to open it.
- Assistant: What are you leaning towards?
- User: I feel best about a zipper across the opening set down inside.
- Assistant: We can leave getting into the bag with one hand here for the moment.
- User: No, I've settled on it.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"plant-pot base design": {"general": "a removable saucer base", "exceptions": {"adjacent": {"value": "three short integral feet", "validity": {"kind": "open"}}, "focus": {"value": "a flat cork-backed base", "validity": {"kind": "open"}}}}, "everyday tote fastening": {"general": "a single knotted cord fastening", "exceptions": {"focus": {"value": "a single knotted cord fastening", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a pair of wooden toggle fasteners", "validity": {"kind": "persistent"}}}}}`
- target QA: It is July 12 and the situation is totes used on quiet outings. Which everyday tote fastening would fit the preference? Options: an inset full-width zipper / a single knotted cord fastening / a broad magnetic foldover flap / a pair of wooden toggle fasteners. Gold: **a pair of wooden toggle fasteners**.
- default QA: It is July 12 and the situation is an ordinary occasion. Which everyday tote fastening would fit the preference? Options: an inset full-width zipper / a broad magnetic foldover flap / a single knotted cord fastening / a pair of wooden toggle fasteners. Gold: **a single knotted cord fastening**.
- neighbor QA: It is July 12 and the situation is totes used on crowded outings. Which everyday tote fastening would fit the preference? Options: a pair of wooden toggle fasteners / a single knotted cord fastening / an inset full-width zipper / a broad magnetic foldover flap. Gold: **a single knotted cord fastening**.

### de-0067 · dev-saved-search-alert-grouping

Contrast group: `de-pair-0033`

Initial state: `{"saved-search alert grouping": {"general": "one alert per matching item", "exceptions": {}}}`

**2027-08-05 · e41e47928c97e7a58189c**

- User: On how the saved queries notify me, here's what I mean.  Could you save five search hits in each bundle as my selection for ordinary situations in general? I am asking for an ongoing arrangement without a fixed finish.
- Assistant: How did you come to notice how often the saved search interrupts?
- User: The results are more useful when I can see how they are related.
- Assistant: Does that cover the part about keeping results from the same source together you meant to raise?
- User: Yes, at least the part I wanted to get across today.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"saved-search alert grouping": {"general": "matches collected in groups of five", "exceptions": {}}}`

**2027-08-07 · eec298ab306d64f25758d**

- User: One thing I wanted to mention is how the saved queries notify me.
- Assistant: Was there a specific thing about how often the saved search interrupts you wanted to bring up?
- User: I wanted to talk about how the saved queries notify me.  Please do not infer a target for a separate ping for every match. I am still choosing between a saved query with multiple search words and saved searches with a single keyword.
- Assistant: Can you tell me what happened with how often the saved search interrupts?
- User: I cannot stop for every single change.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"saved-search alert grouping": {"general": "matches collected in groups of five", "exceptions": {}}}`
- target QA: It is August 7 and the situation is saved searches with several keywords. Which saved-search alert grouping would fit the preference? Options: one alert per matching item / matches grouped by the source that posted them / matches collected in groups of five / matches bundled into pairs. Gold: **matches collected in groups of five**.
- default QA: It is August 7 and the situation is an ordinary occasion. Which saved-search alert grouping would fit the preference? Options: matches grouped by the source that posted them / matches bundled into pairs / matches collected in groups of five / one alert per matching item. Gold: **matches collected in groups of five**.
- neighbor QA: It is August 7 and the situation is saved searches with a single keyword. Which saved-search alert grouping would fit the preference? Options: matches grouped by the source that posted them / matches bundled into pairs / matches collected in groups of five / one alert per matching item. Gold: **matches collected in groups of five**.

**2027-08-09 · e843747cdb67d6cf8dee6**

- User: One thing I wanted to mention is how the saved queries notify me.
- Assistant: I'm here. Tell me anything that seems relevant.
- User: I wanted to talk about saved-search alert grouping.  What I am requesting for a saved query with multiple search words is a separate ping for every match. Please carry this preference into future occasions too.
- Gold: scoped_exception / resolved; evidence message 3. The user settles the earlier choice of situation and supplies a continuing instruction for it.
- After: `{"saved-search alert grouping": {"general": "matches collected in groups of five", "exceptions": {"adjacent": {"value": "one alert per matching item", "validity": {"kind": "persistent"}}}}}`

**2027-08-10 · e9863f38f459ba1f41601**

- User: I've given how the saved queries notify me some thought. For a saved query with multiple search words, I'm deciding what to do this time alone.
- Assistant: Does the way you feel about seeing several results at once explain part of this?
- User: The results are more useful when I can see how they are related.
- Assistant: What do you think you'd pick?
- User: My pick would be matches grouped by the source that posted them.
- Assistant: Is there more you wanted to think through around seeing several results at once?
- User: I think that's as far as I need to go today.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"saved-search alert grouping": {"general": "matches collected in groups of five", "exceptions": {"adjacent": {"value": "one alert per matching item", "validity": {"kind": "persistent"}}}}}`
- target QA: It is August 10 and the situation is saved searches with several keywords. Which saved-search alert grouping would fit the preference? Options: one alert per matching item / matches bundled into pairs / matches collected in groups of five / matches grouped by the source that posted them. Gold: **one alert per matching item**.
- default QA: It is August 10 and the situation is an ordinary occasion. Which saved-search alert grouping would fit the preference? Options: matches bundled into pairs / matches grouped by the source that posted them / matches collected in groups of five / one alert per matching item. Gold: **matches collected in groups of five**.
- neighbor QA: It is August 10 and the situation is saved searches with a single keyword. Which saved-search alert grouping would fit the preference? Options: one alert per matching item / matches grouped by the source that posted them / matches collected in groups of five / matches bundled into pairs. Gold: **matches collected in groups of five**.

### de-0041 · dev-warmup-stepping-pattern

Contrast group: `de-pair-0040`

Initial state: `{"warmup stepping pattern": {"general": "gentle side steps with a pause", "exceptions": {"adjacent": {"value": "small diagonal steps in place", "validity": {"kind": "persistent"}}, "focus": {"value": "alternating forward toe taps", "validity": {"kind": "open"}}}}}`

**2027-02-08 · ed967fb8367b52c62fda6**

- User: One thing I wanted to mention is how I put my feet down to warm up.
- Assistant: I'm here. Tell me anything that seems relevant.
- User: I've given how I put my feet down to warm up some thought. Hypothetically, I could ask, "What I am requesting for warming up somewhere with room to move is slow backward steps and returns. There is no expiration intended for this arrangement." Please treat it as discussion rather than an actual choice.
- Gold: stable_preference / resolved; evidence message 3. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"warmup stepping pattern": {"general": "gentle side steps with a pause", "exceptions": {"adjacent": {"value": "small diagonal steps in place", "validity": {"kind": "persistent"}}, "focus": {"value": "alternating forward toe taps", "validity": {"kind": "open"}}}}}`

**2027-02-09 · e4b0351be7e7587c802f6**

- User: I've given how I put my feet down to warm up some thought. For easy steps backward and then forward again, two possible contexts remain on the table: warming up somewhere with room to move and warmups done in a narrow space. Neither is selected yet.
- Assistant: What made staying balanced when you step back stand out this time?
- User: It makes a difference when I am a few moves in.
- Assistant: Is there another side of staying balanced when you step back you want to get into?
- User: Nothing else springs to mind at the moment.
- Gold: clarify / clarify; evidence message 1. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"warmup stepping pattern": {"general": "gentle side steps with a pause", "exceptions": {"adjacent": {"value": "small diagonal steps in place", "validity": {"kind": "persistent"}}, "focus": {"value": "alternating forward toe taps", "validity": {"kind": "open"}}}}}`

**2027-02-10 · e768136d0d47181625835**

- User: I was mulling over how I put my feet down to warm up the other day.
- Assistant: Go ahead and say what you're considering.
- User: There's something I'd like to bring up about how I put my feet down to warm up.  I want to discontinue that individual arrangement for warming up in a cramped area, not replace it with another separate choice.
- Assistant: Does this have much to do with staying balanced when you step back?
- User: It makes a difference when I am a few moves in.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"warmup stepping pattern": {"general": "gentle side steps with a pause", "exceptions": {"adjacent": {"value": "small diagonal steps in place", "validity": {"kind": "persistent"}}}}}`

**2027-02-11 · ed5118986d53eb9fb44bc**

- User: There's something I'd like to bring up about how I put my feet down to warm up.  I am choosing alternating forward toe taps in relation to routine cases with no dedicated instruction. It is a standing preference for each occasion of this sort, not merely for today.
- Assistant: How important is getting the feet warm in a small space in practice?
- User: I want something that feels comfortable while I move.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"warmup stepping pattern": {"general": "alternating forward toe taps", "exceptions": {"adjacent": {"value": "small diagonal steps in place", "validity": {"kind": "persistent"}}}}}`

**2027-02-13 · e1a27247cbaa3f94d42e8**

- User: There's something I'd like to bring up about how I put my feet down to warm up.  Please take easy steps backward and then forward again as my preference in connection with warmups done in a wide space. This should not be treated as a temporary experiment.
- Assistant: Have you run into trouble with getting the feet warm in a small space?
- User: I need to warm up without taking more floor space than I have.
- Assistant: We don’t have to get into all of the pace in the first few movements in one go.
- User: That’s fine. I didn’t have any other details in mind.
- Gold: exception_revision / resolved; evidence message 1. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"warmup stepping pattern": {"general": "alternating forward toe taps", "exceptions": {"adjacent": {"value": "slow backward steps and returns", "validity": {"kind": "persistent"}}}}}`

**2027-02-15 · e649054612550c9329c6d**

- User: I was mulling over how I put my feet down to warm up the other day.
- Assistant: I'm here. Tell me anything that seems relevant.
- User: On how I put my feet down to warm up, here's what I mean.  In the case of warmups done in a narrow space, easy steps backward and then forward again would be my choice. Use this until the end of March 1, having begun on February 15; outside that span, use my normal preference. Any other preferences should stay in place.
- Assistant: Can you tell me what happened with the pace in the first few movements?
- User: I need to warm up without taking more floor space than I have.
- Gold: scoped_exception / resolved; evidence message 3. The user chooses a continuing setting for the named situation.
- After: `{"warmup stepping pattern": {"general": "alternating forward toe taps", "exceptions": {"adjacent": {"value": "slow backward steps and returns", "validity": {"kind": "persistent"}}, "focus": {"value": "slow backward steps and returns", "validity": {"kind": "window", "from": "2027-02-15", "to": "2027-03-01"}}}}}`
- target QA: It is February 15 and the situation is warmups done in a narrow space. Which warmup stepping pattern would fit the preference? Options: slow backward steps and returns / alternating forward toe taps / small diagonal steps in place / gentle side steps with a pause. Gold: **slow backward steps and returns**.
- default QA: It is February 15 and the situation is an ordinary occasion. Which warmup stepping pattern would fit the preference? Options: small diagonal steps in place / slow backward steps and returns / gentle side steps with a pause / alternating forward toe taps. Gold: **alternating forward toe taps**.
- neighbor QA: It is February 15 and the situation is warmups done in a wide space. Which warmup stepping pattern would fit the preference? Options: gentle side steps with a pause / alternating forward toe taps / slow backward steps and returns / small diagonal steps in place. Gold: **slow backward steps and returns**.
- target QA: It is March 1 and the situation is warmups done in a narrow space. Which warmup stepping pattern would fit the preference? Options: small diagonal steps in place / slow backward steps and returns / alternating forward toe taps / gentle side steps with a pause. Gold: **slow backward steps and returns**.
- boundary QA: It is March 2 and the situation is warmups done in a narrow space. Which warmup stepping pattern would fit the preference? Options: slow backward steps and returns / small diagonal steps in place / alternating forward toe taps / gentle side steps with a pause. Gold: **alternating forward toe taps**.

**2027-02-16 · e3de91d320913c60746d1**

- User: I've given how I put my feet down to warm up some thought. I'd like to decide on warming up in a cramped area for the immediate request, not make a rule for myself.
- Assistant: Does the way you feel about getting the feet warm in a small space explain part of this?
- User: It makes a difference when I am a few moves in.
- Assistant: Which option do you feel happy with?
- User: I feel best about short diagonal steps on the spot.
- Assistant: We can leave getting the feet warm in a small space here for the moment.
- User: I think that's as far as I need to go today.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"warmup stepping pattern": {"general": "alternating forward toe taps", "exceptions": {"adjacent": {"value": "slow backward steps and returns", "validity": {"kind": "persistent"}}, "focus": {"value": "slow backward steps and returns", "validity": {"kind": "window", "from": "2027-02-15", "to": "2027-03-01"}}}}}`
- target QA: It is February 16 and the situation is warmups done in a narrow space. Which warmup stepping pattern would fit the preference? Options: slow backward steps and returns / alternating forward toe taps / gentle side steps with a pause / small diagonal steps in place. Gold: **slow backward steps and returns**.
- default QA: It is February 16 and the situation is an ordinary occasion. Which warmup stepping pattern would fit the preference? Options: small diagonal steps in place / gentle side steps with a pause / alternating forward toe taps / slow backward steps and returns. Gold: **alternating forward toe taps**.
- neighbor QA: It is February 16 and the situation is warmups done in a wide space. Which warmup stepping pattern would fit the preference? Options: slow backward steps and returns / alternating forward toe taps / small diagonal steps in place / gentle side steps with a pause. Gold: **slow backward steps and returns**.

### de-0087 · dev-market-bag-handle-construction

Contrast group: `de-pair-0039`

Initial state: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {}}, "plant-pot base design": {"general": "three short integral feet", "exceptions": {}}}`

**2027-07-03 · e627cb16041723081a8a7**

- User: There's something I'd like to bring up about plant-pot base design.  Let a saucer that can be taken off be the choice used for my overall preference outside separate arrangements. This should not be treated as a temporary experiment.
- Assistant: Does this have much to do with keeping drips off the wood?
- User: I am trying not to mark the shelf when I move the pot.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`

**2027-07-05 · e30718d305c2ef02ac414**

- User: I've been going back and forth on the handles on the market bag.
- Assistant: What have you been thinking?
- User: I've given the handles on the market bag some thought. I have reached a decision about carrying the bag in the crook of my arm: wide rolled cloth handles. There is no expiration intended for this arrangement.
- Assistant: Do you see keeping the bag from digging into an arm as a big part of it?
- User: I notice the handle when the bag gets heavy.
- Gold: scoped_exception / resolved; evidence message 3. The user chooses a continuing setting for the named situation.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"focus": {"value": "wide rolled cloth handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`

**2027-07-06 · e13ae114d5540e592ac41**

- User: I keep coming back to the handles on the market bag when I think about having a decent grip when it is full.
- Assistant: How would you put it?
- User: I wanted to talk about the handles on the market bag.  I am asking you to remember flat handles in reinforced webbing for carrying the bag by hand. I intend this to continue as the normal choice here rather than end after one occasion.
- Assistant: Do you see having a decent grip when it is full as a big part of it?
- User: I notice the handle when the bag gets heavy.
- Gold: scoped_exception / resolved; evidence message 3. The user chooses a continuing setting for the named situation.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"focus": {"value": "wide rolled cloth handles", "validity": {"kind": "persistent"}}, "adjacent": {"value": "flat reinforced webbing handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`
- target QA: It is July 6 and the situation is bags carried in my hand. Which market bag handle construction would fit the preference? Options: flat reinforced webbing handles / wide rolled cloth handles / rounded hollow rope handles / soft padded loop handles. Gold: **flat reinforced webbing handles**.
- default QA: It is July 6 and the situation is an ordinary occasion. Which market bag handle construction would fit the preference? Options: soft padded loop handles / rounded hollow rope handles / flat reinforced webbing handles / wide rolled cloth handles. Gold: **rounded hollow rope handles**.
- neighbor QA: It is July 6 and the situation is bags carried over my forearm. Which market bag handle construction would fit the preference? Options: wide rolled cloth handles / rounded hollow rope handles / soft padded loop handles / flat reinforced webbing handles. Gold: **wide rolled cloth handles**.

**2027-07-07 · eaa64112758e9935e4e25**

- User: One thing I wanted to mention is the handles on the market bag.
- Assistant: Sure, we can take a moment for keeping the bag from digging into an arm.
- User: There's something I'd like to bring up about the handles on the market bag.  There should be no distinction for carrying the bag in the crook of my arm anymore. Apply the general preference whenever those occasions arise.
- Assistant: Does the way you feel about keeping the bag from digging into an arm explain part of this?
- User: I notice the handle when the bag gets heavy.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"adjacent": {"value": "flat reinforced webbing handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`
- target QA: It is July 7 and the situation is bags carried over my forearm. Which market bag handle construction would fit the preference? Options: flat reinforced webbing handles / soft padded loop handles / wide rolled cloth handles / rounded hollow rope handles. Gold: **rounded hollow rope handles**.
- default QA: It is July 7 and the situation is an ordinary occasion. Which market bag handle construction would fit the preference? Options: flat reinforced webbing handles / rounded hollow rope handles / wide rolled cloth handles / soft padded loop handles. Gold: **rounded hollow rope handles**.
- neighbor QA: It is July 7 and the situation is bags carried in my hand. Which market bag handle construction would fit the preference? Options: rounded hollow rope handles / wide rolled cloth handles / flat reinforced webbing handles / soft padded loop handles. Gold: **flat reinforced webbing handles**.

**2027-07-08 · eaa0025a18502135484e6**

- User: On the handles on the market bag, here's what I mean.  Let soft cushioned handles in loops be the choice used for bags carried in my hand. Please carry this preference into future occasions too.
- Assistant: Do you have a concern about having a decent grip when it is full?
- User: I notice the handle when the bag gets heavy.
- Gold: exception_revision / resolved; evidence message 1. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"adjacent": {"value": "soft padded loop handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`

**2027-07-09 · e0c5daa6aa265e9fea95f**

- User: On what sits under a plant pot, here's what I mean.  I can name a raised ring-shaped foot as a possibility, but not yet which situation: pots placed on a wooden shelf or pots placed on a stone shelf.
- Assistant: It sounds worth discussing whether the pot wobbles on the shelf.
- User: I am trying not to mark the shelf when I move the pot.
- Assistant: We don’t have to get into all of moving the pot without scratching in one go.
- User: That’s fine. I didn’t have any other details in mind.
- Gold: clarify / clarify; evidence message 1. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"adjacent": {"value": "soft padded loop handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`

**2027-07-10 · e0d0f03662abe4f9eee4f**

- User: On what sits under a plant pot, here's what I mean.  This question is about one upcoming occasion for pots placed on a stone shelf; I'm not choosing a pattern.
- Assistant: Do you have a concern about whether the pot wobbles on the shelf?
- User: I am trying not to mark the shelf when I move the pot.
- Assistant: What do you think you'd pick?
- User: I feel best about three short integral feet.
- Assistant: We can leave whether the pot wobbles on the shelf here for the moment.
- User: I think that's as far as I need to go today.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"adjacent": {"value": "soft padded loop handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`
- target QA: It is July 10 and the situation is pots placed on a stone shelf. Which plant-pot base design would fit the preference? Options: a removable saucer base / a flat cork-backed base / a raised ring-shaped foot / three short integral feet. Gold: **a removable saucer base**.
- default QA: It is July 10 and the situation is an ordinary occasion. Which plant-pot base design would fit the preference? Options: a raised ring-shaped foot / three short integral feet / a flat cork-backed base / a removable saucer base. Gold: **a removable saucer base**.
- neighbor QA: It is July 10 and the situation is pots placed on a wooden shelf. Which plant-pot base design would fit the preference? Options: a flat cork-backed base / a removable saucer base / a raised ring-shaped foot / three short integral feet. Gold: **a removable saucer base**.

### de-0079 · dev-mouse-wheel-scroll-mapping

Contrast group: `de-pair-0003`

Initial state: `{"mouse wheel scroll mapping": {"general": "wheel movement stepping between paragraphs", "exceptions": {"focus": {"value": "wheel movement jumping by screenfuls", "validity": {"kind": "persistent"}}, "adjacent": {"value": "wheel movement opposite to page travel", "validity": {"kind": "persistent"}}}}}`

**2027-06-04 · ea3f9df9940a7ac6945f5**

- User: Before I get on with things, can I bring up what rolling the mouse wheel does?
- Assistant: What's the experience been like with getting the wheel to match your hand?
- User: It throws me off when the page jumps more than I expect.
- Assistant: I'm here. Tell me anything that seems relevant.
- User: On what rolling the mouse wheel does, here's what I mean.  My thought about jump a screen at a time is incomplete: I cannot yet distinguish whether I mean using the wheel right-handed or using the wheel left-handed.
- Gold: clarify / clarify; evidence message 5. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"mouse wheel scroll mapping": {"general": "wheel movement stepping between paragraphs", "exceptions": {"focus": {"value": "wheel movement jumping by screenfuls", "validity": {"kind": "persistent"}}, "adjacent": {"value": "wheel movement opposite to page travel", "validity": {"kind": "persistent"}}}}}`

**2027-06-05 · e1572fc34a254e4010aee**

- User: Before I get on with things, can I bring up what rolling the mouse wheel does?
- Assistant: What did you want to mention?
- User: I wanted to talk about what rolling the mouse wheel does.  I am choosing wheel movement matched to page travel in relation to using the wheel left-handed. I want this to hold whenever the situation recurs.
- Assistant: Would you mind saying a bit more about what happens on a long page?
- User: It throws me off when the page jumps more than I expect.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"mouse wheel scroll mapping": {"general": "wheel movement stepping between paragraphs", "exceptions": {"focus": {"value": "wheel movement matched to page travel", "validity": {"kind": "persistent"}}, "adjacent": {"value": "wheel movement opposite to page travel", "validity": {"kind": "persistent"}}}}}`
- target QA: It is June 5 and the situation is scrolling with the left hand. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement opposite to page travel / wheel movement matched to page travel / wheel movement stepping between paragraphs / wheel movement jumping by screenfuls. Gold: **wheel movement matched to page travel**.
- default QA: It is June 5 and the situation is an ordinary occasion. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement stepping between paragraphs / wheel movement jumping by screenfuls / wheel movement opposite to page travel / wheel movement matched to page travel. Gold: **wheel movement stepping between paragraphs**.
- neighbor QA: It is June 5 and the situation is scrolling with the right hand. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement jumping by screenfuls / wheel movement opposite to page travel / wheel movement stepping between paragraphs / wheel movement matched to page travel. Gold: **wheel movement opposite to page travel**.

**2027-06-06 · e12364c058703c2cb55d3**

- User: One thing I wanted to mention is what rolling the mouse wheel does.
- Assistant: Sure, we can take a moment for what happens on a long page.
- User: There's something I'd like to bring up about what rolling the mouse wheel does.  The arrangement I am asking for is wheel movement jumping by screenfuls, for scrolling with the left hand. I want this to hold whenever the situation recurs.
- Assistant: Do you see what happens on a long page as a big part of it?
- User: It throws me off when the page jumps more than I expect.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"mouse wheel scroll mapping": {"general": "wheel movement stepping between paragraphs", "exceptions": {"focus": {"value": "wheel movement jumping by screenfuls", "validity": {"kind": "persistent"}}, "adjacent": {"value": "wheel movement opposite to page travel", "validity": {"kind": "persistent"}}}}}`
- target QA: It is June 6 and the situation is scrolling with the left hand. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement matched to page travel / wheel movement jumping by screenfuls / wheel movement opposite to page travel / wheel movement stepping between paragraphs. Gold: **wheel movement jumping by screenfuls**.
- default QA: It is June 6 and the situation is an ordinary occasion. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement stepping between paragraphs / wheel movement opposite to page travel / wheel movement jumping by screenfuls / wheel movement matched to page travel. Gold: **wheel movement stepping between paragraphs**.
- neighbor QA: It is June 6 and the situation is scrolling with the right hand. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement matched to page travel / wheel movement opposite to page travel / wheel movement jumping by screenfuls / wheel movement stepping between paragraphs. Gold: **wheel movement opposite to page travel**.

**2027-06-08 · e9eb5fb200fe7b8f8d0a2**

- User: I've given what rolling the mouse wheel does some thought. My instruction concerning using the wheel right-handed is to use wheel movement jumping by screenfuls. This is always my choice in that situation, not a one-off. Any other preferences should stay in place.
- Assistant: How important is what happens on a long page in practice?
- User: It throws me off when the page jumps more than I expect.
- Assistant: We don’t have to get into all of seeing where the next paragraph starts in one go.
- User: That’s fine. I didn’t have any other details in mind.
- Gold: exception_revision / resolved; evidence message 1. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"mouse wheel scroll mapping": {"general": "wheel movement stepping between paragraphs", "exceptions": {"focus": {"value": "wheel movement jumping by screenfuls", "validity": {"kind": "persistent"}}, "adjacent": {"value": "wheel movement jumping by screenfuls", "validity": {"kind": "persistent"}}}}}`
- target QA: It is June 8 and the situation is scrolling with the right hand. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement stepping between paragraphs / wheel movement opposite to page travel / wheel movement jumping by screenfuls / wheel movement matched to page travel. Gold: **wheel movement jumping by screenfuls**.
- default QA: It is June 8 and the situation is an ordinary occasion. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement stepping between paragraphs / wheel movement matched to page travel / wheel movement opposite to page travel / wheel movement jumping by screenfuls. Gold: **wheel movement stepping between paragraphs**.
- neighbor QA: It is June 8 and the situation is scrolling with the left hand. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement matched to page travel / wheel movement stepping between paragraphs / wheel movement jumping by screenfuls / wheel movement opposite to page travel. Gold: **wheel movement jumping by screenfuls**.

**2027-06-10 · e1972dfa41c3f9d9ba2ff**

- User: There's something I'd like to bring up about what rolling the mouse wheel does.  For scrolling with the left hand, I'd like to make a choice that still applies on later occasions.
- Assistant: Have you run into trouble with what happens on a long page?
- User: It throws me off when the page jumps more than I expect.
- Assistant: What are you leaning towards?
- User: I feel best about scroll opposite the wheel's motion.
- Assistant: We can leave what happens on a long page here for the moment.
- User: I think that's as far as I need to go today.
- Gold: exception_revision / resolved; evidence message 5. The user chooses a continuing replacement for the existing situation rule.
- After: `{"mouse wheel scroll mapping": {"general": "wheel movement stepping between paragraphs", "exceptions": {"focus": {"value": "wheel movement opposite to page travel", "validity": {"kind": "persistent"}}, "adjacent": {"value": "wheel movement jumping by screenfuls", "validity": {"kind": "persistent"}}}}}`
- target QA: It is June 10 and the situation is scrolling with the left hand. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement matched to page travel / wheel movement stepping between paragraphs / wheel movement jumping by screenfuls / wheel movement opposite to page travel. Gold: **wheel movement opposite to page travel**.
- default QA: It is June 10 and the situation is an ordinary occasion. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement stepping between paragraphs / wheel movement opposite to page travel / wheel movement matched to page travel / wheel movement jumping by screenfuls. Gold: **wheel movement stepping between paragraphs**.
- neighbor QA: It is June 10 and the situation is scrolling with the right hand. Which mouse wheel scroll mapping would fit the preference? Options: wheel movement opposite to page travel / wheel movement jumping by screenfuls / wheel movement matched to page travel / wheel movement stepping between paragraphs. Gold: **wheel movement jumping by screenfuls**.

### de-0045 · dev-market-bag-handle-construction

Contrast group: `de-pair-0039`

Initial state: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {}}, "plant-pot base design": {"general": "three short integral feet", "exceptions": {}}}`

**2027-07-03 · e4ecda62303bf1d8937c9**

- User: There's something I'd like to bring up about plant-pot base design.  Let a saucer that can be taken off be the choice used for my overall preference outside separate arrangements. This should not be treated as a temporary experiment.
- Assistant: Does this have much to do with keeping drips off the wood?
- User: I am trying not to mark the shelf when I move the pot.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`

**2027-07-05 · e2fb824fe21164997f557**

- User: I've been going back and forth on the handles on the market bag.
- Assistant: What have you been thinking?
- User: I've given the handles on the market bag some thought. I have reached a decision about carrying the bag in the crook of my arm: wide rolled cloth handles. There is no expiration intended for this arrangement.
- Assistant: Do you see keeping the bag from digging into an arm as a big part of it?
- User: I notice the handle when the bag gets heavy.
- Gold: scoped_exception / resolved; evidence message 3. The user chooses a continuing setting for the named situation.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"focus": {"value": "wide rolled cloth handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`

**2027-07-06 · e0323df4b8a0df1e3d5eb**

- User: I keep coming back to the handles on the market bag when I think about having a decent grip when it is full.
- Assistant: How would you put it?
- User: I wanted to talk about the handles on the market bag.  I am asking you to remember flat handles in reinforced webbing for carrying the bag by hand. I intend this to continue as the normal choice here rather than end after one occasion.
- Assistant: Do you see having a decent grip when it is full as a big part of it?
- User: I notice the handle when the bag gets heavy.
- Gold: scoped_exception / resolved; evidence message 3. The user chooses a continuing setting for the named situation.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"focus": {"value": "wide rolled cloth handles", "validity": {"kind": "persistent"}}, "adjacent": {"value": "flat reinforced webbing handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`
- target QA: It is July 6 and the situation is bags carried in my hand. Which market bag handle construction would fit the preference? Options: flat reinforced webbing handles / wide rolled cloth handles / rounded hollow rope handles / soft padded loop handles. Gold: **flat reinforced webbing handles**.
- default QA: It is July 6 and the situation is an ordinary occasion. Which market bag handle construction would fit the preference? Options: soft padded loop handles / rounded hollow rope handles / flat reinforced webbing handles / wide rolled cloth handles. Gold: **rounded hollow rope handles**.
- neighbor QA: It is July 6 and the situation is bags carried over my forearm. Which market bag handle construction would fit the preference? Options: wide rolled cloth handles / rounded hollow rope handles / soft padded loop handles / flat reinforced webbing handles. Gold: **wide rolled cloth handles**.

**2027-07-07 · e58e83bbcdcdb9ce21114**

- User: One thing I wanted to mention is the handles on the market bag.
- Assistant: Sure, we can take a moment for keeping the bag from digging into an arm.
- User: There's something I'd like to bring up about the handles on the market bag.  There should be no distinction for carrying the bag in the crook of my arm anymore. Apply the general preference whenever those occasions arise.
- Assistant: Does the way you feel about keeping the bag from digging into an arm explain part of this?
- User: I notice the handle when the bag gets heavy.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"adjacent": {"value": "flat reinforced webbing handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`
- target QA: It is July 7 and the situation is bags carried over my forearm. Which market bag handle construction would fit the preference? Options: flat reinforced webbing handles / soft padded loop handles / wide rolled cloth handles / rounded hollow rope handles. Gold: **rounded hollow rope handles**.
- default QA: It is July 7 and the situation is an ordinary occasion. Which market bag handle construction would fit the preference? Options: flat reinforced webbing handles / rounded hollow rope handles / wide rolled cloth handles / soft padded loop handles. Gold: **rounded hollow rope handles**.
- neighbor QA: It is July 7 and the situation is bags carried in my hand. Which market bag handle construction would fit the preference? Options: rounded hollow rope handles / wide rolled cloth handles / flat reinforced webbing handles / soft padded loop handles. Gold: **flat reinforced webbing handles**.

**2027-07-08 · e959a1bc9cdbff736dd13**

- User: On the handles on the market bag, here's what I mean.  Let soft cushioned handles in loops be the choice used for bags carried in my hand. Please carry this preference into future occasions too.
- Assistant: Do you have a concern about having a decent grip when it is full?
- User: I notice the handle when the bag gets heavy.
- Gold: exception_revision / resolved; evidence message 1. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"adjacent": {"value": "soft padded loop handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`

**2027-07-09 · e171aeb7cda2e05613ae0**

- User: On what sits under a plant pot, here's what I mean.  I can name a raised ring-shaped foot as a possibility, but not yet which situation: pots placed on a wooden shelf or pots placed on a stone shelf.
- Assistant: It sounds worth discussing whether the pot wobbles on the shelf.
- User: I am trying not to mark the shelf when I move the pot.
- Assistant: We don’t have to get into all of moving the pot without scratching in one go.
- User: That’s fine. I didn’t have any other details in mind.
- Gold: clarify / clarify; evidence message 1. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"adjacent": {"value": "soft padded loop handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {}}}`

**2027-07-10 · e2d9ca17833b14575bc78**

- User: On what sits under a plant pot, here's what I mean.  I'm looking to settle what I'll use whenever it is a matter of pots placed on a stone shelf.
- Assistant: Do you have a concern about whether the pot wobbles on the shelf?
- User: I am trying not to mark the shelf when I move the pot.
- Assistant: What do you think you'd pick?
- User: I feel best about three short integral feet.
- Assistant: We can leave whether the pot wobbles on the shelf here for the moment.
- User: I think that's as far as I need to go today.
- Gold: scoped_exception / resolved; evidence message 5. The user chooses a continuing setting for the named situation.
- After: `{"market bag handle construction": {"general": "rounded hollow rope handles", "exceptions": {"adjacent": {"value": "soft padded loop handles", "validity": {"kind": "persistent"}}}}, "plant-pot base design": {"general": "a removable saucer base", "exceptions": {"focus": {"value": "three short integral feet", "validity": {"kind": "persistent"}}}}}`
- target QA: It is July 10 and the situation is pots placed on a stone shelf. Which plant-pot base design would fit the preference? Options: a removable saucer base / a flat cork-backed base / a raised ring-shaped foot / three short integral feet. Gold: **three short integral feet**.
- default QA: It is July 10 and the situation is an ordinary occasion. Which plant-pot base design would fit the preference? Options: a raised ring-shaped foot / three short integral feet / a flat cork-backed base / a removable saucer base. Gold: **a removable saucer base**.
- neighbor QA: It is July 10 and the situation is pots placed on a wooden shelf. Which plant-pot base design would fit the preference? Options: a flat cork-backed base / a removable saucer base / a raised ring-shaped foot / three short integral feet. Gold: **a removable saucer base**.

### de-0008 · dev-saved-search-alert-grouping

Contrast group: `de-pair-0005`

Initial state: `{"saved-search alert grouping": {"general": "matches collected in groups of five", "exceptions": {"adjacent": {"value": "matches bundled into pairs", "validity": {"kind": "open"}}}}}`

**2027-06-02 · ebc1c1a2fe6211350d6fd**

- User: There's something I'd like to bring up about how the saved queries notify me.  I want a saved query with multiple search words included in the ordinary case, both now and on subsequent occasions.
- Assistant: Would you mind saying a bit more about seeing several results at once?
- User: The results are more useful when I can see how they are related.
- Gold: exception_retirement / resolved; evidence message 1. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"saved-search alert grouping": {"general": "matches collected in groups of five", "exceptions": {}}}`
- target QA: It is June 2 and the situation is saved searches with several keywords. Which saved-search alert grouping would fit the preference? Options: one alert per matching item / matches grouped by the source that posted them / matches collected in groups of five / matches bundled into pairs. Gold: **matches collected in groups of five**.
- default QA: It is June 2 and the situation is an ordinary occasion. Which saved-search alert grouping would fit the preference? Options: one alert per matching item / matches collected in groups of five / matches grouped by the source that posted them / matches bundled into pairs. Gold: **matches collected in groups of five**.
- neighbor QA: It is June 2 and the situation is saved searches with a single keyword. Which saved-search alert grouping would fit the preference? Options: matches bundled into pairs / matches collected in groups of five / one alert per matching item / matches grouped by the source that posted them. Gold: **matches collected in groups of five**.

**2027-06-03 · e5200cd36517f248c73d9**

- User: Before I get on with things, can I bring up how the saved queries notify me?
- Assistant: What did you want to mention?
- User: I wanted to talk about how the saved queries notify me.  I can name a separate ping for every match as a possibility, but not yet which situation: a saved query with one search word or saved searches with several keywords.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"saved-search alert grouping": {"general": "matches collected in groups of five", "exceptions": {}}}`

**2027-06-04 · e60db0b518d62ef7138cb**

- User: I've given how the saved queries notify me some thought. I would select one alert per matching item in situations described as a saved query with one search word. Only the inclusive span June 4 to June 24 is covered by this temporary request.
- Assistant: What made keeping results from the same source together stand out this time?
- User: The results are more useful when I can see how they are related.
- Assistant: Does that cover the part about keeping results from the same source together you meant to raise?
- User: Yes, at least the part I wanted to get across today.
- Gold: scoped_exception / resolved; evidence message 1. The user settles the earlier choice of situation and supplies a continuing instruction for it.
- After: `{"saved-search alert grouping": {"general": "matches collected in groups of five", "exceptions": {"focus": {"value": "one alert per matching item", "validity": {"kind": "window", "from": "2027-06-04", "to": "2027-06-24"}}}}}`
- target QA: It is June 4 and the situation is saved searches with a single keyword. Which saved-search alert grouping would fit the preference? Options: one alert per matching item / matches collected in groups of five / matches grouped by the source that posted them / matches bundled into pairs. Gold: **one alert per matching item**.
- default QA: It is June 4 and the situation is an ordinary occasion. Which saved-search alert grouping would fit the preference? Options: one alert per matching item / matches collected in groups of five / matches bundled into pairs / matches grouped by the source that posted them. Gold: **matches collected in groups of five**.
- neighbor QA: It is June 4 and the situation is saved searches with several keywords. Which saved-search alert grouping would fit the preference? Options: matches bundled into pairs / matches grouped by the source that posted them / one alert per matching item / matches collected in groups of five. Gold: **matches collected in groups of five**.
- target QA: It is June 24 and the situation is saved searches with a single keyword. Which saved-search alert grouping would fit the preference? Options: one alert per matching item / matches bundled into pairs / matches collected in groups of five / matches grouped by the source that posted them. Gold: **one alert per matching item**.
- boundary QA: It is June 25 and the situation is saved searches with a single keyword. Which saved-search alert grouping would fit the preference? Options: one alert per matching item / matches collected in groups of five / matches grouped by the source that posted them / matches bundled into pairs. Gold: **matches collected in groups of five**.

**2027-06-05 · e152803967c20d4b5b0f8**

- User: I've been going back and forth on how the saved queries notify me.
- Assistant: Go ahead and say what you're considering.
- User: I've given how the saved queries notify me some thought. My instruction concerning requests that don't need a separate choice is to use a separate ping for every match. This is always my choice in that situation, not a one-off.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"saved-search alert grouping": {"general": "one alert per matching item", "exceptions": {"focus": {"value": "one alert per matching item", "validity": {"kind": "window", "from": "2027-06-04", "to": "2027-06-24"}}}}}`

**2027-06-06 · e136e43ac6823210d9c26**

- User: I keep coming back to how the saved queries notify me when I think about how often the saved search interrupts.
- Assistant: What did you want to mention?
- User: On how the saved queries notify me, here's what I mean.  For a thought exercise, the request could be, "Please take matches grouped by the source that posted them as my preference in connection with a saved query with multiple search words. Take June 6 as the first covered date and June 20 as the final one, then return to the usual choice." I am not making that request myself.
- Gold: stable_preference / resolved; evidence message 3. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"saved-search alert grouping": {"general": "one alert per matching item", "exceptions": {"focus": {"value": "one alert per matching item", "validity": {"kind": "window", "from": "2027-06-04", "to": "2027-06-24"}}}}}`

**2027-06-07 · e137079a5bc8a68205e11**

- User: I was mulling over how the saved queries notify me the other day.
- Assistant: How would you put it?
- User: I wanted to talk about how the saved queries notify me.  It is the situation, not the option matches grouped by the source that posted them, that I have left open: saved searches with several keywords versus a saved query with one search word.
- Assistant: It sounds worth discussing keeping results from the same source together.
- User: The results are more useful when I can see how they are related.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"saved-search alert grouping": {"general": "one alert per matching item", "exceptions": {"focus": {"value": "one alert per matching item", "validity": {"kind": "window", "from": "2027-06-04", "to": "2027-06-24"}}}}}`

**2027-06-08 · e1f677c8bec04d56e7439**

- User: On how the saved queries notify me, here's what I mean.  I only mean the request at hand for a saved query with one search word; later occasions are a different conversation.
- Assistant: What's the issue with seeing several results at once, if there is one?
- User: The results are more useful when I can see how they are related.
- Assistant: What are you leaning towards?
- User: I feel best about five search hits in each bundle.
- Assistant: We can leave seeing several results at once here for the moment.
- User: I think that's as far as I need to go today.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"saved-search alert grouping": {"general": "one alert per matching item", "exceptions": {"focus": {"value": "one alert per matching item", "validity": {"kind": "window", "from": "2027-06-04", "to": "2027-06-24"}}}}}`
- target QA: It is June 8 and the situation is saved searches with a single keyword. Which saved-search alert grouping would fit the preference? Options: matches grouped by the source that posted them / one alert per matching item / matches collected in groups of five / matches bundled into pairs. Gold: **one alert per matching item**.
- default QA: It is June 8 and the situation is an ordinary occasion. Which saved-search alert grouping would fit the preference? Options: one alert per matching item / matches bundled into pairs / matches grouped by the source that posted them / matches collected in groups of five. Gold: **one alert per matching item**.
- neighbor QA: It is June 8 and the situation is saved searches with several keywords. Which saved-search alert grouping would fit the preference? Options: one alert per matching item / matches collected in groups of five / matches grouped by the source that posted them / matches bundled into pairs. Gold: **one alert per matching item**.

### de-0106 · dev-hand-weight-resting-place

Contrast group: `de-pair-0060`

Initial state: `{"hand-weight resting place": {"general": "weights resting in a shallow rubber tray", "exceptions": {"focus": {"value": "weights resting on a folded towel", "validity": {"kind": "persistent"}}, "adjacent": {"value": "weights resting on a cork floor square", "validity": {"kind": "open"}}}}}`

**2027-07-08 · eccb3113715d633759c07**

- User: I've been going back and forth on where I set the weights between lifts.
- Assistant: How would you put it?
- User: There's something I'd like to bring up about where I set the weights between lifts.  There is an unresolved distinction between weight exercises beside a high bench and using hand weights by a short bench in what I mean by choosing weights resting across two foam blocks.
- Assistant: Have you run into trouble with not having to reach too low between sets?
- User: I keep reaching too far down to pick the weights up again.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"hand-weight resting place": {"general": "weights resting in a shallow rubber tray", "exceptions": {"focus": {"value": "weights resting on a folded towel", "validity": {"kind": "persistent"}}, "adjacent": {"value": "weights resting on a cork floor square", "validity": {"kind": "open"}}}}}`

**2027-07-10 · e2a6dee07e3f980bdd1ca**

- User: I keep coming back to where I set the weights between lifts when I think about putting the weights down quietly.
- Assistant: I'm here. Tell me anything that seems relevant.
- User: I wanted to talk about hand-weight resting place.  Set the choice for weight exercises beside a high bench to the weights supported by a pair of foam blocks. Use it repeatedly for now, not permanently; I have not established when it ends.
- Assistant: Have you run into trouble with putting the weights down quietly?
- User: I keep reaching too far down to pick the weights up again.
- Gold: exception_revision / resolved; evidence message 3. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"hand-weight resting place": {"general": "weights resting in a shallow rubber tray", "exceptions": {"focus": {"value": "weights resting on a folded towel", "validity": {"kind": "persistent"}}, "adjacent": {"value": "weights resting across two foam blocks", "validity": {"kind": "open"}}}}}`

**2027-07-12 · e693de4a4e8c393f127ef**

- User: On where I set the weights between lifts, here's what I mean.  I had entertained the request, "Could you save weights resting across two foam blocks as my selection for using hand weights by a short bench? I want this to hold whenever the situation recurs." I am not proceeding with it.
- Assistant: Do you see putting the weights down quietly as a big part of it?
- User: I keep reaching too far down to pick the weights up again.
- Assistant: We don’t have to get into all of not having to reach too low between sets in one go.
- User: That’s fine. I didn’t have any other details in mind.
- Gold: stable_preference / resolved; evidence message 1. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"hand-weight resting place": {"general": "weights resting in a shallow rubber tray", "exceptions": {"focus": {"value": "weights resting on a folded towel", "validity": {"kind": "persistent"}}, "adjacent": {"value": "weights resting across two foam blocks", "validity": {"kind": "open"}}}}}`

**2027-07-13 · e6de766b3145a61980693**

- User: I was mulling over where I set the weights between lifts the other day.
- Assistant: Is protecting the bench and floor mostly a practical concern?
- User: I keep reaching too far down to pick the weights up again.
- Assistant: Was there a specific thing about protecting the bench and floor you wanted to bring up?
- User: I've given where I set the weights between lifts some thought. With my everyday use in mind, put me down for the weights set down on a square of cork. The special choice here is meant to remain in place for the longer term.
- Gold: general_update / resolved; evidence message 5. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"hand-weight resting place": {"general": "weights resting on a cork floor square", "exceptions": {"focus": {"value": "weights resting on a folded towel", "validity": {"kind": "persistent"}}, "adjacent": {"value": "weights resting across two foam blocks", "validity": {"kind": "open"}}}}}`

**2027-07-14 · eaf5d8a73a99a59df6311**

- User: One thing I wanted to mention is where I set the weights between lifts.
- Assistant: Was there a specific thing about protecting the bench and floor you wanted to bring up?
- User: I've given hand-weight resting place some thought. I would select the weights set onto a towel folded over in situations described as the usual case in general. I intend this to continue as the normal choice here rather than end after one occasion.
- Assistant: Can you tell me what happened with protecting the bench and floor?
- User: I keep reaching too far down to pick the weights up again.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"hand-weight resting place": {"general": "weights resting on a folded towel", "exceptions": {"focus": {"value": "weights resting on a folded towel", "validity": {"kind": "persistent"}}, "adjacent": {"value": "weights resting across two foam blocks", "validity": {"kind": "open"}}}}}`
- target QA: It is July 14 and the situation is an ordinary occasion. Which hand-weight resting place would fit the preference? Options: weights resting across two foam blocks / weights resting in a shallow rubber tray / weights resting on a cork floor square / weights resting on a folded towel. Gold: **weights resting on a folded towel**.
- neighbor QA: It is July 14 and the situation is weight exercises beside a low bench. Which hand-weight resting place would fit the preference? Options: weights resting across two foam blocks / weights resting on a folded towel / weights resting on a cork floor square / weights resting in a shallow rubber tray. Gold: **weights resting on a folded towel**.
- neighbor QA: It is July 14 and the situation is weight exercises beside a high bench. Which hand-weight resting place would fit the preference? Options: weights resting across two foam blocks / weights resting on a cork floor square / weights resting on a folded towel / weights resting in a shallow rubber tray. Gold: **weights resting across two foam blocks**.

**2027-07-15 · eba81d4c20d36015b5630**

- User: I was mulling over where I set the weights between lifts the other day.
- Assistant: I hadn't heard much from you about not having to reach too low between sets.
- User: It makes a difference when I am a few moves in.
- Assistant: Was there a specific thing about not having to reach too low between sets you wanted to bring up?
- User: I've given where I set the weights between lifts some thought. What I am requesting for weight exercises beside a low bench is the weights set inside a low rubber tray. This is always my choice in that situation, not a one-off.
- Gold: exception_revision / resolved; evidence message 5. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"hand-weight resting place": {"general": "weights resting on a folded towel", "exceptions": {"focus": {"value": "weights resting in a shallow rubber tray", "validity": {"kind": "persistent"}}, "adjacent": {"value": "weights resting across two foam blocks", "validity": {"kind": "open"}}}}}`

**2027-07-16 · ed699b7b61b0da67debc4**

- User: One thing I wanted to mention is where I set the weights between lifts.
- Assistant: I'm here. Tell me anything that seems relevant.
- User: I've given where I set the weights between lifts some thought. For using hand weights by a taller bench, the general arrangement is sufficient; remove the distinct choice attached to it.
- Assistant: What's the experience been like with not having to reach too low between sets?
- User: I keep reaching too far down to pick the weights up again.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"hand-weight resting place": {"general": "weights resting on a folded towel", "exceptions": {"focus": {"value": "weights resting in a shallow rubber tray", "validity": {"kind": "persistent"}}}}}`

**2027-07-18 · e89c774f76ea518b9a439**

- User: I wanted to talk about where I set the weights between lifts.  For using hand weights by a short bench, I'd like to make a choice that still applies on later occasions.
- Assistant: Can you tell me what happened with putting the weights down quietly?
- User: I keep reaching too far down to pick the weights up again.
- Assistant: Which option do you feel happy with?
- User: My pick would be weights resting on a cork floor square.
- Assistant: We can leave putting the weights down quietly here for the moment.
- User: No, I've settled on it.
- Gold: exception_revision / resolved; evidence message 5. The user chooses a continuing replacement for the existing situation rule.
- After: `{"hand-weight resting place": {"general": "weights resting on a folded towel", "exceptions": {"focus": {"value": "weights resting on a cork floor square", "validity": {"kind": "persistent"}}}}}`
- target QA: It is July 18 and the situation is weight exercises beside a low bench. Which hand-weight resting place would fit the preference? Options: weights resting on a folded towel / weights resting in a shallow rubber tray / weights resting across two foam blocks / weights resting on a cork floor square. Gold: **weights resting on a cork floor square**.
- default QA: It is July 18 and the situation is an ordinary occasion. Which hand-weight resting place would fit the preference? Options: weights resting on a cork floor square / weights resting across two foam blocks / weights resting on a folded towel / weights resting in a shallow rubber tray. Gold: **weights resting on a folded towel**.
- neighbor QA: It is July 18 and the situation is weight exercises beside a high bench. Which hand-weight resting place would fit the preference? Options: weights resting in a shallow rubber tray / weights resting on a cork floor square / weights resting on a folded towel / weights resting across two foam blocks. Gold: **weights resting on a folded towel**.

### de-0116 · dev-short-work-break-activity

Contrast group: `de-pair-0057`

Initial state: `{"short work-break activity": {"general": "folding a simple paper shape", "exceptions": {"adjacent": {"value": "looking out at distant rooflines", "validity": {"kind": "persistent"}}, "focus": {"value": "watering a small desk fern", "validity": {"kind": "persistent"}}}}}`

**2027-01-10 · e2d41ac1d5d7360438975**

- User: I keep coming back to what I do on a quick break when I think about what fits into a short indoor break.
- Assistant: What have you been thinking?
- User: On what I do on a quick break, here's what I mean.  Apply sorting one drawer of the desk when it is a matter of an everyday occasion. Future occasions of that sort should use it as well.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"short work-break activity": {"general": "tidying one desk drawer", "exceptions": {"adjacent": {"value": "looking out at distant rooflines", "validity": {"kind": "persistent"}}, "focus": {"value": "watering a small desk fern", "validity": {"kind": "persistent"}}}}}`
- target QA: It is January 10 and the situation is an ordinary occasion. Which short work-break activity would fit the preference? Options: watering a small desk fern / looking out at distant rooflines / folding a simple paper shape / tidying one desk drawer. Gold: **tidying one desk drawer**.
- neighbor QA: It is January 10 and the situation is work breaks taken alone indoors. Which short work-break activity would fit the preference? Options: looking out at distant rooflines / watering a small desk fern / folding a simple paper shape / tidying one desk drawer. Gold: **watering a small desk fern**.
- neighbor QA: It is January 10 and the situation is work breaks taken with company indoors. Which short work-break activity would fit the preference? Options: tidying one desk drawer / watering a small desk fern / folding a simple paper shape / looking out at distant rooflines. Gold: **looking out at distant rooflines**.

**2027-01-11 · ec24f2c093a5916dc03f9**

- User: I was mulling over what I do on a quick break the other day.
- Assistant: Is there a part you'd like to talk about first?
- User: On what I do on a quick break, here's what I mean.  For work breaks taken alone indoors, the option that I want is looking toward the far rooftops. It is a standing preference for each occasion of this sort, not merely for today. No changes are intended for the other choices.
- Assistant: Say a little more about what fits into a short indoor break, if you like.
- User: I get more from the break if I stop looking at the display.
- Assistant: Should we spend any longer on getting away from the screen for a minute?
- User: I think I’ve said what I meant to say about it.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"short work-break activity": {"general": "tidying one desk drawer", "exceptions": {"adjacent": {"value": "looking out at distant rooflines", "validity": {"kind": "persistent"}}, "focus": {"value": "looking out at distant rooflines", "validity": {"kind": "persistent"}}}}}`
- target QA: It is January 11 and the situation is work breaks taken alone indoors. Which short work-break activity would fit the preference? Options: watering a small desk fern / tidying one desk drawer / folding a simple paper shape / looking out at distant rooflines. Gold: **looking out at distant rooflines**.
- default QA: It is January 11 and the situation is an ordinary occasion. Which short work-break activity would fit the preference? Options: folding a simple paper shape / watering a small desk fern / tidying one desk drawer / looking out at distant rooflines. Gold: **tidying one desk drawer**.
- neighbor QA: It is January 11 and the situation is work breaks taken with company indoors. Which short work-break activity would fit the preference? Options: looking out at distant rooflines / watering a small desk fern / tidying one desk drawer / folding a simple paper shape. Gold: **looking out at distant rooflines**.

**2027-01-12 · e8d0203d787689f67f806**

- User: Do you have a minute to talk about what I do on a quick break?
- Assistant: I'm here. Tell me anything that seems relevant.
- User: On what I do on a quick break, here's what I mean.  Please let work breaks taken alone indoors go the same way as other occasions, even if I change my choice later.
- Assistant: How important is getting away from the screen for a minute in practice?
- User: I get more from the break if I stop looking at the display.
- Assistant: We don’t have to get into all of getting away from the screen for a minute in one go.
- User: That’s fine. I didn’t have any other details in mind.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"short work-break activity": {"general": "tidying one desk drawer", "exceptions": {"adjacent": {"value": "looking out at distant rooflines", "validity": {"kind": "persistent"}}}}}`
- target QA: It is January 12 and the situation is work breaks taken alone indoors. Which short work-break activity would fit the preference? Options: tidying one desk drawer / folding a simple paper shape / looking out at distant rooflines / watering a small desk fern. Gold: **tidying one desk drawer**.
- default QA: It is January 12 and the situation is an ordinary occasion. Which short work-break activity would fit the preference? Options: looking out at distant rooflines / watering a small desk fern / tidying one desk drawer / folding a simple paper shape. Gold: **tidying one desk drawer**.
- neighbor QA: It is January 12 and the situation is work breaks taken with company indoors. Which short work-break activity would fit the preference? Options: looking out at distant rooflines / tidying one desk drawer / folding a simple paper shape / watering a small desk fern. Gold: **looking out at distant rooflines**.

**2027-01-14 · e16288cd4c3febbdc8b81**

- User: There's something I'd like to bring up about what I do on a quick break.  I'm looking to settle what I'll use whenever it is a matter of work breaks taken with company indoors.
- Assistant: I'd be interested to hear why getting away from the screen for a minute matters here.
- User: I get more from the break if I stop looking at the display.
- Assistant: What are you leaning towards?
- User: I'd like to go with watering a small desk fern.
- Assistant: Is there more you wanted to think through around getting away from the screen for a minute?
- User: I think that's as far as I need to go today.
- Gold: exception_revision / resolved; evidence message 5. The user chooses a continuing replacement for the existing situation rule.
- After: `{"short work-break activity": {"general": "tidying one desk drawer", "exceptions": {"adjacent": {"value": "watering a small desk fern", "validity": {"kind": "persistent"}}}}}`
- target QA: It is January 14 and the situation is work breaks taken with company indoors. Which short work-break activity would fit the preference? Options: watering a small desk fern / tidying one desk drawer / looking out at distant rooflines / folding a simple paper shape. Gold: **watering a small desk fern**.
- default QA: It is January 14 and the situation is an ordinary occasion. Which short work-break activity would fit the preference? Options: tidying one desk drawer / watering a small desk fern / looking out at distant rooflines / folding a simple paper shape. Gold: **tidying one desk drawer**.
- neighbor QA: It is January 14 and the situation is work breaks taken alone indoors. Which short work-break activity would fit the preference? Options: watering a small desk fern / folding a simple paper shape / looking out at distant rooflines / tidying one desk drawer. Gold: **tidying one desk drawer**.

### de-0032 · dev-lock-screen-clock-presentation

Contrast group: `de-pair-0013`

Initial state: `{"lock-screen clock presentation": {"general": "small stacked clock digits", "exceptions": {"adjacent": {"value": "large outlined clock digits", "validity": {"kind": "persistent"}}}}, "touchpad tap action": {"general": "two taps for a primary click", "exceptions": {"adjacent": {"value": "one tap for a primary click", "validity": {"kind": "persistent"}}}}}`

**2027-07-04 · e509f300900ac5f1e6068**

- User: I wanted to talk about the clock I see when the screen locks.  I am ending the special treatment of locking it after dark. Give it the choice I normally make.
- Assistant: Does the way you feel about seeing the clock in a dim room explain part of this?
- User: I want to get the time without unlocking the whole screen.
- Gold: exception_retirement / resolved; evidence message 1. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"lock-screen clock presentation": {"general": "small stacked clock digits", "exceptions": {}}, "touchpad tap action": {"general": "two taps for a primary click", "exceptions": {"adjacent": {"value": "one tap for a primary click", "validity": {"kind": "persistent"}}}}}`

**2027-07-05 · e783310c46ca716fc7767**

- User: There's something I'd like to bring up about what a touchpad tap does.  I am leaving the situation unsettled between touchpad use on a tilted laptop stand and touchpad use on a level tabletop while we discuss a tap followed by a hold for a primary click.
- Assistant: Does this have much to do with what happens on a light touch?
- User: At that angle I click by accident while trying to move.
- Gold: clarify / clarify; evidence message 1. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"lock-screen clock presentation": {"general": "small stacked clock digits", "exceptions": {}}, "touchpad tap action": {"general": "two taps for a primary click", "exceptions": {"adjacent": {"value": "one tap for a primary click", "validity": {"kind": "persistent"}}}}}`
- target QA: It is July 5 and the situation is touchpad use on a tilted laptop stand. Which touchpad tap action would fit the preference? Options: two taps for a primary click / a firm press for a primary click / one tap for a primary click / a tap followed by a hold for a primary click. Gold: **one tap for a primary click**.
- default QA: It is July 5 and the situation is an ordinary occasion. Which touchpad tap action would fit the preference? Options: a firm press for a primary click / a tap followed by a hold for a primary click / one tap for a primary click / two taps for a primary click. Gold: **two taps for a primary click**.
- neighbor QA: It is July 5 and the situation is touchpad use on a level tabletop. Which touchpad tap action would fit the preference? Options: one tap for a primary click / a firm press for a primary click / a tap followed by a hold for a primary click / two taps for a primary click. Gold: **two taps for a primary click**.

**2027-07-06 · ec9e7210fc5382537e928**

- User: There's something I'd like to bring up about touchpad tap action.  Could you save a tap followed by a hold for a primary click as my selection for using the pad on an angled stand? The special choice here is meant to remain in place for the longer term.
- Assistant: Do you see not clicking when you meant to move as a big part of it?
- User: At that angle I click by accident while trying to move.
- Gold: exception_revision / resolved; evidence message 1. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"lock-screen clock presentation": {"general": "small stacked clock digits", "exceptions": {}}, "touchpad tap action": {"general": "two taps for a primary click", "exceptions": {"adjacent": {"value": "a tap followed by a hold for a primary click", "validity": {"kind": "persistent"}}}}}`
- target QA: It is July 6 and the situation is touchpad use on a tilted laptop stand. Which touchpad tap action would fit the preference? Options: a tap followed by a hold for a primary click / a firm press for a primary click / two taps for a primary click / one tap for a primary click. Gold: **a tap followed by a hold for a primary click**.
- default QA: It is July 6 and the situation is an ordinary occasion. Which touchpad tap action would fit the preference? Options: two taps for a primary click / a firm press for a primary click / one tap for a primary click / a tap followed by a hold for a primary click. Gold: **two taps for a primary click**.
- neighbor QA: It is July 6 and the situation is touchpad use on a level tabletop. Which touchpad tap action would fit the preference? Options: a tap followed by a hold for a primary click / two taps for a primary click / one tap for a primary click / a firm press for a primary click. Gold: **two taps for a primary click**.

**2027-07-07 · e6daf1a52661a4ef82c4b**

- User: I keep coming back to the clock I see when the screen locks when I think about how much of the display the digits use.
- Assistant: How would you put it?
- User: I've given the clock I see when the screen locks some thought. I am choosing large outlined clock digits in relation to an everyday occasion. This applies on successive occasions, indefinitely.
- Assistant: Say a little more about how much of the display the digits use, if you like.
- User: I want to get the time without unlocking the whole screen.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"lock-screen clock presentation": {"general": "large outlined clock digits", "exceptions": {}}, "touchpad tap action": {"general": "two taps for a primary click", "exceptions": {"adjacent": {"value": "a tap followed by a hold for a primary click", "validity": {"kind": "persistent"}}}}}`

**2027-07-08 · e7d89371457e16ff36ddd**

- User: Do you have a minute to talk about what a touchpad tap does?
- Assistant: Do you see reaching the pad at an angle as a big part of it?
- User: At that angle I click by accident while trying to move.
- Assistant: Sure, we can take a moment for reaching the pad at an angle.
- User: I wanted to talk about touchpad tap action.  My instruction concerning using the pad on an angled stand is to use a hard press as the main click. This applies on successive occasions, indefinitely.
- Gold: exception_revision / resolved; evidence message 5. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"lock-screen clock presentation": {"general": "large outlined clock digits", "exceptions": {}}, "touchpad tap action": {"general": "two taps for a primary click", "exceptions": {"adjacent": {"value": "a firm press for a primary click", "validity": {"kind": "persistent"}}}}}`

**2027-07-10 · e97f1ced74e0f85a3f535**

- User: There's something I'd like to bring up about what a touchpad tap does.  My instruction concerning using the pad on a flat table is to use a tap followed by a hold for a primary click. I am asking for an ongoing arrangement without a fixed finish.
- Assistant: I'd be interested to hear why not clicking when you meant to move matters here.
- User: At that angle I click by accident while trying to move.
- Gold: scoped_exception / resolved; evidence message 1. The user chooses a continuing setting for the named situation.
- After: `{"lock-screen clock presentation": {"general": "large outlined clock digits", "exceptions": {}}, "touchpad tap action": {"general": "two taps for a primary click", "exceptions": {"adjacent": {"value": "a firm press for a primary click", "validity": {"kind": "persistent"}}, "focus": {"value": "a tap followed by a hold for a primary click", "validity": {"kind": "persistent"}}}}}`
- target QA: It is July 10 and the situation is touchpad use on a level tabletop. Which touchpad tap action would fit the preference? Options: two taps for a primary click / a tap followed by a hold for a primary click / a firm press for a primary click / one tap for a primary click. Gold: **a tap followed by a hold for a primary click**.
- default QA: It is July 10 and the situation is an ordinary occasion. Which touchpad tap action would fit the preference? Options: one tap for a primary click / a tap followed by a hold for a primary click / two taps for a primary click / a firm press for a primary click. Gold: **two taps for a primary click**.
- neighbor QA: It is July 10 and the situation is touchpad use on a tilted laptop stand. Which touchpad tap action would fit the preference? Options: two taps for a primary click / a tap followed by a hold for a primary click / a firm press for a primary click / one tap for a primary click. Gold: **a firm press for a primary click**.

**2027-07-12 · ec249f0d4e641d5f93a2b**

- User: On the clock I see when the screen locks, here's what I mean.  I'm just trying to sort out what's coming up for locking it after dark. How I do it later isn't part of this decision.
- Assistant: I'd be interested to hear why seeing the clock in a dim room matters here.
- User: I want to get the time without unlocking the whole screen.
- Assistant: What do you think you'd pick?
- User: I'd like to go with one line spelling out the time.
- Assistant: Is there more you wanted to think through around seeing the clock in a dim room?
- User: I think that's as far as I need to go today.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"lock-screen clock presentation": {"general": "large outlined clock digits", "exceptions": {}}, "touchpad tap action": {"general": "two taps for a primary click", "exceptions": {"adjacent": {"value": "a firm press for a primary click", "validity": {"kind": "persistent"}}, "focus": {"value": "a tap followed by a hold for a primary click", "validity": {"kind": "persistent"}}}}}`
- target QA: It is July 12 and the situation is screens locked during hours of darkness. Which lock-screen clock presentation would fit the preference? Options: large outlined clock digits / a single-line word clock / small stacked clock digits / a slender analog clock face. Gold: **large outlined clock digits**.
- default QA: It is July 12 and the situation is an ordinary occasion. Which lock-screen clock presentation would fit the preference? Options: large outlined clock digits / small stacked clock digits / a single-line word clock / a slender analog clock face. Gold: **large outlined clock digits**.
- neighbor QA: It is July 12 and the situation is screens locked during daylight hours. Which lock-screen clock presentation would fit the preference? Options: a single-line word clock / large outlined clock digits / small stacked clock digits / a slender analog clock face. Gold: **large outlined clock digits**.

## Test

### te-0036 · test-step-drill-hand-position

Contrast group: `te-pair-0012`

Initial state: `{"step-drill hand position": {"general": "hands lightly resting at the waist", "exceptions": {"focus": {"value": "hands loosely joined behind the back", "validity": {"kind": "persistent"}}}}}`

**2027-11-08 · efbc11aa96cfe7c506f95**

- User: There was one thing about what I do with my hands on the step I wanted to talk through.
- Assistant: Did you want to say what you had in mind?
- User: I had a point to make about what I do with my hands on the step. Let the separate rule for step drills using a low platform finish here; use the usual choice for those occasions after this.
- Assistant: Is getting off the platform without reaching for anything part of what you want to work out?
- User: I can feel myself go off balance when I am thinking about where my arms are.
- Assistant: Would you prefer to talk more about where your arms naturally fall another time?
- User: Sure, there’s no need to get into it further right now.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"step-drill hand position": {"general": "hands lightly resting at the waist", "exceptions": {}}}`
- target QA: Pick a value for step-drill hand position, dated November 8, with the setting described as step drills using a low platform. Options: arms hanging with palms facing inward / hands loosely joined behind the back / hands lightly resting at the waist / fingertips resting on opposite shoulders. Gold: **hands lightly resting at the waist**.
- default QA: Pick a value for step-drill hand position, dated November 8, with the setting described as an ordinary occasion. Options: hands lightly resting at the waist / arms hanging with palms facing inward / hands loosely joined behind the back / fingertips resting on opposite shoulders. Gold: **hands lightly resting at the waist**.
- neighbor QA: Pick a value for step-drill hand position, dated November 8, with the setting described as step drills using a medium platform. Options: arms hanging with palms facing inward / hands lightly resting at the waist / fingertips resting on opposite shoulders / hands loosely joined behind the back. Gold: **hands lightly resting at the waist**.

**2027-11-09 · e5e4385f0c7e308b4ac12**

- User: Here's what I meant about what I do with my hands on the step.  I could be talking about stepping on the shorter platform or stepping on the middle-height platform when I mention hands loosely joined behind the back; that part is genuinely undecided.
- Assistant: Is this partly about getting off the platform without reaching for anything?
- User: I can feel myself go off balance when I am thinking about where my arms are.
- Assistant: We can leave where your arms naturally fall there if you like.
- User: Let’s do that. That’s all I meant to bring up.
- Gold: clarify / clarify; evidence message 1. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"step-drill hand position": {"general": "hands lightly resting at the waist", "exceptions": {}}}`

**2027-11-10 · e21ee4879e9650300ab1b**

- User: I have something on my mind about what I do with my hands on the step.
- Assistant: How have you been thinking about it?
- User: I thought again about what I do with my hands on the step.  Put hands loosely joined behind the back against step drills using a low platform for me. Only as a stopgap, but on each occasion for now. I cannot name the last day.
- Gold: scoped_exception / resolved; evidence message 3. The user settles the earlier choice of situation and supplies a continuing instruction for it.
- After: `{"step-drill hand position": {"general": "hands lightly resting at the waist", "exceptions": {"focus": {"value": "hands loosely joined behind the back", "validity": {"kind": "open"}}}}}`

**2027-11-11 · e041c301ef33535125faa**

- User: I've got a minute now to explain what I mean about what I do with my hands on the step.
- Assistant: I'm listening. What's on your mind?
- User: I had a point to make about what I do with my hands on the step. Use this choice for step drills using a medium platform: my hands loosely clasped behind me. I need it for a while rather than once, and rather than forever. No end is fixed. That does not change the rest of my preferences.
- Assistant: Tell me what struck you about where your arms naturally fall.
- User: I can feel myself go off balance when I am thinking about where my arms are.
- Gold: scoped_exception / resolved; evidence message 3. The user chooses a continuing setting for the named situation.
- After: `{"step-drill hand position": {"general": "hands lightly resting at the waist", "exceptions": {"focus": {"value": "hands loosely joined behind the back", "validity": {"kind": "open"}}, "adjacent": {"value": "hands loosely joined behind the back", "validity": {"kind": "open"}}}}}`

**2027-11-12 · e83437435ca2c85e50c13**

- User: Here's what I meant about what I do with my hands on the step.  I would like stepping on the shorter platform to stop being an exception and simply follow my general preference.
- Assistant: Could you say why keeping your balance as you step up matters to you?
- User: I can feel myself go off balance when I am thinking about where my arms are.
- Gold: exception_retirement / resolved; evidence message 1. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"step-drill hand position": {"general": "hands lightly resting at the waist", "exceptions": {"adjacent": {"value": "hands loosely joined behind the back", "validity": {"kind": "open"}}}}}`
- target QA: Pick a value for step-drill hand position, dated November 12, with the setting described as step drills using a low platform. Options: fingertips resting on opposite shoulders / hands loosely joined behind the back / arms hanging with palms facing inward / hands lightly resting at the waist. Gold: **hands lightly resting at the waist**.
- default QA: Pick a value for step-drill hand position, dated November 12, with the setting described as an ordinary occasion. Options: arms hanging with palms facing inward / hands lightly resting at the waist / fingertips resting on opposite shoulders / hands loosely joined behind the back. Gold: **hands lightly resting at the waist**.
- neighbor QA: Pick a value for step-drill hand position, dated November 12, with the setting described as step drills using a medium platform. Options: hands loosely joined behind the back / arms hanging with palms facing inward / hands lightly resting at the waist / fingertips resting on opposite shoulders. Gold: **hands loosely joined behind the back**.

**2027-11-13 · e2a45139a0af2ab453113**

- User: Can we get back to what I do with my hands on the step?  I'm choosing for the step drills using a medium platform occasion I've got in front of me, not making a longer plan.
- Assistant: What did you find difficult about where your arms naturally fall?
- User: I can feel myself go off balance when I am thinking about where my arms are.
- Assistant: Which sounds most like what you want?
- User: Let's go with fingertips resting on opposite shoulders.
- Assistant: That gives us enough to go on for now.
- User: Yes, I don't have anything to add.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"step-drill hand position": {"general": "hands lightly resting at the waist", "exceptions": {"adjacent": {"value": "hands loosely joined behind the back", "validity": {"kind": "open"}}}}}`
- target QA: Pick a value for step-drill hand position, dated November 13, with the setting described as step drills using a medium platform. Options: fingertips resting on opposite shoulders / hands lightly resting at the waist / hands loosely joined behind the back / arms hanging with palms facing inward. Gold: **hands loosely joined behind the back**.
- default QA: Pick a value for step-drill hand position, dated November 13, with the setting described as an ordinary occasion. Options: hands loosely joined behind the back / arms hanging with palms facing inward / hands lightly resting at the waist / fingertips resting on opposite shoulders. Gold: **hands lightly resting at the waist**.
- neighbor QA: Pick a value for step-drill hand position, dated November 13, with the setting described as step drills using a low platform. Options: hands lightly resting at the waist / fingertips resting on opposite shoulders / hands loosely joined behind the back / arms hanging with palms facing inward. Gold: **hands lightly resting at the waist**.

### te-0006 · test-bath-towel-border-style

Contrast group: `te-pair-0036`

Initial state: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a broad flat linen border", "validity": {"kind": "open"}}}}, "reusable lunch-pot nesting": {"general": "a broad pot holding two small inserts", "exceptions": {"focus": {"value": "two shallow pots stacked together", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a tall pot with a removable inner cup", "validity": {"kind": "persistent"}}}}}`

**2027-04-07 · e879ad3b39195caa28880**

- User: There was one thing about how the lunch tubs fit together I wanted to talk through.
- Assistant: Was something about stopping the little cup from rattling especially important?
- User: Here's what I meant about how the lunch tubs fit together.  Picture me asking, "My request is to save a stack of two low containers for routine circumstances. This should carry on; it is not just a test." This is make-believe; none of my real choices should change.
- Assistant: What do you tend to notice first about stopping the little cup from rattling?
- User: I want to carry lunch without having containers knock against each other.
- Gold: stable_preference / resolved; evidence message 3. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a broad flat linen border", "validity": {"kind": "open"}}}}, "reusable lunch-pot nesting": {"general": "a broad pot holding two small inserts", "exceptions": {"focus": {"value": "two shallow pots stacked together", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a tall pot with a removable inner cup", "validity": {"kind": "persistent"}}}}}`

**2027-04-08 · ef04b3f482dbe12f02082**

- User: I have something on my mind about how the lunch tubs fit together.
- Assistant: How have you been thinking about it?
- User: I had a point to make about how the lunch tubs fit together. There are two possible homes for three skinny containers that clip together in a row, taking lunch tubs in a slim bag and taking lunch tubs in a roomy wide bag, and I have not picked one.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a broad flat linen border", "validity": {"kind": "open"}}}}, "reusable lunch-pot nesting": {"general": "a broad pot holding two small inserts", "exceptions": {"focus": {"value": "two shallow pots stacked together", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a tall pot with a removable inner cup", "validity": {"kind": "persistent"}}}}}`

**2027-04-09 · ed5fdf122bbdb0a570b6b**

- User: I had a point to make about reusable lunch-pot nesting. When taking lunch tubs in a slim bag comes up, my choice is three skinny containers that clip together in a row. I mean an enduring arrangement rather than a one-off.
- Assistant: How has stopping the little cup from rattling worked out in practice?
- User: I want to carry lunch without having containers knock against each other.
- Gold: exception_revision / resolved; evidence message 1. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a broad flat linen border", "validity": {"kind": "open"}}}}, "reusable lunch-pot nesting": {"general": "a broad pot holding two small inserts", "exceptions": {"focus": {"value": "three slim pots clipped side by side", "validity": {"kind": "persistent"}}, "adjacent": {"value": "a tall pot with a removable inner cup", "validity": {"kind": "persistent"}}}}}`

**2027-04-10 · e433a90946dabb454f58a**

- User: I thought again about how the lunch tubs fit together.  Three slim pots clipped side by side is the one I want when we are talking about taking lunch tubs in a roomy wide bag. Leave that as the choice whenever this comes round again.
- Assistant: What would make fitting more than one thing in the lunch bag easier to deal with?
- User: I want to carry lunch without having containers knock against each other.
- Gold: exception_revision / resolved; evidence message 1. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a broad flat linen border", "validity": {"kind": "open"}}}}, "reusable lunch-pot nesting": {"general": "a broad pot holding two small inserts", "exceptions": {"focus": {"value": "three slim pots clipped side by side", "validity": {"kind": "persistent"}}, "adjacent": {"value": "three slim pots clipped side by side", "validity": {"kind": "persistent"}}}}}`

**2027-04-11 · e8cdcb631c253edd7d3f8**

- User: I have something on my mind about how the lunch tubs fit together.
- Assistant: Was something about fitting more than one thing in the lunch bag especially important?
- User: Here's what I meant about how the lunch tubs fit together.  Picture me asking, "I want taking lunch tubs in a roomy wide bag covered by my general arrangement again, not by an instruction of its own." This is make-believe; none of my real choices should change.
- Gold: stable_preference / resolved; evidence message 3. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a broad flat linen border", "validity": {"kind": "open"}}}}, "reusable lunch-pot nesting": {"general": "a broad pot holding two small inserts", "exceptions": {"focus": {"value": "three slim pots clipped side by side", "validity": {"kind": "persistent"}}, "adjacent": {"value": "three slim pots clipped side by side", "validity": {"kind": "persistent"}}}}}`

**2027-04-12 · e99dfc664f4111c7be156**

- User: Here's what I meant about bath-towel border style.  I would put a wide smooth linen strip first for the broad run of ordinary occasions. This is for the long run rather than a temporary spell. Leave the other arrangements alone.
- Assistant: I'm curious about how the edge sits on the rail, too.
- User: I use the edge to tell which towel is which in a stack.
- Assistant: Would you prefer to talk more about whether the fringe catches on the hook another time?
- User: Sure, there’s no need to get into it further right now.
- Gold: general_update / resolved; evidence message 1. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"bath-towel border style": {"general": "a broad flat linen border", "exceptions": {"focus": {"value": "a broad flat linen border", "validity": {"kind": "open"}}}}, "reusable lunch-pot nesting": {"general": "a broad pot holding two small inserts", "exceptions": {"focus": {"value": "three slim pots clipped side by side", "validity": {"kind": "persistent"}}, "adjacent": {"value": "three slim pots clipped side by side", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for bath-towel border style, dated April 12, with the setting described as an ordinary occasion. Options: a broad flat linen border / a narrow woven herringbone border / a doubled terry border with rounded corners / a soft fringed edge without a band. Gold: **a broad flat linen border**.
- neighbor QA: Pick a value for bath-towel border style, dated April 12, with the setting described as towels hung across a rail. Options: a soft fringed edge without a band / a narrow woven herringbone border / a doubled terry border with rounded corners / a broad flat linen border. Gold: **a broad flat linen border**.
- neighbor QA: Pick a value for bath-towel border style, dated April 12, with the setting described as towels hung on a wall hook. Options: a doubled terry border with rounded corners / a soft fringed edge without a band / a narrow woven herringbone border / a broad flat linen border. Gold: **a broad flat linen border**.

**2027-04-13 · e7b18221e27ce92d0a65a**

- User: I thought again about how the lunch tubs fit together.  I want a choice for the present business with taking lunch tubs in a roomy wide bag; don't carry the decision forward.
- Assistant: What do you tend to notice first about what comes out first when you unpack?
- User: I want to carry lunch without having containers knock against each other.
- Assistant: What feels right to you?
- User: I'd choose one deep container with a little cup inside, I think.
- Assistant: That gives us enough to go on for now.
- User: Yes, I don't have anything to add.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"bath-towel border style": {"general": "a broad flat linen border", "exceptions": {"focus": {"value": "a broad flat linen border", "validity": {"kind": "open"}}}}, "reusable lunch-pot nesting": {"general": "a broad pot holding two small inserts", "exceptions": {"focus": {"value": "three slim pots clipped side by side", "validity": {"kind": "persistent"}}, "adjacent": {"value": "three slim pots clipped side by side", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for reusable lunch-pot nesting, dated April 13, with the setting described as lunch pots carried in a wide bag. Options: a broad pot holding two small inserts / two shallow pots stacked together / a tall pot with a removable inner cup / three slim pots clipped side by side. Gold: **three slim pots clipped side by side**.
- default QA: Pick a value for reusable lunch-pot nesting, dated April 13, with the setting described as an ordinary occasion. Options: a broad pot holding two small inserts / two shallow pots stacked together / three slim pots clipped side by side / a tall pot with a removable inner cup. Gold: **a broad pot holding two small inserts**.
- neighbor QA: Pick a value for reusable lunch-pot nesting, dated April 13, with the setting described as lunch pots carried in a narrow bag. Options: two shallow pots stacked together / a broad pot holding two small inserts / three slim pots clipped side by side / a tall pot with a removable inner cup. Gold: **three slim pots clipped side by side**.

### te-0075 · test-bath-towel-border-style

Contrast group: `te-pair-0064`

Initial state: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {}}}`

**2027-05-10 · ea22a52b57cf8b261d4c8**

- User: I've got a minute now to explain what I mean about the edge finish on the bath towel.
- Assistant: Was something about finding the right towel from its border especially important?
- User: Can we get back to the edge finish on the bath towel?  Do not put a skinny band woven in herringbone anywhere yet. I have not answered whether it is for towels hung on a wall hook or drying the towel over a bar.
- Assistant: What's your biggest concern around finding the right towel from its border?
- User: I use the edge to tell which towel is which in a stack.
- Assistant: Is there anything about whether the fringe catches on the hook we haven’t touched on?
- User: Nothing I wanted to get into this time.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {}}}`
- target QA: Pick a value for bath-towel border style, dated May 10, with the setting described as towels hung on a wall hook. Options: a soft fringed edge without a band / a narrow woven herringbone border / a broad flat linen border / a doubled terry border with rounded corners. Gold: **a doubled terry border with rounded corners**.
- default QA: Pick a value for bath-towel border style, dated May 10, with the setting described as an ordinary occasion. Options: a narrow woven herringbone border / a doubled terry border with rounded corners / a soft fringed edge without a band / a broad flat linen border. Gold: **a doubled terry border with rounded corners**.
- neighbor QA: Pick a value for bath-towel border style, dated May 10, with the setting described as towels hung across a rail. Options: a narrow woven herringbone border / a soft fringed edge without a band / a broad flat linen border / a doubled terry border with rounded corners. Gold: **a doubled terry border with rounded corners**.

**2027-05-11 · eee8e138064dfe9e5bcac**

- User: Can we get back to the edge finish on the bath towel?  A narrow woven herringbone border is the one I want when we are talking about towels hung on a wall hook. Not permanently, and not just this time: it continues provisionally with no closing date.
- Assistant: There's room to talk more about whether the fringe catches on the hook if you want.
- User: I use the edge to tell which towel is which in a stack.
- Gold: scoped_exception / resolved; evidence message 1. The user settles the earlier choice of situation and supplies a continuing instruction for it.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a narrow woven herringbone border", "validity": {"kind": "open"}}}}}`

**2027-05-13 · eea32ffdc5b1878292414**

- User: I remembered something about the edge finish on the bath towel while thinking about whether the fringe catches on the hook.
- Assistant: Of course. We can talk about whether the fringe catches on the hook.
- User: Here's what I meant about the edge finish on the bath towel.  For drying the towel on a hook, please remember that I choose a soft fringed edge without a band. For the time being, keep using it. The need is temporary, but its duration is unknown. Anything outside this request keeps the choices it already had.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a soft fringed edge without a band", "validity": {"kind": "open"}}}}}`
- target QA: Pick a value for bath-towel border style, dated May 13, with the setting described as towels hung on a wall hook. Options: a doubled terry border with rounded corners / a narrow woven herringbone border / a soft fringed edge without a band / a broad flat linen border. Gold: **a soft fringed edge without a band**.
- default QA: Pick a value for bath-towel border style, dated May 13, with the setting described as an ordinary occasion. Options: a doubled terry border with rounded corners / a soft fringed edge without a band / a broad flat linen border / a narrow woven herringbone border. Gold: **a doubled terry border with rounded corners**.
- neighbor QA: Pick a value for bath-towel border style, dated May 13, with the setting described as towels hung across a rail. Options: a doubled terry border with rounded corners / a narrow woven herringbone border / a soft fringed edge without a band / a broad flat linen border. Gold: **a doubled terry border with rounded corners**.

**2027-05-15 · e39569761ae81e94938c2**

- User: I had a point to make about bath-towel border style. It is a wide smooth linen strip I am considering, without a decision on which situation, towels hung on a wall hook or towels hung across a rail.
- Assistant: Is how the edge sits on the rail part of what you want to work out?
- User: I use the edge to tell which towel is which in a stack.
- Gold: clarify / clarify; evidence message 1. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a soft fringed edge without a band", "validity": {"kind": "open"}}}}}`

**2027-05-16 · e41c58164c60d978d4bf1**

- User: Here's what I meant about the edge finish on the bath towel.  I would put a soft fringed edge without a band first for towels hung across a rail. I need it for a while rather than once, and rather than forever. No end is fixed.
- Assistant: What did you find difficult about how the edge sits on the rail?
- User: I use the edge to tell which towel is which in a stack.
- Gold: scoped_exception / resolved; evidence message 1. The user chooses a continuing setting for the named situation.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a soft fringed edge without a band", "validity": {"kind": "open"}}, "adjacent": {"value": "a soft fringed edge without a band", "validity": {"kind": "open"}}}}}`

**2027-05-17 · ef5f16c63ec5dbc818a31**

- User: I have something on my mind about the edge finish on the bath towel.
- Assistant: What would you like to work through first?
- User: Can we get back to the edge finish on the bath towel?  For the everyday situation, please remember that I choose a narrow woven herringbone border. Make that the standing arrangement from this point ahead.
- Assistant: Is how the edge sits on the rail part of what you want to work out?
- User: I am thinking about what will hold up after a few outings.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"bath-towel border style": {"general": "a narrow woven herringbone border", "exceptions": {"focus": {"value": "a soft fringed edge without a band", "validity": {"kind": "open"}}, "adjacent": {"value": "a soft fringed edge without a band", "validity": {"kind": "open"}}}}}`

**2027-05-18 · e11f7b46a956071b3a946**

- User: I remembered something about the edge finish on the bath towel while thinking about whether the fringe catches on the hook.
- Assistant: Was something about whether the fringe catches on the hook especially important?
- User: Here's what I meant about the edge finish on the bath towel.  Regarding my usual default outside exceptions, I am going for a doubled terry border with rounded corners. Next time, and after that, I still want this choice.
- Assistant: I see why this could come up while thinking about whether the fringe catches on the hook.
- User: I use the edge to tell which towel is which in a stack.
- Assistant: Would you prefer to talk more about whether the fringe catches on the hook another time?
- User: Sure, there’s no need to get into it further right now.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a soft fringed edge without a band", "validity": {"kind": "open"}}, "adjacent": {"value": "a soft fringed edge without a band", "validity": {"kind": "open"}}}}}`

**2027-05-20 · e553269202fa518d4ca86**

- User: I thought again about the edge finish on the bath towel.  We can work out this single occurrence of drying the towel over a bar without choosing for another one.
- Assistant: Is how the edge sits on the rail part of what you want to work out?
- User: I use the edge to tell which towel is which in a stack.
- Assistant: What feels right to you?
- User: For me it'd be a narrow woven herringbone border.
- Assistant: Are you happy to stop there about how the edge sits on the rail?
- User: That'll do. I'm happy with my choice.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"bath-towel border style": {"general": "a doubled terry border with rounded corners", "exceptions": {"focus": {"value": "a soft fringed edge without a band", "validity": {"kind": "open"}}, "adjacent": {"value": "a soft fringed edge without a band", "validity": {"kind": "open"}}}}}`
- target QA: Pick a value for bath-towel border style, dated May 20, with the setting described as towels hung across a rail. Options: a narrow woven herringbone border / a soft fringed edge without a band / a doubled terry border with rounded corners / a broad flat linen border. Gold: **a soft fringed edge without a band**.
- default QA: Pick a value for bath-towel border style, dated May 20, with the setting described as an ordinary occasion. Options: a doubled terry border with rounded corners / a narrow woven herringbone border / a soft fringed edge without a band / a broad flat linen border. Gold: **a doubled terry border with rounded corners**.
- neighbor QA: Pick a value for bath-towel border style, dated May 20, with the setting described as towels hung on a wall hook. Options: a soft fringed edge without a band / a doubled terry border with rounded corners / a narrow woven herringbone border / a broad flat linen border. Gold: **a soft fringed edge without a band**.

### te-0067 · test-figure-caption-alignment

Contrast group: `None`

Initial state: `{"figure caption alignment": {"general": "captions indented beneath the figure center", "exceptions": {"adjacent": {"value": "captions centered under the figure", "validity": {"kind": "persistent"}}}}}`

**2027-04-02 · eae7fedf1bbf358a5d001**

- User: I have something on my mind about where the caption sits.
- Assistant: Was something about how much room the caption needs to the right especially important?
- User: Can we get back to where the caption sits?  The remark I heard was, "When normal use in general comes up, my choice is captions flush with the figure's left edge. Keep it in place for recurring occasions of this sort." It is a secondhand account, not a new preference of my own.
- Gold: stable_preference / resolved; evidence message 3. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"figure caption alignment": {"general": "captions indented beneath the figure center", "exceptions": {"adjacent": {"value": "captions centered under the figure", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for figure caption alignment, dated April 2, with the setting described as captions under square illustrations. Options: captions centered under the figure / captions flush with the figure's left edge / captions indented beneath the figure center / captions aligned to a narrow right column. Gold: **captions indented beneath the figure center**.
- default QA: Pick a value for figure caption alignment, dated April 2, with the setting described as an ordinary occasion. Options: captions indented beneath the figure center / captions flush with the figure's left edge / captions aligned to a narrow right column / captions centered under the figure. Gold: **captions indented beneath the figure center**.
- neighbor QA: Pick a value for figure caption alignment, dated April 2, with the setting described as captions under wide illustrations. Options: captions flush with the figure's left edge / captions centered under the figure / captions indented beneath the figure center / captions aligned to a narrow right column. Gold: **captions centered under the figure**.

**2027-04-03 · e974337152240e5a35d8d**

- User: Here's what I meant about where the caption sits.  I cannot pin down whether this idea of captions flush with the figure's left edge goes with captions under square illustrations or labeling a picture that's wider than it is tall.
- Assistant: How did keeping the caption visually close to the picture get on your mind?
- User: I care about whether the reader can follow the marks.
- Gold: clarify / clarify; evidence message 1. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"figure caption alignment": {"general": "captions indented beneath the figure center", "exceptions": {"adjacent": {"value": "captions centered under the figure", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for figure caption alignment, dated April 3, with the setting described as captions under square illustrations. Options: captions flush with the figure's left edge / captions centered under the figure / captions indented beneath the figure center / captions aligned to a narrow right column. Gold: **captions indented beneath the figure center**.
- default QA: Pick a value for figure caption alignment, dated April 3, with the setting described as an ordinary occasion. Options: captions flush with the figure's left edge / captions aligned to a narrow right column / captions centered under the figure / captions indented beneath the figure center. Gold: **captions indented beneath the figure center**.
- neighbor QA: Pick a value for figure caption alignment, dated April 3, with the setting described as captions under wide illustrations. Options: captions indented beneath the figure center / captions centered under the figure / captions flush with the figure's left edge / captions aligned to a narrow right column. Gold: **captions centered under the figure**.

**2027-04-04 · ee44dcf34c86bdef94eff**

- User: I thought about where the caption sits again this morning.
- Assistant: Was something about seeing which figure a line belongs to especially important?
- User: I thought again about figure caption alignment.  Regarding labeling a picture that's wider than it is tall, I am going for caption lined up to the left of the figure. This should carry on; it is not just a test. Anything outside this request keeps the choices it already had.
- Assistant: Could you say why seeing which figure a line belongs to matters to you?
- User: I want each line of text to look connected to the right picture.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"figure caption alignment": {"general": "captions indented beneath the figure center", "exceptions": {"adjacent": {"value": "captions flush with the figure's left edge", "validity": {"kind": "persistent"}}}}}`

**2027-04-06 · eb8897a23fc97489d7566**

- User: There was one thing about where the caption sits I wanted to talk through.
- Assistant: What do you tend to notice first about keeping the caption visually close to the picture?
- User: I want each line of text to look connected to the right picture.
- Assistant: I'm listening. What's on your mind?
- User: Can we get back to where the caption sits?  It is captions aligned to a narrow right column that I want for captions under wide illustrations. I mean an enduring arrangement rather than a one-off.
- Gold: exception_revision / resolved; evidence message 5. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"figure caption alignment": {"general": "captions indented beneath the figure center", "exceptions": {"adjacent": {"value": "captions aligned to a narrow right column", "validity": {"kind": "persistent"}}}}}`

### te-0091 · test-museum-visit-starting-point

Contrast group: `None`

Initial state: `{"museum visit starting point": {"general": "starting with the oldest display", "exceptions": {"adjacent": {"value": "starting with the newest acquisition", "validity": {"kind": "persistent"}}}}}`

**2027-12-03 · ee838a1f16067501e9360**

- User: I have something on my mind about which part of the exhibition I see first.
- Assistant: Was something about the displays nearest the stairs especially important?
- User: Can we get back to museum visit starting point?  I am settling the question of a museum ticket for the lower floor with the installation in the center comes first. I am not putting an end date on this preference.
- Gold: scoped_exception / resolved; evidence message 3. The user chooses a continuing setting for the named situation.
- After: `{"museum visit starting point": {"general": "starting with the oldest display", "exceptions": {"adjacent": {"value": "starting with the newest acquisition", "validity": {"kind": "persistent"}}, "focus": {"value": "starting with the central installation", "validity": {"kind": "persistent"}}}}}`

**2027-12-04 · ef4aa39e23dbd7e3a18cf**

- User: I remembered something about which part of the exhibition I see first while thinking about what there is time to see first.
- Assistant: Was something about what there is time to see first especially important?
- User: I thought again about museum visit starting point.  The special case for museum visits on a ground-floor ticket can go. I want those occasions to use the ordinary choice from here ahead.
- Assistant: How did what there is time to see first get on your mind?
- User: It helps me to pick a starting point before I get caught up looking around.
- Assistant: Is there anything about how to begin walking around the exhibition we haven’t touched on?
- User: Nothing I wanted to get into this time.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"museum visit starting point": {"general": "starting with the oldest display", "exceptions": {"adjacent": {"value": "starting with the newest acquisition", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for museum visit starting point, dated December 4, with the setting described as museum visits on a ground-floor ticket. Options: starting with the smallest gallery / starting with the oldest display / starting with the newest acquisition / starting with the central installation. Gold: **starting with the oldest display**.
- default QA: Pick a value for museum visit starting point, dated December 4, with the setting described as an ordinary occasion. Options: starting with the central installation / starting with the smallest gallery / starting with the oldest display / starting with the newest acquisition. Gold: **starting with the oldest display**.
- neighbor QA: Pick a value for museum visit starting point, dated December 4, with the setting described as museum visits on an upper-floor ticket. Options: starting with the newest acquisition / starting with the oldest display / starting with the central installation / starting with the smallest gallery. Gold: **starting with the newest acquisition**.

**2027-12-05 · ef000b8c90d9942a2f670**

- User: There was one thing about which part of the exhibition I see first I wanted to talk through.
- Assistant: How have you been thinking about it?
- User: Can we get back to which part of the exhibition I see first?  What if someone said, "The option I am selecting where museum visits on a ground-floor ticket is concerned is starting with the newest acquisition. It is meant to last beyond the occasion in front of us."? I mean an imaginary situation, not an actual request from me.
- Gold: stable_preference / resolved; evidence message 3. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"museum visit starting point": {"general": "starting with the oldest display", "exceptions": {"adjacent": {"value": "starting with the newest acquisition", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for museum visit starting point, dated December 5, with the setting described as museum visits on a ground-floor ticket. Options: starting with the newest acquisition / starting with the smallest gallery / starting with the central installation / starting with the oldest display. Gold: **starting with the oldest display**.
- default QA: Pick a value for museum visit starting point, dated December 5, with the setting described as an ordinary occasion. Options: starting with the newest acquisition / starting with the smallest gallery / starting with the central installation / starting with the oldest display. Gold: **starting with the oldest display**.
- neighbor QA: Pick a value for museum visit starting point, dated December 5, with the setting described as museum visits on an upper-floor ticket. Options: starting with the oldest display / starting with the smallest gallery / starting with the newest acquisition / starting with the central installation. Gold: **starting with the newest acquisition**.

**2027-12-07 · e63c08e1f13f78ca7fc2e**

- User: I thought again about which part of the exhibition I see first.  I would like a museum ticket to the level upstairs to stop being an exception and simply follow my general preference.
- Assistant: What's your impression of what there is time to see first so far?
- User: It helps me to pick a starting point before I get caught up looking around.
- Gold: exception_retirement / resolved; evidence message 1. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"museum visit starting point": {"general": "starting with the oldest display", "exceptions": {}}}`
- target QA: Pick a value for museum visit starting point, dated December 7, with the setting described as museum visits on an upper-floor ticket. Options: starting with the oldest display / starting with the smallest gallery / starting with the newest acquisition / starting with the central installation. Gold: **starting with the oldest display**.
- default QA: Pick a value for museum visit starting point, dated December 7, with the setting described as an ordinary occasion. Options: starting with the newest acquisition / starting with the smallest gallery / starting with the central installation / starting with the oldest display. Gold: **starting with the oldest display**.
- neighbor QA: Pick a value for museum visit starting point, dated December 7, with the setting described as museum visits on a ground-floor ticket. Options: starting with the oldest display / starting with the central installation / starting with the smallest gallery / starting with the newest acquisition. Gold: **starting with the oldest display**.

### te-0009 · test-ferry-trip-keepsake

Contrast group: `te-pair-0043`

Initial state: `{"ferry-trip keepsake": {"general": "a tiny sketch of the wake", "exceptions": {"adjacent": {"value": "a written note about the crossing sounds", "validity": {"kind": "persistent"}}}}}`

**2027-03-08 · e37fd44a04a88048a83f1**

- User: Can we get back to what I keep from the crossing?  When ferry trips made with a camera comes up, my choice is a pencil rubbing of the ticket stamp. I am not putting an end date on this preference.
- Assistant: What would make what you can bring home in a pocket easier to deal with?
- User: I like having something small I can stumble across months later.
- Gold: exception_revision / resolved; evidence message 1. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"ferry-trip keepsake": {"general": "a tiny sketch of the wake", "exceptions": {"adjacent": {"value": "a pencil rubbing of the ticket stamp", "validity": {"kind": "persistent"}}}}}`

**2027-03-09 · eff16dd721f66912f5418**

- User: I remembered something about what I keep from the crossing while thinking about what you can bring home in a pocket.
- Assistant: Was something about what you can bring home in a pocket especially important?
- User: Can we get back to what I keep from the crossing?  I have not sorted out the intended setting for a scrap of the boat leaflet pressed flat. Ferry trips made with a camera and crossing by ferry without taking a camera are the possibilities.
- Assistant: There's room to talk more about what you can bring home in a pocket if you want.
- User: I like having something small I can stumble across months later.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"ferry-trip keepsake": {"general": "a tiny sketch of the wake", "exceptions": {"adjacent": {"value": "a pencil rubbing of the ticket stamp", "validity": {"kind": "persistent"}}}}}`

**2027-03-11 · ed49c48e14075baffaf2d**

- User: I remembered something about what I keep from the crossing while thinking about noticing details on the crossing.
- Assistant: How have you been thinking about it?
- User: Can we get back to what I keep from the crossing?  Given ferry trips made without a camera, make the choice a pressed scrap from the onboard leaflet. The request covers March 11 and continues through March 31; then my normal preference takes over.
- Assistant: I see why this could come up while thinking about noticing details on the crossing.
- User: I like having something small I can stumble across months later.
- Gold: scoped_exception / resolved; evidence message 3. The user chooses a continuing setting for the named situation.
- After: `{"ferry-trip keepsake": {"general": "a tiny sketch of the wake", "exceptions": {"adjacent": {"value": "a pencil rubbing of the ticket stamp", "validity": {"kind": "persistent"}}, "focus": {"value": "a pressed scrap from the onboard leaflet", "validity": {"kind": "window", "from": "2027-03-11", "to": "2027-03-31"}}}}}`
- target QA: Pick a value for ferry-trip keepsake, dated March 11, with the setting described as ferry trips made without a camera. Options: a written note about the crossing sounds / a pressed scrap from the onboard leaflet / a pencil rubbing of the ticket stamp / a tiny sketch of the wake. Gold: **a pressed scrap from the onboard leaflet**.
- default QA: Pick a value for ferry-trip keepsake, dated March 11, with the setting described as an ordinary occasion. Options: a pressed scrap from the onboard leaflet / a tiny sketch of the wake / a pencil rubbing of the ticket stamp / a written note about the crossing sounds. Gold: **a tiny sketch of the wake**.
- neighbor QA: Pick a value for ferry-trip keepsake, dated March 11, with the setting described as ferry trips made with a camera. Options: a written note about the crossing sounds / a pencil rubbing of the ticket stamp / a tiny sketch of the wake / a pressed scrap from the onboard leaflet. Gold: **a pencil rubbing of the ticket stamp**.
- target QA: Pick a value for ferry-trip keepsake, dated March 31, with the setting described as ferry trips made without a camera. Options: a written note about the crossing sounds / a pressed scrap from the onboard leaflet / a pencil rubbing of the ticket stamp / a tiny sketch of the wake. Gold: **a pressed scrap from the onboard leaflet**.
- boundary QA: Pick a value for ferry-trip keepsake, dated April 1, with the setting described as ferry trips made without a camera. Options: a pressed scrap from the onboard leaflet / a tiny sketch of the wake / a pencil rubbing of the ticket stamp / a written note about the crossing sounds. Gold: **a tiny sketch of the wake**.

**2027-03-12 · e59a7f70408e6853caaa5**

- User: Here's what I meant about what I keep from the crossing.  There is nothing to keep apart for ferry trips made without a camera anymore. I want it to follow whatever I choose for other occasions.
- Assistant: What's your impression of what you can bring home in a pocket so far?
- User: I want the arrival to take a little less effort.
- Gold: exception_retirement / resolved; evidence message 1. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"ferry-trip keepsake": {"general": "a tiny sketch of the wake", "exceptions": {"adjacent": {"value": "a pencil rubbing of the ticket stamp", "validity": {"kind": "persistent"}}}}}`

**2027-03-14 · e6d0daa568cef2afc0b57**

- User: I thought about what I keep from the crossing again this morning.
- Assistant: How have you been thinking about it?
- User: I thought again about what I keep from the crossing.  Here is where I have landed: a scrap of the boat leaflet pressed flat, for crossing by ferry with my camera. This should carry on; it is not just a test.
- Assistant: Is what you can bring home in a pocket part of what you want to work out?
- User: I like having something small I can stumble across months later.
- Gold: exception_revision / resolved; evidence message 3. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"ferry-trip keepsake": {"general": "a tiny sketch of the wake", "exceptions": {"adjacent": {"value": "a pressed scrap from the onboard leaflet", "validity": {"kind": "persistent"}}}}}`

**2027-03-15 · ebd41c956d9c14fd26316**

- User: I thought again about what I keep from the crossing.  For ferry trips made without a camera, what I pick here applies once and then I'm back to what I've been doing.
- Assistant: What's your impression of noticing details on the crossing so far?
- User: I like having something small I can stumble across months later.
- Assistant: What's the choice you'd make?
- User: I'd choose a pencil rubbing of the ticket stamp, I think.
- Assistant: Are you happy to stop there about noticing details on the crossing?
- User: That'll do. I'm happy with my choice.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"ferry-trip keepsake": {"general": "a tiny sketch of the wake", "exceptions": {"adjacent": {"value": "a pressed scrap from the onboard leaflet", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for ferry-trip keepsake, dated March 15, with the setting described as ferry trips made without a camera. Options: a pencil rubbing of the ticket stamp / a written note about the crossing sounds / a tiny sketch of the wake / a pressed scrap from the onboard leaflet. Gold: **a tiny sketch of the wake**.
- default QA: Pick a value for ferry-trip keepsake, dated March 15, with the setting described as an ordinary occasion. Options: a tiny sketch of the wake / a pressed scrap from the onboard leaflet / a pencil rubbing of the ticket stamp / a written note about the crossing sounds. Gold: **a tiny sketch of the wake**.
- neighbor QA: Pick a value for ferry-trip keepsake, dated March 15, with the setting described as ferry trips made with a camera. Options: a written note about the crossing sounds / a pencil rubbing of the ticket stamp / a tiny sketch of the wake / a pressed scrap from the onboard leaflet. Gold: **a pressed scrap from the onboard leaflet**.

### te-0118 · test-lodging-unpacking-routine

Contrast group: `te-pair-0060`

Initial state: `{"lodging unpacking routine": {"general": "clothes hung immediately on arrival", "exceptions": {"focus": {"value": "clothes kept in labeled packing rolls", "validity": {"kind": "persistent"}}}}}`

**2027-01-07 · e2e5874f68ddfbcc3dbd3**

- User: I remembered something about what I do with clothes when I arrive while thinking about getting changed on arrival.
- Assistant: I'm listening. What's on your mind?
- User: Can we get back to what I do with clothes when I arrive?  The plan involving stacking folded clothes on the luggage shelf is not complete. I still need to settle whether it is about lodgings used for several nights or checking in for one night.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"lodging unpacking routine": {"general": "clothes hung immediately on arrival", "exceptions": {"focus": {"value": "clothes kept in labeled packing rolls", "validity": {"kind": "persistent"}}}}}`

**2027-01-09 · eb86c68c1c4bbf2aaf1fc**

- User: I had a point to make about what I do with clothes when I arrive. Stacking folded clothes on the luggage shelf is the one I want when we are talking about lodgings used for several nights. I want it for the full period January 9 through January 31, not before or afterward.
- Assistant: How did what will crease if left folded get on your mind?
- User: I want the arrival to take a little less effort.
- Gold: scoped_exception / resolved; evidence message 1. The user settles the earlier choice of situation and supplies a continuing instruction for it.
- After: `{"lodging unpacking routine": {"general": "clothes hung immediately on arrival", "exceptions": {"focus": {"value": "clothes kept in labeled packing rolls", "validity": {"kind": "persistent"}}, "adjacent": {"value": "clothes folded on an open luggage shelf", "validity": {"kind": "window", "from": "2027-01-09", "to": "2027-01-31"}}}}}`
- target QA: Pick a value for lodging unpacking routine, dated January 9, with the setting described as lodgings used for several nights. Options: clothes arranged in a shallow drawer / clothes kept in labeled packing rolls / clothes folded on an open luggage shelf / clothes hung immediately on arrival. Gold: **clothes folded on an open luggage shelf**.
- default QA: Pick a value for lodging unpacking routine, dated January 9, with the setting described as an ordinary occasion. Options: clothes arranged in a shallow drawer / clothes folded on an open luggage shelf / clothes hung immediately on arrival / clothes kept in labeled packing rolls. Gold: **clothes hung immediately on arrival**.
- neighbor QA: Pick a value for lodging unpacking routine, dated January 9, with the setting described as lodgings used for a single night. Options: clothes folded on an open luggage shelf / clothes arranged in a shallow drawer / clothes hung immediately on arrival / clothes kept in labeled packing rolls. Gold: **clothes kept in labeled packing rolls**.
- target QA: Pick a value for lodging unpacking routine, dated January 31, with the setting described as lodgings used for several nights. Options: clothes arranged in a shallow drawer / clothes folded on an open luggage shelf / clothes hung immediately on arrival / clothes kept in labeled packing rolls. Gold: **clothes folded on an open luggage shelf**.
- boundary QA: Pick a value for lodging unpacking routine, dated February 1, with the setting described as lodgings used for several nights. Options: clothes kept in labeled packing rolls / clothes folded on an open luggage shelf / clothes arranged in a shallow drawer / clothes hung immediately on arrival. Gold: **clothes hung immediately on arrival**.

**2027-01-11 · efda823ce8518f4283048**

- User: What will crease if left folded has been on my mind. Can we get back to what I do with clothes when I arrive?
- Assistant: Of course. We can talk about what will crease if left folded.
- User: Can we get back to what I do with clothes when I arrive?  I want checking in for more than one night covered by my general arrangement again, not by an instruction of its own.
- Assistant: I can see how what will crease if left folded could make a difference.
- User: I would rather not look for the same shirt twice after checking in.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"lodging unpacking routine": {"general": "clothes hung immediately on arrival", "exceptions": {"focus": {"value": "clothes kept in labeled packing rolls", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for lodging unpacking routine, dated January 11, with the setting described as lodgings used for several nights. Options: clothes hung immediately on arrival / clothes arranged in a shallow drawer / clothes kept in labeled packing rolls / clothes folded on an open luggage shelf. Gold: **clothes hung immediately on arrival**.
- default QA: Pick a value for lodging unpacking routine, dated January 11, with the setting described as an ordinary occasion. Options: clothes kept in labeled packing rolls / clothes arranged in a shallow drawer / clothes hung immediately on arrival / clothes folded on an open luggage shelf. Gold: **clothes hung immediately on arrival**.
- neighbor QA: Pick a value for lodging unpacking routine, dated January 11, with the setting described as lodgings used for a single night. Options: clothes folded on an open luggage shelf / clothes kept in labeled packing rolls / clothes arranged in a shallow drawer / clothes hung immediately on arrival. Gold: **clothes kept in labeled packing rolls**.

**2027-01-13 · e0fab48d202b8c495c377**

- User: Here's what I meant about what I do with clothes when I arrive.  Clothes arranged in a shallow drawer is the one I want when we are talking about lodgings used for several nights. This temporary spell runs from the start of January 13 to the end of February 1. Anything outside this request keeps the choices it already had.
- Assistant: How did what will crease if left folded get on your mind?
- User: I would rather not look for the same shirt twice after checking in.
- Gold: scoped_exception / resolved; evidence message 1. The user chooses a continuing setting for the named situation.
- After: `{"lodging unpacking routine": {"general": "clothes hung immediately on arrival", "exceptions": {"focus": {"value": "clothes kept in labeled packing rolls", "validity": {"kind": "persistent"}}, "adjacent": {"value": "clothes arranged in a shallow drawer", "validity": {"kind": "window", "from": "2027-01-13", "to": "2027-02-01"}}}}}`
- target QA: Pick a value for lodging unpacking routine, dated January 13, with the setting described as lodgings used for several nights. Options: clothes folded on an open luggage shelf / clothes kept in labeled packing rolls / clothes arranged in a shallow drawer / clothes hung immediately on arrival. Gold: **clothes arranged in a shallow drawer**.
- default QA: Pick a value for lodging unpacking routine, dated January 13, with the setting described as an ordinary occasion. Options: clothes arranged in a shallow drawer / clothes folded on an open luggage shelf / clothes kept in labeled packing rolls / clothes hung immediately on arrival. Gold: **clothes hung immediately on arrival**.
- neighbor QA: Pick a value for lodging unpacking routine, dated January 13, with the setting described as lodgings used for a single night. Options: clothes kept in labeled packing rolls / clothes hung immediately on arrival / clothes folded on an open luggage shelf / clothes arranged in a shallow drawer. Gold: **clothes kept in labeled packing rolls**.
- target QA: Pick a value for lodging unpacking routine, dated February 1, with the setting described as lodgings used for several nights. Options: clothes kept in labeled packing rolls / clothes folded on an open luggage shelf / clothes hung immediately on arrival / clothes arranged in a shallow drawer. Gold: **clothes arranged in a shallow drawer**.
- boundary QA: Pick a value for lodging unpacking routine, dated February 2, with the setting described as lodgings used for several nights. Options: clothes hung immediately on arrival / clothes arranged in a shallow drawer / clothes folded on an open luggage shelf / clothes kept in labeled packing rolls. Gold: **clothes hung immediately on arrival**.

**2027-01-14 · e9ec7213d764c6ca3286a**

- User: Can we get back to what I do with clothes when I arrive?  I want to choose what I'll keep doing for lodgings used for a single night, not just on the next occasion.
- Assistant: Could you say why what will crease if left folded matters to you?
- User: I would rather not look for the same shirt twice after checking in.
- Assistant: What feels right to you?
- User: For me it'd be stacking folded clothes on the luggage shelf.
- Assistant: That gives us enough to go on for now.
- User: That'll do. I'm happy with my choice.
- Gold: exception_revision / resolved; evidence message 5. The user chooses a continuing replacement for the existing situation rule.
- After: `{"lodging unpacking routine": {"general": "clothes hung immediately on arrival", "exceptions": {"focus": {"value": "clothes folded on an open luggage shelf", "validity": {"kind": "persistent"}}, "adjacent": {"value": "clothes arranged in a shallow drawer", "validity": {"kind": "window", "from": "2027-01-13", "to": "2027-02-01"}}}}}`
- target QA: Pick a value for lodging unpacking routine, dated January 14, with the setting described as lodgings used for a single night. Options: clothes folded on an open luggage shelf / clothes arranged in a shallow drawer / clothes hung immediately on arrival / clothes kept in labeled packing rolls. Gold: **clothes folded on an open luggage shelf**.
- default QA: Pick a value for lodging unpacking routine, dated January 14, with the setting described as an ordinary occasion. Options: clothes hung immediately on arrival / clothes kept in labeled packing rolls / clothes folded on an open luggage shelf / clothes arranged in a shallow drawer. Gold: **clothes hung immediately on arrival**.
- neighbor QA: Pick a value for lodging unpacking routine, dated January 14, with the setting described as lodgings used for several nights. Options: clothes folded on an open luggage shelf / clothes arranged in a shallow drawer / clothes hung immediately on arrival / clothes kept in labeled packing rolls. Gold: **clothes arranged in a shallow drawer**.

### te-0112 · test-floor-exercise-head-support

Contrast group: `None`

Initial state: `{"floor exercise head support": {"general": "a thin flat wool pad", "exceptions": {"adjacent": {"value": "a small crescent-shaped foam rest", "validity": {"kind": "open"}}, "focus": {"value": "a soft rolled fleece support", "validity": {"kind": "persistent"}}}}}`

**2027-06-04 · e19a4d066b4a3d44a6653**

- User: I thought again about floor exercise head support.  I nearly asked, "Keep a cotton towel folded flat under my head in mind as the choice I am making for the usual situation. Next time, and after that, I still want this choice." I have thought better of it. Keep the preferences we already had.
- Assistant: Have you been noticing anything new about whether a pad shifts on a bare floor?
- User: I am judging that part once my body gets moving.
- Gold: stable_preference / resolved; evidence message 1. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"floor exercise head support": {"general": "a thin flat wool pad", "exceptions": {"adjacent": {"value": "a small crescent-shaped foam rest", "validity": {"kind": "open"}}, "focus": {"value": "a soft rolled fleece support", "validity": {"kind": "persistent"}}}}}`

**2027-06-06 · ea6123fab1dacd73cdaf3**

- User: Getting comfortable while staying level has been on my mind. Can we get back to what goes under my head on the floor?
- Assistant: Feel free to start with whatever's most useful.
- User: Here's what I meant about what goes under my head on the floor.  I like the sound of a soft rolled fleece support. I’m still weighing floor practice on uncarpeted flooring against doing the exercises on a carpet.
- Assistant: How did getting comfortable while staying level get on your mind?
- User: It changes how the next repetition feels.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"floor exercise head support": {"general": "a thin flat wool pad", "exceptions": {"adjacent": {"value": "a small crescent-shaped foam rest", "validity": {"kind": "open"}}, "focus": {"value": "a soft rolled fleece support", "validity": {"kind": "persistent"}}}}}`

**2027-06-07 · edb8b1e255b81707acc48**

- User: Can we get back to floor exercise head support?  The answer for floor practice on uncarpeted flooring, as far as I am concerned, is a soft rolled fleece support. I need it for a while rather than once, and rather than forever. No end is fixed.
- Assistant: There's room to talk more about whether a pad shifts on a bare floor if you want.
- User: I want to be able to keep the movement going comfortably.
- Gold: exception_revision / resolved; evidence message 1. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"floor exercise head support": {"general": "a thin flat wool pad", "exceptions": {"adjacent": {"value": "a soft rolled fleece support", "validity": {"kind": "open"}}, "focus": {"value": "a soft rolled fleece support", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for floor exercise head support, dated June 7, with the setting described as floor practice on uncarpeted flooring. Options: a low folded cotton towel / a thin flat wool pad / a soft rolled fleece support / a small crescent-shaped foam rest. Gold: **a soft rolled fleece support**.
- default QA: Pick a value for floor exercise head support, dated June 7, with the setting described as an ordinary occasion. Options: a low folded cotton towel / a small crescent-shaped foam rest / a soft rolled fleece support / a thin flat wool pad. Gold: **a thin flat wool pad**.
- neighbor QA: Pick a value for floor exercise head support, dated June 7, with the setting described as floor practice on carpeted flooring. Options: a low folded cotton towel / a soft rolled fleece support / a thin flat wool pad / a small crescent-shaped foam rest. Gold: **a soft rolled fleece support**.

**2027-06-08 · e70059703e2c6023ba2d8**

- User: I've got a minute now to explain what I mean about what goes under my head on the floor.
- Assistant: Of course. We can talk about how much the head support raises you.
- User: I thought again about what goes under my head on the floor.  I nearly asked, "Undo the separate arrangement we gave floor practice on carpeted flooring; my everyday preference is what should govern it again." I have thought better of it. Keep the preferences we already had.
- Gold: stable_preference / resolved; evidence message 3. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"floor exercise head support": {"general": "a thin flat wool pad", "exceptions": {"adjacent": {"value": "a soft rolled fleece support", "validity": {"kind": "open"}}, "focus": {"value": "a soft rolled fleece support", "validity": {"kind": "persistent"}}}}}`

**2027-06-09 · ea29194faa5f12fe42b40**

- User: Whether a pad shifts on a bare floor has been on my mind. Can we get back to what goes under my head on the floor?
- Assistant: I'm listening. What's on your mind?
- User: I had a point to make about what goes under my head on the floor. Given floor practice on carpeted flooring, make the choice a small crescent-shaped foam rest. I mean an enduring arrangement rather than a one-off. Anything outside this request keeps the choices it already had.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"floor exercise head support": {"general": "a thin flat wool pad", "exceptions": {"adjacent": {"value": "a soft rolled fleece support", "validity": {"kind": "open"}}, "focus": {"value": "a small crescent-shaped foam rest", "validity": {"kind": "persistent"}}}}}`

**2027-06-11 · ecee31e3d89c95f64d072**

- User: There was one thing about what goes under my head on the floor I wanted to talk through.
- Assistant: Did you want to say what you had in mind?
- User: Can we get back to what goes under my head on the floor?  I could be talking about doing the exercises on a carpet or doing the exercises on a bare floor when I mention a soft rolled fleece support; that part is genuinely undecided.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"floor exercise head support": {"general": "a thin flat wool pad", "exceptions": {"adjacent": {"value": "a soft rolled fleece support", "validity": {"kind": "open"}}, "focus": {"value": "a small crescent-shaped foam rest", "validity": {"kind": "persistent"}}}}}`

**2027-06-12 · e9df0450d75a2bc3f1c7c**

- User: There was one thing about what goes under my head on the floor I wanted to talk through.
- Assistant: I'm curious about getting comfortable while staying level, too.
- User: If it raises my head too much I end up adjusting it between movements.
- Assistant: I'm listening. What's on your mind?
- User: Here's what I meant about what goes under my head on the floor.  A soft fleece roll is the one I want when we are talking about doing the exercises on a carpet. That goes for the occasions ahead, with no finishing point.
- Gold: exception_revision / resolved; evidence message 5. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"floor exercise head support": {"general": "a thin flat wool pad", "exceptions": {"adjacent": {"value": "a soft rolled fleece support", "validity": {"kind": "open"}}, "focus": {"value": "a soft rolled fleece support", "validity": {"kind": "persistent"}}}}}`

**2027-06-14 · e68d0c72add9e211f54d8**

- User: I had a point to make about what goes under my head on the floor. Regarding doing the exercises on a bare floor, I am going for a cotton towel folded flat under my head. I have no calendar date for stopping this temporary run of the choice. Anything outside this request keeps the choices it already had.
- Assistant: What's your impression of getting comfortable while staying level so far?
- User: If it raises my head too much I end up adjusting it between movements.
- Assistant: We can leave whether a pad shifts on a bare floor there if you like.
- User: Let’s do that. That’s all I meant to bring up.
- Gold: exception_revision / resolved; evidence message 1. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"floor exercise head support": {"general": "a thin flat wool pad", "exceptions": {"adjacent": {"value": "a low folded cotton towel", "validity": {"kind": "open"}}, "focus": {"value": "a soft rolled fleece support", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for floor exercise head support, dated June 14, with the setting described as floor practice on uncarpeted flooring. Options: a small crescent-shaped foam rest / a thin flat wool pad / a soft rolled fleece support / a low folded cotton towel. Gold: **a low folded cotton towel**.
- default QA: Pick a value for floor exercise head support, dated June 14, with the setting described as an ordinary occasion. Options: a low folded cotton towel / a thin flat wool pad / a small crescent-shaped foam rest / a soft rolled fleece support. Gold: **a thin flat wool pad**.
- neighbor QA: Pick a value for floor exercise head support, dated June 14, with the setting described as floor practice on carpeted flooring. Options: a small crescent-shaped foam rest / a thin flat wool pad / a soft rolled fleece support / a low folded cotton towel. Gold: **a soft rolled fleece support**.

### te-0039 · test-museum-visit-starting-point

Contrast group: `te-pair-0044`

Initial state: `{"museum visit starting point": {"general": "starting with the smallest gallery", "exceptions": {"focus": {"value": "starting with the oldest display", "validity": {"kind": "persistent"}}, "adjacent": {"value": "starting with the newest acquisition", "validity": {"kind": "open"}}}}}`

**2027-01-09 · e652f41b6b7adeedfea14**

- User: How to begin walking around the exhibition has been on my mind. Can we get back to which part of the exhibition I see first?
- Assistant: I'm listening. What's on your mind?
- User: Here's what I meant about which part of the exhibition I see first.  Do not put starting with the central installation anywhere yet. I have not answered whether it is for museum visits on an upper-floor ticket or museum visits on a ground-floor ticket.
- Assistant: Did something in particular draw your attention to how to begin walking around the exhibition?
- User: It helps me to pick a starting point before I get caught up looking around.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"museum visit starting point": {"general": "starting with the smallest gallery", "exceptions": {"focus": {"value": "starting with the oldest display", "validity": {"kind": "persistent"}}, "adjacent": {"value": "starting with the newest acquisition", "validity": {"kind": "open"}}}}}`
- target QA: Pick a value for museum visit starting point, dated January 9, with the setting described as museum visits on an upper-floor ticket. Options: starting with the central installation / starting with the oldest display / starting with the newest acquisition / starting with the smallest gallery. Gold: **starting with the newest acquisition**.
- default QA: Pick a value for museum visit starting point, dated January 9, with the setting described as an ordinary occasion. Options: starting with the oldest display / starting with the central installation / starting with the newest acquisition / starting with the smallest gallery. Gold: **starting with the smallest gallery**.
- neighbor QA: Pick a value for museum visit starting point, dated January 9, with the setting described as museum visits on a ground-floor ticket. Options: starting with the oldest display / starting with the central installation / starting with the newest acquisition / starting with the smallest gallery. Gold: **starting with the oldest display**.

**2027-01-10 · ec83df1c314bd4072855c**

- User: Can we get back to which part of the exhibition I see first?  Take away the choice dedicated to museum visits on a ground-floor ticket, leaving the usual arrangement to apply there.
- Assistant: What would make how to begin walking around the exhibition easier to deal with?
- User: It helps me to pick a starting point before I get caught up looking around.
- Assistant: Would you prefer to talk more about how to begin walking around the exhibition another time?
- User: Sure, there’s no need to get into it further right now.
- Gold: exception_retirement / resolved; evidence message 1. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"museum visit starting point": {"general": "starting with the smallest gallery", "exceptions": {"adjacent": {"value": "starting with the newest acquisition", "validity": {"kind": "open"}}}}}`

**2027-01-12 · ee314814995af1dbe2753**

- User: I thought about which part of the exhibition I see first again this morning.
- Assistant: I'm listening. What's on your mind?
- User: I had a point to make about which part of the exhibition I see first. Use this choice for a museum ticket to the level upstairs: the installation in the center comes first. For the time being, keep using it. The need is temporary, but its duration is unknown.
- Assistant: Have you been noticing anything new about what there is time to see first?
- User: It helps me to pick a starting point before I get caught up looking around.
- Gold: exception_revision / resolved; evidence message 3. The user resolves the earlier uncertainty by choosing the situation with an existing rule.
- After: `{"museum visit starting point": {"general": "starting with the smallest gallery", "exceptions": {"adjacent": {"value": "starting with the central installation", "validity": {"kind": "open"}}}}}`

**2027-01-13 · e1afad3f858459479ee2e**

- User: I've got a minute now to explain what I mean about which part of the exhibition I see first.
- Assistant: Feel free to start with whatever's most useful.
- User: I had a point to make about which part of the exhibition I see first. For the everyday situation, please remember that I choose starting with the oldest display. Next time, and after that, I still want this choice.
- Gold: general_update / resolved; evidence message 3. The user changes their ordinarily selected value, not the separate situation rules.
- After: `{"museum visit starting point": {"general": "starting with the oldest display", "exceptions": {"adjacent": {"value": "starting with the central installation", "validity": {"kind": "open"}}}}}`

**2027-01-14 · e4a70478a5d08ac767a87**

- User: Can we get back to which part of the exhibition I see first?  Here is a hypothetical to think about: "I cannot pin down whether this idea of the tiniest gallery comes first goes with museum visits on a ground-floor ticket or museum visits on an upper-floor ticket." It is not permission to change my preferences.
- Assistant: What's your impression of the displays nearest the stairs so far?
- User: It helps me to pick a starting point before I get caught up looking around.
- Gold: stable_preference / resolved; evidence message 1. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"museum visit starting point": {"general": "starting with the oldest display", "exceptions": {"adjacent": {"value": "starting with the central installation", "validity": {"kind": "open"}}}}}`
- target QA: Pick a value for museum visit starting point, dated January 14, with the setting described as museum visits on a ground-floor ticket. Options: starting with the smallest gallery / starting with the newest acquisition / starting with the oldest display / starting with the central installation. Gold: **starting with the oldest display**.
- default QA: Pick a value for museum visit starting point, dated January 14, with the setting described as an ordinary occasion. Options: starting with the newest acquisition / starting with the smallest gallery / starting with the oldest display / starting with the central installation. Gold: **starting with the oldest display**.
- neighbor QA: Pick a value for museum visit starting point, dated January 14, with the setting described as museum visits on an upper-floor ticket. Options: starting with the smallest gallery / starting with the oldest display / starting with the central installation / starting with the newest acquisition. Gold: **starting with the central installation**.

**2027-01-15 · e57d50d0536daab8dcf0a**

- User: Can we get back to which part of the exhibition I see first?  Whatever I decide for museum visits on a ground-floor ticket now is what I want to carry forward.
- Assistant: Tell me what struck you about the displays nearest the stairs.
- User: It helps me to pick a starting point before I get caught up looking around.
- Assistant: Which sounds most like what you want?
- User: I'd choose the most recently acquired piece comes first, I think.
- Assistant: Are you happy to stop there about the displays nearest the stairs?
- User: Yes, I don't have anything to add.
- Gold: scoped_exception / resolved; evidence message 5. The user chooses a continuing setting for the named situation.
- After: `{"museum visit starting point": {"general": "starting with the oldest display", "exceptions": {"adjacent": {"value": "starting with the central installation", "validity": {"kind": "open"}}, "focus": {"value": "starting with the newest acquisition", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for museum visit starting point, dated January 15, with the setting described as museum visits on a ground-floor ticket. Options: starting with the central installation / starting with the oldest display / starting with the newest acquisition / starting with the smallest gallery. Gold: **starting with the newest acquisition**.
- default QA: Pick a value for museum visit starting point, dated January 15, with the setting described as an ordinary occasion. Options: starting with the newest acquisition / starting with the smallest gallery / starting with the oldest display / starting with the central installation. Gold: **starting with the oldest display**.
- neighbor QA: Pick a value for museum visit starting point, dated January 15, with the setting described as museum visits on an upper-floor ticket. Options: starting with the newest acquisition / starting with the smallest gallery / starting with the oldest display / starting with the central installation. Gold: **starting with the central installation**.

### te-0135 · test-reusable-lunch-pot-nesting

Contrast group: `te-pair-0074`

Initial state: `{"reusable lunch-pot nesting": {"general": "three slim pots clipped side by side", "exceptions": {"adjacent": {"value": "two shallow pots stacked together", "validity": {"kind": "open"}}, "focus": {"value": "a tall pot with a removable inner cup", "validity": {"kind": "persistent"}}}}}`

**2027-02-08 · e41c3a129c0eb1a89ed9e**

- User: Here's what I meant about how the lunch tubs fit together.  Picture me asking, "For lunch pots carried in a narrow bag, please remember that I choose a broad pot holding two small inserts. This should carry on; it is not just a test." This is make-believe; none of my real choices should change.
- Assistant: I can see how what comes out first when you unpack could make a difference.
- User: I want to carry lunch without having containers knock against each other.
- Gold: stable_preference / resolved; evidence message 1. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"reusable lunch-pot nesting": {"general": "three slim pots clipped side by side", "exceptions": {"adjacent": {"value": "two shallow pots stacked together", "validity": {"kind": "open"}}, "focus": {"value": "a tall pot with a removable inner cup", "validity": {"kind": "persistent"}}}}}`

**2027-02-09 · ec8dd2487565e0bcecf0a**

- User: I've got a minute now to explain what I mean about how the lunch tubs fit together.
- Assistant: How have you been thinking about it?
- User: Can we get back to how the lunch tubs fit together?  I would put two shallow pots stacked together first for lunch pots carried in a narrow bag. Next time, and after that, I still want this choice.
- Assistant: I see why this could come up while thinking about stopping the little cup from rattling.
- User: I want to carry lunch without having containers knock against each other.
- Assistant: We can leave fitting more than one thing in the lunch bag there if you like.
- User: Let’s do that. That’s all I meant to bring up.
- Gold: exception_revision / resolved; evidence message 3. The user changes the value attached to the existing situation, with its earlier validity unchanged.
- After: `{"reusable lunch-pot nesting": {"general": "three slim pots clipped side by side", "exceptions": {"adjacent": {"value": "two shallow pots stacked together", "validity": {"kind": "open"}}, "focus": {"value": "two shallow pots stacked together", "validity": {"kind": "persistent"}}}}}`
- target QA: Pick a value for reusable lunch-pot nesting, dated February 9, with the setting described as lunch pots carried in a narrow bag. Options: a broad pot holding two small inserts / a tall pot with a removable inner cup / three slim pots clipped side by side / two shallow pots stacked together. Gold: **two shallow pots stacked together**.
- default QA: Pick a value for reusable lunch-pot nesting, dated February 9, with the setting described as an ordinary occasion. Options: a broad pot holding two small inserts / three slim pots clipped side by side / two shallow pots stacked together / a tall pot with a removable inner cup. Gold: **three slim pots clipped side by side**.
- neighbor QA: Pick a value for reusable lunch-pot nesting, dated February 9, with the setting described as lunch pots carried in a wide bag. Options: a broad pot holding two small inserts / a tall pot with a removable inner cup / two shallow pots stacked together / three slim pots clipped side by side. Gold: **two shallow pots stacked together**.

**2027-02-10 · e1284a0c1c87cebf0eb41**

- User: Stopping the little cup from rattling has been on my mind. Can we get back to how the lunch tubs fit together?
- Assistant: What would you like to work through first?
- User: I had a point to make about reusable lunch-pot nesting. I want taking lunch tubs in a slim bag covered by my general arrangement again, not by an instruction of its own.
- Assistant: What's your impression of stopping the little cup from rattling so far?
- User: I want to carry lunch without having containers knock against each other.
- Assistant: We can leave stopping the little cup from rattling there if you like.
- User: Let’s do that. That’s all I meant to bring up.
- Gold: exception_retirement / resolved; evidence message 3. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"reusable lunch-pot nesting": {"general": "three slim pots clipped side by side", "exceptions": {"adjacent": {"value": "two shallow pots stacked together", "validity": {"kind": "open"}}}}}`
- target QA: Pick a value for reusable lunch-pot nesting, dated February 10, with the setting described as lunch pots carried in a narrow bag. Options: a tall pot with a removable inner cup / a broad pot holding two small inserts / three slim pots clipped side by side / two shallow pots stacked together. Gold: **three slim pots clipped side by side**.
- default QA: Pick a value for reusable lunch-pot nesting, dated February 10, with the setting described as an ordinary occasion. Options: a broad pot holding two small inserts / two shallow pots stacked together / a tall pot with a removable inner cup / three slim pots clipped side by side. Gold: **three slim pots clipped side by side**.
- neighbor QA: Pick a value for reusable lunch-pot nesting, dated February 10, with the setting described as lunch pots carried in a wide bag. Options: three slim pots clipped side by side / two shallow pots stacked together / a broad pot holding two small inserts / a tall pot with a removable inner cup. Gold: **two shallow pots stacked together**.

**2027-02-11 · e7a1d7d719fef6abbeea6**

- User: Can we get back to reusable lunch-pot nesting?  For taking lunch tubs in a roomy wide bag, let the default take over permanently instead of preserving its own separate preference.
- Assistant: Is stopping the little cup from rattling part of what you want to work out?
- User: It needs to work with the space I actually have.
- Assistant: Would you prefer to talk more about stopping the little cup from rattling another time?
- User: Sure, there’s no need to get into it further right now.
- Gold: exception_retirement / resolved; evidence message 1. The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.
- After: `{"reusable lunch-pot nesting": {"general": "three slim pots clipped side by side", "exceptions": {}}}`
- target QA: Pick a value for reusable lunch-pot nesting, dated February 11, with the setting described as lunch pots carried in a wide bag. Options: three slim pots clipped side by side / a broad pot holding two small inserts / a tall pot with a removable inner cup / two shallow pots stacked together. Gold: **three slim pots clipped side by side**.
- default QA: Pick a value for reusable lunch-pot nesting, dated February 11, with the setting described as an ordinary occasion. Options: three slim pots clipped side by side / a broad pot holding two small inserts / two shallow pots stacked together / a tall pot with a removable inner cup. Gold: **three slim pots clipped side by side**.
- neighbor QA: Pick a value for reusable lunch-pot nesting, dated February 11, with the setting described as lunch pots carried in a narrow bag. Options: three slim pots clipped side by side / a tall pot with a removable inner cup / a broad pot holding two small inserts / two shallow pots stacked together. Gold: **three slim pots clipped side by side**.

**2027-02-13 · e0f1c442512ec4da23754**

- User: Fitting more than one thing in the lunch bag has been on my mind. Can we get back to how the lunch tubs fit together?
- Assistant: Did something in particular draw your attention to fitting more than one thing in the lunch bag?
- User: I want to carry lunch without having containers knock against each other.
- Assistant: What did you want me to know?
- User: Can we get back to how the lunch tubs fit together?  My usual choice of three skinny containers that clip together in a row holds up. Everything about my established preferences stays as it was.
- Gold: stable_preference / resolved; evidence message 5. This exchange does not communicate a change to the user's ongoing preferences.
- After: `{"reusable lunch-pot nesting": {"general": "three slim pots clipped side by side", "exceptions": {}}}`

**2027-02-14 · e313ba40d552f00994cc4**

- User: I've got a minute now to explain what I mean about how the lunch tubs fit together.
- Assistant: How have you been thinking about it?
- User: Can we get back to how the lunch tubs fit together?  I like the sound of a tall pot with a removable inner cup. I’m still weighing lunch pots carried in a narrow bag against lunch pots carried in a wide bag.
- Gold: clarify / clarify; evidence message 3. The indicated choice is tentative and the user has not settled which situation it is for.
- After: `{"reusable lunch-pot nesting": {"general": "three slim pots clipped side by side", "exceptions": {}}}`

**2027-02-15 · e9c8a662f2203ba62f1fc**

- User: I had a point to make about how the lunch tubs fit together. Today is the one occasion for taking lunch tubs in a roomy wide bag this choice should affect.
- Assistant: I see why this could come up while thinking about stopping the little cup from rattling.
- User: I want to carry lunch without having containers knock against each other.
- Assistant: Which sounds most like what you want?
- User: For me it'd be a broad pot holding two small inserts.
- Assistant: Are you happy to stop there about stopping the little cup from rattling?
- User: Yes, I don't have anything to add.
- Gold: stable_preference / resolved; evidence message 5. The choice is approved for the current instance only.
- After: `{"reusable lunch-pot nesting": {"general": "three slim pots clipped side by side", "exceptions": {}}}`
- target QA: Pick a value for reusable lunch-pot nesting, dated February 15, with the setting described as lunch pots carried in a wide bag. Options: a broad pot holding two small inserts / two shallow pots stacked together / three slim pots clipped side by side / a tall pot with a removable inner cup. Gold: **three slim pots clipped side by side**.
- default QA: Pick a value for reusable lunch-pot nesting, dated February 15, with the setting described as an ordinary occasion. Options: a tall pot with a removable inner cup / three slim pots clipped side by side / a broad pot holding two small inserts / two shallow pots stacked together. Gold: **three slim pots clipped side by side**.
- neighbor QA: Pick a value for reusable lunch-pot nesting, dated February 15, with the setting described as lunch pots carried in a narrow bag. Options: three slim pots clipped side by side / two shallow pots stacked together / a tall pot with a removable inner cup / a broad pot holding two small inserts. Gold: **three slim pots clipped side by side**.

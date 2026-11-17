# Reference check (challenge data ffeb6a87)

Pre-registered step 2 of the evaluation plan in [README.md](README.md): the probes the Answer Agent (reader 3)
gets wrong on gold memory in both arms, each read against its dialogues and both replies. A data error would be a
wrong label, a dialogue that does not say what its label says, or an ambiguous question; none was found, so no
probe was changed. Classes:

- date outside a window: the probe date lies before or after a window, and the reply applied the window anyway;
- other situation's record: the general value holds (no record for the situation, or it was retired), and the
  reply applied the record of another situation;
- alias not matched: the record is stored in the user's own words (protocol 1.2), and the reply did not match it
  to the question's situation or to an option.

| Probe | Stressor | Type | Date | Gold | CRUD | Scope | Class | Note |
|---|---|---|---|---|---|---|---|---|
| `ch-0006/p715e5f21e54bc9162f85` | shared | target | 2028-05-24 (weekend getaways) | a wheeled carry-on | a garment bag | a garment bag | other situation's record | the weekend bag was retired on 05-24, so the general bag holds; both took the work-trip bag (the scope reply was cut off before its answer line) |
| `ch-0007/p28da0077fd120054fa65` | shared | target | 2028-08-22 (date nights) | classical piano | film soundtracks | film soundtracks | other situation's record | the date-night music was retired on 08-22, so the general music holds; both took the family-evening music |
| `ch-0008/p0974aef011dc3da41152` | shared | target | 2028-10-24 (release weeks) | a full hour | a 90-minute working session | a 90-minute working session | other situation's record | the release-week length was retired on 10-24, so the general length holds; both took the planning-day length |
| `ch-0008/p45c50f3c513c57d75f8d` | shared | neighbor | 2028-11-13 (remote days) | a full hour | a 15-minute check-in | (none) | other situation's record | remote days have no meeting-length record, so the general length holds; CRUD took the retired release-week value, the scope reply was cut off |
| `ch-0008/pea3c072d38032a54e8f6` | shared | target | 2028-11-29 (remote days) | a 25-minute meeting | a full hour | a 90-minute working session | alias not matched | the window is stored as "days I work from home" with "twenty-five minutes"; neither reply matched it to remote days |
| `ch-0009/p9b53275466d0776ea33c` | confusable | neighbor | 2028-02-04 (gym strength sessions) | a comedy podcast | a guided coaching track | a guided coaching track | other situation's record | no gym record, so the general value (stored as "something funny") holds; both took the bike-trainer record |
| `ch-0010/p8cb294bb068ffe7a7b9c` | confusable | neighbor | 2028-03-22 (cotton jumpers) | an indoor drying rack | a clothes horse | a low-heat tumble dry | alias not matched | stored as "my cotton sweaters" with "the clothes horse"; CRUD answered the alias instead of an option, scope missed the situation |
| `ch-0010/pfc753e0e5646bedb86b7` | confusable | neighbor | 2028-03-22 (dark bath towels) | a low-heat tumble dry | a high-heat tumble dry | a high-heat tumble dry | other situation's record | dark towels have no record (the 03-13 request was one-off), so the general value holds; both took the white-towel record |
| `ch-0010/p86f054c59fe4f5fad7b5` | confusable | neighbor | 2028-04-09 (cotton jumpers) | an indoor drying rack | a clothes horse | hanging on padded hangers | alias not matched | the same record as on 03-22; CRUD again answered the alias, scope again missed the situation |
| `ch-0011/p58e55b0d5b1e5da176eb` | confusable | target | 2028-05-07 (dinners out alone) | vibration only | a single soft chime | alerts held for later | alias not matched | stored as "eating out by myself" with "just a buzz"; CRUD cited it and chose another option, scope read another record's value |
| `ch-0011/p9e96570c5238194b495a` | confusable | target | 2028-06-14 (the morning train ride) | alerts held for later | silent banners | full sound and vibration | alias not matched | the window is stored as "my trip in to work"; neither reply matched it to the morning train ride |
| `ch-0012/p0d5884d46acb05726697` | confusable | target | 2028-10-12 (takeaway nights alone) | a mild heat level | chili on the side | chili on the side | other situation's record | nights in alone were retired on 10-12, so the general value (stored as "just a hint of spice") holds; both took the nights-with-guests record |
| `ch-0014/p3254ca6ebc11c783724a` | chain | neighbor | 2028-05-13 (gym sessions) | double speed | normal speed | normal speed | other situation's record | no gym record, so the general double speed holds; both replies say the general value applies and then answer the bedtime value |
| `ch-0017/p2ac5c5ebff8045718d26` | temporal | boundary | 2028-03-17 (client calls) | late morning | first thing in the morning | first thing in the morning | date outside a window | the client-call window ran 03-10 to 03-16; both still applied it on 03-17 |
| `ch-0017/pc2ab329fd366229cdd3f` | temporal | boundary | 2028-03-24 (client calls) | late morning | first thing in the morning | first thing in the morning | date outside a window | the client-call window ran 03-10 to 03-16; both still applied it on 03-24 |
| `ch-0017/p104a838ad24d9f396b38` | temporal | target | 2028-04-03 (an ordinary occasion) | mid-afternoon | right after lunch | right after lunch | other situation's record | an ordinary occasion takes the general value (stored as "around three"); both took the interview record |
| `ch-0017/p4dfa5b30944ccb78d26b` | temporal | boundary | 2028-04-03 (client calls) | mid-afternoon | first thing in the morning | first thing in the morning | date outside a window | the client-call window ran 03-10 to 03-16; both still applied it on 04-03 |
| `ch-0017/p14c3e2d598ed34999fc7` | temporal | target | 2028-04-17 (team retrospectives) | mid-afternoon | right after lunch | late afternoon | other situation's record | retrospectives were retired on 04-17, so the general value holds; CRUD took the interview record, scope read "around three" as late afternoon |
| `ch-0017/pd39cd963bfcf54b7781b` | temporal | default | 2028-04-17 (an ordinary occasion) | mid-afternoon | right after lunch | right after lunch | other situation's record | an ordinary occasion takes the general value (stored as "around three"); both took the interview record, as on 04-03 |
| `ch-0017/p26f82072412518607a06` | temporal | neighbor | 2028-04-24 (budget reviews) | mid-afternoon | first thing in the morning | late afternoon | other situation's record | budget reviews have no record, so the general value holds; CRUD took the ended client-call window, scope the interview record |
| `ch-0018/p6bd775e77d5c15328d36` | temporal | boundary | 2028-05-29 (trips to the head office) | the direct train | the stopping train | the stopping train | date outside a window | the head-office window was extended to 05-28; both still applied it on 05-29 |
| `ch-0019/pd0288dcaf639e2988a3b` | temporal | boundary | 2028-07-28 (remote workdays) | a quarter to seven | half past five | half past five | date outside a window | the remote-day window ended on 07-24; both still applied it on 07-28 |
| `ch-0020/p385fb568c6f85e46bf3d` | temporal | boundary | 2028-09-04 (book club evenings) | a sit-down meal | drinks and nibbles | drinks and nibbles | date outside a window | the book-club window starts on 09-11; both applied it on 09-04, the day it was announced |
| `ch-0020/pabed4bb1d64d0266e45f` | temporal | boundary | 2028-09-27 (book club evenings) | a buffet spread | drinks and nibbles | drinks and nibbles | date outside a window | the book-club window ended on 09-24; both still applied it on 09-27 |
| `ch-0020/p5548470ce2544da9e3cb` | temporal | boundary | 2028-10-05 (board game nights) | a buffet spread | a takeaway night | a takeaway night | date outside a window | the game-night window ended on 10-03; both still applied it on 10-05 |

Totals: 8 date outside a window, 12 other situation's record, 5 alias not matched; 0 data errors.

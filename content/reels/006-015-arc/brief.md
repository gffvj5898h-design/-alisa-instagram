# Human brief — Reels 006–015

## Goal
Continue directly from canonical Reels 005 as one serial, emotionally deep relationship arc. ChatGPT writes scripts; Grok generates one 1080×1920 start frame per episode and gets every frame into GitHub through the binary data plane. Every episode is 15 seconds, strict 9:16, Russian dialogue, photorealistic smartphone cinematic, and ends with a hook.

## Identity and reveal rules
- Alice always uses `character/references/alice-master-face.jpg`; never generate a similar blonde from text.
- Male face is forbidden in Reels 006–014. Voice, POV, hands, shoulder, silhouette or unreadable reflection are allowed.
- First full male face reveal is Reels 015 only.
- Start frames contain no text.

## Unknown man internal canon
Name: Андрей Лавров. Age: 44. Profession: architect-restorer. Divorced, emotionally cautious, has not let anyone close for a long time. In the restaurant from the failed first-date evening he was also on a personal meeting that went badly / never really happened. He noticed Alice leaving because she looked like someone tired of pretending everything was fine. He later found her public professional trace by the visible name of her interior-design studio on the folder/materials she carried. No hacking or magic contact discovery.

## Episode arc
### 006 — Завтра утром (`006-tomorrow-morning`)
He answers why he wrote: he wanted to approach in the restaurant but did not. He proposes no date, just coffee tomorrow morning. Hook: 09:00. Alice: «Посмотрим.» Start-frame: Alice at home at night with phone, composed curiosity.

### 007 — Ваш кофе (`007-your-coffee`)
First physical meeting, but no male face. POV from inside a car; Alice brings takeaway coffee to the open window. He says she actually came. He notes she did not ask his name; she says it is not needed yet. Hook: deliberate anonymity.

### 008 — Пока без имён (`008-no-names-yet`)
They make anonymity a game: one day, one question, no names. His first question: «Почему ты всё время уходишь первой?» Start-frame: Alice walking through daytime Saint Petersburg with phone.

### 009 — Почему ты уходишь первой? (`009-why-you-leave-first`)
Alice says she learned not to stay where everything is already clear / false. Her return question: «Ты женат?» He: «Нет. Но всё чуть сложнее.» Hook on the complication.

### 010 — Чуть сложнее (`010-a-bit-more-complicated`)
He is not married, but has avoided starting from zero for a long time. Alice asks why now. He says she looked as tired of pretending as he felt. Start-frame: evening studio/home, phone, tension becoming intimacy.

### 011 — Пешком (`011-on-foot`)
Second brief meeting, evening walk in Saint Petersburg. Male shoulder/hand/silhouette only. He admits he is nervous. Alice asks if he is nervous now. He says: «Сильно.» Hook: real mutual attraction.

### 012 — Как ты меня нашёл? (`012-how-you-found-me`)
Alice finally asks how he found her. He explains the studio name on her folder/materials, says he searched and deleted the first message three times before sending. Hook: deliberate effort rather than coincidence.

### 013 — То, о чём я молчу (`013-what-i-dont-say`)
Alice admits she has not let anyone close for a long time and prefers leaving first to rebuilding herself later. He says he understood that in the restaurant and wrote anyway. Hook is emotional reciprocity.

### 014 — Завтра без игр (`014-no-more-games-tomorrow`)
He says they have played with mystery long enough. Tomorrow he will tell his name and why he was in that restaurant. Alice asks what exactly will end. He says: «Игры.» Hook promises reveal.

### 015 — Андрей (`015-andrey`)
First male face reveal. He introduces himself as Андрей Лавров, 44, architect-restorer. He explains that he too had come to a personal meeting that did not really happen, then noticed Alice leaving. Alice: «Ну здравствуй, Андрей.» End of anonymous-man arc and start of a real relationship arc.

## Required text package per episode
- `concept.md`: episode goal, one new fact, emotional arc, location, Alice visual look, production gate.
- `storyboard.md`: 0–4 s / 4–9 s / 9–12 s / 12–15 s, exact Russian dialogue, final hook.
- `prompt-grok.md`: production-ready prompt, identity lock, start-frame description, no male face before 015, no identity drift.

## Generation/import rule
For every start frame Grok must actually use the canonical identity reference, generate exactly one 1080×1920 image, then use `production/GROK_BINARY_UPLOAD.md` to get exact bytes into the target `stills/start-frame.jpg`. Success means target + receipt exist on `main`, not merely that an image appeared in chat.

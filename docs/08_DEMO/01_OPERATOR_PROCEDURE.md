# Professor Command Sheet

Wake phrase: `Hey Pi`

This sheet describes the fixed 19-command offline speech-command vocabulary. Example utterances are legitimate demo phrases, but only the statuses marked by the evidence table should be treated as empirically verified.

| Command label | Canonical command | Example natural utterances | Expected action | Expected response | Current verification status |
| --- | --- | --- | --- | --- | --- |
| `PLAY_MUSIC` | "play music" | "play music", "play my music", "start the music" | Local music action | `responses/play_music.wav` | `DEMO_READY_STRONG_CURRENT_AND_PRIOR_EVIDENCE` |
| `WEATHER` | "weather" | "weather", "what is the weather", "weather information" | Local weather placeholder | `responses/weather.wav` | `DEMO_READY_STRONG_CURRENT_AND_PRIOR_EVIDENCE` |
| `TIME` | "time" | "time", "what time is it", "current time" | Local time placeholder | `responses/time.wav` | `CALLABLE_NOT_VERIFIED_NOT_DEMO_READY` |
| `LIGHT_ON` | "lights on" | "lights on", "turn on the light", "switch the light on" | Light on action | `responses/light_on.wav` | `PRIOR_DEMO_SUPPORTED_LATEST_RUN_NOT_VERIFIED_REPEAT_BEFORE_DEMO` |
| `LIGHT_OFF` | "lights off" | "lights off", "turn off the light", "switch the light off" | Light off action | `responses/light_off.wav` | `DEMO_READY_STRONG_CURRENT_AND_PRIOR_EVIDENCE` |
| `LIGHT_DIM` | "dim the light" | "dim the light", "dim lights", "lower the brightness" | Light dim action | `responses/light_dim.wav` | `PRIOR_DEMO_SUPPORTED_LATEST_RUN_NOT_VERIFIED_REPEAT_BEFORE_DEMO` |
| `BRIGHTNESS` | "brightness" | "brightness", "adjust brightness", "change brightness" | Brightness adjust action | `responses/brightness.wav` | `CALLABLE_VERIFIED_THIS_RUN_REPEAT_BEFORE_DEMO` |
| `TIMER` | "timer" | "timer", "set timer", "set a timer" | Timer action | `responses/timer.wav` | `DEMO_READY_STRONG_CURRENT_AND_PRIOR_EVIDENCE` |
| `ALARM` | "alarm" | "alarm", "set alarm", "set an alarm" | Alarm action | `responses/alarm.wav` | `DEMO_READY_STRONG_CURRENT_AND_PRIOR_EVIDENCE` |
| `TEMPERATURE` | "temperature" | "temperature", "adjust temperature", "set temperature" | Thermostat placeholder | `responses/temperature.wav` | `CALLABLE_UNSAFE_NOT_DEMO_READY_PRIOR_ACCEPTED_WRONG` |
| `NEXT` | "next" | "next", "next item", "skip to next" | Media next action | `responses/next.wav` | `PRIOR_DEMO_SUPPORTED_LATEST_RUN_NOT_VERIFIED_REPEAT_BEFORE_DEMO` |
| `PAUSE` | "pause" | "pause", "pause music", "pause it" | Media pause action | `responses/pause.wav` | `DEMO_READY_STRONG_CURRENT_AND_PRIOR_EVIDENCE` |
| `STOP` | "stop" | "stop", "stop music", "stop it" | Media stop action | `responses/stop.wav` | `DEMO_READY_STRONG_CURRENT_AND_PRIOR_EVIDENCE` |
| `VOLUME_UP` | "volume up" | "volume up", "increase volume", "turn volume up" | Volume up action | `responses/volume_up.wav` | `CALLABLE_NOT_VERIFIED_NOT_DEMO_READY` |
| `VOLUME_DOWN` | "volume down" | "volume down", "decrease volume", "turn volume down" | Volume down action | `responses/volume_down.wav` | `CALLABLE_NOT_VERIFIED_NOT_DEMO_READY` |
| `CREATE_REMINDER` | "create reminder" | "create reminder", "make a reminder", "remind me" | Create reminder placeholder | `responses/create_reminder.wav` | `PRIOR_DEMO_SUPPORTED_LATEST_RUN_NOT_VERIFIED_REPEAT_BEFORE_DEMO` |
| `LIST_REMINDERS` | "list reminders" | "list reminders", "show reminders", "what are my reminders" | List reminders action | `responses/list_reminders.wav` | `DEMO_READY_STRONG_CURRENT_AND_PRIOR_EVIDENCE` |
| `CALL` | "call" | "call", "start call", "make a call" | Call placeholder | `responses/call.wav` | `CALLABLE_NOT_VERIFIED_NOT_DEMO_READY` |
| `MESSAGE` | "message" | "message", "send message", "write a message" | Message placeholder | `responses/message.wav` | `PRIOR_DEMO_SUPPORTED_LATEST_RUN_NOT_VERIFIED_REPEAT_BEFORE_DEMO` |



## One sentence explanation					
This is an offline speech-command recognition system running locally on a Raspberry Pi 5. It does not use cloud speech recognition, an LLM, or general speech-to-text.					
                    
## Technical flow					
Live microphone audio → preprocessing → E37 wake gate → E50 command CNN → E40 confidence guardrail → deterministic router → local action → recorded response → return to listening.					
                    
## Demo flow					
1. Power on the Raspberry Pi 5 with touchscreen, microphone, and speaker connected.					
2. Open the VCM Offline application on the Pi touchscreen.					
3. Press START LISTENING.					
4. GUI shows WAKE ME UP					
5. Say "Hey Pi" and then a supported command.					
6.  A recognized command is accepted by the confidence policy, routed to its corresponding local action, produces its mapped response audio, and returns to listening.					
7. Press STOP VCM  to end demo.					
                    
## DataSet Schema					
                    
E50 command vocabulary: 19 labels		Actions			
At start		"WAKE ME UP" Say "hey Pi.			
Wake accepted		"I AM AWAKE" I am at your command.			
PLAY_MUSIC		Playing your favorite song  PLAYBACK			
WEATHER		Here's the weather information  PLAYBACK			
LIGHT_ON		Switching the lights on PLAYBACK			
LIGHT_OFF		Switching the lights off PLAYBACK			
LIGHT_DIM		Dimming the lights PLAYBACK			
TIMER		Setting the timer PLAYBACK			
ALARM		Setting the alarm PLAYBACK			
PAUSE		Making a pause PLAYBACK			
STOP		Stopping PLAYBACK			
LIST_REMINDERS		Here are your reminders PLAYBACK			
MESSAGE		Sending the message PLAYBACK			
NEXT		Playing the next song PLAYBACK			
CREATE_REMINDER		Buy groceries and medicines PLAYBACK			
CALL		Calling your mother PLAYBACK			
TEMPERATURE		Adjusting the temperature PLAYBACK			
                    
OTHERS					
SILENCE		At wake gate: "I AM NOT AWAKE", say "Hey Pi" any time			
        At command gate: "I DIDN’T UNDERSTAND", say "Hey Pi" immediately			
                    
UNACCEPTED COMMANDS		"I DIDN'T UNDERSTAND"			
UNKNOWN COMMANDS		"I CAN’T DO THAT"			
                    
## Demo guide					
Situation	Top message	Second line	NOTES		
Ready / after successful command	WAKE ME UP	Say "hey pi"	you can now say "hey pi" to wake it up		
Wake gate missed/rejected	I AM NOT AWAKE	Say "hey pi" again.	you can now say "hey pi" to repeat wake up command; If no command is successfully recognized during the command window, the runtime returns to its existing listening/rejection behavior.		
Wake accepted, command window open	SAY WHAT YOU NEED	I am at your command.	you can now say a command (check list)		
Command rejected, predicted listed command	I DIDN'T UNDERSTAND	Say "hey pi" again.	you can now say "hey pi" to repeat wake up command; if you don’t speak, it will treat it as a command		
Command rejected, predicted UNKNOWN	I CAN'T DO THAT	Say "hey pi" again.	you can say "hey pi "		
GUI stopped	STOPPED	VCM stopped or Runtime is not running	stops the run		
                    
If you say alexa and the screen goes to SAY WHAT YOU NEED, that means the wake model accepted it as wake. Log that as wake false accept / alternate wake, not GUI failure.					
If you say open the window after wake and it shows I CAN'T DO THAT, the command prediction was UNKNOWN.					
If open the window shows I DIDN'T UNDERSTAND, the model predicted some listed command below threshold, so the GUI cannot know it was semantically unknown.					

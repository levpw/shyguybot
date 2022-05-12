# shyguybot
shyguybot is a discord bot focused on game Mario Kart 8 Deluxe.

1. Installation

Install the dependencies according to environment.yml. Use conda if you like.

Create .env file, you need a discord bot token (necessary) and a DEEPL token (optional) for $translation function.

See:
https://github.com/theskumar/python-dotenv/

Also:
https://discord.com/developers/docs/topics/oauth2

Use python shyguy.py to run.

for more.

2. Functions

Below are the current functions of shyguybot

$help

Displace help message, which will be this.

$hello

Say hello

<img width="263" alt="Screen Shot 2022-05-12 at 08 25 30" src="https://user-images.githubusercontent.com/86674677/168074459-7acc4355-e4fd-4563-a1f2-52d6b06f4f4b.png">

$choose

Choose from following arguments, need to be seperated by space.

$choose arg1 arg2 ...

<img width="268" alt="Screen Shot 2022-05-12 at 08 26 01" src="https://user-images.githubusercontent.com/86674677/168074500-84d81381-4159-412b-b854-5c8c97c6745e.png">

$say

Use DEEPL to translate input into a target language (given as argument)

$say arg1 arg2

<img width="251" alt="Screen Shot 2022-05-12 at 08 26 18" src="https://user-images.githubusercontent.com/86674677/168074539-be58708d-696e-4b3c-baae-44649347e1a2.png">

$calc

Simple calculation using sympy

$calc arg1

<img width="246" alt="Screen Shot 2022-05-12 at 08 28 14" src="https://user-images.githubusercontent.com/86674677/168074716-289685e4-a83f-48b2-86bb-a3c36731fa77.png">

$learn

This function tells shyguy to remember a specific answer to a question

$learn arg1 arg2

<img width="397" alt="Screen Shot 2022-05-12 at 11 32 42" src="https://user-images.githubusercontent.com/86674677/168123765-283de725-a766-4879-9121-93633b642fe8.png">

$forget

Use forget to remove remembered answer to a question

$forget arg1

<img width="251" alt="Screen Shot 2022-05-12 at 11 33 03" src="https://user-images.githubusercontent.com/86674677/168123917-ec1bb1f4-e36b-406a-8f8d-3433e3b1074a.png">

$maketable

Call this function to create a table for mario kart 8 deluxe match result. Easyocr is used for text recognition.
An in-game screenshot must be used to generate result, you can either use the image at final result screen (type=0) or the image at 12th race screen (type=1). You can also specify the position of the player (1-12) taking the screenshot as the second argument. Paste the image into the chat and send.

Use $maketable sample to see a sample result.

You could make change to the text read result and send the result to generate the table.

$maketable type position image

<img width="242" alt="Screen Shot 2022-05-12 at 13 27 15" src="https://user-images.githubusercontent.com/86674677/168133918-b6faf8e1-b0fe-4876-aa1d-060de6e11b00.png">

<img width="345" alt="Screen Shot 2022-05-12 at 13 27 29" src="https://user-images.githubusercontent.com/86674677/168133943-38afcc49-ec06-4f12-b328-09af1f503006.png">

<img width="795" alt="Screen Shot 2022-05-12 at 13 27 39" src="https://user-images.githubusercontent.com/86674677/168133962-11282a50-4977-4cab-a814-1daebec1c80d.png">

<img width="678" alt="Screen Shot 2022-05-12 at 13 28 02" src="https://user-images.githubusercontent.com/86674677/168133986-1d3ecac0-9f12-437c-8114-b86e0efed28c.png">

(Since CNN is used, servers with little resource may not be able to run this function.)

$nita

Find mario kart 8 deluxe NITA result from https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vRDdedRm18RtIu2hB9l5WrbaClaIPnZAVh_Xf7IeGzmsOVHcNdjoD3VWo8EdMxJ7JKdtcbFnebLjCcV/pubhtml

Track name input can be either abbreviation, full name, or partial name, rank can be integer from 1 to 10.

$nita trackname rank

<img width="371" alt="Screen Shot 2022-05-12 at 13 39 03" src="https://user-images.githubusercontent.com/86674677/168135894-0c9fbead-d6db-4220-9b8a-959b002ac95a.png">

$wiggler

Find mario kart 8 deluxe wiggler NITA result from https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vTOT3PJwMcMrOE--rBPV3Vz1SUegmpmpCtP8NzMQoxHljks2JDaYQ8H1pj4Pi0i5xOmnnS3eDAxc4zY/pubhtml

Track name input can be either abbreviation, full name, or partial name, rank can be integer from 1 to 10.

$wiggler trackname rank

<img width="441" alt="Screen Shot 2022-05-12 at 13 39 28" src="https://user-images.githubusercontent.com/86674677/168135929-ceecea08-5e4d-4356-9f57-5b3bccd8d10e.png">

$wr

Find mario kart 8 deluxe world record result from https://mkwrs.com/mk8dx/wrs.php

Track name input can be either abbreviation, full name, or partial name. Link to video when possible.

$wr trackname

<img width="658" alt="Screen Shot 2022-05-12 at 13 39 43" src="https://user-images.githubusercontent.com/86674677/168135984-f950c24e-9df6-4c72-a029-125d73881f9a.png">

3. Interactive

@shyguy to use this function. It can use information from $learn function, or random response.
Use @shyguy show me arg1 to let shyguy send an image of the topic. Use @shyguy language code arg1 to find language code to be used for $say.

<img width="383" alt="Screen Shot 2022-05-12 at 14 09 21" src="https://user-images.githubusercontent.com/86674677/168140849-dcc741c3-610c-4d2e-bb1c-506ddaf5a85c.png">

language code may be inaccesible due to website (https://www.loc.gov/standards/iso639-2/php/code_list.php) restriction on your server.

4. Custom commands

use _cc to call this function. You can add, remove, or update a command. Or you could list all the commands in your guild. Custom commands can also be called using _customcommand. You can also call _random to use a random command in your guild.

<img width="253" alt="Screen Shot 2022-05-12 at 14 26 18" src="https://user-images.githubusercontent.com/86674677/168143685-63d513fb-1ba8-4d93-bc68-1d8b8cf3b061.png">

<img width="257" alt="Screen Shot 2022-05-12 at 14 26 38" src="https://user-images.githubusercontent.com/86674677/168143704-2f7cf5fe-9bea-419a-b76f-98db3874ee90.png">

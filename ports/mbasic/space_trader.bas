10 REM Space Trader Game
30 GOSUB 10000: REM Initialize variables and arrays
40 GOSUB 30000: REM Show welcome message
50 REM Main game loop
60 REM G = 1 means game is running
70 GOTO 90
80 REM Main loop
90 IF G = 0 THEN GOTO 110
100 GOSUB 1000: GOTO 90
110 PRINT
120 PRINT "Game over! You retired"
130 PRINT "Final score: "; INT((AG * CR)/1000)
140 END

1000 REM Exchange subroutine
1010 PRINT
1020 PRINT "Captain: "; CN$
1030 PRINT "Starship: "; SN$
1040 PRINT "Age: "; AG
1050 PRINT "Credits: "; CR
1060 PRINT
1070 PRINT "=== Celastra Exchange ==="
1080 PRINT "1. Buy Goods"
1090 PRINT "2. Sell Goods"
1100 PRINT "3. Upgrade Ship"
1110 PRINT "4. Ship Computer"
1120 PRINT "5. Launch Ship"
1130 PRINT "Choose option 1-5"
1140 INPUT CH$
1150 IF CH$ = "1" THEN GOSUB 2000
1160 IF CH$ = "2" THEN GOSUB 3000
1170 IF CH$ = "3" THEN GOSUB 4000
1180 IF CH$ = "4" THEN GOSUB 5000
1190 IF CH$ = "5" THEN GOSUB 6000
1200 RETURN

2000 REM Buy goods subroutine
2010 IF TR <= 0 THEN GOTO 2200
2020 R = INT(RND(1) * GC) + 1
2030 GD$ = G$(R)
2040 PR = INT(RND(1) * 281) + 20
2050 R = INT(RND(1) * TC) + 1
2060 TD$ = T$(R)
2070 PRINT
2080 PRINT TD$; " is selling "; GD$; " for "; PR; " credits."
2090 PRINT "Buy "; GD$; "?"
2100 TR = TR - 1
2110 PRINT "1. Yes 2. No: ";
2120 INPUT CH$
2130 IF CH$ <> "1" THEN GOTO 2180
2140 IF CR < PR THEN PRINT "Not enough credits.": GOTO 2180
2150 CR = CR - PR
2160 GOSUB 20000: REM Add good to inventory
2170 PRINT "Bought "; GD$; "."
2175 GOSUB 20100: REM Handle trade tax
2177 IF G = 0 THEN RETURN
2180 GOTO 2250
2200 PRINT
2210 PRINT "No traders available."
2250 PRINT
2260 PRINT "Press ENTER to continue...";
2270 INPUT D$
2280 RETURN

3000 REM Sell goods subroutine
3010 IF TR <= 0 THEN GOTO 3200
3020 IF GO = 0 THEN PRINT: PRINT "No goods to sell.": GOTO 3250
3030 GOSUB 20200: REM Get random owned good
3040 PR = INT(RND(1) * 151) + 50
3050 R = INT(RND(1) * TC) + 1
3060 TD$ = T$(R)
3070 PRINT
3080 PRINT TD$; " is buying "; SG$; " for "; PR; " credits."
3090 PRINT "Sell "; SG$; "?"
3100 TR = TR - 1
3110 PRINT "1. Yes 2. No: ";
3120 INPUT CH$
3130 IF CH$ <> "1" THEN GOTO 3180
3140 CR = CR + PR
3150 GOSUB 20300: REM Remove good from inventory
3160 PRINT "Sold "; SG$; "."
3170 GOSUB 20100: REM Handle trade tax
3175 IF G = 0 THEN RETURN
3180 GOTO 3250
3200 PRINT
3210 PRINT "No traders available."
3250 PRINT
3260 PRINT "Press ENTER to continue...";
3270 INPUT D$
3280 RETURN

4000 REM Upgrade ship subroutine
4010 PRINT
4020 PRINT "=== Upgrade Ship ==="
4030 PRINT "1. Engine"
4040 PRINT "2. Hold"
4050 PRINT "3. Shields"
4060 PRINT "4. Weapons"
4070 PRINT "Choose upgrade: ";
4080 INPUT CH$
4090 IF CH$ = "1" AND CR >= 500 THEN EN = EN + 1: CR = CR - 500: PRINT "Upgraded engine!": GOTO 4130
4100 IF CH$ = "2" AND CR >= 300 THEN HD = HD + 1: CR = CR - 300: PRINT "Upgraded hold!": GOTO 4130
4110 IF CH$ = "3" AND CR >= 400 THEN SH = SH + 1: CR = CR - 400: PRINT "Upgraded shields!": GOTO 4130
4120 IF CH$ = "4" AND CR >= 400 THEN WP = WP + 1: CR = CR - 400: PRINT "Upgraded weapons!": GOTO 4130
4125 PRINT "Not enough credits."
4130 RETURN

5000 REM Ship computer subroutine
5010 PRINT
5020 PRINT "=== Ship Computer ==="
5030 PRINT "1. Instructions"
5040 PRINT "2. View Ship Status"
5050 PRINT "3. Register Ship Name"
5060 PRINT "4. Register Captain Name"
5070 PRINT "5. Exit Game"
5080 PRINT "Choose option 1-5: ";
5090 INPUT CH$
5100 IF CH$ = "1" THEN GOSUB 5500
5110 IF CH$ = "2" THEN GOSUB 5600
5120 IF CH$ = "3" THEN GOSUB 5700
5130 IF CH$ = "4" THEN GOSUB 5800
5140 IF CH$ = "5" THEN PRINT: PRINT "Exiting the game...": G = 0
5150 RETURN

5500 REM Instructions subroutine
5510 PRINT
5520 PRINT "About the Game:"
5530 PRINT
5540 PRINT "You take the role of a space"
5550 PRINT "trader named Reynolds,"
5560 PRINT "commanding your starship"
5570 PRINT "Intrepid. Your base is at"
5580 PRINT "the Celastra Exchange space station."
5590 PRINT
5600 PRINT "Press ENTER to continue...";
5610 INPUT D$
5620 PRINT
5630 PRINT "Your journey begins at the"
5640 PRINT "age of 30, and the game"
5650 PRINT "ends when you retire, aged"
5660 PRINT "60, from the Trading Guild."
5670 PRINT
5680 PRINT "Due to hibernation you only"
5690 PRINT "age when docked at the"
5700 PRINT "Celastra Exchange. Your"
5710 PRINT "final score is based on the"
5720 PRINT "credits you have accrued."
5730 PRINT
5740 PRINT "Press ENTER to continue...";
5750 INPUT D$
5760 PRINT
5770 PRINT "How to Play:"
5780 PRINT
5790 PRINT "1. Start with 1000 credits."
5800 PRINT "2. At each turn, you'll visit"
5810 PRINT "the Celastra Exchange where you can:"
5820 PRINT
5830 PRINT " - Buy Goods"
5840 PRINT " - Sell Goods"
5850 PRINT " - Upgrade your Ship"
5860 PRINT
5870 PRINT "On each visit to the Exchange a"
5880 PRINT "selection of trades will be available."
5890 PRINT
5900 PRINT "Press ENTER to continue...";
5910 INPUT D$
5920 PRINT
5930 PRINT "You will have to pay a tax"
5940 PRINT "of 5 credits on each trade"
5950 PRINT "at the Celastra Exchange."
5960 PRINT
5970 PRINT "You will also have to pay"
5980 PRINT "a docking fee of 20 credits"
5990 PRINT "when docking at the Celastra"
6000 PRINT "Exchange. Your ship will be"
6010 PRINT "impounded if you cannot pay."
6020 PRINT
6030 PRINT "Press ENTER to continue...";
6040 INPUT D$
6050 PRINT
6060 PRINT "3. During exploration, you'll"
6070 PRINT "face 1 to 4 encounters based"
6080 PRINT "on your engine stat:"
6090 PRINT
6100 PRINT " - Pirate Attack"
6110 PRINT " - Meet a Trader"
6120 PRINT " - Explore a Planet (you may"
6130 PRINT "   encounter pirates, traders"
6140 PRINT "   or receive a boon)"
6150 PRINT " - Explore empty space"
6160 PRINT
6170 PRINT "Press ENTER to continue...";
6180 INPUT D$
6190 PRINT
6200 PRINT "Ship Stats:"
6210 PRINT
6220 PRINT "Engine: Number of encounters"
6230 PRINT "per turn."
6240 PRINT "Hold: How many goods you can"
6250 PRINT "carry."
6260 PRINT "Shields: Helps defend your"
6270 PRINT "ship in battle."
6280 PRINT "Weapons: Affects your"
6290 PRINT "offensive power in battles."
6300 PRINT
6310 PRINT "Press ENTER to return to the game";
6320 INPUT D$
6330 RETURN

5600 REM View ship status subroutine
5610 PRINT
5620 PRINT "Ship: "; SN$
5630 PRINT "Captain: "; CN$
5640 PRINT "Age: "; AG
5650 PRINT "Credits: "; CR
5660 PRINT "Engine: "; EN
5670 PRINT "Hold: "; HD
5680 PRINT "Shields: "; SH
5690 PRINT "Weapons: "; WP
5700 PRINT
5710 IF GO = 0 THEN PRINT "Goods: None": GOTO 5760
5720 PRINT "Goods:"
5730 FOR I = 1 TO MG
5740   IF GQ(I) > 0 THEN PRINT " - "; PG$(I); " x"; GQ(I)
5750 NEXT I
5760 PRINT
5770 PRINT "Press ENTER to continue...";
5780 INPUT D$
5790 RETURN

5700 REM Register ship name subroutine
5710 PRINT
5720 PRINT "Enter your new ship name: ";
5730 INPUT SN$
5740 PRINT "Ship renamed to "; SN$
5750 RETURN

5800 REM Register captain name subroutine
5810 PRINT
5820 PRINT "Enter your new captain name: ";
5830 INPUT CN$
5840 PRINT "Captain renamed to "; CN$
5850 RETURN

6000 REM Exploration subroutine
6010 LC$ = "space"
6020 EC = 1: REM Encounter counter
6030 GOTO 6040
6035 REM Exploration loop
6040 IF EC > EN THEN GOTO 6120: REM Exit exploration after engine encounters
6050 R = INT(RND(1) * 4) + 1
6060 IF R = 1 THEN GOSUB 7000: REM Pirate attack
6070 IF R = 2 THEN GOSUB 8000: REM Trader encounter
6080 IF R = 3 THEN GOSUB 9000: REM Planet encounter
6090 IF R = 4 THEN PRINT: PRINT "Nothing here...": PRINT
6100 PRINT "Press ENTER to continue exploring...";
6110 INPUT D$
6115 IF G = 0 THEN RETURN
6117 EC = EC + 1: GOTO 6040
6120 PRINT
6130 PRINT "Docking back at the Exchange..."
6140 LC$ = "exchange"
6150 IF CR - 20 < 0 THEN PRINT: PRINT "You were unable to pay docking fees": PRINT "so your ship has been impounded.": G = 0: RETURN
6160 TR = INT(RND(1) * 5) + 6
6170 CR = CR - 20
6180 PRINT
6190 PRINT "Docked at the Celastra Exchange."
6200 PRINT "Docking fees: 20 credits"
6210 PRINT
6220 PRINT "Press ENTER to continue...";
6230 INPUT D$
6240 AG = AG + 1
6250 IF AG >= 60 THEN G = 0
6260 RETURN

7000 REM Pirate attack subroutine
7010 R = INT(RND(1) * PC) + 1
7020 PI$ = P$(R)
7030 PRINT
7040 PRINT "Pirate "; PI$; " attacks!"
7050 IF WP > INT(RND(1) * 3) THEN PRINT "You won the battle!": GOTO 7100
7060 IF SH > INT(RND(1) * 3) THEN PRINT "You escaped the battle,": PRINT "but your ship took some damage!": GOTO 7070
7065 PRINT "Lost the battle! Pirates stole": PRINT "your goods and damaged your ship.": GOSUB 20400: REM Clear all goods
7070 R = INT(RND(1) * 4) + 1
7075 IF R = 1 THEN S$ = "engine"
7080 IF R = 2 THEN S$ = "hold"
7085 IF R = 3 THEN S$ = "shields"
7090 IF R = 4 THEN S$ = "weapons"
7095 GOSUB 21000: REM Decrement stat
7100 RETURN

8000 REM Trader encounter subroutine
8010 PRINT
8020 PRINT "Met a trader!"
8030 GOSUB 2000: REM Buy goods
8040 RETURN

9000 REM Planet encounter subroutine
9010 R = INT(RND(1) * PL) + 1
9020 PN$ = L$(R)
9030 PRINT
9040 PRINT "Landed on "; PN$; "."
9050 R = INT(RND(1) * 3) + 1
9060 IF R = 1 THEN PRINT "Received a boon!": UP = INT(RND(1) * 4) + 1: GOSUB 21500: PRINT U$; " has been increased by 1!"
9070 IF R = 2 THEN GOSUB 7000: REM Fight
9080 IF R = 3 THEN GOSUB 8000: REM Trade
9090 RETURN

10000 REM Initialize variables
10010 MG = 30: REM Maximum number of different goods
10020 PL = 27: REM Maximum number of planets
10030 PC = 32: REM Maximum number of pirates
10040 TC = 16: REM Maximum number of traders
10050 DIM G$(MG), L$(PL), P$(PC), T$(TC)
10060 DIM PG$(MG), GQ(MG)
10070 GC = 29: REM Number of goods
10080 GO = 0: REM Number of types of goods owned
10090 G$(1) = "Plasma": G$(2) = "Void Ore": G$(3) = "Warp Cells"
10100 G$(4) = "Nanites": G$(5) = "Ion Flux": G$(6) = "Tachyons"
10110 G$(7) = "Deflectors": G$(8) = "Quantum Cores"
10200 L$(1) = "Zanxor": L$(2) = "Novus": L$(3) = "Kalrix": L$(4) = "Velor"
10210 L$(5) = "Gorath": L$(6) = "Zethar": L$(7) = "Avolon": L$(8) = "Krylith"
10300 P$(1) = "Havok": P$(2) = "Kane": P$(3) = "Fang": P$(4) = "Blaze"
10310 P$(5) = "Talon": P$(6) = "Shrike": P$(7) = "Scorn": P$(8) = "Claw"
10400 T$(1) = "Vex": T$(2) = "Orion": T$(3) = "Luna"
10410 T$(4) = "Darius": T$(5) = "Seraphina": T$(6) = "Jericho"
10420 T$(7) = "Thalia": T$(8) = "Corda"
10500 AG = 30: REM Player age
10510 LC$ = "exchange": REM Player location
10520 CR = 1000: REM Player credits
10530 EN = 1: REM Player engine
10540 HD = 5: REM Player hold
10550 SH = 1: REM Player shields
10560 WP = 1: REM Player weapons
10570 SN$ = "Intrepid": REM Ship name
10580 CN$ = "Reynolds": REM Captain name
10590 TR = INT(RND(1) * 5) + 6: REM Exchange traders
10600 G = 1: REM Game running flag
10610 RETURN

20000 REM Add good to inventory
20010 F = 0: REM Found flag
20020 FOR I = 1 TO MG
20030   IF PG$(I) = GD$ THEN GQ(I) = GQ(I) + 1: F = 1: I = MG: REM Exit loop
20040 NEXT I
20050 IF F = 0 THEN GOSUB 20500: REM Add new good
20060 RETURN

20100 REM Handle trade tax
20110 IF LC$ <> "exchange" THEN RETURN
20120 IF CR - 5 < 0 THEN PRINT: PRINT "You were unable to pay the trade tax": PRINT "so your ship has been impounded.": G = 0: RETURN
20130 CR = CR - 5
20140 PRINT "Trade tax of 5 credits paid."
20150 RETURN

20200 REM Get random owned good
20210 TC = 0: REM Temporary counter
20220 FOR I = 1 TO MG
20230   IF GQ(I) > 0 THEN TC = TC + 1
20240 NEXT I
20250 R = INT(RND(1) * TC) + 1
20260 TC = 0
20270 FOR I = 1 TO MG
20280   IF GQ(I) > 0 THEN TC = TC + 1
20290   IF TC = R THEN SG$ = PG$(I): SI = I: I = MG: REM Exit loop
20300 NEXT I
20310 RETURN

20300 REM Remove good from inventory
20310 GQ(SI) = GQ(SI) - 1
20320 IF GQ(SI) = 0 THEN PG$(SI) = "": GO = GO - 1
20330 RETURN

20400 REM Clear all goods
20410 FOR I = 1 TO MG
20420   PG$(I) = ""
20430   GQ(I) = 0
20440 NEXT I
20450 GO = 0
20460 RETURN

20500 REM Add new good
20510 FOR I = 1 TO MG
20520   IF PG$(I) = "" THEN PG$(I) = GD$: GQ(I) = 1: GO = GO + 1: I = MG: REM Exit loop
20530 NEXT I
20540 RETURN

21000 REM Decrement stat
21010 IF S$ = "engine" THEN GOSUB 21100
21020 IF S$ = "hold" THEN GOSUB 21200
21030 IF S$ = "shields" THEN GOSUB 21300
21040 IF S$ = "weapons" THEN GOSUB 21400
21050 PRINT S$; " has been reduced by 1."
21060 RETURN

21100 REM Decrement engine
21110 EN = EN - 1
21120 IF EN <= 0 THEN EN = 0: PRINT "With no working engines, you are now adrift in the cold void of space. Game over!": G = 0
21130 RETURN

21200 REM Decrement hold
21210 HD = HD - 1
21220 IF HD < 0 THEN HD = 0
21230 TG = 0: REM Total goods
21240 FOR I = 1 TO MG
21250   TG = TG + GQ(I)
21260 NEXT I
21270 IF TG > HD THEN GOSUB 21600: REM Jettison goods
21280 RETURN

21300 REM Decrement shields
21310 SH = SH - 1
21320 IF SH < 0 THEN SH = 0
21330 RETURN

21400 REM Decrement weapons
21410 WP = WP - 1
21420 IF WP < 0 THEN WP = 0
21430 RETURN

21500 REM Increase ship stat
21510 IF UP = 1 THEN EN = EN + 1: U$ = "engine"
21520 IF UP = 2 THEN HD = HD + 1: U$ = "hold"
21530 IF UP = 3 THEN SH = SH + 1: U$ = "shields"
21540 IF UP = 4 THEN WP = WP + 1: U$ = "weapons"
21550 RETURN

21600 REM Jettison goods
21610 TG = 0: REM Total goods
21620 FOR I = 1 TO MG
21630   TG = TG + GQ(I)
21640 NEXT I
21650 IF TG <= HD THEN GOTO 21720
21660 GOSUB 20200: REM Get random owned good
21670 GQ(SI) = GQ(SI) - 1
21680 IF GQ(SI) = 0 THEN PG$(SI) = "": GO = GO - 1
21690 TG = TG - 1
21700 GOTO 21650
21710 REM End of jettison loop
21720 PRINT "Due to hold damage, goods had to be jettisoned."
21730 RETURN

30000 REM Welcome message
30010 PRINT "Welcome to Space Trader !"
30020 PRINT
30030 PRINT "Your mission is to explore"
30040 PRINT "the galaxy and make your"
30050 PRINT "fortune."
30060 PRINT
30070 PRINT "Press ENTER to continue...";
30080 INPUT D$
30090 RETURN
START TRANSACTION;
/* ******************************** CREATE DATABASE ******************************** */

CREATE DATABASE IF NOT EXISTS spartanbrewdb;

/* ****************************************************************************** */
/* ******************************** CREATE TABLE ******************************** */

CREATE TABLE IF NOT EXISTS spartanbrewdb.beer_info (
BEER_ID 			INT(11) NOT NULL AUTO_INCREMENT,
BEER_NAME 			VARCHAR(255) DEFAULT NULL,
BEER_TYPE 			VARCHAR(255) DEFAULT NULL,
BEER_STYLE 			VARCHAR(255) DEFAULT NULL,
BEER_DESCRIPTION 	TEXT,
BEER_URL 			VARCHAR(255) DEFAULT NULL,
BEER_ABV			DOUBLE(2,1) DEFAULT NULL,
BEER_IBU			DOUBLE(3,1) DEFAULT NULL,
BEER_SRM			DOUBLE(3,1) DEFAULT NULL,
BEER_OG				DOUBLE(4,3) DEFAULT NULL,
BREWING_PROGRAM_ID 	INT(11) NOT NULL,
PRIMARY KEY (BEER_ID),
CHECK (BEER_ID>1000000)
/* FOREIGN KEY(BREWING_PROGRAM_ID) REFERENCES brewing_programs(BREWING_PROGRAM_ID) */
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='beer data' AUTO_INCREMENT=1000000;

CREATE TABLE IF NOT EXISTS spartanbrewdb.beer_styles (
BEER_TYPE 			VARCHAR(255) DEFAULT NULL,
BEER_STYLE 			VARCHAR(255) DEFAULT NULL,
BEER_STYLE_DESCRIPTION TEXT,
UNIQUE(BEER_TYPE,BEER_STYLE)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='beer styles';

CREATE TABLE IF NOT EXISTS spartanbrewdb.brewer_info (
BREWER_ID 			INT(11) NOT NULL AUTO_INCREMENT,
BREWER_FIRST_NAME 	VARCHAR(255) NOT NULL,
BREWER_LAST_NAME 	VARCHAR(255) NOT NULL,
BREWER_EMAIL		VARCHAR(255) NOT NULL,
BREWER_PASSWORD_HASH VARCHAR(255) NOT NULL,
BREWER_LOGIN_STATUS TINYINT(1) NOT NULL DEFAULT '0',
SPARTANBREW_ID 		VARCHAR(16) NOT NULL,
REGISTRATION_DATE	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (BREWER_ID),
UNIQUE(BREWER_EMAIL),
UNIQUE(SPARTANBREW_ID),
CHECK (BREWER_ID>1000000)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='brewer info' AUTO_INCREMENT=1000000;

CREATE TABLE IF NOT EXISTS spartanbrewdb.brewing_sessions (
BREWING_SESSION_ID	INT(11) NOT NULL AUTO_INCREMENT,
SPARTANBREW_ID 		VARCHAR(16) NOT NULL,
BREWER_ID 			INT(11) NOT NULL,
BEER_ID 			INT(11) NOT NULL,
ELAPSED_TIME 		TIME NULL,
REMAINING_TIME		TIME NULL,
TEMPERATURE_F		DOUBLE(4,1) NOT NULL DEFAULT '0.0',
TEMPERATURE_C		DOUBLE(4,1) NOT NULL DEFAULT '0.0',
SANITIZE_EQUIPMENT	TINYINT(1) NOT NULL DEFAULT '1',
ADD_WATER_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_GRAINS_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_GRAINS_TEMP		DOUBLE(4,1) NOT NULL DEFAULT '0',
REMOVE_GRAINS_FLAG	TINYINT(1) NOT NULL DEFAULT '0',
REMOVE_GRAINS_TIME	TIME NULL,
ADD_LME_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_DME_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
WORT_BOILING_TIME	TIME NULL,
ADD_HOPS_1_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_HOPS_1_TIME		TIME NULL,
ADD_HOPS_2_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_HOPS_2_TIME		TIME NULL,
ADD_HOPS_3_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_HOPS_3_TIME		TIME NULL,
ADD_HOPS_4_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_HOPS_4_TIME		TIME NULL,
ADD_WHIRLFLOC_FLAG	TINYINT(1) NOT NULL DEFAULT '0',
COOLING_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
SOLENOID_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_YEAST_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
FINISH_FLAG			TINYINT(1) NOT NULL DEFAULT '0',
BREWING_DATE_START	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (BREWING_SESSION_ID),
UNIQUE(BREWER_ID),
CHECK (BREWING_SESSION_ID>1000000)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='brewing sessions' AUTO_INCREMENT=1000000;

CREATE TABLE IF NOT EXISTS spartanbrewdb.brewing_history (
BREWING_SESSION_ID	INT(11) NOT NULL,
SPARTANBREW_ID 		VARCHAR(16) NOT NULL,
BREWER_ID 			INT(11) NOT NULL,
SESSION_TEMP		DOUBLE(5,2) DEFAULT NULL,
TOTAL_SESSION_TIME	TIME NOT NULL,
ADD_WATER			TINYINT(1) NOT NULL DEFAULT '0',
ADD_LME				TINYINT(1) NOT NULL DEFAULT '0',
ADD_HOPS			TINYINT(1) NOT NULL DEFAULT '0',
ADD_WTAB			TINYINT(1) NOT NULL DEFAULT '0',
ADD_YEAST			TINYINT(1) NOT NULL DEFAULT '0',
BREWING_DATE_START	TIMESTAMP NOT NULL,
BREWING_DATE_END	TIMESTAMP NOT NULL,
PRIMARY KEY (BREWING_SESSION_ID),
UNIQUE(BREWER_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='brewing history';

CREATE TABLE IF NOT EXISTS spartanbrewdb.brewing_programs (
BREWING_PROGRAM_ID 	INT(11) NOT NULL AUTO_INCREMENT,
SANITIZE_EQUIPMENT	TINYINT(1) NOT NULL DEFAULT '0',
ADD_WATER_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_GRAINS_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_GRAINS_TEMP		DOUBLE(4,1) NOT NULL DEFAULT '0',
REMOVE_GRAINS_FLAG	TINYINT(1) NOT NULL DEFAULT '0',
REMOVE_GRAINS_TIME	TIME NOT NULL,
ADD_LME_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_DME_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
WORT_BOILING_TIME	TIME NOT NULL,
ADD_HOPS_1_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_HOPS_1_TIME		TIME NOT NULL,
ADD_HOPS_2_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_HOPS_2_TIME		TIME NOT NULL,
ADD_HOPS_3_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_HOPS_3_TIME		TIME NOT NULL,
ADD_HOPS_4_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
ADD_HOPS_4_TIME		TIME NOT NULL,
ADD_WHIRLFLOC_FLAG	TINYINT(1) NOT NULL DEFAULT '0',
ADD_YEAST_FLAG		TINYINT(1) NOT NULL DEFAULT '0',
PRIMARY KEY (BREWING_PROGRAM_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='brewing programs' AUTO_INCREMENT=1000000;

/* ***************************************************************************** */
/* ******************************** INSERT INTO ******************************** */
/*
0 = Not yet added
1 = Needs to be added next
2 = Successfully added
3 = N/A (not required)
*/
INSERT INTO spartanbrewdb.brewing_programs (SANITIZE_EQUIPMENT,ADD_WATER_FLAG,ADD_GRAINS_FLAG,ADD_GRAINS_TEMP,REMOVE_GRAINS_FLAG,REMOVE_GRAINS_TIME,ADD_LME_FLAG,ADD_DME_FLAG,
											WORT_BOILING_TIME,ADD_HOPS_1_FLAG,ADD_HOPS_1_TIME,ADD_HOPS_2_FLAG,ADD_HOPS_2_TIME,ADD_HOPS_3_FLAG,ADD_HOPS_3_TIME,ADD_HOPS_4_FLAG,
											ADD_HOPS_4_TIME,ADD_WHIRLFLOC_FLAG,ADD_YEAST_FLAG) VALUES
('1','0','0','165','0','00:30:00','0','3','01:05:00','0','00:05:00','0','00:35:00','0','00:55:00','3','00:00:00','3','0'),
('1','0','0','165','0','00:00:15','0','3','00:01:00','0','00:00:15','0','00:00:15','0','00:00:15','3','00:00:00','3','0');

INSERT INTO spartanbrewdb.beer_styles (BEER_TYPE,BEER_STYLE,BEER_STYLE_DESCRIPTION) VALUES
('Ale','American Ale',''),
('Ale','Australian Ale',''),
('Ale','Belgian / French Ale',''),
('Ale','English Ale',''),
('Ale','German Ale',''),
('Ale','Irish Ale',''),
('Ale','Scottish Ale',''),
('Lager','American Lager',''),
('Lager','Czech Lager',''),
('Lager','European Lager',''),
('Lager','German Lager',''),
('Lager','Japanese Lager','');

INSERT INTO spartanbrewdb.beer_info (BEER_ID,BEER_NAME,BEER_TYPE,BEER_STYLE,BEER_DESCRIPTION,BEER_URL,BEER_ABV,BEER_IBU,BEER_SRM,BEER_OG,BREWING_PROGRAM_ID) VALUES
('', 'Altbier', 'Ale', 'German Ale', 'German for "old ale", Altbiers are a German version of Brown Ale. A malty beer with a firm bitterness. The yeast, Whitelabs WLP011 European, does not produce many esters so the style is low in fruitiness for an Ale. This is further enhanced by cold aging for a month or two. It is rare to find a good commercial example of Altbier in the U.S. The malt extract for this kit is made entirely from German Pilsner Malt, giving it that classic European flavor.', 'http://morebeer.com/products/altbier-extract-beer-kit.html', '5.00', '30.0', '16.0', '1.052','1000000'),
('', 'Amber Ale - Gluten Free', 'Ale', 'American Ale', 'Our Amber Ale kit includes Dark Candi Syrup to add color. We recommend brewing this beer after you''ve tried using just sorghum and rice extract. Candi Syrup will add sweetness which helps mask the pepper like flavors from sorghum. We encourage you to experiment with our line of Candi Syrup.', 'http://morebeer.com/products/amber-ale-gluten-free-extract.html', '5.30', '23.7', '16.7', '1.050','1000000'),
('', 'Amber Lager', 'Lager', 'American Lager', 'Similar to a popular East Coast lager, this recipe features a light soft malt flavor combines with an interesting and pronounced hop flavor/finish to produce a very tasy beer.', 'http://morebeer.com/products/amber-lager-extract-beer-kit.html', '4.50', '35.0', '11.0', '1.045','1000001'),
('', 'Amber Light Ale', 'Ale', 'American Ale', 'This recipe is our basic blonde ale kit with a little more "flare". We included a nice blend of Crystal 40L and Crystal 120L to add a slight nutty caramel flavor. A malt forward beer with a nice citrus aroma. This is definitely a great session beer to share with your friends.', 'http://morebeer.com/products/amber-light-ale-extract-beer-kit-1.html', '4.90', '20.0', '14.0', '1.046','1000000'),
('', 'American Ale', 'Ale', 'American Ale', 'A light colored, hoppy Pale Ale that really depicts the Cascade hop in both flavor and aroma. Light in color but not in flavor!', 'http://morebeer.com/products/american-ale-extract-beer-kit.html', '4.50', '55.0', '9.0', '1.046','1000000'),
('', 'American Amber Ale', 'Ale', 'American Ale', 'A rich Amber Ale. An American variation of an English Pale Ale. Features Willamette hops for flavor and aroma. The combination of the darker Crystal malts with Willamette hops provides for a flavor that is distinctly different than our American Pale Ale. Higher in alcohol with a creamy mouth feel.', 'http://morebeer.com/products/american-amber-ale-extract-beer-kit.html', '5.00', '50.0', '12.0', '1.052','1000000'),
('', 'American Brown Ale', 'Ale', 'American Ale', 'An American variation of a Brown Ale that falls between an Amber Ale and a Porter. SpartanBrew!''s Brown Ale has a firm, but not overwhelming bitterness, with lots of Cascade hop flavor in the finish. A 1/4lb of chocolate malt is used to give the beer its brown color and roasty malt flavor.', 'http://morebeer.com/products/american-brown-ale-extract-beer-kit.html', '4.50', '50.0', '18.0', '1.047','1000000'),
('', 'American Honey Pale Ale', 'Ale', 'American Ale', 'Truly a classic American Pale Ale recipe! This ale will deliver a smooth blend of Cascade floral character and biterness, tempered by a slight sweetness from the honey. The California Wildflower Honey delivers just enough residual sweetness to result in an amazingly balanced, hoppily delicious pale ale.', 'http://morebeer.com/products/american-honey-pale-ale-extract-beer-kit.html', '6.00', '40.0', '7.0', '1.054','1000000'),
('', 'American Honey Porter', 'Ale', 'American Ale', 'This is an amazingly drinkable porter recipe which will have you coming back for more! The classic porter character of roast and coffee is beautifully balanced by a pleasant bitterness and a slight nutty taste. This is a beer which will be fantastic fresh, and even better if you can keep your hands off long enough to let it age! The honey character is nearly buried under the porter character, but provides an interesting and refreshing spin on the classic porter!', 'http://morebeer.com/products/american-honey-porter-extract-beer-kit.html', '6.00', '33.0', '26.0', '1.055','1000000'),
('', 'American IPA', 'Ale', 'American Ale', 'An IPA is like a Pale Ale on steroids - take a pale ale and add more malt, more grain, and more hops. Our version, with 9 lbs of malt extract and 5.5 oz of Magnum and Cascade, is big. IPA is drinkable right away but gets better with 1-2 months of aging, as the alcohol mellows and the different flavors mix together.', 'http://morebeer.com/products/american-ipa-extract-beer-kit.html', '6.00', '84.0', '10.0', '1.060','1000000'),
('', 'American Lite Ale', 'Ale', 'American Ale', 'A lite beer similiar to the major American brands. Not much flavor, not much bitterness, not much of anything to tell you the truth. However, sometimes that is exactly what we are looking for. A good beer for general mass-consumption. Uses dry rice extract as part of the base.', 'http://morebeer.com/products/american-lite-ale-extract-beer-kit.html', '3.50', '12.0', '3.3', '1.035','1000000'),
('', 'American Pale Ale II', 'Ale', 'American Ale', 'Looking for the perfect Pale Ale to share with friends this summer? Do you like a Pale Ale with a rich malt flavor and a ton of hop character but without an overwhelming bitterness? Then the Pale Ale II should be your next brew. We took our American Pale recipe and upped the malt, threw a ton of hops in the finish for flavor, but kept the bitterness the same. We think toning down the perceived bitterness is one reason we consistently get great reviews from brewers sharing this with friends. Keeping it real: Part of the success of this kit is blending a lot of Willamette and Cascade hops in the finish. This isn''t a wild, new or crazy idea... this is old school. Cascade and Willamette were the hops that helped put craft brewing on the map in the 1980''s. The reason they are still so popular... they make a damn good beer. Truly delectable and different yet still keeping it real.\n\n', 'http://morebeer.com/products/american-pale-ale-ii-extract-beer-kit.html', '5.20', '55.0', '11.0', '1.055','1000000'),
('', 'American Red Ale', 'Ale', 'American Ale', 'Red Ale is technically not a beer style category. Oh, well. It was created (and is continually evolving) in microbreweries throughout the US. Usually very similar to Amber Ale but with additional, darker crystal malts. SpartanBrew! takes a different approach. We make it red with 2oz of Roasted Barley. The result is a red-colored beer but without the deeper, caramalized flavors. We add a combination of Cascade and Northern Brewer hops that combine with the malt flavors to make this a unique beer you won''t find anywhere else', 'http://morebeer.com/products/american-red-ale-extract-beer-kit.html', '4.50', '42.0', '15.0', '1.048','1000000'),
('', 'American Wheat', 'Ale', 'American Ale', 'A really low-bitterness, mild, smooth beer for easy, frequent drinking. This beer is a great choice if you want to customize a beer with any of our fruit purees or flavorings. An ideal summertime thirst quencher.', 'http://morebeer.com/products/american-wheat-extract-beer-kit.html', '3.80', '15.0', '6.0', '1.040','1000000'),
('', 'B3 Stout', 'Ale', 'American Ale', 'When we developed this stout over the years we were going for a flavor that was similar to Guinness but with reduced bitterness and more malt flavor. We use 1 lb of Roasted Barley and leave out the Chocolate and Black Patent found in many stouts. This provides for a very clean, precise dark malt flavor. We always talk customers into this kit and they are always thankful we did. Our best selling stout recipe.', 'http://morebeer.com/products/b3-stout-extract-beer-kit.html', '5.30', '40.0', '36.0', '1.055','1000000'),
('', 'Barley Wine', 'Ale', 'American Ale', 'Barleywine - made from barley but can be aged like wine. Our Barleywine has a beautiful copper color, voluptous body, and inviting smells of malt and hops. But don''t let the good looks catch you off guard. This is a powerful beer with a bitter, yet balanced bite. Recipe includes 12 lbs of malt extract with Caravienne and Caramunich malts for steeping. Huge flavor with a good balance between malt and hops. This will age gracefully for years. Not for everyone, but those who like Barley Wines love this recipe.', 'http://morebeer.com/products/barley-wine-extract-beer-kit.html', '7.80', '84.0', '16.0', '1.080','1000000'),
('', 'Belgian Ale', 'Ale', 'Belgian / French Ale', 'Belgian ales are really about creating a simple yet elegant malt base upon which the unique Belgian yeast strains can create their wonderful, complex flavors. This Belgian Ale is their equivalent of our pale ale in alcoholic strength and body. The difference is that the hops are very subdued and only complimentary where as in many American beers hops can create a majority of the flavor profile. One is not better than the other just different, and we love diversity in beer.', 'http://morebeer.com/products/belgian-ale-extract-beer-kit.html', '5.00', '33.0', '4.0', '1.050','1000000'),
('', 'Belgian Dubbel', 'Ale', 'Belgian / French Ale', 'Our signature Belgian Dubbel kit is to die for! We use the traditional grains: Belgian Special B and Caramunich malts which give it a slight caramel flavor that the Trippel does not have. Pour a glass, close your eyes and imagine yourself as a monk with a job to do. Now get to work and sample that beer.', 'http://morebeer.com/products/belgian-dubbel-extract-beer-kit.html', '5.90', '22.0', '16.0', '1.060','1000000'),
('', 'Belgian Pale Ale', 'Ale', 'Belgian / French Ale', 'Sometimes you want to drink a belgian but not get too buzzed too quickly. So we created this belgian pale ale that has the spicy phenolics you want but without a lot of alcohol. Still packed with a lot of flavor from the caramunich and special B. We include 8oz of corn sugar to help dry out the beer during fermentation as well. Belgians are suppose be dry but bold in flavor. We give you the SpartanBrew! Belgian Pale Ale.', 'http://morebeer.com/products/belgian-pale-ale-extract-beer-kit-1.html', '5.20', '20.0', '14.0', '1.052','1000000'),
('', 'Belgian Saison', 'Ale', 'Belgian / French Ale', 'Traditionally brewed in the farms of Belgium, Saisons were the thirst quenchers of the farmers. Fruity/spicy notes combined with a dry finish and a somewhat high hop bill than one would expect, these beers were perfect for a hot Summer day in the fields. Our Saison kit brings the flavor of the old world to the backyards and picnics of today. Generous amounts of Munich Extract give the beer a light backbone of malt, while the CaraMunich lends body and character.', 'http://morebeer.com/products/belgian-saison-extract-beer-kit.html', '8.00', '20.0', '10.0', '1.082','1000000'),
('', 'Belgian Trippel', 'Ale', 'Belgian / French Ale', 'Liquid Gold! So smooth for a beer with an alcohol by weight of 7%! This recipe includes quality sugar, plus an immense amount of both dried and liquid Light Malt Extract, hops and uses the Trappist yeast strain. It leaves lots of classic phenolic flavor, but produces a very soft body without a high alcohol bite. Not that bitter, this golden beer is about a strong and complex malt body. It may take a goblet or two to grow on you, but once you acquire the taste.... some would say "beervana." The malt extract for this kit is made entirely from German Pilsner Malt, giving it that classic European flavor.', 'http://morebeer.com/products/belgian-trippel-extract-beer-kit.html', '7.00', '24.0', '6.0', '1.074','1000000'),
('', 'Berry Beer', 'Ale', 'American Ale', 'A low hopped beer featuring dried wheat malt extract, dextrin for body and natural raspberry flavoring. A crowd pleaser and a good party beer.', 'http://morebeer.com/products/berry-beer-extract-kit.html', '4.00', '12.0', '7.0', '1.042','1000000'),
('', 'Best Bitter Ale', 'Ale', 'English Ale', 'A really easy-drinking, yet extremely flavorful English-style beer that features English Carastan malt. Light golden color combines with lots of British Kent Golding hops to provide the British equivalent of SpartanBrew!''s Light Ale, though with more flavor. Don''t let the name fool you; the bitterness is really quite moderate. Start drinking this beer and before you realize it you will have gone through a few pints.', 'http://morebeer.com/products/bitter-ale-extract-beer-kit.html', '4.00', '27.0', '7.0', '1.043','1000000'),
('', 'Biere de Garde', 'Lager', 'European Lager', 'The "Original Gatoraid", Bière de Garde was said to give the French and Belgian farmer a much needed boost of energy during the day, due to the low alcohol and relatively high residual sugar content. Our version has a bit more malt than tradition dictates, but we think you will find this beer highly drinkable. The malt is the focus of this style of beer, with a slight toasty nose from the Munich. A yeasty character is not uncommon, and is achieved by an extended period of contact with the yeast bed – some commercial breweries go for up to six weeks! This should be fermented at 64°F.', 'http://morebeer.com/products/biere-de-garde-extract-beer-kit.html', '8.00', '20.0', '15.0', '1.082','1000000'),
('', 'DOZE Black IPA', 'Ale', 'American Ale', 'This beer is inspired by the style many refer to as Cascadian Dark Ale or Black IPA, however it is not intended to fit the mold of any particular guideline. Mostly it is big, dark, hoppy, and delicious.', 'http://morebeer.com/products/black-ipa-doze-extract-beer-kit.html', '6.50', '74.0', '26.0', '1.068','1000000'),
('', 'Blonde Ale', 'Ale', 'American Ale', 'A Blonde Ale is a great starter beer for those who are new to craft beer. An easy drinking ale, low in esters, balanced with enough hop character to accentuate the malt profile. We brew this beer for big party events.', 'http://morebeer.com/products/blonde-ale-extract-beer-kit-1.html', '4.50', '15.0', '8.0', '1.045','1000000'),
('', 'Bock', 'Lager', 'German Lager', 'An extremely malty, copper colored beer. A lager requiring cold fermentation in the 48 to 58 degree range. The hop flavor is subdued in favor of the rich maltiness. Let it age for about six months at lagering temperatures, but it will be ready to drink after only one month. Higher in alcohol. The malt extract for this kit is made entirely from German Pilsner Malt, giving it that classic European flavor.', 'http://morebeer.com/products/bock-extract-beer-kit.html', '6.00', '12.0', '10.0', '1.064','1000000'),
('', 'Brown Porter', 'Ale', 'American Ale', 'If you like maltiness emphasized with a hint of chocolate roastiness and subtle caramel nuttiness this is the beer for you. Medium-low to medium hop bitterness. Light brown to dark brown in color, often with ruby highlights.', 'http://morebeer.com/products/brown-porter-extract-beer-kit-1.html', '5.20', '30.0', '20.0', '1.048','1000000'),
('', 'California Common Ale', 'Ale', 'American Ale', 'California Common is a unique tasting beer that typically utilizes Northern Brewer hops. With subdued fruity flavors, good hop bite and medium maltiness, this beer still retains its unique qualities due to a famous liquid yeast strain that retains lager characteristics up to 65 degrees.', 'http://morebeer.com/products/california-common-ale-extract-beer-kit.html', '4.50', '38.0', '12.0', '1.045','1000000'),
('', 'Citra Pale Ale', 'Ale', 'American Ale', 'If you''re looking for a great session pale ale this is your beer. Featuring the incredibly famous Citra Hops, we''ve packed this recipe with a hop bomb of floral aromas and subtle grapefruit flavors.', 'http://morebeer.com/products/citra-pale-ale-extract-beer-kit.html', '5.50', '45.0', '5.0', '1.050','1000000'),
('', 'Columbus IPA', 'Ale', 'American Ale', 'An IPA recipe that features the high oil content Columbus hop in the finish. Lots and lots of aroma combined with very evident hop flavor. The Columbus hop flavor and aroma help work to soften the apparent bitterness. The malt extract and grain remains the same as the American IPA recipe.', 'http://morebeer.com/products/columbus-ipa-extract-beer-kit.html', '6.00', '64.0', '10.0', '1.060','1000000'),
('', 'Doppelbock', 'Lager', 'German Lager', 'We are in general agreement in the shop, this is the recipe for the best Bock we have ever tasted. The secret to great Bock is to use high percentages of Munich malt. With 9 lbs of Munich Malt Extract, we''re able to pull it off and bring you one big, bad (in a good way), Bock!', 'http://morebeer.com/products/kit-doppelbock.html', '9.10', '20.0', '16.0', '1.092','1000000'),
('', 'Dunkelweizen', 'Ale', 'German Ale', 'A true Dunkelweizen recipe. This beer style focuses on the traditional hefeweizen flavors and aroma''s but with more malt flavor. A nice blend of caramunich and chocolate malt help give the beer a nice dark color and round malt character.', 'http://morebeer.com/products/dunkelweizen-extract-beer-kit-1.html', '5.20', '10.0', '19.0', '1.051','1000000'),
('', 'English IPA', 'Ale', 'English Ale', 'This English IPA features Ultralight Malt Extract and British Kent Goldings and Magnum hops for a nice, unique English flavor. It comes with 1 oz of toasted French Oak Chips that can be added to the fermenter after the first week of fermentation.', 'http://morebeer.com/products/english-ipa-extract-beer-kit.html', '6.50', '55.0', '11.0', '1.067','1000000'),
('', 'English Pale Ale', 'Ale', 'English Ale', 'English Pales are not that bitter. There is more emphasis on the malt which tends to have caramel and roasted notes. Traditionally these beers are poured from a cask, usually flat without any CO2. If you''re serving this beer at home we encourage you to only carbonate around 6-8psi to have a true English pale ale experience.', 'http://morebeer.com/products/english-pale-ale-extract-beer-kit-1.html', '4.00', '26.0', '14.0', '1.040','1000000'),
('', 'Extra Special Bitter Ale', 'Ale', 'English Ale', 'Big, smooth malt flavor and the mellow aroma of British Kent Golding hops. In the English draft style, with a firm hop bitterness and mellow hop flavor.', 'http://morebeer.com/products/extra-special-bitter-ale-extract-beer-kit.html', '4.50', '40.0', '11.0', '1.047','1000000'),
('', 'Flanders Red Ale', 'Ale', 'Belgian / French Ale', 'Deep red in color with a nice malt structure, this beer is based on those from certain regions of Belgium, and have distinct sour overtones to them. This is due to the wild spores that inhabit the air - and some breweries - of the area. While this would normally be a "bad" thing, the infection lends special tart and sour qualities unlike any other beer can. For a more traditional spin on this kit, try aging it on some oak cubes!', 'http://morebeer.com/products/flanders-red-ale-extract-beer-kit.html', '6.00', '20.0', '18.0', '1.064','1000000'),
('', 'Galaxy Extra Pale', 'Ale', 'Australian Ale', 'Behold, our extra pale kit featuring hops from the land down under...Australia! This over the top pale is a hop bomb! A classic American Pale Ale with deep aromas of passion fruit and citrus.', 'http://morebeer.com/products/galaxy-extra-pale-extract-beer-kit.html', '6.00', '55.0', '12.0', '1.060','1000000'),
('', 'German Hefeweizen', 'Ale', 'German Ale', 'A German-Style Wheat Beer with a blond color and hazy appearance. There is very little hops in this recipe because the flavor is based primarily on the flavor of the very specialized Hefeweizen yeast. Six pounds of Bavarian Dried Wheat Malt Extract, 60% wheat and 40% barley, is used as the base extract. A simple, yet award winning recipe that has become a favorite with our customers who enjoy German-Style Wheat Beer.', 'http://morebeer.com/products/german-hefeweizen-extract-beer-kit.html', '4.50', '13.0', '7.0', '1.048','1000000'),
('', 'Honey Ale - Gluten Free', 'Ale', 'American Ale', 'This ale recipe features the use of clover honey, dried rice extract and sorghum. Try adding some dark candi syrup to give it some color. Gluten free beers are a different world when it comes to finding a suitable replacement for the base extract. Celiacs are alleric to the hordein protein found in the base malts such as 2-Row and Pilsner malt. They are also allergic to the gliadin protein found in wheat which is the biggest offender of the two proteins.As a homebrewer your goal is to find a suitable fermentable that can emulate the maltiness in beer. Our Gluten recipes use Sorghum extract for the base fermentables.Hops aggressively cut through the maltiness from sorghum easily.Hop additions in gluten free beers tend to be 40-50% less than normal. All our gluten kits include dry yeast due to the small traces of the gliadin protein found in liquid yeast.(Although lab research has found the yeast metabolize the gliadin protein after fermentation and significantly reduce the ppm present.)', 'http://morebeer.com/products/honey-ale-gluten-free-extract.html', '5.50', '15.0', '5.0', '1.055','1000000'),
('', 'Hop Blonde', 'Ale', 'American Ale', 'This Hop Blonde is definitely one that you won''t forget! You''ll dream about it. You''ll get nervous when it is near, but you know that you two are made for each other. The recipe is actually a semi-standard blonde recipe, but it''s that "Simcoe personality" that makes this blonde so unique! Our Hop Blonde is well balanced, and the dry hop addition makes this beer slightly complex, but still easy to enjoy.', 'http://morebeer.com/products/hop-blonde-extract-beer-kit-2.html', '4.70', '30.0', '5.0', '1.045','1000000'),
('', 'Imperial Stout', 'Ale', 'American Ale', 'Bubbling Crude, Black Gold, Texas Tea - you may not strike oil in your backyard, but you can make Imperial Stout at home. With a texture and color similar to black crude oil, this monstrous, thick, chewy beer takes a minimum of six months to age out. The foundation of the beer is 12 lbs of malt extract. Then we throw in some Crystal, Chocolate, Roasted Barley and Black Patent malts. Yes, there are two additions of hops in this recipe but you probably will never taste them through all that malt flavor. This is a great beer for sipping in front of the fire. Will age for years, eventually gaining some Port-like flavors.', 'http://morebeer.com/products/imperial-stout-extract-beer-kit.html', '8.00', '80.0', '37.0', '1.083','1000000'),
('', 'IPA II "BKG Bomb"', 'Ale', 'English Ale', 'Where do German Malts and English Hops exist side by side in peace and unlikely harmony. In our BKG Bomb of an IPA! This big brusing beer, with an amazing mouth feel from copius amounts of Munich Malt Extract, is big on deep malt flavor and big on alcohol. It is the antithesis of todays super citrusy hopped, pale colored IPAs. This is all about malt, malt, malt and how British Kent Goldings (BKG) hops blend oh so well with a malt heavy beer. British Kent Goldings are the most prized ale hops in England and known for their subtle nature and floral aromas that really compliment malt flavors. Do you need a little extra sustenance to make it through the winter? Do you like to slice your beer with a knife? Do you need a break from over-the-top hopped IPA''s? If you answered yes to any of these questions, The BKG Bomb IPA II should be your next beer.', 'http://morebeer.com/products/ipa-ii-bkg-bomb-extract-beer-kit.html', '7.20', '84.0', '11.5', '1.075','1000000'),
('', 'Irish Red Ale', 'Ale', 'Irish Ale', 'This beer is similar to a big Amber Ale, but is so unusual it does not really fit within any category. Contains Aromatic malt to provide malty flavor and aroma. Features dark Crystal malts, including Special B, and a pinch of Roasted Barley for a deep, red color and a very distinctive caramel flavor. This is one of our most popular ingredient kits about which we receive a lot of positive feedback from satisfied customers. If you''re going to be venturing into new realms of taste discovery, this is a winning ticket we can solidly recommend! Our best selling kit.', 'http://morebeer.com/products/irish-red-ale-extract-beer-kit.html', '4.50', '43.0', '22.0', '1.048','1000000'),
('', 'Kolsch Ale', 'Ale', 'German ale', 'A German Lager/Ale that is traditional made in Köln Germany. Features a Kölsch yeast strain that retains its crisp lager-like characteristics even at warmer temperatures. Ideally this kit requires fermentation between 58 - 64F followed by cold aging for several weeks, it is a very tasty summer brew. Blond color, low hop bitterness, smooth flavor - grab a few bottles and head for the pool. This kit includes 4 pound of our SpartanBrew German Pilsner liquid malt extract for authentic pils type flavor and 2 pounds of Cooper DME to give a more complex malt flavor to this light beer style. Also comes with 4 ounces of Dextrin powder to boost mouthfeel.', 'http://morebeer.com/products/kolsch-ale-extract-beer-kit.html', '4.00', '30.0', '5.5', '1.042','1000000'),
('', 'Light Ale', 'Ale', 'American Ale', 'A good transition beer for those individuals used to easy drinking American styles. This beer has the same bitterness levels (low) as American beers, but is an all-malt product, as there is no rice or corn used. Light golden color. Experience the difference of good taste!', 'http://morebeer.com/products/light-ale-extract-beer-kit.html', '3.80', '15.0', '7.0', '1.040','1000000'),
('', 'Light Ale - Gluten Free', 'Ale', 'American Ale', 'This light ale recipe is the most basic gluten free kit we offer. An ideal first low gluten brew so you can get an idea of what malt flavors sorghum contributes to beer. This recipe is light and easy drinking. Gluten free beers are a different world when it comes to finding a suitable replacement for the base extract. Celiacs are alleric to the hordein protein found in the base malts such as 2-Row and Pilsner malt. They are also allergic to the gliadin protein found in wheat which is the biggest offender of the two proteins.As a homebrewer your goal is to find a suitable fermentable that can emulate the maltiness in beer.\n\nOur Gluten recipes use Sorghum extract for the base fermentables.Hops aggressively cut through the maltiness from sorghum easily.Hop additions in gluten free beers tend to be 40-50% less than normal.\n\nAll our gluten kits include dry yeast due to the small traces of the gliadin protein found in liquid yeast.(Although lab research has found the yeast metabolize the gliadin protein after fermentation and significantly reduce the ppm present.)', 'http://morebeer.com/products/light-ale-gluten-free-extract.html', '5.10', '16.0', '4.0', '1.045','1000000'),
('', 'Malty Brown Ale', 'Ale', 'English Ale', 'The malt predominates in this smooth, complex wonderful beer. Bring it to different parts of the mouth to taste malt, bitterness, hop flavor. Features Munich extract and Abbey malt for a malty flavor and aroma. British Kent Golding hops in the finish provide for authentic English flavor. Loosely created in the Northern England Brown Style, but bigger in every way. You can''t buy this at your local grocery store! SpartanBrew! partner Olin Schultz''s favorite beer.', 'http://morebeer.com/products/malty-brown-ale-extract-beer-kit.html', '5.90', '33.0', '18.0', '1.056','1000000'),
('', 'Mild Brown Ale', 'Ale', 'English Ale', 'An English-style "session" ale, low in bitterness, but big on flavor. Usually served on-draft in England, it is a beer with a slight roast flavor from the chocolate colored malt. Lower in alcohol than most ales, thereby allowing you and your guests to quaff several pints in a tasting "session". It is best consumed within 2-8 weeks in the bottle, but will age nicely over the course of 3 months.', 'http://morebeer.com/products/mild-brown-ale-extract-beer-kit.html', '3.40', '23.0', '16.0', '1.033','1000000'),
('', 'Munich Helles', 'Lager', 'German Lager', 'A big blond German Lager. Soft body with low to medium bitterness of about 32 IBU and predominate malt flavor. We make it at the upper limits of gravity, according to style guidelines, with 8 lbs of malt extract. The malt for this kit is made entirely from German Pilsner Malt, giving it that classic pilsner flavor.', 'http://morebeer.com/products/munich-helles-extract-beer-kit.html', '5.00', '30.0', '6.0', '1.054','1000000'),
('', 'Nut Brown Ale', 'Ale', 'American Ale', 'Our Nut Brown Ale has a richer, maltier, less bitter flavor than the American Brown Ale. Victory malt provides a nutty, biscuity flavor. A very full, robust beer.', 'http://morebeer.com/products/nut-brown-ale-extract-beer-kit.html', '5.00', '30.0', '16.0', '1.053','1000000'),
('', 'ObSession IPA', 'Ale', 'American Ale', 'If you''re looking for a new IPA to obsess over, look no further! This Session IPA is a beautiful blend of Warrior, Simcoe, Centennial and HBC-342 Experimental hops that bring the beer to right around 60 IBUs. While the general rule of thumb has been "one or two IPAs and you''re feeling it", at just under 5%, we like to think of this beer as a hop lovers dream. The type of IPA that you can open up at noon, get the grill going, and forget worrying about how you''re going to feel after drinking 8% IPAs for a few hours! (Yes, we know that feeling too...) A half pound of corn sugar helps this one finish out nice and dry, while a small amount of acidulated malt will help make those hops pop. The clean bitterness of Warrior balances perfectly with a slightly sweet malt profile, all topped off with a white, frothy head thanks to the wheat malt.', 'http://morebeer.com/products/obsession-ipa-extract-beer-kit.html', '5.00', '60.0', '6.0', '1.050','1000000'),
('', 'Octoberfest', 'Lager', 'German Lager', 'This fest beer, historically brewed in spring and aged in cold caves over the summer, is a copper-colored Lager with an emphasis on that German malt flavor. Our recipe achieves that malt flavor with lots of Pilsner malt extract. The use of Caravienne and Caramunich malts contribute the copper color and a unique, subdued toffee/malt flavor. First-addition hops are Hallertauer, while finishing-hops are Czech Saaz. To make this as an Ale use the WLP011 European option below. The Ale yeast works because it has a subdued fruitiness and intense maltiness.', 'http://morebeer.com/products/octoberfest-extract-beer-kit.html', '5.60', '22.0', '11.0', '1.056','1000000'),
('', 'Old Ale', 'Ale', 'American Ale', 'Old Ale kit has a nice richness and complexity that you don''t find with most Old Ales. The crystal malts provide a great caramel backbone, perfect for aging for 4-6 months.\n\nTip: try aging this beer on 1-2 oz of French or Hungarian Oak Cubes for a great old world flavor!', 'http://morebeer.com/products/ale-extract-beer-kit.html', '8.00', '5.6', '26.0', '1.083','1000000'),
('', 'Pilsner', 'Lager', 'German Lager', 'A crisp, golden pilsner with a light malt flavor that comes from SpartanBrew! Pilsner malt extract. The spicy hop flavor comes from the Czech Saaz hops that are added late in the boil. Low in fruity esters as is characteristic of this style. Added body comes from the addition of Dextrin Powder.', 'http://morebeer.com/products/pilsner-extract-beer-kit.html', '4.60', '30.0', '5.0', '1.046','1000000'),
('', 'Porter', 'Ale', 'American Ale', 'A good first dark beer. Chocolate and Black Patent malts are the backbone of this style. They are the roasted grains that give Porter its dark color and roasty flavor. Our recipe also features dextrin powder which gives it a creamy body. The Northern Brewer hops impart a nice, but not overpowering, bitterness.', 'http://morebeer.com/products/porter-extract-beer-kit.html', '4.80', '33.0', '30.0', '1.050','1000000'),
('', 'Red Kolsch Ale', 'Ale', 'German Ale', 'An interesting take on a Kölsch. Inspired by our craving for German Kölsch Beers, we tried to capture the drinkability but enhance the color and maltiness. Imagine a ale beer that is ruby in color and drinks like a lager! This is it!', 'http://morebeer.com/products/red-klsch-ale-extract-beer-kit.html', '5.00', '20.0', '17.0', '1.046','1000000'),
('', 'Renegade Rye', 'Ale', 'American Ale', 'Feeling a little rebellious? Like a pale ale that has gone astray? While the Renegade Rye doesn''t break all the rules, it certainly deserts the path of an average pale ale! The backbone of this brew is our rye liquid malt extract, which adds slight fruity and spicy characteristics to the malt flavors. The clean bitterness from Magnum hops allows these malt flavors to mix perfectly with the aromas of Columbus, Citra, and Centennial hops. So go ahead; brew the Renegade Rye and rebel against standard pale ales!', 'http://morebeer.com/products/renegade-rye-extract-beer-kit.html', '4.80', '40.0', '6.0', '1.045','1000000'),
('', 'Scotch Ale', 'Ale', 'Scottish Ale', 'An extremely malty beer that really emphasizes malt over hops. Most styles are more balanced, which means the bitterness of the hops is proportional to the sweetness of the malt. Not true with our Scotch ale where the deep malt flavor is king. Scotch Ale yeast strains typically ferment well in the low-to-mid 60''s and leave behind very few esters or fruity flavors, which further emphasizes the malt. This recipe has over 11 lbs of malt extract and only one ounce of hops!', 'http://morebeer.com/products/scotch-ale-extract-beer-kit.html', '8.00', '20.0', '19.0', '1.084','1000000'),
('', 'Scottish 60 Shilling Ale', 'Ale', 'Scottish Ale', 'Clean malty beer that finishes on the dry side. Low hops, along with low alcohol percentage, make this beer a great session beer!', 'http://morebeer.com/products/scottish-60-shilling-ale-extract-beer-kit.html', '3.50', '16.0', '23.0', '1.032','1000000'),
('', 'Scottish Export "80/-" Ale', 'Ale', 'Scottish Ale', 'This Scottish Export has a rich malty character balanced by a firm Northern Brewer bittering hop. Bready toasted notes will come through as you drink it. Scottish Exports are great session beers and are meant for bulk consumption. The "80/-" represents the original cost of the beer in Scotland: 80 shillings!', 'http://morebeer.com/products/scottish-export-80-ale-extract-beer-kit-1.html', '4.50', '30.0', '17.0', '1.046','1000000'),
('', 'Simcoe SMaSH IPA', 'Ale', 'American Ale', 'What happens when you make a single malt and single hop IPA using our Ultralight Malt Extract mixed with Simcoe hops? Deliciousness, in a glass. This brew comes in at around 6.5% ABV and 65 IBUs, making for a crisp, hop forward, west coast style IPA. Without the characteristics of specialty malts or multiple hop varietals, the bitterness, flavors and aromas of Simcoe really shine through. If you''re looking for a winning combination, try our Ultralight Extract & Simcoe SMaSH IPA today!', 'http://morebeer.com/products/simcoe-smash-ipa-extract-beer-kit.html', '6.50', '60.0', '5.0', '1.062','1000000'),
('', 'Smoked Scotch Ale', 'Ale', 'Scottish Ale', 'Same as our regular scotch ale but with a 1/4 lb of smoked grain. This is a great beer to lay down and age for up to a couple of years.', 'http://morebeer.com/products/smoked-scotch-ale-extract-beer-kit.html', '8.00', '20.0', '19.0', '1.084','1000000'),
('', 'Sour Belgian Blonde', 'Ale', 'Belgian / French Ale', 'This Belgian Style Blonde, destined for a 100% Brettanomyces fermentation was born right here in our parking lot! On a whim, the CS Team decided to have fun with it and add 1 lb of California Golden Raisins per 5 gallons with the second dose of Brettanomyces. The sugars in the raisins ferment out completely and seem to be an excellent source of food for our ‘lil wild buddy''s. The end result: A classic lambic that is as mild or as wild as you make it! This is a great base recipe for a Belgian Style Blonde Ale. Great body and mouthfeel balanced with a funky delicious sour edge. So have fun with this Lambic Recipe and make it your own! Tips: Patience, patience, patience. If brewing All-Grain, try mashing higher for some added body. (We recommend 156F.) Brettanomyces loves oxygen just as much, or maybe more than Saccharomyces spread the love! Use restraint with these critters, don’t add the whole kitchen sink. Experiment with one to two cultures per batch, at intervals, and preferably with a small amount of a new food source. Patience. CA Golden Raisins are an excellent food source! (ahem, hint hint!) Don’t disturb the fermentation vessel while the pellicle is formed. The pellicle provides protection from excessive oxidation over the long aging time. Patience. Use excellent sanitary methods when working with our wild lil buddy’s to ensure a clean brewhouse. Try adding any local fruit as a food source for the bugs and wild yeasts. They love it! Patience!', 'http://morebeer.com/products/sour-belgian-blond-extract-beer-kit.html', '6.00', '7.0', '4.0', '1.060','1000000'),
('', 'Stout', 'Ale', '', 'Very similar to our Porter, but includes Roasted Barley and a higher hopping rate for that true, coffee-like, burnt-Stout flavor. This is a micro-brewery-style Dry Stout with a pretty good dose of bitterness. Full, crisp flavor, black color, and a nice, dry finish.', 'http://morebeer.com/products/stout-extract-beer-kit.html', '4.50', '30.0', '36.0', '1.046','1000000'),
('', 'Strawberry Blonde', 'Ale', 'American Ale', 'This beautiful beer is definitely one that will catch your attention! With a light, malt forward approach, the base beer is delicious on its own. When you add the natural strawberry flavoring (included), it truly becomes a delicate, but flavorful, masterpiece. This is a beer that everyone can enjoy, at pretty much anytime of the day. During a BBQ in the afternoon or relaxing in the evening, we''re pretty sure you''ll want to have another! We include 4 oz of our natural strawberry flavoring, which provides a noticeable but not overpowering flavor.', 'http://morebeer.com/products/strawberry-blonde-ale-extract-beer-kit.html', '4.50', '16.0', '6.0', '1.045','1000000'),
('', 'Sweet Stout', 'Ale', 'American Ale', 'A sweet stout uses lactose (milk sugar) to add a silky creamy texture to the body of the beer. This beer is rich and full of roasted flavors complimented with a sweetness from the lactose. Lactose is un-fermentable which adds a creamy body to the beer.', 'http://morebeer.com/products/sweet-stout-extract-beer-kit-1.html', '4.50', '40.0', '38.0', '1.047','1000000'),
('', 'Vienna Lager', 'Lager', 'European Lager', 'A European lager packed with incredible maltiness. A very easy drinking beer, low in hop character with a clean malt profile. This is a lager which requires cold fermentation. Takes 4-6 weeks to ferment in primary but is well worth the wait. Goes well with pretzel''s and sausages.', 'http://morebeer.com/products/vienna-lager-extract-beer-kit-1.html', '4.40', '12.0', '10.0', '1.044','1000000');

INSERT INTO spartanbrewdb.brewer_info (BREWER_FIRST_NAME, BREWER_LAST_NAME, BREWER_EMAIL, BREWER_PASSWORD_HASH, SPARTANBREW_ID) VALUES
('Admin', 'Admin', 'admin@spartanbrew.net', '$2y$10$7sZ4Y0hyFeW3hHHo6MkwpekBY1.9XtIuZG2SEdHtA9SSqY5HQeK5G', '0000000000000000'),
('Guest', 'Guest', 'guest@spartanbrew.net', '$2y$10$yDlq2bBBonPEXDcIclkezuFR8WTxDePdotz7fUZmRVoJYplv/0yxq', '0000000000000001'),
('Lorenzo', 'Javier', 'loj90@sbcglobal.net', '$2y$10$OfUZmyWB/xXQ5rK5mH9gZuHl3f.lgZ4jidcaQ3D8qTZdoAtsDgk1q', '0000000000000002'),
('David', 'Bui', 'davidbui101@hotmail.com', '$2y$10$CMHIHINw/dU4ZTugftF7verrrhf2D0UsIEEDNVCodh4Lju4UTd4i2', '0000000000000003'),
('Delfin', 'Libaste', 'dlibaste@gmail.com', '$2y$10$JpTwWgKSH5tzT/3BrtCRUe7e7UteYzpdiDk0mJDFG03mbeHd.LeXi', '0000000000000004');

/* ********************************** COMMIT ********************************** */

COMMIT WORK;

/* ****************************************************************************** */

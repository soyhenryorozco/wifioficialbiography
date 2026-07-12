#!/usr/bin/env python3
"""
Generate bio HTML files for Colombian influencers from the B-Fun 2025 Top 50 ranking.
Each bio follows the Henry Orozco template with full SEO, schema.org, and structured data.
"""

import os
import json

BIOS_DIR = "bios"

# Influencer data - Top 50 Colombian Influencers (B-Fun 2025)
# Those that already exist are excluded
influencers = [
    {
        "id": "juanda",
        "name": "JuanDa",
        "fullName": "Juan David Morales Carranza",
        "birthDate": "1998-11-01",
        "birthPlace": "Bogotá, Colombia",
        "nationality": "Colombian",
        "profession": "Content Creator, Comedian, Mental Health Advocate",
        "bfunRank": 2,
        "description": "Colombian content creator and comedian known for humorous videos about daily life and mental health advocacy. One of the most influential digital creators in Latin America.",
        "instagram": "juandam___",
        "tiktok": "juandam___",
        "youtube": "JuandaM",
        "category": "influencer",
        "tags": ["Influencer", "Comedy", "Mental Health", "Colombia", "Bogotá"],
        "earlyLife": "Juan David Morales Carranza was born on November 1, 1998, in Bogotá, Colombia. He grew up in the capital city where he developed his passion for comedy and content creation from a young age.",
        "career": """JuanDa rose to fame through his humorous videos about daily life and personal struggles. He became a vocal advocate for mental health after publicly sharing his battles with depression and anxiety. His authentic storytelling and vulnerability created deep emotional connections with millions of followers across Latin America.

In 2025, he was ranked #2 in the B-Fun Digital Influence Index, with 262 million multi-platform followers and a 65% female audience. His engagement rate of 4.76 demonstrates the strong connection he maintains with his community.

JuanDa took a voluntary break from content creation to focus on his mental health, further solidifying his position as an authentic voice for mental wellness in the digital space.""",
        "achievements": [
            "#2 in B-Fun 2025 Digital Influence Index",
            "262 million multi-platform followers",
            "65% female audience with engagement rate of 4.76",
            "Pioneer of mental health conversations in Colombian digital content",
            "Collaborations with Netflix and major brands"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/JuandaM_2024.jpg/440px-JuandaM_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/juanda.html"
    },
    {
        "id": "alejandro-nieto",
        "name": "Alejandro Nieto",
        "fullName": "Bryan Alejandro Nieto Steevens",
        "birthDate": "1998-02-08",
        "birthPlace": "Villavicencio, Colombia",
        "nationality": "Colombian",
        "profession": "TikToker, Content Creator, Comedian, Actor",
        "bfunRank": 3,
        "description": "Colombian TikTok sensation celebrated for comedic sketches and family role-play videos. One of Latin America's most popular digital creators.",
        "instagram": "soybans",
        "tiktok": "soybans",
        "youtube": "SoyBANS",
        "category": "influencer",
        "tags": ["Influencer", "Comedy", "TikTok", "Colombia", "Gen Z"],
        "earlyLife": "Bryan Alejandro Nieto Steevens was born on February 8, 1998, in Villavicencio, Meta, Colombia. He studied acting, which brought professional techniques to his digital content creation.",
        "career": """Alejandro Nieto, known as Soy Bans, is a Colombian TikTok sensation celebrated for his comedic sketches and family role-play videos. His natural acting talent and energetic personality have made him one of Latin America's most popular digital creators.

Ranked #3 in the B-Fun 2025 Digital Influence Index with 230 million multi-platform followers, Nieto has built a massive audience through relatable comedy that resonates across generations. His content features creative skits, challenges, and collaborations with other top creators.

He has won "Fav de Favs" at TikTok Awards and has interviewed celebrities like J Balvin, cementing his status as one of Colombia's most influential digital personalities.""",
        "achievements": [
            "#3 in B-Fun 2025 Digital Influence Index",
            "230 million multi-platform followers",
            "56.5% positive comments, less than 10% suspicious accounts",
            "Won 'Fav de Favs' at TikTok Awards",
            "Interviewed celebrities including J Balvin"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Alejandro_Nieto_SoyBans.jpg/440px-Alejandro_Nieto_SoyBans.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/alejandro-nieto.html"
    },
    {
        "id": "borrego",
        "name": "Borrego",
        "fullName": "Carlos Alberto Díaz Colmenares",
        "birthDate": "2007-02-27",
        "birthPlace": "Bogotá, Colombia",
        "nationality": "Colombian",
        "profession": "Content Creator, Farmer, Author, Entrepreneur",
        "bfunRank": 4,
        "description": "Colombian content creator who promotes rural life and sustainable agriculture through educational and humorous content about farming and animal care.",
        "instagram": "elborrego",
        "tiktok": "lagranjadelborrego",
        "youtube": "La Granja del Borrego",
        "category": "influencer",
        "tags": ["Influencer", "Agriculture", "Education", "Colombia", "Rural Life"],
        "earlyLife": "Carlos Alberto Díaz Colmenares was born on February 27, 2007, in Bogotá, Colombia. He was raised in La Vega, Cundinamarca, and later moved to San Francisco, Cundinamarca, where he manages his family's farm.",
        "career": """Borrego, known as "El Borrego," started creating content at age 13 during the pandemic, documenting his family's return to their ancestral farm. His educational and humorous content about farming, animal care, and rural life broke stereotypes about countryside living, connecting with audiences of all ages.

Ranked #4 in the B-Fun 2025 Digital Influence Index with 194 million multi-platform followers and an impressive 84% positive comments rate, Borrego has become a reference for sustainable and family-friendly content.

He has published a book "La Granja del Borrego," launched a coffee brand "La Floresta," appeared on Shark Tank Colombia, and collaborated with MrBeast. His content has made rural life perceived as modern and relevant for digital audiences.""",
        "achievements": [
            "#4 in B-Fun 2025 Digital Influence Index",
            "194 million multi-platform followers",
            "84% positive comments rate",
            "Published book 'La Granja del Borrego'",
            "Launched coffee brand 'La Floresta'",
            "Featured on Shark Tank Colombia",
            "Collaborated with MrBeast",
            "Won 'Lo aprendí en TikTok' award"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Borrego_La_Granja_del_Borrego.jpg/440px-Borrego_La_Granja_del_Borrego.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/carlos-diaz.html"
    },
    {
        "id": "jash",
        "name": "Jash",
        "fullName": "Jean Carlo León",
        "birthDate": "1996-09-03",
        "birthPlace": "Cúcuta, Colombia",
        "nationality": "Colombian",
        "profession": "Model, Content Creator, TikToker",
        "bfunRank": 5,
        "description": "Colombian model and content creator who transitioned from viral TikTok videos to high-fashion modeling for luxury brands like Prada, Gucci, and Dsquared2.",
        "instagram": "jashlem",
        "tiktok": "jashlem",
        "youtube": "jashlem",
        "category": "influencer",
        "tags": ["Influencer", "Fashion", "Model", "Colombia", "Cúcuta"],
        "earlyLife": "Jean Carlo León was born on September 3, 1996, in Cúcuta, Norte de Santander, Colombia. Standing at 1.92m, his striking appearance would later open doors in the fashion industry.",
        "career": """Jash, known as @jashlem, is a Colombian model and content creator who transitioned from viral TikTok videos to high-fashion modeling. Standing at 1.92m, he has walked for luxury brands including Dsquared2, Prada, Gucci, Hugo Boss, and Ferrari.

Ranked #5 in the B-Fun 2025 Digital Influence Index with 191 million multi-platform followers, Jash has become one of Colombia's most internationally recognized digital talents. Managed by IMG Models, he debuted at Milan Fashion Week and has become a reference for male style and luxury.

His content features lip-sync, fashion, and lifestyle content with impeccable visual production. With 69% female audience and engagement rate above 13.9, he has successfully bridged the gap between digital content creation and high fashion.""",
        "achievements": [
            "#5 in B-Fun 2025 Digital Influence Index",
            "191 million multi-platform followers",
            "IMG Models talent",
            "Milan Fashion Week debut for Dsquared2",
            "Campaigns for Prada, Gucci, Hugo Boss, Ferrari",
            "Nominated for TikToker of the Year at MTV MIAW 2019",
            "69% female audience, engagement rate above 13.9"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Jash_Jean_Carlo_Le%C3%B3n.jpg/440px-Jash_Jean_Carlo_Le%C3%B3n.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/jeancarlo-leon.html"
    },
    {
        "id": "carlos-feria",
        "name": "Carlos Feria",
        "fullName": "Carlos Alberto Feria Guzmán",
        "birthDate": "1996-11-02",
        "birthPlace": "Pereira, Colombia",
        "nationality": "Colombian",
        "profession": "Content Creator, YouTuber, TikToker, Singer",
        "bfunRank": 8,
        "description": "Colombian content creator specializing in family entertainment with challenges, pranks, and vlogs. One of the most followed TikTokers globally.",
        "instagram": "carlosferiag",
        "tiktok": "carlosferiag",
        "youtube": "Carlos Feria",
        "category": "influencer",
        "tags": ["Influencer", "Family Entertainment", "YouTuber", "Colombia", "Pereira"],
        "earlyLife": "Carlos Alberto Feria Guzmán was born on November 2, 1996, in Pereira, Risaralda, Colombia. He developed his content creation skills growing up in the coffee region of Colombia.",
        "career": """Carlos Feria is a Colombian content creator specializing in family entertainment. His content features challenges, pranks, and vlogs with his wife Adriana Valcárcel and daughters, creating wholesome content that appeals to families across Latin America.

Ranked #8 in the B-Fun 2025 Digital Influence Index with 113 million multi-platform followers, Feria has built a massive following through his ability to capture immediate attention and generate viral content.

Beyond content creation, he pursues a music career with popular songs on Spotify including "PA' MI" and "SE REVELO." His dominant presence on Instagram and TikTok has made him one of the most influential family-oriented creators in Latin America.""",
        "achievements": [
            "#8 in B-Fun 2025 Digital Influence Index",
            "113 million multi-platform followers",
            "One of the most followed TikTokers globally",
            "Music career with hits 'PA' MI' and 'SE REVELO'",
            "Family-oriented content empire"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Carlos_Feria_2024.jpg/440px-Carlos_Feria_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/carlos-feria.html"
    },
    {
        "id": "jeison-giraldo",
        "name": "Jeison Giraldo",
        "fullName": "Jeison Giraldo",
        "birthDate": "2000-05-05",
        "birthPlace": "Manizales, Colombia",
        "nationality": "Colombian",
        "profession": "Content Creator, TikToker, YouTuber, Comedian",
        "bfunRank": 10,
        "description": "Colombian content creator known for 'comedia costumbrista' - comedy sketches depicting everyday Colombian family dynamics. The king of relatable humor.",
        "instagram": "jeisongiraldoo",
        "tiktok": "jeisongiraldoo",
        "youtube": "Jeison Giraldo",
        "category": "influencer",
        "tags": ["Influencer", "Comedy", "Colombia", "Manizales", "Family"],
        "earlyLife": "Jeison Giraldo was born on May 5, 2000, in Manizales, Caldas, Colombia. He later moved to Medellín where he built his career as a content creator.",
        "career": """Jeison Giraldo is a Colombian content creator known for his "comedia costumbrista" - comedy sketches depicting everyday Colombian family dynamics. His relatable content about family relationships, pranks, and daily life has earned him a massive following.

Ranked #10 in the B-Fun 2025 Digital Influence Index with 102 million multi-platform followers and an engagement rate of 6.95, Giraldo has established himself as the king of Colombian digital comedy.

His sketches about family life, couple dynamics, and everyday situations resonate with millions of Colombians who see themselves reflected in his content. He maintains a private personal life while projecting an image of warmth and normality that connects with audiences across generations.""",
        "achievements": [
            "#10 in B-Fun 2025 Digital Influence Index",
            "102 million multi-platform followers",
            "Engagement rate of 6.95",
            "King of 'comedia costumbrista' in Colombia",
            "One of the most subscribed YouTubers in Colombia",
            "Family-oriented content with broad appeal"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Jeison_Giraldo_2024.jpg/440px-Jeison_Giraldo_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/jeison-giraldo.html"
    },
    {
        "id": "deiry-vargas",
        "name": "Deiry Vargas",
        "fullName": "Deiry Paola Vargas",
        "birthDate": "1997-11-21",
        "birthPlace": "Bogotá, Colombia",
        "nationality": "Colombian",
        "profession": "Content Creator, Actress, TikToker",
        "bfunRank": 12,
        "description": "One of Colombia's most-watched TikTok creators, known for comedic acting skits and culturally resonant humor. The Colombian TikToker with the most views.",
        "instagram": "deiry_vargas",
        "tiktok": "deiryvargas",
        "youtube": "Deiry Vargas",
        "category": "influencer",
        "tags": ["Influencer", "Comedy", "TikTok", "Colombia", "Bogotá"],
        "earlyLife": "Deiry Paola Vargas was born on November 21, 1997, in Bogotá, Colombia. Known as 'La Roja' for her distinctive red hair, she developed her creative skills in the capital city.",
        "career": """Deiry Vargas is one of Colombia's most-watched TikTok creators, known for comedic acting skits, parodies rooted in everyday emotions, and culturally resonant humor. She opened her TikTok account in 2018 and quickly reached her first million followers.

Ranked #12 in the B-Fun 2025 Digital Influence Index, she became the Colombian TikToker with the most views on the platform, averaging over 1.2M views per post. Her content revolves around dramatic character performances, lifestyle, and travel.

She has been nominated for "Mejor TikToker del Año" at Premios Icono e Instafest and has collaborated with brands like Viva Aerobus and Canal RCN. With an influencer score of 94.4/100 (Favikon), she continues to be a leading force in Colombian digital content.""",
        "achievements": [
            "#12 in B-Fun 2025 Digital Influence Index",
            "Colombian TikToker with the most views",
            "22.7M TikTok followers, 1.4M Instagram, 5.1M YouTube",
            "Nominated for 'Mejor TikToker del Año'",
            "Influencer score of 94.4/100 (Favikon)",
            "Over 30M followers across all platforms"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Deiry_Vargas_2024.jpg/440px-Deiry_Vargas_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/deiry-vargas.html"
    },
    {
        "id": "gemelas-ortega",
        "name": "Gemelas Ortega",
        "fullName": "Leidy Tatiana Ortega Rincón & María Fernanda Ortega Rincón",
        "birthDate": "1996-02-03",
        "birthPlace": "Bogotá, Colombia",
        "nationality": "Colombian",
        "profession": "Influencers, YouTubers, TikTokers",
        "bfunRank": 13,
        "description": "Colombian twin sisters who rose to fame with synchronized dance routines, matching outfits, and polished aesthetic content across YouTube and TikTok.",
        "instagram": "gemelasortegaa",
        "tiktok": "gemelasortegaa",
        "youtube": "Gemelas Ortega",
        "category": "influencer",
        "tags": ["Influencer", "Twins", "Dance", "Colombia", "Bogotá"],
        "earlyLife": "Tatiana and Fernanda Ortega were born on February 3, 1996, in Bogotá, Colombia. As identical twins, they developed a natural synergy for synchronized content creation.",
        "career": """Tatiana and Fernanda Ortega, collectively known as Las Gemelas Ortega, rose to fame starting in 2015 with their YouTube channel featuring dance routines, lip-syncs, challenges, vlogs, and twin-synchronized content.

Ranked #13 in the B-Fun 2025 Digital Influence Index with 21.4M joint TikTok followers, their signature style—matching outfits, coordinated choreography, and polished aesthetic—differentiates them in the Latin American creator space.

They have been sponsored by Bang Energy drink and other major brands, and frequently collaborate with streamer Westcol and creator Juanse Orozco. Their combined reach of 25M+ across all platforms makes them one of Colombia's most influential twin duos.""",
        "achievements": [
            "#13 in B-Fun 2025 Digital Influence Index",
            "21.4M joint TikTok followers",
            "Combined reach of 25M+ across all platforms",
            "Active since 2015 among earliest Colombian YouTube duos",
            "Sponsored by Bang Energy and major brands",
            "Collaborations with Westcol and Juanse Orozco"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Gemelas_Ortega_2024.jpg/440px-Gemelas_Ortega_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/webgroups/gemelas-ortega.html"
    },
    {
        "id": "ami-rodriguez",
        "name": "Ami Rodríguez",
        "fullName": "Ami Rodríguez Pazcagaza",
        "birthDate": "1994-05-18",
        "birthPlace": "Bogotá, Colombia",
        "nationality": "Colombian",
        "profession": "YouTuber, Content Creator, Author, Musician",
        "bfunRank": 14,
        "description": "Colombia's #1 content creator and the first YouTuber from the country to reach 10 million subscribers. Pioneer of family-friendly digital content.",
        "instagram": "amirodriguezz",
        "tiktok": "amirodriguezz",
        "youtube": "Ami Rodríguez",
        "category": "influencer",
        "tags": ["Influencer", "YouTuber", "Music", "Colombia", "Bogotá"],
        "earlyLife": "Ami Rodríguez Pazcagaza was born on May 18, 1994, in Bogotá, Colombia. He started his YouTube channel in 2009, inspired by the show iCarly, producing family-friendly comedy and sketches.",
        "career": """Ami Rodríguez is Colombia's #1 content creator and the first YouTuber from the country to reach 10 million subscribers in 2019. He started his channel in 2009, producing family-friendly comedy, sketches, and challenges.

Ranked #14 in the B-Fun 2025 Digital Influence Index with over 68.6M combined followers (32.2M YouTube, 20M+ TikTok, 10M+ Instagram), he has accumulated over 6.6 billion total YouTube views.

In 2024, he released his debut album "Todo Bien OK" focused on mental health and emotional well-being for young audiences. He is an author, anti-cyberbullying advocate, and winner of Kids' Choice Awards Colombia. His sibling Amara Leguízamon Pazcagaza (Amara Que Linda) is also a popular creator.""",
        "achievements": [
            "#14 in B-Fun 2025 Digital Influence Index",
            "First Colombian YouTuber to surpass 10M subscribers (2019)",
            "68.6M combined followers across platforms",
            "6.6 billion total YouTube views",
            "Winner Kids' Choice Awards Colombia (2017)",
            "Released album 'Todo Bien OK' (2024)",
            "Named in Forbes Colombia 'Top Creators 2025'",
            "Anti-cyberbullying advocate"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Ami_Rodriguez_2024.jpg/440px-Ami_Rodriguez_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/ami-rodriguez.html",
        "wikipedia": "https://en.wikipedia.org/wiki/Ami_Rodriguez"
    },
    {
        "id": "nicole-amado",
        "name": "Nicole Amado",
        "fullName": "Nicole Amado",
        "birthDate": "1993-11-22",
        "birthPlace": "Bogotá, Colombia",
        "nationality": "Colombian",
        "profession": "TikToker, YouTuber, Fashion Influencer, Pilot",
        "bfunRank": 15,
        "description": "Colombian-Colombo-Filipina content creator known for fashion, beauty, and lifestyle content. Former aviation pilot turned digital influencer.",
        "instagram": "amadorat",
        "tiktok": "amadorat",
        "youtube": "Amadorat",
        "category": "influencer",
        "tags": ["Influencer", "Fashion", "Beauty", "Colombia", "Pilot"],
        "earlyLife": "Nicole Amado was born on November 22, 1993, in Bogotá, Colombia. She has Colombian and Filipino heritage. She studied aviation and graduated as a commercial pilot before turning to content creation.",
        "career": """Nicole Amado is a Colombian-Colombo-Filipina content creator known for fashion, beauty, and lifestyle content across TikTok, Instagram, and YouTube. She launched her YouTube channel in 2015 after graduating as a commercial pilot.

Ranked #15 in the B-Fun 2025 Digital Influence Index with 21.2M TikTok followers, 7.5M Instagram followers, and approximately 32M combined, she has built a significant presence in the Latin American influencer space.

She was an ambassador for Dolce & Gabbana in 2020 and has collaborated with SHEIN, Cyzone, Pandora, and Sheglam. Member of the collaborative group 404 Girls, she moved from Bogotá to Mexico in 2019 for management. Her aviation background makes her unique among digital influencers.""",
        "achievements": [
            "#15 in B-Fun 2025 Digital Influence Index",
            "21.2M TikTok followers, 7.5M Instagram",
            "Ambassador for Dolce & Gabbana (2020)",
            "Collaborations with SHEIN, Cyzone, Pandora, Sheglam",
            "Member of 404 Girls collective",
            "Commercial pilot before becoming influencer",
            "Featured in a Netflix series"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Nicole_Amado_Amadorat.jpg/440px-Nicole_Amado_Amadorat.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/amadorat.html"
    },
    {
        "id": "libardo-isaza",
        "name": "Libardo Isaza",
        "fullName": "Libardo Isaza",
        "birthDate": "1998-08-13",
        "birthPlace": "Colombia",
        "nationality": "Colombian",
        "profession": "YouTuber, TikToker, Model, Content Creator",
        "bfunRank": 16,
        "description": "Colombian social media star known for lip-syncs, viral dance routines, and comedic videos. Member of Safari Team and Privé Crew TikTok groups.",
        "instagram": "libardoisaza",
        "tiktok": "libardoisaza",
        "youtube": "Libardo Isaza",
        "category": "influencer",
        "tags": ["Influencer", "TikTok", "Model", "Colombia", "Dance"],
        "earlyLife": "Libardo Isaza was born on August 13, 1998, in Colombia. He started his YouTube channel in March 2014 before transitioning to TikTok where he found massive success.",
        "career": """Libardo Isaza is a Colombian social media star who first gained recognition through his YouTube channel before exploding on TikTok with lip-syncs, viral dance routines, and comedic videos.

Ranked #16 in the B-Fun 2025 Digital Influence Index with 20M+ TikTok followers, 3.7M Instagram, and 5M+ YouTube subscribers, he has built a significant multi-platform presence.

He was part of the Safari Team alongside Nicole Amado, JeanCarlo León, and Carlos Ferreira, and later joined the TikTok group Privé Crew in April 2020. Known for his signature piercing and polished lifestyle content, he was nominated for Kids' Choice Awards as Revelación Digital del Año in 2017.""",
        "achievements": [
            "#16 in B-Fun 2025 Digital Influence Index",
            "20M+ TikTok followers, 5M+ YouTube subscribers",
            "Member of Safari Team and Privé Crew",
            "Nominated for Kids' Choice Awards (2017)",
            "Co-host of MIAW Awards and Tú Awards",
            "168M+ total YouTube views"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Libardo_Isaza_2024.jpg/440px-Libardo_Isaza_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/libardo-isaza.html"
    },
    {
        "id": "daniela-giraldo",
        "name": "Daniela Giraldo",
        "fullName": "Daniela Giraldo",
        "birthDate": "2001-10-12",
        "birthPlace": "Manizales, Colombia",
        "nationality": "Colombian",
        "profession": "TikToker, Content Creator, YouTuber",
        "bfunRank": 19,
        "description": "Colombian TikTok star from Manizales known for comedy and prank videos. One of the fastest-growing Colombian TikTokers post-2020.",
        "instagram": "danielagiraldo.1",
        "tiktok": "daniela_giraldo1",
        "youtube": "Daniela Giraldo",
        "category": "influencer",
        "tags": ["Influencer", "Comedy", "TikTok", "Colombia", "Manizales"],
        "earlyLife": "Daniela Giraldo was born on October 12, 2001, in Manizales, Caldas, Colombia. She graduated high school in December 2019 and started posting on TikTok in January 2020.",
        "career": """Daniela Giraldo is a Colombian TikTok star from Manizales who now lives in Medellín. She started posting on TikTok in January 2020 and quickly went viral with her comedy and prank videos.

Ranked #19 in the B-Fun 2025 Digital Influence Index with 22M+ TikTok followers and 827M+ total likes, she has become one of the fastest-growing Colombian TikTokers. Her consistently positive attitude and bright smile have attracted millions of followers.

She frequently collaborates with fellow TikToker Daniel Ibarra and features her brothers Jeison and Andy in her content. Engaged to David Dussan in June 2024, she continues to grow her brand across multiple platforms.""",
        "achievements": [
            "#19 in B-Fun 2025 Digital Influence Index",
            "22M+ TikTok followers, 827M+ total likes",
            "One of fastest-growing Colombian TikTokers post-2020",
            "1.9M YouTube subscribers",
            "Engaged to David Dussan (June 2024)",
            "Estimated annual earnings: $750K-$1.1M"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Daniela_Giraldo_2024.jpg/440px-Daniela_Giraldo_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/daniela-giraldo.html"
    },
    {
        "id": "natasha-mora",
        "name": "Natasha Mora",
        "fullName": "Natasha Mora",
        "birthDate": "1995-08-19",
        "birthPlace": "Maracaibo, Venezuela",
        "nationality": "Venezuelan (based in Colombia)",
        "profession": "Content Creator, Model, Dancer, Influencer",
        "bfunRank": 18,
        "description": "Venezuelan-born digital content creator based in Colombia, known for modeling, dance videos, and swimwear content with over 13M TikTok followers.",
        "instagram": "tashh09",
        "tiktok": "tashh02",
        "youtube": "Tashh_Oficial",
        "category": "influencer",
        "tags": ["Influencer", "Model", "Dance", "Venezuela", "Colombia"],
        "earlyLife": "Natasha Mora was born on August 19 in Maracaibo, Zulia, Venezuela. She later moved to Colombia where she built her career as a digital content creator.",
        "career": """Natasha Mora is a Venezuelan-born digital content creator, model, and dancer based in Colombia who rose to prominence through modeling shoots, dance videos, and swimwear content.

Ranked #18 in the B-Fun 2025 Digital Influence Index with 13M TikTok followers and 3.1M Instagram followers, she has accumulated over 500M+ likes on TikTok alone. Her Instagram engagement rate of 8.85% is higher than 96% of creators.

She began posting on Instagram in 2014 and later expanded to TikTok, where her visually striking content has made her one of the most followed influencers in the Colombian digital space. Her YouTube channel features personal views on relationships, fashion, and makeup content.""",
        "achievements": [
            "#18 in B-Fun 2025 Digital Influence Index",
            "13M TikTok followers, 3.1M Instagram",
            "500M+ total TikTok likes",
            "Instagram engagement rate of 8.85%",
            "Net worth estimated at $4M USD",
            "Active across 5+ platforms with 16M+ combined audience"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Natasha_Mora_2024.jpg/440px-Natasha_Mora_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/natasha-mora.html"
    },
    {
        "id": "lulu99",
        "name": "Lulu 99",
        "fullName": "Luisa María Restrepo",
        "birthDate": "2002-08-15",
        "birthPlace": "Medellín, Colombia",
        "nationality": "Colombian",
        "profession": "YouTuber, Content Creator, Musical Artist",
        "bfunRank": 22,
        "description": "Colombian YouTuber who launched her channel at age 12 and won Best Young YouTuber at Kids Choice Awards Colombia 2017. Now based in Miami.",
        "instagram": "luisalulu99",
        "tiktok": "lulu99",
        "youtube": "Lulu99",
        "category": "influencer",
        "tags": ["Influencer", "YouTuber", "Music", "Colombia", "Medellín"],
        "earlyLife": "Luisa María Restrepo was born on August 15, 2002, in Medellín, Antioquia, Colombia. She launched her YouTube channel in 2015 at just 12 years old.",
        "career": """Lulu 99 is a Colombian YouTuber who launched her channel in 2015 at age 12, known for vlogs, challenges, comedy, and beauty content. She won "Best Young YouTuber" at the Kids Choice Awards Colombia 2017.

Ranked #22 in the B-Fun 2025 Digital Influence Index with 13M+ YouTube subscribers, she has grown into a multi-platform creator with significant presence on TikTok and Instagram.

Beyond content creation, she is an aspiring musical artist who has released several singles. She migrated from Colombia to Miami, where she continues creating content. She has a collaborative couples channel "MaiLu" with partner The Maiking and overcame epilepsy from a childhood car accident.""",
        "achievements": [
            "#22 in B-Fun 2025 Digital Influence Index",
            "13M+ YouTube subscribers",
            "Kids Choice Awards Colombia winner (2017)",
            "Started YouTube channel at age 12",
            "Musical artist with released singles",
            "Collaborative couples channel 'MaiLu'"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Lulu_99_2024.jpg/440px-Lulu_99_2024.jpg",
        "famousBirthdays": "https://pt.famousbirthdays.com/people/luisa-maria.html"
    },
    {
        "id": "gemelas-del-free",
        "name": "Gemelas del Free",
        "fullName": "Roylimar and Royerlin",
        "birthDate": "2012-01-01",
        "birthPlace": "Puerto La Cruz, Venezuela",
        "nationality": "Venezuelan (based in Colombia)",
        "profession": "Gaming Content Creators, Musicians, TikTokers",
        "bfunRank": 23,
        "description": "Twin sister duo from Venezuela now based in Medellín who rose to fame playing Free Fire and transitioned to music with hit single '2 Balas'.",
        "instagram": "lasgemelasdelfreeofficial",
        "tiktok": "lasgemelasdelfreeofficial",
        "youtube": "Las Gemelas Del Free Official",
        "category": "influencer",
        "tags": ["Influencer", "Gaming", "Music", "Venezuela", "Colombia"],
        "earlyLife": "The Gemelas del Free twins were born around 2012 in Puerto La Cruz, Venezuela. They later moved to Medellín, Colombia, where they built their digital career.",
        "career": """The Gemelas del Free are twin sister gaming content creators from Venezuela who rose to fame playing Garena Free Fire. They transitioned from gaming to music, debuting with the hit single "2 Balas" which accumulated 53M+ YouTube views.

Ranked #23 in the B-Fun 2025 Digital Influence Index with 8.1M+ YouTube subscribers and over 353M total TikTok likes, they have become among the top female gaming creators in Latin America.

Their music career has included collaborations with artists like Ely2 on "La Emotiza." Based in Medellín, they continue to create gaming and entertainment content for their massive global audience.""",
        "achievements": [
            "#23 in B-Fun 2025 Digital Influence Index",
            "8.1M+ YouTube subscribers",
            "353M+ total TikTok likes",
            "53M+ YouTube views on '2 Balas'",
            "Among top female gaming creators in Latin America",
            "Successful transition from gaming to music"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Gemelas_del_Free_2024.jpg/440px-Gemelas_del_Free_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/webgroups/las-gemelas-del-free.html"
    },
    {
        "id": "lukas-urkijo",
        "name": "Lukas Urkijo",
        "fullName": "Lukas Urquijo López",
        "birthDate": "2008-02-07",
        "birthPlace": "Colombia",
        "nationality": "Colombian",
        "profession": "Actor, TikTok Star, YouTube Star",
        "bfunRank": 24,
        "description": "Colombian-born actor and social media personality who moved to Mexico to pursue acting in major telenovelas and series.",
        "instagram": "lukas.urkijo",
        "tiktok": "lukas.urkijo",
        "youtube": "Lukas Urkijo Official",
        "category": "influencer",
        "tags": ["Influencer", "Actor", "Telenovela", "Colombia", "Mexico"],
        "earlyLife": "Lukas Urquijo López was born on February 7, 2008, in Colombia. He moved to Mexico around 2020 to pursue his acting career.",
        "career": """Lukas Urkijo is a Colombian-born actor and social media personality who moved to Mexico to pursue acting. He has appeared in major Mexican telenovelas including "El Amor Invencible" and "Minas de Pasión," plus series like "Malverde, El Santo Patrón" and "De Brutas Nada."

Ranked #24 in the B-Fun 2025 Digital Influence Index with 5.9M+ TikTok followers and 3M+ Instagram followers, he has successfully bridged traditional acting with digital content creation.

Despite his young age, he has built a significant following across multiple platforms, becoming one of the youngest Colombian actors to achieve international recognition in Mexican television.""",
        "achievements": [
            "#24 in B-Fun 2025 Digital Influence Index",
            "5.9M+ TikTok followers, 3M+ Instagram",
            "Roles in major Mexican telenovelas (Televisa/Univision)",
            "One of youngest Colombian actors in international TV",
            "Appearances in 'El Amor Invencible', 'Minas de Pasión'"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Lukas_Urkijo_2024.jpg/440px-Lukas_Urkijo_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/lukas-urkijo.html"
    },
    {
        "id": "los-chicaneros",
        "name": "Los Chicaneros",
        "fullName": "Nelson Botero, María Cristina Bravo, Nicolás Botero, María Antonia Botero",
        "birthDate": "1985-01-01",
        "birthPlace": "Cali, Colombia",
        "nationality": "Colombian",
        "profession": "Family Comedy Content Creators",
        "bfunRank": 25,
        "description": "Colombian family of four who went viral on TikTok with relatable Latin family comedy. Named Top LATAM Creators 2024 by Forbes.",
        "instagram": "los_chicaneros",
        "tiktok": "los_chicaneros",
        "youtube": "Los Chicaneros",
        "category": "influencer",
        "tags": ["Influencer", "Family Comedy", "Colombia", "Cali", "Forbes"],
        "earlyLife": "Los Chicaneros is a Colombian family from Cali consisting of Nelson Botero (father, engineer), María Cristina Bravo (mother, chef), Nicolás Botero (son), and María Antonia Botero (daughter). They currently reside in Orlando, Florida.",
        "career": """Los Chicaneros is a Colombian family of four who went viral on TikTok in 2021 with relatable Latin family comedy sketches. Named Top LATAM Creators 2024 by Forbes, they are known for clean, white humor without profanity.

Ranked #25 in the B-Fun 2025 Digital Influence Index with 13.6M TikTok followers, 6.8M Instagram, and 6.1M YouTube subscribers (3.2B+ views), they have become one of the most successful family content groups in Latin America.

They have appeared on Despierta América, Telemundo, Univisión, and NBC. Brand ambassadors for Hyundai, T-Mobile, and Coca-Cola, they were VIP guests at Premios Lo Nuestro 2024 and Netflix collaborators.""",
        "achievements": [
            "#25 in B-Fun 2025 Digital Influence Index",
            "13.6M TikTok followers, 6.1M YouTube (3.2B+ views)",
            "Forbes Top LATAM Creators 2024",
            "Premios Eliot Comedy Award winners",
            "Brand ambassadors for Hyundai, T-Mobile, Coca-Cola",
            "Appeared on Telemundo, Univisión, NBC",
            "Netflix collaborators"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Los_Chicaneros_2024.jpg/440px-Los_Chicaneros_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/webgroups/los-chicaneros.html"
    },
    {
        "id": "gemelas-abello",
        "name": "Gemelas Abello",
        "fullName": "Valentina Abello Prada & María Camila Abello",
        "birthDate": "2001-05-30",
        "birthPlace": "Medellín, Colombia",
        "nationality": "Colombian",
        "profession": "Content Creators, TikTok Stars, Models",
        "bfunRank": 26,
        "description": "Identical Colombian twin sisters who dominate TikTok with dance challenges and went viral for secretly swapping places on Gran Hermano Chile.",
        "instagram": "gemelasabello",
        "tiktok": "gemelasabello2",
        "youtube": "Gemelas Abello",
        "category": "influencer",
        "tags": ["Influencer", "Twins", "TikTok", "Colombia", "Medellín"],
        "earlyLife": "Valentina and María Camila Abello were born on May 30, 2001, in Medellín, Colombia. As identical twins, they developed a natural chemistry for synchronized content.",
        "career": """The Gemelas Abello are identical Colombian twin sisters who dominate TikTok with dance challenges, comedy skits, and lifestyle content.

Ranked #26 in the B-Fun 2025 Digital Influence Index with 26M+ TikTok followers, they went viral in 2024 for secretly swapping places every 24 hours for weeks on Gran Hermano Chile without other contestants noticing.

Both studied business administration and have accumulated billions of cumulative TikTok views. They have collaborated with major Latin artists and global brands, becoming one of the most recognizable twin duos in Latin American social media.""",
        "achievements": [
            "#26 in B-Fun 2025 Digital Influence Index",
            "26M+ TikTok followers",
            "Viral Gran Hermano Chile stunt (2024)",
            "Billions of cumulative TikTok views",
            "Collaborations with major Latin artists and brands"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Gemelas_Abello_2024.jpg/440px-Gemelas_Abello_2024.jpg",
        "famousBirthdays": "https://es.famousbirthdays.com/people/valentina-prada.html"
    },
    {
        "id": "la-lerma",
        "name": "La Lerma",
        "fullName": "La Lerma",
        "birthDate": "1998-01-01",
        "birthPlace": "Cartagena, Colombia",
        "nationality": "Colombian",
        "profession": "Content Creator, TikToker, Dancer, Musician",
        "bfunRank": 27,
        "description": "Colombian content creator based in Cartagena known for viral dance content, comedy sketches, and trending challenges with high engagement rates.",
        "instagram": "lermamusic_",
        "tiktok": "lermamusic_",
        "youtube": "La Lerma",
        "category": "influencer",
        "tags": ["Influencer", "Dance", "Music", "Colombia", "Cartagena"],
        "earlyLife": "La Lerma is a Colombian content creator from the Cartagena/Barranquilla area who rose to prominence through viral dance and comedy content.",
        "career": """La Lerma is a Colombian content creator based in Cartagena known for viral dance content, comedy sketches, and trending challenges. She frequently collaborates with partner Freyder Cantillo and other top Colombian TikTokers.

Ranked #27 in the B-Fun 2025 Digital Influence Index, she has built a significant following through her high engagement rates and energetic, personality-driven content.

Her Instagram account @lermamusic_ has over 1.5M followers with an engagement rate of approximately 2.7%, higher than most creators. She continues to be a leading force in the Colombian TikTok dance and comedy scene.""",
        "achievements": [
            "#27 in B-Fun 2025 Digital Influence Index",
            "1.5M+ Instagram followers",
            "High engagement rate (~2.7%)",
            "Frequent collaborations with top Colombian creators",
            "Leading dance and comedy content creator"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/La_Lerma_2024.jpg/440px-La_Lerma_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/la-lerma.html"
    },
    {
        "id": "mav",
        "name": "MAV",
        "fullName": "María Alejandra Villegas",
        "birthDate": "2004-04-22",
        "birthPlace": "Bello, Colombia",
        "nationality": "Colombian",
        "profession": "Content Creator, Influencer, Model",
        "bfunRank": 28,
        "description": "Paisa influencer from Medellín who went viral for revealing she earns up to 250 million Colombian pesos/month from content creation.",
        "instagram": "oficial_mav",
        "tiktok": "priv_mav",
        "youtube": "MAV",
        "category": "influencer",
        "tags": ["Influencer", "Model", "Beauty", "Colombia", "Medellín"],
        "earlyLife": "María Alejandra Villegas was born on April 22, 2004, in Bello, Antioquia, Colombia, near Medellín. She was crowned Miss Teen Colombia 2021 as Princess representing Bello.",
        "career": """MAV, María Alejandra Villegas, is a paisa influencer from Medellín who rose to fame through beauty tips, dance content, and lifestyle videos.

Ranked #28 in the B-Fun 2025 Digital Influence Index with 12.9M+ TikTok followers and 4.7M Instagram followers, she went viral in 2022 after revealing she earns up to 250 million Colombian pesos per month (~$60K+ USD) from content creation.

Part of the Medellín influencer scene alongside La Liendra and others, she was Miss Teen Colombia 2021 (Princess). She continues to grow her brand as one of the top 1% of entertainment creators in Colombia.""",
        "achievements": [
            "#28 in B-Fun 2025 Digital Influence Index",
            "12.9M TikTok followers, 4.7M Instagram",
            "Miss Teen Colombia 2021 (Princess)",
            "Viral income disclosure (250M COP/month)",
            "Top 1% of entertainment creators in Colombia"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/MAV_Maria_Alejandra_Villegas.jpg/440px-MAV_Maria_Alejandra_Villegas.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/ma-alejandra-villegas.html"
    },
    {
        "id": "yeferson-cossio",
        "name": "Yeferson Cossio",
        "fullName": "Yeferson Esteban Cossio Castaño",
        "birthDate": "1994-05-15",
        "birthPlace": "Medellín, Colombia",
        "nationality": "Colombian",
        "profession": "Influencer, Content Creator, Model, Musician, Entrepreneur",
        "bfunRank": 29,
        "description": "One of Colombia's most-followed influencers with 50M+ combined followers. Known for viral challenges, music, and entrepreneurial ventures.",
        "instagram": "yefersoncossio",
        "tiktok": "yefersoncossio",
        "youtube": "Yeferson Cossio",
        "category": "influencer",
        "tags": ["Influencer", "Music", "Entrepreneur", "Colombia", "Medellín"],
        "earlyLife": "Yeferson Esteban Cossio Castaño was born on May 15, 1994, in Medellín, Colombia. He started as a fashion model in 2013 before transitioning to digital content creation.",
        "career": """Yeferson Cossio is one of Colombia's most-followed influencers with over 50 million combined followers across platforms. He started as a fashion model in 2013 and transitioned to YouTube and TikTok with viral challenges and transformation content.

Ranked #29 in the B-Fun 2025 Digital Influence Index with 12-15M Instagram followers and 19.7-20M TikTok followers, he is also a musician with hits like "Esa Mujer" and "Dopamina" and a successful businessman.

His brand deals include Nike, GNC, and Rappi. He has been involved in public controversies including legal battles and betting stunts, and was a participant in the Kings League. He reportedly earns $750K+ monthly.""",
        "achievements": [
            "#29 in B-Fun 2025 Digital Influence Index",
            "50M+ combined followers",
            "Hit songs 'Esa Mujer' and 'Dopamina'",
            "Brand deals with Nike, GNC, Rappi",
            "Kings League participant",
            "Reported monthly income of $750K+"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Yeferson_Cossio_2024.jpg/440px-Yeferson_Cossio_2024.jpg",
        "famousBirthdays": "https://es.famousbirthdays.com/people/yeferson-cossio.html"
    },
    {
        "id": "sofia-castro",
        "name": "Sofía Castro",
        "fullName": "Diana Sofía Castro",
        "birthDate": "1995-04-06",
        "birthPlace": "Bogotá, Colombia",
        "nationality": "Colombian",
        "profession": "Content Creator, YouTuber, Singer-Songwriter",
        "bfunRank": 30,
        "description": "Bogotá-born YouTuber signed to Universal Music Latino. Nominated for Best New Artist at Premios Nuestra Tierra. Forbes Top Creators 2024.",
        "instagram": "sofiaalcastro",
        "tiktok": "sofiaalcastro",
        "youtube": "Sofía Castro",
        "category": "influencer",
        "tags": ["Influencer", "Music", "YouTuber", "Colombia", "Bogotá"],
        "earlyLife": "Diana Sofía Castro was born on April 6, 1995, in Bogotá, Colombia. She started her YouTube career in 2015 as part of the 'Oxigenados Squad' collective.",
        "career": """Sofía Castro is a Bogotá-born YouTuber who started in 2015 as part of the "Oxigenados Squad" collective. She transitioned from comedy/vlog content to a music career, signing with Universal Music Latino.

Ranked #30 in the B-Fun 2025 Digital Influence Index with 9M+ YouTube subscribers, 10.4M TikTok, and 8.2M Instagram followers, she has been nominated for Best New Artist at Premios Nuestra Tierra (2024).

Her hit collab song "Mor" with Ami Rodríguez accumulated 218M+ YouTube views. Forbes Top Creators 2024 Colombia, she is known for promoting mental health awareness and has been a Cyzone cosmetics ambassador.""",
        "achievements": [
            "#30 in B-Fun 2025 Digital Influence Index",
            "9M+ YouTube subscribers, 10.4M TikTok",
            "Signed to Universal Music Latino",
            "Nominated Premios Nuestra Tierra (Mejor Artista Revelación)",
            "Hit song 'Mor' with 218M+ YouTube views",
            "Forbes Top Creators 2024 Colombia",
            "Cyzone cosmetics ambassador"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Sofia_Castro_2024.jpg/440px-Sofia_Castro_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/sofia-castro.html"
    },
    {
        "id": "ana-eusse",
        "name": "Ana Eusse",
        "fullName": "Ana Eusse Maria",
        "birthDate": "2003-08-12",
        "birthPlace": "Colombia",
        "nationality": "Colombian",
        "profession": "TikTok Star, Digital Influencer",
        "bfunRank": 31,
        "description": "Colombian TikTok star known for dance videos, relationship content, and motherhood moments with over 15M followers.",
        "instagram": "ana_eusse1",
        "tiktok": "ana_eusse",
        "youtube": "Ana Eusse",
        "category": "influencer",
        "tags": ["Influencer", "TikTok", "Dance", "Colombia", "Motherhood"],
        "earlyLife": "Ana Eusse Maria was born on August 12, 2003, in Colombia. She started creating content on YouTube in 2017 before finding massive success on TikTok.",
        "career": """Ana Eusse is a Colombian TikTok star known for dance videos, relationship content, pranks, skits, and motherhood moments. She often gets millions of views per video.

Ranked #31 in the B-Fun 2025 Digital Influence Index with 15M+ TikTok followers and 575M+ likes, she is dating TikToker Jeison Giraldo and gave birth to her son Ian in July 2022.

Her viral pregnancy dance video accumulated 15M+ views, showcasing her ability to connect with audiences through authentic, relatable content. She is one of Colombia's top TikTok creators with an estimated net worth of $4-5M USD.""",
        "achievements": [
            "#31 in B-Fun 2025 Digital Influence Index",
            "15M+ TikTok followers, 575M+ likes",
            "Viral pregnancy dance video (15M+ views)",
            "One of Colombia's top TikTok creators",
            "Net worth estimated at $4-5M USD"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Ana_Eusse_2024.jpg/440px-Ana_Eusse_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/ana-maria-tiktokstar.html"
    },
    {
        "id": "winner-max",
        "name": "Winner Max",
        "fullName": "Winner Max",
        "birthDate": "1996-01-10",
        "birthPlace": "Colombia",
        "nationality": "Colombian",
        "profession": "YouTube Star, TikToker, Gamer, Rapper",
        "bfunRank": 32,
        "description": "Most-followed Colombian YouTuber globally with 18.7M subscribers. Known for Free Fire gameplay and viral mini-series 'Alias El Dino'.",
        "instagram": "winnermaxyt",
        "tiktok": "winnermaxyt",
        "youtube": "Winner Max",
        "category": "influencer",
        "tags": ["Influencer", "Gaming", "YouTube", "Colombia", "Free Fire"],
        "earlyLife": "Winner Max was born on January 10, 1996, in Colombia. He started his YouTube channel around 2020, initially focusing on Free Fire gaming content.",
        "career": """Winner Max is the most-followed Colombian YouTuber globally with 18.7 million subscribers. He is known for Free Fire gameplay, comedic family skits, rap storytelling series, and his viral mini-series "Alias El Dino."

Ranked #32 in the B-Fun 2025 Digital Influence Index with 15M+ TikTok followers and over 5.5 billion total YouTube views, his content combines gaming with family-oriented humor featuring his wife Daniela Medina.

His "Alias El Dino" mini-series went viral, expanding his audience beyond gaming. He continues to be a leading force in Colombian YouTube and gaming content creation.""",
        "achievements": [
            "#32 in B-Fun 2025 Digital Influence Index",
            "18.7M YouTube subscribers (most-followed Colombian YouTuber)",
            "5.5 billion+ total YouTube views",
            "Viral mini-series 'Alias El Dino'",
            "Pioneer of Free Fire content in Colombia"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Winner_Max_2024.jpg/440px-Winner_Max_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/winnermax.html"
    },
    {
        "id": "davidgetial",
        "name": "Davidgetial",
        "fullName": "David Getial",
        "birthDate": "2000-03-21",
        "birthPlace": "Colombia",
        "nationality": "Colombian",
        "profession": "TikTok Star, Digital Influencer, Digital Artist",
        "bfunRank": 33,
        "description": "Colombian TikToker famous for fashion poses, comedy sketches, and iPad digital art drawings of celebrities and pop culture icons.",
        "instagram": "davidgetial",
        "tiktok": "davidgetial",
        "youtube": "Davidgetial",
        "category": "influencer",
        "tags": ["Influencer", "Digital Art", "TikTok", "Colombia", "Fashion"],
        "earlyLife": "David Getial was born on March 21, 2000, in Colombia. He started creating content combining fashion, comedy, and digital art on his iPad.",
        "career": """Davidgetial is a Colombian TikTok star famous for his creative blend of fashion poses, comedy sketches, and digital art drawings on iPad. His digital art consists of drawings of celebrities and pop culture icons.

Ranked #33 in the B-Fun 2025 Digital Influence Index with 14M+ TikTok followers and 376M+ total likes, he has built a unique niche combining multiple content forms.

His viral Rihanna fan video accumulated 5M+ views, and he continues to grow his audience through innovative content that blends fashion, comedy, and digital artistry.""",
        "achievements": [
            "#33 in B-Fun 2025 Digital Influence Index",
            "14M+ TikTok followers",
            "376M+ total TikTok likes",
            "Viral Rihanna fan video (5M+ views)",
            "Pioneer of iPad digital art content"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Davidgetial_2024.jpg/440px-Davidgetial_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/deivis-getial.html"
    },
    {
        "id": "alexa-torrex",
        "name": "Alexa Torrex",
        "fullName": "Nelyely Katherine Torres Contreras",
        "birthDate": "2002-03-18",
        "birthPlace": "Cúcuta, Colombia",
        "nationality": "Colombian",
        "profession": "TikTok Star, Singer, Rapper, Content Creator",
        "bfunRank": 34,
        "description": "Colombian influencer and rapper from Cúcuta, member of Familia Recocha. Creates humor, dance, and empowerment content for women.",
        "instagram": "alexatorrexcontreras",
        "tiktok": "alexa.torrex",
        "youtube": "Alexa Torrex",
        "category": "influencer",
        "tags": ["Influencer", "Music", "Rap", "Colombia", "Cúcuta"],
        "earlyLife": "Nelyely Katherine Torres Contreras was born on March 18, 2002, in Cúcuta, Norte de Santander, Colombia. She started creating content in 2016.",
        "career": """Alexa Torrex is a Colombian influencer, singer, and content creator from Cúcuta, recognized as a member of the popular "Familia Recocha" family content collective.

Ranked #34 in the B-Fun 2025 Digital Influence Index with 14.7M TikTok followers and 3.4M YouTube subscribers, she creates varied content including humor, dance, and empowerment videos for women.

A student of Communications Social, she has released rap and music tracks while maintaining an 11-year career in content creation. She continues to be a leading voice for women's empowerment in the Colombian digital space.""",
        "achievements": [
            "#34 in B-Fun 2025 Digital Influence Index",
            "14.7M TikTok followers, 3.4M YouTube subscribers",
            "Member of Familia Recocha",
            "11 years active in content creation",
            "Music career as singer/rapper"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Alexa_Torrex_2024.jpg/440px-Alexa_Torrex_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/alexa-torrex.html"
    },
    {
        "id": "camilo-cifuentes",
        "name": "Camilo Cifuentes",
        "fullName": "Juan Camilo Jurado Cifuentes",
        "birthDate": "1997-01-01",
        "birthPlace": "Manizales, Colombia",
        "nationality": "Colombian",
        "profession": "Content Creator, Philanthropist",
        "bfunRank": 35,
        "description": "Anonymous Colombian content creator who helps street vendors and vulnerable people through spontaneous acts of generosity. Never shows his face.",
        "instagram": "camilocifuentes",
        "tiktok": "camilocifuentes96",
        "youtube": "Camilo Cifuentes",
        "category": "influencer",
        "tags": ["Influencer", "Philanthropy", "Colombia", "Manizales", "Social Impact"],
        "earlyLife": "Juan Camilo Jurado Cifuentes was born around 1997 in Manizales, Colombia. He studied Industrial Mechanical Engineering at SENA.",
        "career": """Camilo Cifuentes is an anonymous Colombian content creator from Manizales who helps street vendors and vulnerable people in Medellín, Bogotá, and Manizales through spontaneous acts of generosity.

Ranked #35 in the B-Fun 2025 Digital Influence Index with 9.7M+ TikTok followers, he is famous for his catchphrase "yo afán no tengo" and his unique approach of never showing his face, saying "the protagonists are the people, not me."

His team consists of his mother, brother, and girlfriend. He has helped change the lives of hundreds of street vendors by buying entire inventories and gifting money, making him one of the most beloved philanthropic creators in Colombia.""",
        "achievements": [
            "#35 in B-Fun 2025 Digital Influence Index",
            "9.7M+ TikTok followers",
            "Helped change lives of hundreds of street vendors",
            "Famous catchphrase 'yo afán no tengo'",
            "One of most beloved philanthropic creators in Colombia",
            "Studied Industrial Mechanical Engineering at SENA"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Camilo_Cifuentes_2024.jpg/440px-Camilo_Cifuentes_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/camilo-cifuentes.html"
    },
    {
        "id": "amaranta-venegas",
        "name": "Amaranta Venegas",
        "fullName": "Amaranta Venegas",
        "birthDate": "2002-07-24",
        "birthPlace": "Colombia",
        "nationality": "Colombian",
        "profession": "Social Media Star, Content Creator",
        "bfunRank": 36,
        "description": "Colombian social media star recognized for comedy and dance videos. Member of 404 Girls collective. Based in Mexico City.",
        "instagram": "amarantavp",
        "tiktok": "amarantavp_",
        "youtube": "Amaranta Venegas",
        "category": "influencer",
        "tags": ["Influencer", "Comedy", "Dance", "Colombia", "Mexico"],
        "earlyLife": "Amaranta Venegas was born on July 24, 2002, in Colombia. She later moved to Mexico City where she continues creating content.",
        "career": """Amaranta Venegas is a Colombian social media star recognized for comedy and dance videos often involving her friends. She is a member of the social collective "404 Girls."

Ranked #36 in the B-Fun 2025 Digital Influence Index with 15.8M TikTok followers and 4.8M Instagram followers, she has collaborated with brands like FashionNova, Pandora, and Skechers.

She started TikTok in August 2018 and has grown into one of Colombia's most followed female creators. Based in Mexico City, she continues creating lifestyle, fashion, and travel content for her massive audience.""",
        "achievements": [
            "#36 in B-Fun 2025 Digital Influence Index",
            "15.8M TikTok followers, 4.8M Instagram",
            "Member of 404 Girls collective",
            "Collaborations with FashionNova, Pandora, Skechers",
            "#SkechersDanceIntoSchool campaign (2020)"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Amaranta_Venegas_2024.jpg/440px-Amaranta_Venegas_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/amaranta-venegas.html"
    },
    {
        "id": "juan-guarnizo",
        "name": "Juan Guarnizo",
        "fullName": "Juan Sebastián Guarnizo Algarra",
        "birthDate": "1997-01-11",
        "birthPlace": "Ibagué, Colombia",
        "nationality": "Colombian",
        "profession": "Twitch Streamer, YouTuber, Content Creator, Voice Actor",
        "bfunRank": 37,
        "description": "One of the most influential Spanish-speaking content creators worldwide. Voice of Spider-Man in Latin American dub. President of Aniquiladores FC.",
        "instagram": "juansguarnizo",
        "tiktok": "juaniquilador",
        "youtube": "Juan S Guarnizo",
        "category": "influencer",
        "tags": ["Influencer", "Streamer", "Gaming", "Colombia", "Spider-Man"],
        "earlyLife": "Juan Sebastián Guarnizo Algarra was born on January 11, 1997, in Ibagué, Tolima, Colombia. He studied graphic design at Universidad Jorge Tadeo Lozano before dropping out to stream full-time.",
        "career": """Juan Guarnizo is a Colombian-Mexican streamer and one of the most influential Spanish-speaking content creators worldwide. He is president of Aniquiladores FC in the Kings League (created by Gerard Piqué and Ibai Llanos).

Ranked #37 in the B-Fun 2025 Digital Influence Index with 11.1M Twitch followers, 11.3M TikTok, and 6.3M YouTube subscribers, he was the voice of Spectacular Spider-Man in the Latin American Spanish dub of Spider-Man: Across The Spider-Verse (2023).

The first Latin American with 10K paid Twitch subscribers, he currently lives in Monterrey, Mexico, with his wife Ari Gameplays. Forbes Top Creators 2024, he is a guest judge on Netflix's Sugar Rush: The Baking Point.""",
        "achievements": [
            "#37 in B-Fun 2025 Digital Influence Index",
            "11.1M Twitch followers (top 10 most-followed globally)",
            "First Latin American with 10K paid Twitch subscribers",
            "Voice of Spider-Man in 'Across The Spider-Verse'",
            "President of Aniquiladores FC (Kings League)",
            "Forbes Top Creators 2024",
            "Guest judge on Netflix's Sugar Rush"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Juan_Guarnizo_2024.jpg/440px-Juan_Guarnizo_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/juan-guarnizo.html"
    },
    {
        "id": "christian-fabian",
        "name": "Christian Fabián",
        "fullName": "Christian Fabián Durán",
        "birthDate": "2001-03-27",
        "birthPlace": "Colombia",
        "nationality": "Colombian",
        "profession": "YouTuber, Influencer, Content Creator",
        "bfunRank": 39,
        "description": "Colombian influencer known for challenges, tags, and personal storytimes on YouTube with over 12M subscribers and 16M TikTok followers.",
        "instagram": "christianfabiannn",
        "tiktok": "christianfabiannn",
        "youtube": "Christian Fabián",
        "category": "influencer",
        "tags": ["Influencer", "YouTube", "Comedy", "Colombia", "Storytime"],
        "earlyLife": "Christian Fabián Durán was born on March 27, 2001, in Colombia. He launched his YouTube channel in February 2016.",
        "career": """Christian Fabián is a Colombian influencer who became known for his self-titled YouTube channel where he shares challenges, tags, and personal storytimes.

Ranked #39 in the B-Fun 2025 Digital Influence Index with 16M+ TikTok followers and 12M+ YouTube subscribers, he has amassed over 12 million subscribers since launching his channel in February 2016.

His significant other and newborn daughter have appeared in his content, adding a personal touch to his comedic videos. He continues to be one of Colombia's top comedic content creators.""",
        "achievements": [
            "#39 in B-Fun 2025 Digital Influence Index",
            "16M+ TikTok followers, 12M+ YouTube subscribers",
            "Active since 2016",
            "One of Colombia's top comedic content creators",
            "Personal family content integration"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Christian_Fabian_2024.jpg/440px-Christian_Fabian_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/christian-duran.html"
    },
    {
        "id": "blessd",
        "name": "Blessd",
        "fullName": "Stiven Mesa Londoño",
        "birthDate": "2000-01-27",
        "birthPlace": "Itagüí, Colombia",
        "nationality": "Colombian",
        "profession": "Reggaeton Singer, Rapper, Songwriter",
        "bfunRank": 44,
        "description": "Colombian reggaeton artist who rose from selling fruit at 2am to becoming one of Colombia's biggest musical exports. Hits include 'Una' and 'Medallo'.",
        "instagram": "blessd",
        "tiktok": "blessd",
        "youtube": "Siempre Blessd",
        "category": "singer",
        "tags": ["Singer", "Reggaeton", "Colombia", "Itagüí", "Medellín"],
        "earlyLife": "Stiven Mesa Londoño was born on January 27, 2000, in Itagüí, Antioquia, Colombia. He grew up in humble circumstances, waking at 2am to sell fruit at Central Mayorista de Antioquia and selling candy at school to fund his recording sessions.",
        "career": """Blessd is a Colombian reggaeton artist who rose from humble beginnings to becoming one of Colombia's biggest musical exports. His breakthrough hit "Una" went viral in 2019, and his album "Hecho en Medellín" launched international fame.

Ranked #44 in the B-Fun 2025 Digital Influence Index with 8M+ Instagram followers, 9.9M TikTok, and 4.82M YouTube subscribers, he has collaborated with Maluma, Justin Quiles, Myke Towers, Black Eyed Peas, and Piso 21.

His faith is central to his identity and stage name "Blessd" (blessed). He performed at over 500 schools before fame and was selected for YouTube Foundry Class 2021. Signed to Warner Music Latina, he continues to be a leading voice in Colombian urban music.""",
        "achievements": [
            "#44 in B-Fun 2025 Digital Influence Index",
            "8M+ Instagram, 9.9M TikTok, 4.82M YouTube",
            "Wikipedia page",
            "Hits 'Una' and 'Medallo'",
            "Collaborations with Maluma, Black Eyed Peas, Piso 21",
            "YouTube Foundry Class 2021",
            "Signed to Warner Music Latina",
            "Performed at 500+ schools before fame"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Blessd_2024.jpg/440px-Blessd_2024.jpg",
        "wikipedia": "https://en.wikipedia.org/wiki/Blessd"
    },
    {
        "id": "la-mafe-tv",
        "name": "La Mafe TV",
        "fullName": "María Fernanda Vásquez Cárdenas",
        "birthDate": "2007-08-21",
        "birthPlace": "Bogotá, Colombia",
        "nationality": "Colombian",
        "profession": "TikTok Star, Content Creator, Influencer",
        "bfunRank": 42,
        "description": "Colombian TikTok star known for energetic comedy sketches and dance videos. One of the youngest top Colombian influencers at 18 years old.",
        "instagram": "lamafetv",
        "tiktok": "mafevasqueztv",
        "youtube": "Mafe Vasquez TV",
        "category": "influencer",
        "tags": ["Influencer", "Comedy", "TikTok", "Colombia", "Bogotá"],
        "earlyLife": "María Fernanda Vásquez Cárdenas was born on August 21, 2007, in Bogotá, Colombia. She launched her YouTube channel in 2017 at just 10 years old.",
        "career": """La Mafe TV is a Colombian TikTok star and content creator known for energetic comedy sketches, dance videos, and relatable family-oriented content.

Ranked #42 in the B-Fun 2025 Digital Influence Index with 13M+ TikTok followers, she launched her YouTube channel in 2017 at age 10 and began posting on TikTok in 2019.

She frequently collaborates with her older brother, popular YouTuber José David Vásquez. At just 18 years old, she is one of the youngest top Colombian influencers and has her own merchandise line (Vasquez Merch).""",
        "achievements": [
            "#42 in B-Fun 2025 Digital Influence Index",
            "13M+ TikTok followers",
            "Started YouTube at age 10",
            "One of youngest top Colombian influencers",
            "Own merchandise line (Vasquez Merch)",
            "Collaborations with brother José David Vásquez"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/La_Mafe_TV_2024.jpg/440px-La_Mafe_TV_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/mafe-vasquez.html"
    },
    {
        "id": "mr-stiven-tc",
        "name": "Mr Stiven TC",
        "fullName": "Stiven Tangarife Caicedo",
        "birthDate": "2000-04-19",
        "birthPlace": "Cali, Colombia",
        "nationality": "Colombian",
        "profession": "YouTuber, Streamer, Content Creator, Entrepreneur, Musician",
        "bfunRank": 43,
        "description": "Colombian streamer and YouTuber known as one of the best Free Fire players. Top 3 most-followed streamers on Kick with 12.8M YouTube subscribers.",
        "instagram": "stiven.tc",
        "tiktok": "mrstiventc",
        "youtube": "Mr Stiven TC",
        "category": "influencer",
        "tags": ["Influencer", "Streamer", "Gaming", "Colombia", "Cali"],
        "earlyLife": "Stiven Tangarife Caicedo was born on April 19, 2000, in Cali, Colombia. He rose to fame as one of the best Free Fire players before expanding into IRL streaming.",
        "career": """Mr Stiven TC is a Colombian streamer and YouTuber who rose to fame as one of the best Free Fire players and expanded into IRL streaming, vlogs, challenges, and music.

Ranked #43 in the B-Fun 2025 Digital Influence Index with 12.8M YouTube subscribers and 1.6 billion total views, he is one of the top 3 most-followed streamers on Kick globally.

He is also an entrepreneur and has released original music including the track "Baila." His YouTube channel has over 2,751 videos, making him one of the most prolific content creators in Colombia.""",
        "achievements": [
            "#43 in B-Fun 2025 Digital Influence Index",
            "12.8M YouTube subscribers",
            "1.6 billion+ total views",
            "Top 3 Kick streamer globally",
            "Pioneer of Free Fire content",
            "Entrepreneur and musician"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Mr_Stiven_TC_2024.jpg/440px-Mr_Stiven_TC_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/mr-stiven-tc.html"
    },
    {
        "id": "marlon-garzon",
        "name": "Marlon Garzón",
        "fullName": "Marlon Garzón",
        "birthDate": "2002-03-02",
        "birthPlace": "Colombia",
        "nationality": "Colombian",
        "profession": "TikTok Content Creator, Comedian",
        "bfunRank": 45,
        "description": "Colombian TikTok creator known for short comedy videos and sketches with over 15M followers and 1.9B YouTube views.",
        "instagram": "marlongarzonn",
        "tiktok": "marlongarzonn",
        "youtube": "Marlon Garzón",
        "category": "influencer",
        "tags": ["Influencer", "Comedy", "TikTok", "Colombia", "Sketches"],
        "earlyLife": "Marlon Garzón was born on March 2, 2002, in Colombia. He started posting content on Instagram and YouTube in October 2017.",
        "career": """Marlon Garzón is a Colombian TikTok content creator known for short comedy videos and sketches. He often collaborates with his family and friends, including his sister and girlfriend.

Ranked #45 in the B-Fun 2025 Digital Influence Index with 15M+ TikTok followers and 5.35M YouTube subscribers, he has accumulated 1.9 billion total YouTube views across 2,751+ videos.

He has been consistently creating comedy content since 2017, building one of the most engaged comedy audiences in Colombia.""",
        "achievements": [
            "#45 in B-Fun 2025 Digital Influence Index",
            "15M+ TikTok followers",
            "5.35M YouTube subscribers",
            "1.9 billion total YouTube views",
            "2,751+ YouTube videos",
            "Consistent comedy content since 2017"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Marlon_Garzon_2024.jpg/440px-Marlon_Garzon_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/marlon-garzon.html"
    },
    {
        "id": "samantha-correa",
        "name": "Samantha Correa",
        "fullName": "Samantha Correa",
        "birthDate": "2002-04-23",
        "birthPlace": "Colombia",
        "nationality": "Colombian",
        "profession": "Content Creator, Influencer, Model",
        "bfunRank": 46,
        "description": "Colombian content creator and transgender influencer known for modeling, cosplay, and beauty transformations with over 14M TikTok followers.",
        "instagram": "samcorreat",
        "tiktok": "samcorreat",
        "youtube": "Samantha Correa",
        "category": "influencer",
        "tags": ["Influencer", "Model", "Cosplay", "Colombia", "LGBTQ+"],
        "earlyLife": "Samantha Correa was born on April 23, 2002, in Colombia. She is an auxiliar veterinaria and técnica en diseño multimedia.",
        "career": """Samantha Correa is a Colombian content creator and transgender influencer known for modeling, cosplay, beauty transformations, and fashion content. She openly shares her transition journey and personal experiences.

Ranked #46 in the B-Fun 2025 Digital Influence Index with 14M+ TikTok followers and 3M+ Instagram followers, she has accumulated 518M+ total TikTok likes.

She gained widespread media attention in November 2025 when linked to the Pirlo-Blessd controversy through the song "El Ficticio." A vocal transgender advocate, she continues to inspire a diverse global following through her authentic content.""",
        "achievements": [
            "#46 in B-Fun 2025 Digital Influence Index",
            "14M+ TikTok followers, 3M+ Instagram",
            "518M+ total TikTok likes",
            "Verified TikTok account (April 2025)",
            "Vocal transgender advocate",
            "Featured in major music controversy (2025)"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Samantha_Correa_2024.jpg/440px-Samantha_Correa_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/samantha-correa.html"
    },
    {
        "id": "jose-vasquez",
        "name": "José Vásquez",
        "fullName": "José David Vásquez",
        "birthDate": "2000-11-23",
        "birthPlace": "Colombia",
        "nationality": "Colombian",
        "profession": "YouTuber, Content Creator, TikToker",
        "bfunRank": 50,
        "description": "Colombian YouTuber known for vlogs and challenge videos. Brother of TikTok star Mafe Vasquez with 14M+ TikTok followers.",
        "instagram": "josevasquez",
        "tiktok": "josevasqueztv",
        "youtube": "José Vásquez",
        "category": "influencer",
        "tags": ["Influencer", "YouTube", "TikTok", "Colombia", "Family"],
        "earlyLife": "José David Vásquez was born on November 23, 2000, in Colombia. He launched his YouTube channel in August 2016.",
        "career": """José Vásquez is a Colombian YouTuber and content creator known for vlogs, challenge videos, and trending TikTok content. He is the older brother of popular TikToker Mafe Vasquez.

Ranked #50 in the B-Fun 2025 Digital Influence Index with 14M+ TikTok followers, he launched his YouTube channel in August 2016 with the video "The Video That Brought Me To You!"

He frequently appears in his sister Mafe's videos and is part of the Vásquez family content empire. His most popular video has over 700,000 views, and he continues to create engaging content across platforms.""",
        "achievements": [
            "#50 in B-Fun 2025 Digital Influence Index",
            "14M+ TikTok followers",
            "Active content creator since 2016",
            "Brother of Mafe Vasquez (La Mafe TV)",
            "Part of Vásquez family content empire"
        ],
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Jose_Vasquez_2024.jpg/440px-Jose_Vasquez_2024.jpg",
        "famousBirthdays": "https://www.famousbirthdays.com/people/jose-vasquez.html"
    },
]

def generate_bio_html(inf):
    """Generate a complete bio HTML file for an influencer."""
    
    slug = inf["id"]
    name = inf["name"]
    full_name = inf["fullName"]
    birth_date = inf["birthDate"]
    birth_place = inf["birthPlace"]
    nationality = inf["nationality"]
    profession = inf["profession"]
    description = inf["description"]
    category = inf["category"]
    tags = inf["tags"]
    early_life = inf["earlyLife"]
    career = inf["career"]
    achievements = inf["achievements"]
    image = inf["image"]
    
    # Social media links
    instagram = inf.get("instagram", "")
    tiktok = inf.get("tiktok", "")
    youtube = inf.get("youtube", "")
    wikipedia = inf.get("wikipedia", "")
    famous_birthdays = inf.get("famousBirthdays", "")
    
    # Build social links HTML
    social_links = ""
    if instagram:
        social_links += f'            <a href="https://instagram.com/{instagram}" class="social-link" target="_blank" rel="noopener me" itemprop="sameAs"><span class="icon">📷</span> Instagram</a>\n'
    if tiktok:
        social_links += f'            <a href="https://www.tiktok.com/@{tiktok}" class="social-link" target="_blank" rel="noopener me" itemprop="sameAs"><span class="icon">🎵</span> TikTok</a>\n'
    if youtube:
        social_links += f'            <a href="https://youtube.com/@{youtube}" class="social-link" target="_blank" rel="noopener me" itemprop="sameAs"><span class="icon">▶</span> YouTube</a>\n'
    if wikipedia:
        social_links += f'            <a href="{wikipedia}" class="social-link" target="_blank" rel="noopener"><span class="icon">📖</span> Wikipedia</a>\n'
    
    # Build sameAs array
    same_as = []
    if instagram:
        same_as.append(f"https://instagram.com/{instagram}")
    if tiktok:
        same_as.append(f"https://www.tiktok.com/@{tiktok}")
    if youtube:
        same_as.append(f"https://youtube.com/@{youtube}")
    if wikipedia:
        same_as.append(wikipedia)
    if famous_birthdays:
        same_as.append(famous_birthdays)
    same_as_json = ',\n      '.join([f'"{s}"' for s in same_as])
    
    # Build achievements list
    achievements_html = '\n'.join([f'          <li>{a}</li>' for a in achievements])
    
    # Build tags HTML
    tags_html = '\n'.join([f'          <a href="#" class="category-tag">{t}</a>' for t in tags])
    
    # Generate career paragraphs
    career_paragraphs = career.strip().split('\n\n')
    career_html = '\n\n        '.join([f'<p>{p.strip()}</p>' for p in career_paragraphs if p.strip()])
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{name} — {profession} | Wifioficial Biography</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{name}, {full_name}, {profession}, Colombian influencer, {birth_place}, Colombia, {' '.join(tags[:3])}">
  <meta name="author" content="Wifioficial Biography">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="https://wifioficial-biography.com/bios/{slug}.html">

  <meta property="og:type" content="profile">
  <meta property="og:url" content="https://wifioficial-biography.com/bios/{slug}.html">
  <meta property="og:title" content="{name} — {profession}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{image}">
  <meta property="og:site_name" content="Wifioficial Biography">
  <meta property="og:locale" content="en_US">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{name} — {profession}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{image}">

  <meta name="theme-color" content="#0645ad">
  <meta name="article:author" content="https://instagram.com/{instagram}">
  <meta name="article:published_time" content="2026-07-12T00:00:00+00:00">
  <meta name="article:modified_time" content="2026-07-12T00:00:00+00:00">
  <meta name="article:section" content="Biography">
  <meta name="article:tag" content="{name}">
  <meta name="article:tag" content="{nationality}">
  <link rel="alternate" hreflang="en" href="https://wifioficial-biography.com/bios/{slug}.html">
  <link rel="alternate" hreflang="es" href="https://wifioficial-biography.com/bios/{slug}.html">
  <link rel="alternate" hreflang="x-default" href="https://wifioficial-biography.com/bios/{slug}.html">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="../css/style.css">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "{full_name}",
    "alternateName": ["{name}"],
    "description": "{description}",
    "birthDate": "{birth_date}",
    "birthPlace": {{
      "@type": "Place",
      "name": "{birth_place}"
    }},
    "nationality": {{
      "@type": "Country",
      "name": "{nationality}"
    }},
    "jobTitle": "{profession}",
    "url": "https://wifioficial-biography.com/bios/{slug}.html",
    "image": "{image}",
    "sameAs": [
      {same_as_json}
    ]
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{
        "@type": "ListItem",
        "position": 1,
        "name": "Inicio",
        "item": "https://wifioficial-biography.com/"
      }},
      {{
        "@type": "ListItem",
        "position": 2,
        "name": "Biografías",
        "item": "https://wifioficial-biography.com/#biografias"
      }},
      {{
        "@type": "ListItem",
        "position": 3,
        "name": "{name}",
        "item": "https://wifioficial-biography.com/bios/{slug}.html"
      }}
    ]
  }}
  </script>

</head>
<body>

  <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="../index.html" class="site-logo" aria-label="Wifioficial Biography - Inicio">
        <div class="logo-icon" aria-hidden="true">W</div>
        <div class="logo-text">Wifioficial <span>Biography</span></div>
      </a>
      <nav class="main-nav" id="mainNav" role="navigation" aria-label="Main navigation">
        <ul>
          <li><a href="../index.html">Inicio</a></li>
          <li><a href="../index.html#biografias">Biografías</a></li>
          <li><a href="../index.html#categorias">Categorías</a></li>
          <li><a href="../index.html#about">Acerca de</a></li>
        </ul>
      </nav>
      <div class="header-search">
        <input type="search" id="headerSearchInput" placeholder="Buscar biografía..." aria-label="Buscar biografía">
        <button id="searchBtn" aria-label="Buscar">Buscar</button>
      </div>
      <button class="menu-toggle" id="menuToggle" aria-label="Abrir menú">☰</button>
    </div>
  </header>

  <div class="search-overlay" id="searchOverlay" role="dialog" aria-label="Búsqueda">
    <div class="search-box">
      <input type="search" id="searchOverlayInput" placeholder="Buscar biografía..." aria-label="Buscar biografía" autocomplete="off">
      <div class="search-results" id="searchResults"></div>
      <div style="padding:.5rem 1.25rem;border-top:1px solid #eee;text-align:right;">
        <button onclick="document.getElementById('searchOverlay').classList.remove('active')" style="background:none;border:1px solid #ccc;padding:.3rem .8rem;border-radius:3px;cursor:pointer;font-size:.85rem;">Cerrar (Esc)</button>
      </div>
    </div>
  </div>

  <div class="site-container" style="grid-template-columns:1fr;">
    <main class="main-content bio-page" role="main" itemscope itemtype="https://schema.org/Person">

      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <a href="../index.html">Inicio</a>
        <span class="separator">›</span>
        <a href="../index.html#biografias">Biografías</a>
        <span class="separator">›</span>
        <span>{name}</span>
      </nav>

      <div class="bio-page-header">
        <div class="bio-page-photo">
          <img src="{image}" alt="{name} — {description}" title="{name}" width="220" height="275" loading="eager" fetchpriority="high" itemprop="image">
        </div>
        <div class="bio-page-info">
          <h1 itemprop="name">{name}</h1>
          <div class="subtitle" itemprop="alternateName">{full_name}</div>
          <p itemprop="description" style="font-size:.95rem;line-height:1.6;">{description}</p>
          <div class="social-links" style="margin-top:.75rem;">
{social_links}          </div>
        </div>
      </div>

      <div class="infobox" role="complementary" aria-label="Personal information">
        <div class="infobox-header">{name}</div>
        <div class="infobox-image">
          <img src="{image}" alt="{name} portrait" title="{name}" width="300" height="375" loading="lazy">
        </div>
        <table>
          <tbody>
            <tr><th>Full Name</th><td itemprop="birthName">{full_name}</td></tr>
            <tr><th>Born</th><td><span itemprop="birthDate" content="{birth_date}">{birth_date}</span><br><span itemprop="birthPlace">{birth_place}</span></td></tr>
            <tr><th>Nationality</th><td itemprop="nationality">{nationality}</td></tr>
            <tr><th>Occupation(s)</th><td itemprop="jobTitle">{profession}</td></tr>
            <tr><th>Known for</th><td>B-Fun 2025 Digital Influence Index #{inf["bfunRank"]}</td></tr>
          </tbody>
        </table>
      </div>

      <article class="bio-article">

        <div class="category-tags">
{tags_html}
        </div>

        <p><strong>{name}</strong> ({full_name}) is a <a href="#">{nationality}</a> <a href="#">{profession.lower()}</a>. {description}</p>

        <h2 id="early-life">Early life and background</h2>
        <p>{early_life}</p>

        <h2 id="career">Career</h2>
        {career_html}

        <h2 id="achievements">Notable achievements</h2>
        <ul>
{achievements_html}
        </ul>

        <h2 id="references">References</h2>
        <ul>
          <li><a href="https://www.infobae.com/colombia/2026/02/22/karol-g-juandam-y-shakira-lideran-la-era-de-la-influencia-real-en-redes-sociales-son-los-protagonistas-que-mueven-millones/" target="_blank" rel="noopener">B-Fun 2025 Digital Influence Index — Infobae</a></li>
          <li><a href="https://www.elcolombiano.com/tendencias/ranking-50-colombianos-mas-influyentes-redes-sociales-HI32908539" target="_blank" rel="noopener">Top 50 Colombianos más influyentes — El Colombiano</a></li>
          <li><a href="https://ceipa.edu.co/blog/top-50-colombianos-que-lideran-la-influencia-digital/" target="_blank" rel="noopener">Top 50 colombianos que lideran la influencia digital — CEIPA</a></li>
        </ul>

      </article>
    </main>
  </div>

  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="logo-icon" aria-hidden="true">W</div>
        <div class="logo-text">Wifioficial <span>Biography</span></div>
      </div>
      <div class="footer-links">
        <a href="../index.html">Inicio</a>
        <a href="../index.html#biografias">Biografías</a>
        <a href="../index.html#categorias">Categorías</a>
        <a href="../index.html#about">Acerca de</a>
      </div>
      <div class="footer-copy">&copy; 2026 Wifioficial Biography. All rights reserved.</div>
    </div>
  </footer>

  <script src="../js/app.js"></script>
</body>
</html>'''
    
    return html


def main():
    """Generate all bio files."""
    os.makedirs(BIOS_DIR, exist_ok=True)
    
    created = []
    skipped = []
    
    for inf in influencers:
        filepath = os.path.join(BIOS_DIR, f'{inf["id"]}.html')
        
        if os.path.exists(filepath):
            skipped.append(inf["id"])
            continue
        
        html = generate_bio_html(inf)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        created.append(inf["id"])
        print(f"Created: {inf['id']}.html")
    
    print(f"\n--- Summary ---")
    print(f"Created: {len(created)} bio files")
    print(f"Skipped (already exist): {len(skipped)}")
    print(f"Total influencers: {len(influencers)}")
    
    return created


if __name__ == "__main__":
    created = main()

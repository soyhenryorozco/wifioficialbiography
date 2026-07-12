#!/usr/bin/env python3
import json

p = []

def add(name, category, profession, born, birthPlace, nationality, excerpt, tags):
    p.append({"name":name,"category":category,"profession":profession,"born":born,"birthPlace":birthPlace,"nationality":nationality,"excerpt":excerpt,"tags":tags})

# YouTube Stars (1-50)
add("Dude Perfect","youtuber","YouTube Content Creators","March 10, 1992","Dallas, Texas, USA","American","Dude Perfect is an American sports entertainment group known for trick shot videos, battles, and stereotypes on YouTube with over 60 million subscribers.",["youtube","sports","trick shots","comedy","group"])
add("Smosh","youtuber","YouTube Comedy Duo","May 7, 1987","West Sacramento, California, USA","American","Smosh is a YouTube comedy duo founded by Ian Hecox and Anthony Padilla, known for sketch comedy, parodies, and gaming content.","youtube","comedy","sketch","parody","digital creator"])
add("Jenna Mourey","youtuber","YouTuber and Comedian","September 15, 1986","Rochester, New York, USA","American","Known online as Jenna Marbles, she was one of the most popular female YouTubers known for comedic vlogs and commentary before retiring in 2020.","youtube","comedy","vlog","internet culture","former creator"])

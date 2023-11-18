""" for class Individual"""
from __future__ import annotations
from dataclasses import dataclass
import random
import numpy as np
from meme import Meme


@dataclass
class Personality:
    """A person who can have memes in their mind.

    Attributes:
        inclusive (float): the likelyhood of accepting culture meme from 0 to 1
        talkable (float): the likelyhood of spreading culture meme from 0 to 1
        capacity (int): the maximum memes*impressive (memory)
    """
    inclusive: float = random.random()
    talkable: float = random.random()
    capacity: int = 20


class Individual:
    """A person who can have memes in their mind.

    Attributes:
        memes list[(meme, impressive)]
        location Point
        personality (Personality)
    """
    memes: list[(Meme, float)]
    location: np.Point
    personality: Personality

    def __init__(self, location, memes=None, personality=Personality()):
        if memes is None:
            memes = []
        self.memes = memes
        self.location = location
        self.personality = personality

    def forget(self):
        """forgeting the meme
        """
        while self.imp_of_x() > self.personality.capacity:
            min_imp_tuple = min(self.memes, key=lambda x: x[1])
            self.memes.remove(min_imp_tuple)

    def learn_meme(self, meme: Meme, close):
        """Add of reinforce a meme to the individual's mind.

        Args:
            meme (Meme): the newly learned meme
            close (flaot): the parameter describe how close ther relationship is
        """
        incl = self.personality.inclusive
        poss = close * meme.feature.desirability * meme.feature.recency
        imp = close * incl * meme.feature.strength * meme.feature.desirability
        for (now_meme, now_imp) in self.memes:
            diff = abs(now_meme.content - meme.content)
            cred = meme.compare_cred(now_meme)
            match meme.similarity(now_meme):
                case 1, 1:  # similar idea
                    poss = 0
                    blend_content = cred*meme.content + \
                        (1-cred)*now_meme.content
                    now_meme.content = blend_content
                    now_imp += imp*(diff/blend_content)
                    break
                case 1, 0:
                    poss = (1-incl) + incl*poss
                    break
                case 0, 1:
                    poss = (1-incl)*poss + incl
                    break
                case _:
                    continue
        if random.random() < poss:
            self.memes.append((meme, imp))
        self.forget()

    def imp_of_x(self, nation=None, subject=None):
        """the total impression of sth

        Args:
            nation (str, optional): _description_. Defaults to None.
            subject (str, optional): _description_. Defaults to None.

        Returns:
            imp_: the total imp
        """
        imp_ = 0
        for (meme, imp) in self.memes:
            if (meme.nation == nation or nation is None) and \
                    (meme.subject == subject or subject is None):
                imp_ += imp
        return imp_

    def share_memes(self, other: Individual, size):
        """Spread memes to another individual."""
        def choose_meme():
            rand = random.uniform(0, self.imp_of_x())
            current = 0
            for meme, imp in self.memes:
                current += imp
                if current > rand:
                    return meme
        poss = self.personality.talkable*other.personality.talkable
        dis = np.linalg.norm(self.location-other.location)
        close = 1 - np.sqrt(dis/size)
        if random.random() < poss:
            other.learn_meme(choose_meme(), close)

    def diverse_individual(self, location, div: float) -> Individual:
        """Generate a variant individual with random perturbations.

        Args:
            location: the new location
            div (float): Diversity factor   

        Returns:
            Individual: Variant individual with random location, personality   
                    and meme impression values scaled by div.
        """
        new_personality = Personality(
            inclusive=div * random.random() * self.personality.inclusive,
            talkable=div * random.random() * self.personality.talkable,
            capacity=int(div * random.random() * self.personality.capacity)
        )

        new_memes = [(meme.diverse_meme(div), div * random.random() * imp)
                     for meme, imp in self.memes]

        return Individual(
            location=location,
            memes=new_memes,
            personality=new_personality
        )

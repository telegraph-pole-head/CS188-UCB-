""" for class Meme"""
from __future__ import annotations
from dataclasses import dataclass
import random


@dataclass
class Feature:
    """Features of a meme.

    Attributes:
        strength (int): How strongly the meme's message is promoted
        credibility (int): Perceived credibility of meme's source
        desirability (int): How much the content appeals to social motivations  
        recency (float): Benefit from being recent in audiences' minds.
    """
    strength: float = random.random()
    credibility: float = random.random()
    desirability: float = random.random()
    recency: float = random.random()


@dataclass
class Meme:
    """A cultural concept that self-replicates through transmission within a population.

    Attributes:
        nation (str): The nation where the meme originated
        subject (str): Topic or subject of the meme's content
        content (int): The idea, belief or information in the meme
        feature (Feature): The features of the meme
    """

    nation: str
    subject: str
    content: int
    feature: Feature = Feature()

    def similarity(self, meme: Meme):
        """return the similarity of two memes

        Args:
            meme (Meme): _description_

        Returns:
            n: nation
            s: subject
        """
        n = 1 if meme.nation == self.nation else 0
        s = 1 if meme.subject == self.subject else 0
        return n, s

    def compare_cred(self, meme: Meme):
        """return the comparative credibility of two memes

        Args:
            meme (Meme): _description_

        Returns:
            cred: cred of self
        """
        cred1_ = self.feature.credibility
        cred2_ = meme.feature.credibility
        return cred1_/(cred1_ + cred2_)

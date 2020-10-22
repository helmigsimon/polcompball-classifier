# -*- coding: utf-8 -*-
import click
import re
import logging
from tqdm import tqdm
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from bs4 import BeautifulSoup, element
import requests
from pprint import pprint
from dataclasses import dataclass
from multiprocessing import Pool
from functools import partial


CANONICAL_BALLS = 'https://polcompball.fandom.com/wiki/List_of_ideology_balls'
NON_CANONICAL_BALLS = 'https://polcompball.fandom.com/wiki/List_of_non-canon_ideologies'
PARTY_AND_MOVEMENT_BALLS = 'https://polcompball.fandom.com/wiki/List_of_movements'

POLITICAL_POSITIONS = ('Center','Authoritarian Left','Authoritarian Right','Authoritarian Unity','Libertarian Left','Left Unity','Libertarian Unity','Libertarian Right','Right Unity','Non-Quadrant','Off-Compass')


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Obtains data from external sources
    """
    logger = logging.getLogger(__name__)
    logger.info('Obtaining data')
    
@dataclass(unsafe_hash=True)
class Ideology:
    name: str
    page_url: str
    thumbnail_url: str
    position: str
    canon: bool
    non_canon: bool
    party: bool
    movement: bool

def soupify_url(url):
    response = requests.get(url)
    return BeautifulSoup(response.text,'html.parser')

def get_ideology_dict(url):
    return convert_page_to_ideology_dict(url)

def convert_page_to_ideology_set(url):
    soup = soupify_url(url)

    categories = soup.findAll('span',class_='mw-headline')
    canon, non_canon, party, movement = [False]*4

    if url == CANONICAL_BALLS:
        canon = True
    elif url == NON_CANONICAL_BALLS:
        non_canon = True
    elif url == PARTY_AND_MOVEMENT_BALLS:
        pass
    else:
        raise InputError(f'Invalid URL passed: {url}')

       
    ideologies = []

    for category in tqdm(categories):
        category_name = category.text.strip()
        position = category_name if category_name in POLITICAL_POSITIONS else None
        if category_name == 'Movements':
            movement = True
        elif category_name == 'Politial parties':
            party = True

        ideology_collection = category.parent.next_sibling.next_sibling.children

        get_ideo = partial(get_ideology, position=position,canon=canon,non_canon=non_canon,party=party,movement=movement)
        
        category_list = list(
            filter(
                lambda x: x is not None,
                map(get_ideo,ideology_collection)
            )
        )

        ideologies.extend(category_list)

    return ideologies

def get_ideology(idea,**kwargs):
    if isinstance(idea,element.NavigableString):
        return
    ideology_name = idea.text.strip()
    ideology_link = [x for x in idea.findAll('a') if filter_ideology_links(x)][-1].get('href')
    if ideology_link:
        sub = re.sub(r'.+\.com',"",ideology_link)
        if sub:
            ideology_link = sub
        page_url = ''.join(['https://polcompball.fandom.com',ideology_link])
        thumbnail_url = get_thumbnail_url(page_url)
    else:
        page_url, thumbnail_url = None, None
    
    return Ideology(
        name=ideology_name,
        page_url=page_url,
        thumbnail_url=thumbnail_url,
        **kwargs
    )


def filter_ideology_links(ideology_block):
    class_ = ideology_block.attrs.get('class')
    if class_:
        if 'image' in class_:
            return False
        if 'mw_redirect' in class_:
            return True
    return True

def get_thumbnail_url(ideology_url):
    soup = soupify_url(ideology_url)

    try:    
        thumbnail_url = soup.findAll('a',class_='image image-thumbnail')[0].get('href')
    except IndexError:
        thumbnail_url = None

    return thumbnail_url


def ideology_taxonomy_to_set(taxonomy):
    """
    Converts Ideology Taxonomy to Set Format for Lookups
    """
    if isinstance(taxonomy,Ideology):
        return set([taxonomy.name])
    if isinstance(taxonomy,dict):
        set_ = set()
        for key, value in taxonomy.items():
            set_ = set.union(set_,ideology_taxonomy_to_set(value))
        return set_


def combine_same_ideologies(balls):
    name_hash = {}
    for ideology in balls:
        if name_hash.get(ideology.name):
            name_hash[ideology.name] += 1
        else:
            name_hash[ideology.name] = 1
    
    multiple_time_names = [name for name,count in name_hash.items() if count > 1]
    
    multiple_balls = {name: list(filter(lambda x: x.name == name,balls)) for name in multiple_time_names}
    
    combined_balls = []
    
    for name,balls_ in multiple_balls.items():
        kwargs = {attr: None for attr in Ideology.__dict__['__annotations__'].keys()}
        for ball in balls_:
            for attr in kwargs.keys():
                value = getattr(ball,attr)
                if value:
                    kwargs[attr] = value
        combined_balls.append(Ideology(**kwargs))

    combined_ideologies = [*combined_balls, *[ball for ball in balls if ball.name not in multiple_balls.keys()]]
    
    assert len(combined_ideologies) < len(balls)
        
    return combined_ideologies     


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

from urllib import parse
import urllib
import configparser


def getCompetitorList(self):

    config = configparser.ConfigParser()
    config.read('./input/competitors.ini', encoding='utf-8')
    competitors = config['COMPETITORS']

    competitor_list = {
        'ProjectSleep': competitors.get('ProjectSleep').split(','),
        'Slou': competitors.get('Slou').split(','),
        '3boon1': competitors.get('3boon1').split(','),
        'Lanube': competitors.get('Lanube').split(','),
        'Zinus': competitors.get('Zinus').split(','),
        'Brandless': competitors.get('Brandless').split(','),
        'Sleep-gonggam': competitors.get('Sleep-gonggam').split(','),
                        }

    return competitor_list
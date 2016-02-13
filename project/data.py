#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging

def load(filename):
    """loads JSON formatted project data from a file and returns a list."""
    log_msg('load(filename):' + str(filename))
    try:
        file = open(filename)
        load_data = file.read()
        json_data = json.loads(load_data)
        file.close()
        return json_data
    except:
        log_msg('load(filename):' + str(filename))
        print("Error: No such file found.")
        return None


def get_project_count(db):
    """ Retrieves the number of projects in a project list."""
    log_msg('get_project_count(db):' + str(len(db)))
    try:
            project = len(db)
            return project
    except:
        print("Error: No projects found.")
        return None


def get_project(db, id):
    """ Fetches the project with the specified id from the specified list. """
    log_msg('get_project(db, id)' + str(id))
    try:
        for project in db:
            if project['project_no'] == id:
                return project
        return None
    except:
        print("Error: No such project found.")
        return None


def search(db, sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None):
    """ Fetches and sorts projects matching criteria from the specified list. """
    log_msg('Search: techniques:' + str(techniques) + ', search:' + str(search) + ', search_fields:' + str(search_fields))
    found = []
    if search != None:
        search = search.lower()

    try:
        #If search_field is a empty list, nothing is displayed
        if search_fields == []:
            return found

        #If search_field is None, all projects is displayed.
        elif search_fields == None:
            for project in db:
                if search == None:
                    found.append(project)
                else:
                    for key in project:
                        if search in str(project[key]).lower():
                            if project not in found:
                                found.append(project)

        else:
            for project in db:
                if search == None:
                    found.append(project)
                else:
                    for key in search_fields:
                        if search in str(project[key]).lower():
                            if project not in found:
                                found.append(project)

        #Removes the projects that does not have the techniques specified
        if techniques != None and techniques != []:
            for project in found[::-1]:
                keep = False
                for tech in techniques:
                    if tech in project['techniques_used']:
                        keep = True
                if keep == False:
                    found.remove(project)

        #Sorts projects by startdate and sorts them in descending order
        found = sorted(found, key=lambda k: k[sort_by])
        if sort_order == 'desc':
            found.reverse()

        return found
    except:
        print('Error: no search found.')


def get_techniques(db):
    """ Fetches a list of all the techniques from the specified project list."""
    log_msg('get_techniques(db): Size of database:' + str(len(db)))
    technique_list = []
    try:
        for project in db:
            for technique in project['techniques_used']:
                if technique not in technique_list:
                    technique_list.append(technique)
        return sorted(technique_list)
    except:
        print("Error: no such technique found.")


def get_technique_stats(db):
    """ Collects and returns statistics for all techniques in the specified project list. """
    log_msg('get_technique_stats: Size of database:' + str(len(db)))
    tech_stats = {}
    try:
        for project in db:
            for technique in project['techniques_used']:
                if technique not in tech_stats:
                    tech_stats[technique] = []
                tech_stats[technique].append({'id': project['project_no'],
                                              'name': project['project_name']})
        return tech_stats
    except:
        print("Error: no such technique stats found.")


def log_msg(message):
    """Creates a log file that can be looked up at to see if anything went wrong and when it happened."""
    import time
    time_format = "%Y-%m-%d %H:%M:&S"
    with open("doc/log_file.txt", 'a') as log:
        log.write(time.strftime(time_format) + ' - ' +  message +  '\n')

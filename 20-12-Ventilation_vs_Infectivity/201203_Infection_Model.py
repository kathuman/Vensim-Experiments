"""
Python model "201203_Infection_Model.py"
Translated using PySD version 0.10.0
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.py_backend.functions import cache
from pysd.py_backend import functions

_subscript_dict = {}

_namespace = {
    'TIME': 'time',
    'Time': 'time',
    'recovery rate': 'recovery_rate',
    'Recovery time': 'recovery_time',
    'Infected': 'infected',
    'Susceptible': 'susceptible',
    'Air Density': 'air_density',
    'Breathing': 'breathing',
    'Room Volume': 'room_volume',
    'Clean Particles': 'clean_particles',
    'Virus particles': 'virus_particles',
    'Ventilation strength': 'ventilation_strength',
    'Exhalation of Clean Particles': 'exhalation_of_clean_particles',
    'Virus Decay Time': 'virus_decay_time',
    'Virus loss due to Ventilation': 'virus_loss_due_to_ventilation',
    'Person Viral Productivity': 'person_viral_productivity',
    'Overall Virus Concentration': 'overall_virus_concentration',
    'Virus Decay': 'virus_decay',
    'Virus Production': 'virus_production',
    'Clean particle recovery due to vent and Virus Decay':
    'clean_particle_recovery_due_to_vent_and_virus_decay',
    'Contact Frequency': 'contact_frequency',
    'Contacts between suceptible and Virus Particle':
    'contacts_between_suceptible_and_virus_particle',
    'Infection Rate': 'infection_rate',
    'infectivity': 'infectivity',
    'Probability of contact with Virus Particle': 'probability_of_contact_with_virus_particle',
    'Suceptible Contacts': 'suceptible_contacts',
    'FINAL TIME': 'final_time',
    'INITIAL TIME': 'initial_time',
    'SAVEPER': 'saveper',
    'TIME STEP': 'time_step'
}

__pysd_version__ = "0.10.0"

__data = {'scope': None, 'time': lambda: 0}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data['time']()


@cache('step')
def recovery_rate():
    """
    Real Name: b'recovery rate'
    Original Eqn: b'Infected/Recovery time'
    Units: b'Person/Day'
    Limits: (None, None)
    Type: component

    b''
    """
    return infected() / recovery_time()


@cache('run')
def recovery_time():
    """
    Real Name: b'Recovery time'
    Original Eqn: b'14'
    Units: b'Day'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 14


@cache('step')
def infected():
    """
    Real Name: b'Infected'
    Original Eqn: b'INTEG ( Infection Rate-recovery rate, 1)'
    Units: b'Person'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_infected()


@cache('step')
def susceptible():
    """
    Real Name: b'Susceptible'
    Original Eqn: b'INTEG ( recovery rate-Infection Rate, 10)'
    Units: b'Person'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_susceptible()


@cache('run')
def air_density():
    """
    Real Name: b'Air Density'
    Original Eqn: b'1225'
    Units: b'g/m3'
    Limits: (None, None)
    Type: constant

    b'https://en.wikipedia.org/wiki/Density_of_air'
    """
    return 1225


@cache('step')
def breathing():
    """
    Real Name: b'Breathing'
    Original Eqn: b'0.0024*Infected'
    Units: b'g/Day'
    Limits: (None, None)
    Type: component

    b''
    """
    return 0.0024 * infected()


@cache('run')
def room_volume():
    """
    Real Name: b'Room Volume'
    Original Eqn: b'5*5*4'
    Units: b'm3'
    Limits: (None, None)
    Type: constant

    b'Room with a volume of 5 x 5 x 4 meters'
    """
    return 5 * 5 * 4


@cache('step')
def clean_particles():
    """
    Real Name: b'Clean Particles'
    Original Eqn: b'INTEG ( Clean particle recovery due to vent and Virus Decay+Exhalation of Clean Particles-Breathing\\\\ , Air Density*Room Volume)'
    Units: b'g'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_clean_particles()


@cache('step')
def virus_particles():
    """
    Real Name: b'Virus particles'
    Original Eqn: b'INTEG ( Virus Production-Virus Decay-Virus loss due to Ventilation, 0)'
    Units: b'g'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_virus_particles()


@cache('run')
def ventilation_strength():
    """
    Real Name: b'Ventilation strength'
    Original Eqn: b'2000'
    Units: b'g/Day'
    Limits: (0.0, 2000.0, 1.0)
    Type: constant

    b''
    """
    return 2000


@cache('step')
def exhalation_of_clean_particles():
    """
    Real Name: b'Exhalation of Clean Particles'
    Original Eqn: b'Breathing-Virus Production'
    Units: b'g/Day'
    Limits: (None, None)
    Type: component

    b''
    """
    return breathing() - virus_production()


@cache('run')
def virus_decay_time():
    """
    Real Name: b'Virus Decay Time'
    Original Eqn: b'14'
    Units: b'Day'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 14


@cache('step')
def virus_loss_due_to_ventilation():
    """
    Real Name: b'Virus loss due to Ventilation'
    Original Eqn: b'Overall Virus Concentration*Ventilation strength'
    Units: b'g/Day'
    Limits: (None, None)
    Type: component

    b''
    """
    return overall_virus_concentration() * ventilation_strength()


@cache('run')
def person_viral_productivity():
    """
    Real Name: b'Person Viral Productivity'
    Original Eqn: b'0.4'
    Units: b'g/Person'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.4


@cache('step')
def overall_virus_concentration():
    """
    Real Name: b'Overall Virus Concentration'
    Original Eqn: b'Virus particles/Clean Particles'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return virus_particles() / clean_particles()


@cache('step')
def virus_decay():
    """
    Real Name: b'Virus Decay'
    Original Eqn: b'Virus particles/Virus Decay Time'
    Units: b'g/Day'
    Limits: (None, None)
    Type: component

    b''
    """
    return virus_particles() / virus_decay_time()


@cache('step')
def virus_production():
    """
    Real Name: b'Virus Production'
    Original Eqn: b'Infected*Person Viral Productivity'
    Units: b'g/Day'
    Limits: (None, None)
    Type: component

    b''
    """
    return infected() * person_viral_productivity()


@cache('step')
def clean_particle_recovery_due_to_vent_and_virus_decay():
    """
    Real Name: b'Clean particle recovery due to vent and Virus Decay'
    Original Eqn: b'Virus Decay+Virus loss due to Ventilation'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return virus_decay() + virus_loss_due_to_ventilation()


@cache('run')
def contact_frequency():
    """
    Real Name: b'Contact Frequency'
    Original Eqn: b'10000'
    Units: b'1/Day'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 10000


@cache('step')
def contacts_between_suceptible_and_virus_particle():
    """
    Real Name: b'Contacts between suceptible and Virus Particle'
    Original Eqn: b'Suceptible Contacts*Probability of contact with Virus Particle'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return suceptible_contacts() * probability_of_contact_with_virus_particle()


@cache('step')
def infection_rate():
    """
    Real Name: b'Infection Rate'
    Original Eqn: b'Contacts between suceptible and Virus Particle*infectivity'
    Units: b'Person/Day'
    Limits: (None, None)
    Type: component

    b''
    """
    return contacts_between_suceptible_and_virus_particle() * infectivity()


@cache('run')
def infectivity():
    """
    Real Name: b'infectivity'
    Original Eqn: b'0.05'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.05


@cache('step')
def probability_of_contact_with_virus_particle():
    """
    Real Name: b'Probability of contact with Virus Particle'
    Original Eqn: b'Virus particles/Clean Particles'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return virus_particles() / clean_particles()


@cache('step')
def suceptible_contacts():
    """
    Real Name: b'Suceptible Contacts'
    Original Eqn: b'Susceptible*Contact Frequency'
    Units: b'Person/Day'
    Limits: (None, None)
    Type: component

    b''
    """
    return susceptible() * contact_frequency()


@cache('run')
def final_time():
    """
    Real Name: b'FINAL TIME'
    Original Eqn: b'250'
    Units: b'Day'
    Limits: (None, None)
    Type: constant

    b'The final time for the simulation.'
    """
    return 250


@cache('run')
def initial_time():
    """
    Real Name: b'INITIAL TIME'
    Original Eqn: b'0'
    Units: b'Day'
    Limits: (None, None)
    Type: constant

    b'The initial time for the simulation.'
    """
    return 0


@cache('step')
def saveper():
    """
    Real Name: b'SAVEPER'
    Original Eqn: b'TIME STEP'
    Units: b'Day'
    Limits: (0.0, None)
    Type: component

    b'The frequency with which output is stored.'
    """
    return time_step()


@cache('run')
def time_step():
    """
    Real Name: b'TIME STEP'
    Original Eqn: b'0.0078125'
    Units: b'Day'
    Limits: (0.0, None)
    Type: constant

    b'The time step for the simulation.'
    """
    return 0.0078125


_integ_infected = functions.Integ(lambda: infection_rate() - recovery_rate(), lambda: 1)

_integ_susceptible = functions.Integ(lambda: recovery_rate() - infection_rate(), lambda: 10)

_integ_clean_particles = functions.Integ(
    lambda: clean_particle_recovery_due_to_vent_and_virus_decay() + exhalation_of_clean_particles(
    ) - breathing(), lambda: air_density() * room_volume())

_integ_virus_particles = functions.Integ(
    lambda: virus_production() - virus_decay() - virus_loss_due_to_ventilation(), lambda: 0)

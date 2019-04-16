#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created: 8th April 2019
Author: A. P. Naik
Description: Animate trajectories
"""
import pickle
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from constants import kpc
plt.rcParams['text.usetex'] = True


def movie_update(num, sat, tracer1, tracer2, line, s1, s2):
    line.set_data(sat[:num, 0], sat[:num, 1])
    s1.set_offsets(tracer1[:, :2, num])
    s2.set_offsets(tracer2[:, :2, num])
    return (line, s1, s2)


def movie(filename, length=10):

    f = open(filename, 'rb')
    s = pickle.load(f)
    f.close()

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    sat_t = s.sat_traj/kpc
    DM_t = s.DM_traj/kpc
    stars_t = s.stars_traj/kpc

    N_frames = sat_t.shape[0]
    interval = length*1000/(N_frames-1)

    st = r'$\beta={0:.1f},\ r={1:.1f}$'.format(s.beta, s.r_screen/kpc)
    ax.text(0.05, 0.95, st, transform=ax.transAxes, va='center', ha='left')

    # show initial positions in background
    ax.plot(sat_t[:, 0], sat_t[:, 1], ls='dashed', c='grey')
    ax.scatter(DM_t[:, 0, 0], DM_t[:, 1, 0], s=1, c='grey')
    ax.scatter(stars_t[:, 0, 0], stars_t[:, 1, 0], s=1, c='grey')

    # set up initial artists for animation
    l, = ax.plot([], [], c='black')
    s1 = ax.scatter(DM_t[:, 0, 0], DM_t[:, 1, 0], s=1, c='green', label='DM')
    s2 = ax.scatter(stars_t[:, 0, 0], stars_t[:, 1, 0], s=1, c='blue')

    # central MW blob
    circ = plt.Circle((0, 0), s.r_screen/kpc, color='green', fill=False)
    ax.add_artist(circ)
    ax.scatter([0], [0])

    plt.xlim(-100, 100)
    plt.ylim(-100, 100)
    plt.xlabel(r'$x\ [\mathrm{kpc}]$')
    plt.ylabel(r'$y\ [\mathrm{kpc}]$')

    handles = [Line2D([0], [0], marker='.', lw=0, label="Dark matter",
                      mfc='green', mec='green', ms=10),
               Line2D([0], [0], marker='.', lw=0, label="Stars",
                      mfc='blue', mec='blue', ms=10),
               Line2D([0], [0], lw=2, label="Screening Radius", color='green')]
    plt.legend(frameon=False, handles=handles)

    a = FuncAnimation(fig, movie_update, frames=N_frames, blit=True,
                      fargs=(sat_t, DM_t, stars_t, l, s1, s2),
                      interval=interval)

    return a
"""
a cairo exercise

bg      : the image used to color grayscale stripes
layer 0 : black
layer 1 : hundreds of vertical stripes

Individual stripes are painted in layer 1 with the blend operator.
"""

from __future__ import division

import cairo
import random
import math
import sys
import os
import random
random.seed(42*4)
from random import random as rand
from random import randint

W, H = 1200, 800 # responsive

def get_bg():

    if False: # optional bitmap background
        bg_fn = 'bg.png'
        bg_surface = cairo.ImageSurface.create_from_png(bg_fn)
        bg = cairo.Context(bg_surface)
    else: # generated background
        bg_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W), int(H))
        bg = cairo.Context(bg_surface)

        bg_grd = cairo.LinearGradient(0, 0, W, 0)

        hues = [
            [0, 0, 1, 0], # g
            [0, 1, 1, 0], # y
            [0, 1, 0, 0], # r
            [0, 1, 0, 1], # m
            [0, 0, 0, 1], # b
            [0, 0, 1, 1], # c
        ]
        # auto-set gradient stops
        for i, hue in enumerate(hues):
            hue[0] = i/len(hues)
        # auto-wrap gradient end to start
        first = hues[0]
        hues.append( (1, first[1], first[2], first[3]) )

        for hue in hues:
            a = 1
            p, r, g, b = hue
            bg_grd.add_color_stop_rgba(p, r, g, b, a)

        bg.set_source(bg_grd)
        bg.paint()

        #bg_surface.write_to_png('bg-generated.png')

    return bg_surface


def get_mask(w, h, x):

    srf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(srf)

    g = 1 # mask color irrelevant
    a1 = 1
    a2 = 0
    a3 = 0

    mid = randint(3,7)/10
    mid = mid + math.sin(x/W*math.pi)*0.4

    grd = cairo.LinearGradient(0, 0, 0, h)
    grd.add_color_stop_rgba(0.0, g, g, g, a1)
    grd.add_color_stop_rgba(mid, g, g, g, a2)
    grd.add_color_stop_rgba(1.0, g, g, g, a3)

    ctx.set_source(grd)
    ctx.paint()

    return srf

# decorated colored faded stripe
def get_stripe(w, h, x, bg_surface):

    if rand() < 0.6:
        srf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(srf)
        ctx.set_source_surface(bg_surface, -x, 0)
    else:
        srf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w/4), h)
        ctx = cairo.Context(srf)

        x_shifted = x + (rand()-0.5) * W/2 # +/- 25%
        ctx.set_source_surface(bg_surface, -x_shifted, 0)

    mask_surface = get_mask(w, h, x)
    ctx.mask_surface(mask_surface, 0, 0)

    return srf

def main():

    bg_surface = get_bg()

    l0_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W), int(H))
    l0 = cairo.Context(l0_surface)
    l0.set_source_rgb(0, 0, 0)
    l0.paint()

    # add stripes
    if True:
        l0.set_operator(12)
        iters = int(W/6)
        for i in range(iters):
            x = randint(0-32, W+32)
            x = x - x % 4
            s_w = randint(12, 64)
            s_h = H

            stripe_surface = get_stripe(s_w, s_h, x, bg_surface)
            if False: # debug
                fn = 'stripe-withbg-{}.png'.format(i)
                stripe_surface.write_to_png(fn)
                if i==0:
                    os.system(fn)
                    #sys.exit(0)

            x_rando = x + randint(-32,32)

            l0.set_source_surface(stripe_surface, x, 0)
            l0.rectangle(x_rando, 0, s_w, s_h)
            l0.paint_with_alpha(0.4)

    return l0_surface

if __name__ == '__main__':
    img = main()
    fn = 'output-v02-{}x{}.png'.format(W,H)
    img.write_to_png(fn)
    os.system(fn)